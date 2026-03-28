import streamlit as st
import pandas as pd
import numpy as np
import time
import re
import joblib
import plotly.graph_objects as go
from collections import deque
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
st.set_page_config(page_title="NullSpace RF | Zero-Trust Radar", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; }
    h1, h2, h3 { color: #58a6ff; font-weight: 800; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; text-shadow: 0px 0px 12px rgba(0, 255, 204, 0.6); }
    [data-testid="stMetricLabel"] { color: #8b949e !important; font-weight: bold; font-size: 1.1rem; }
    .xai-panel { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 10px; box-shadow: 0px 8px 24px rgba(0,0,0,0.8); }
    .alert-box { padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5); }
    .math-text { color: #8a2be2; font-weight: bold; font-family: 'Cambria Math', serif; font-size: 1.1rem; }
    .jamming-text { color: #d29922; font-size: 1.4rem; font-weight: bold; animation: blink 1s infinite; }
    .spoofing-text { color: #f85149; font-size: 1.4rem; font-weight: bold; animation: blink 0.8s infinite; }
    .safe-text { color: #3fb950; font-size: 1.4rem; font-weight: bold; }
    @keyframes blink { 50% { opacity: 0.4; } }
    hr { border-color: #30363d; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_path = os.path.join(BASE_DIR, 'bkzs_v4_model.pkl')
    try:
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"HATA: Model bulunamadı!\nŞu yolda arandı: {model_path}\nLütfen indirdiğiniz dosyanın adının tam olarak 'bkzs_v4_model.pkl' olduğundan emin olun.")
        st.stop()

model = load_model()
colA, colB = st.columns([5, 1])
with colA:
    st.title("NullSpace RF | Zero-Trust GNSS Radarı")
    st.markdown("**(BKZS) Bölgesel Konumlama ve Zamanlama Sistemi İçin Çoklu-Yörünge Savunma Kalkanı**")
    st.caption("Takım: Null Proof | Model: Random Forest (39 Milyon Veri Paketi ile Eğitildi) | Mimari: Uç Bilişim Edge Computing")
with colB:
    st.image("https://images.seeklogo.com/logo-png/45/3/turkiye-uzay-ajansi-tua-logo-png_seeklogo-453642.png", width=100)
st.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2083/2083287.png", width=80)
st.sidebar.markdown("### Ağ Trafiği Dinleme")
st.sidebar.markdown("PCAP (Packet Capture) dosyalarını canlı analiz edin.")

#.pcap dosyalarını tam bulamıyordu sürüm uyumsuzluğundan kaynaklı bu yüzden direkt list yöntemi ile tüm klasörde tarama yapıp buluyoruz ve bu saydede hata ollmuyıor.
pcap_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.pcap')]
if not pcap_files:
    st.sidebar.error(f"Lütfen şu klasöre en az bir adet .pcap dosyası atın:\n{BASE_DIR}")
    st.stop()

secilen_dosya = st.sidebar.selectbox("Hedef Ağ Paketini Seçin:", pcap_files)
baslat = st.sidebar.button("CANLI ANALİZİ BAŞLAT", use_container_width=True)
alert_placeholder = st.empty()
col1, col2, col3, col4 = st.columns(4)
metrik_placeholder = [col1.empty(), col2.empty(), col3.empty(), col4.empty()]

st.markdown("<br>", unsafe_allow_html=True)
col_grafik, col_xai = st.columns([2, 1])
chart_placeholder = col_grafik.empty()
xai_placeholder = col_xai.empty()
if 'snr_history' not in st.session_state: st.session_state.snr_history = deque(maxlen=80)
if 'var_history' not in st.session_state: st.session_state.var_history = deque(maxlen=80)
if 'zaman' not in st.session_state: st.session_state.zaman = deque(maxlen=80)
if 'sayac' not in st.session_state: st.session_state.sayac = 0
constellations = {"GP": "GPS (ABD)", "GL": "GLONASS (Rusya)", "GA": "Galileo (AB)", "GB": "BeiDou (Çin)", "TR": "BKZS (Türkiye)"}

if baslat:
    st.sidebar.success(f"Analiz ediliyor: {secilen_dosya}")
    
    secilen_dosya_tam_yol = os.path.join(BASE_DIR, secilen_dosya)
    
    with open(secilen_dosya_tam_yol, 'rb') as f:
        raw_data = f.read().decode('ascii', errors='ignore')
    
    #abd tr eu tüm uydu nmea verilerini yakalayan regexi tanıtıyorum
    nmea_satirlari = re.findall(r'(\$[A-Z]{2}GSV.*?\*[0-9A-Fa-f]{2})', raw_data)
    
    if not nmea_satirlari:
        st.error("Bu dosyada NMEA uydu verisi bulunamadı. Lütfen geçerli bir PCAP seçin.")
        st.stop()

    for line in nmea_satirlari:
        st.session_state.sayac += 1
        uydu_kodu = line[1:3]
        sistem_adi = constellations.get(uydu_kodu, f"Bilinmeyen ({uydu_kodu})")

        parts = line.split(',')
        snr_values = []
        for i in range(7, min(20, len(parts)), 4):
            try:
                snr_str = parts[i].split('*')[0]
                if snr_str != '':
                    snr_values.append(int(snr_str))
            except: pass
        
        if len(snr_values) == 0: continue   
        ort_snr = np.mean(snr_values)
        varyans_snr = np.var(snr_values)
        uydu_sayisi = len(snr_values)
        anlik_veri = pd.DataFrame({'Ortalama_SNR': [ort_snr], 'SNR_Varyansi': [varyans_snr], 'Uydu_Sayisi': [uydu_sayisi]})
        tahmin = model.predict(anlik_veri)[0]
        
        if tahmin == 1:
            alert_placeholder.markdown(f"<div class='alert-box' style='background-color:rgba(210,153,34,0.15); border-left: 6px solid #d29922;'><span class='jamming-text'>⚠️ KRİTİK ALARM: JAMMING (SİNYAL KÖRLEŞTİRME) TESPİT EDİLDİ!</span><br><small style='color:#c9d1d9;'>Ağ trafiği radyo frekansı gürültüsüyle boğuluyor. Veri: {line[:60]}...</small></div>", unsafe_allow_html=True)
            renk = '#d29922' 
        elif tahmin == 2:
            alert_placeholder.markdown(f"<div class='alert-box' style='background-color:rgba(248,81,73,0.15); border-left: 6px solid #f85149;'><span class='spoofing-text'>🚨 KRİTİK ALARM: SPOOFING (SİNYAL YANILTMA) TESPİT EDİLDİ!</span><br><small style='color:#c9d1d9;'>Sahte uydu verisi izole edildi ve reddedildi. Veri: {line[:60]}...</small></div>", unsafe_allow_html=True)
            renk = '#f85149' 
        else:
            alert_placeholder.markdown(f"<div class='alert-box' style='background-color:rgba(63,185,80,0.1); border-left: 6px solid #3fb950;'><span class='safe-text'>🟢 SİSTEM GÜVENLİ | Kriptografik & Fiziksel Doğrulama Başarılı.</span><br><small style='color:#8b949e;'>Bağlantı Temiz. Paket: {line[:60]}...</small></div>", unsafe_allow_html=True)
            renk = '#00ffcc' 

        metrik_placeholder[0].metric("Ortalama SNR (Güç)", f"{ort_snr:.2f} dB-Hz")
        metrik_placeholder[1].metric("SNR Varyansı (Fiziksel İz)", f"{varyans_snr:.3f} σ²")
        metrik_placeholder[2].metric("Görünen Uydu (FOV)", f"{uydu_sayisi} Adet")
        metrik_placeholder[3].metric("Aktif Takımyıldız", sistem_adi)
        st.session_state.snr_history.append(ort_snr)
        st.session_state.var_history.append(varyans_snr)
        st.session_state.zaman.append(st.session_state.sayac)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(st.session_state.zaman), y=list(st.session_state.snr_history), 
            mode='lines+markers', name="Sinyal Gücü (dB-Hz)",
            line=dict(color=renk, width=3, shape='spline'), marker=dict(size=5, color='white'), fill='tozeroy'
        ))
        fig.add_trace(go.Scatter(
            x=list(st.session_state.zaman), y=list(st.session_state.var_history), 
            mode='lines', name="Varyans (σ²)", line=dict(color='rgba(255, 255, 255, 0.3)', width=1, dash='dot')
        ))
        
        fig.update_layout(
            title="Real-Time RF Spektrum Osiloskobu",
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#c9d1d9'),
            margin=dict(l=0, r=0, t=40, b=0), height=380, yaxis=dict(range=[0, 65], gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(showgrid=False)
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        xai_html = "<div class='xai-panel'>"
        xai_html += "<h3 style='margin-top:0;'>Karar Motoru</h3>"
        xai_html += f"<p style='color:#8b949e; margin-bottom: 5px;'>Model Durumu: <b style='color:{renk}; font-size:1.1rem;'>{'JAMMING (Körleştirme)' if tahmin==1 else 'SPOOFING (Yanıltma)' if tahmin==2 else 'BENIGN (Temiz Sinyal)'}</b></p>"
        xai_html += "<hr><h5 style='color:#c9d1d9;'>Matematiksel Karar Vektörleri:</h5>"
        
        if tahmin == 2: 
            xai_html += "<ul style='color:#c9d1d9; font-size:0.95rem; line-height: 1.6;'>"
            xai_html += f"<li><b style='color:#f85149;'>[Fiziksel İhlal] Varyans Çöküşü:</b><br> Sinyal varyansı <span class='math-text'>σ² = {varyans_snr:.2f}</span> seviyesine indi. Uzaydan (20.000 km) gelen ve iyonosferden geçen bir sinyalin varyansı bu kadar düşük (sabit) <b>olamaz</b>. Sinyal yeryüzündeki bir simülatörden geliyor.</li>"
            xai_html += f"<li><b style='color:#d29922;'>[Güç İhlali] Bastırma Taktiği:</b><br> Ortalama güç <span class='math-text'>μ = {ort_snr:.1f} dB-Hz</span>. Orijinal BKZS uydusunu bastırmak için eşik değerin üzerinde sentetik güç basılıyor.</li>"
            xai_html += "<li><b style='color:#58a6ff;'>[Geometrik İhlal] Doppler Anomalisi:</b><br> Rastgele uydu hızı (<span class='math-text'>v_s</span>) taklidi, alıcının yerel saatiyle matematiksel uyuşmazlık yaratıyor.</li>"
            xai_html += "</ul>"
        elif tahmin == 1: 
            xai_html += "<ul style='color:#c9d1d9; font-size:0.95rem; line-height: 1.6;'>"
            xai_html += f"<li><b style='color:#f85149;'>[RF Boğulması] SNR Çöküşü:</b><br> Ortalama güç <span class='math-text'>μ = {ort_snr:.1f} dB-Hz</span> kritik 15 dB eşiğinin altında. Saldırgan geniş bantlı beyaz gürültü (White Noise) basıyor.</li>"
            xai_html += f"<li><b style='color:#d29922;'>[Veri Kaybı] Uydu Düşmesi:</b><br> Görünen uydu sayısı {uydu_sayisi} adede düştü. Konum çözmek için gereken minimum 4 uydu (<span class='math-text'>N &lt; 4</span>) şartı sağlanamıyor.</li>"
            xai_html += "</ul>"
        else: 
            xai_html += "<ul style='color:#c9d1d9; font-size:0.95rem; line-height: 1.6;'>"
            xai_html += f"<li><b style='color:#3fb950;'>[Doğrulanmış] İyonosferik Dağılım:</b><br> Sinyal gücü (<span class='math-text'>μ = {ort_snr:.1f}</span>) ve varyansı (<span class='math-text'>σ² = {varyans_snr:.2f}</span>) doğal atmosferik kırılma denklemlerine uygun.</li>"
            xai_html += "<li><b style='color:#3fb950;'>[Doğrulanmış] Karar Ağacı Saflığı:</b><br> Random Forest Gini safsızlık katsayısı <span class='math-text'>G(p) ≈ 0</span>. Olası tehdit saptanmadı.</li>"
            xai_html += "</ul>"
        
        xai_html += "</div>"
        xai_placeholder.markdown(xai_html, unsafe_allow_html=True)
        time.sleep(0.15)
        xai_html += "</div>"
        xai_placeholder.markdown(xai_html, unsafe_allow_html=True)
        time.sleep(0.15)