# 🛰️ NullSpace RF | Zero-Trust GNSS Radar

![Python](https://img.shields.io/badge/Python-3.10-blue)
![AI](https://img.shields.io/badge/AI-RandomForest-green)
![License](https://img.shields.io/badge/License-MIT-orange)
![Status](https://img.shields.io/badge/Status-Research-red)

<div align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Türkiye_Uzay_Ajansı_logo.svg/1024px-Türkiye_Uzay_Ajansı_logo.svg.png" width="150">

<h1>🛰️ NullSpace RF | Zero-Trust GNSS Radar</h1>

<p><b>Bölgesel Konumlama ve Zamanlama Sistemi (BKZS) İçin Açık Kaynaklı, Çoklu-Yörünge Siber Savunma Kalkanı</b></p>

<p><i>TUA Astro Hackathon 2026 - Geliştirici: <b>Team Null Proof</b></i></p>
</div>

---

# 🚀 Proje Vizyonu ve Çözülen Problem

Günümüzde İHA/SİHA'lar, otonom deniz araçları ve kritik altyapılar yönlerini bulmak için **GNSS (Küresel Navigasyon Uydu Sistemleri)** sinyallerine mutlak bağımlıdır. Ancak bu sinyaller yeryüzüne ulaştığında çok zayıftır (yaklaşık **−160 dBW**) ve **Elektronik Harp (EH)** saldırılarına karşı son derece kırılgandır.

**NullSpace RF**, GNSS alıcılarına yönelik gerçekleştirilen iki ölümcül saldırıyı **uç cihazda (Edge Computing)** tespit edip engellemek için tasarlanmıştır.

Desteklenen sistemler:

* GPS
* GLONASS
* Galileo
* BeiDou
* Gelecekteki Türkiye **BKZS** uyduları

Tespit edilen saldırı türleri:

### 1️⃣ Spoofing (Sinyal Yanıltma)

Otonom araçları rotasından çıkarmak için sahte uydu sinyalleri üretilmesi.

### 2️⃣ Jamming (Sinyal Körleştirme)

Yüksek güçlü beyaz gürültü ile GNSS alıcısının sinyal alamaz hale getirilmesi.

---

# 🧠 Yapay Zeka ve Veri

Projemizin yapay zeka modeli sentetik verilerle değil, **CERN altyapısında Zenodo üzerinden yayınlanan MARSIM veri setinden elde edilen gerçek ağ trafiği (PCAP)** ile eğitilmiştir.

### Büyük Veri

Sistem **39.000.000 satırlık rafine ağ paketi** üzerinde eğitilmiş bir **Random Forest** modeli kullanır.

### Sıfır Yanlış Alarm

Savunma sistemleri için kritik olan **Precision metriği** optimize edilmiştir.

* Precision: **%99**
* Yanlış saldırı alarmı: **%1'in altında**

### Açıklanabilir Yapay Zeka (XAI)

NullSpace RF bir **black-box sistem değildir**.

XAI paneli sayesinde:

* saldırının nedeni
* kullanılan özellikler
* fiziksel anomaliler

anlık olarak raporlanır.

---

# 📐 Fiziksel Matematik ve Tespit Vektörleri

NullSpace RF yalnızca makine öğrenmesi kullanmaz.

Aynı zamanda **uzay fiziği ve RF davranışlarını** analiz eder.

---

## 1️⃣ İyonosferik Varyans Çöküşü (Spoofing Tespiti)

Uzaydan gelen GNSS sinyalleri **iyonosferden geçerken doğal bir gürültü ve varyans oluşturur**.

Ancak yerdeki bir **SDR spoofing cihazı** bu doğal varyansı taklit edemez.

Sistem aşağıdaki varyans hesaplamasını yapar:

```
σ² = (1 / N) Σ (xi − μ)²
```

Eğer varyans doğal atmosferik dağılım limitlerinin altına düşerse sistem:

**"Bu sinyal uzaydan gelmiyor"**

sonucuna ulaşır ve bağlantıyı izole eder.

---

## 2️⃣ RF Boğulması ve Uydu Düşmesi (Jamming Tespiti)

Sistem sürekli olarak ortalama sinyal gücünü (**μ**) izler.

Jamming saldırısında:

* bant genişliği beyaz gürültü ile doldurulur
* SNR hızla düşer
* minimum uydu sayısı şartı bozulur

Konum çözümü için gereken minimum uydu sayısı:

```
N ≥ 4
```

Eğer bu şart ihlal edilirse sistem **jamming alarmı üretir.**

---

# 💻 Kurulum ve Kullanım

Sistem düşük donanımlı cihazlar için optimize edilmiştir.

Desteklenen platformlar:

* Raspberry Pi
* İHA yerleşik bilgisayarları
* Edge AI cihazları
* standart Linux makineler

Model boyutu yaklaşık:

**~436 KB**

---

# 1️⃣ Repoyu Klonlayın

```bash
git clone https://github.com/burakdevelopment/nullspacerf.git

cd nullspacerf
```

---

# 2️⃣ Bağımlılıkları Kurun

Python 3.10+ gereklidir.

```bash
pip install scikit-learn streamlit pandas numpy plotly joblib
```

---

# 3️⃣ Başlatın

Radar arayüzünü çalıştırmak için:

```bash
streamlit run bkzs.py
```

---

# 4️⃣ Canlı Analiz

Tarayıcıda açılan arayüzde:

1️⃣ `.pcap` dosyasını yükleyin
2️⃣ **Canlı Analizi Başlat** butonuna tıklayın

Sistem milisaniyeler içinde:

* ağ paketlerini analiz eder
* sinyal davranışlarını ölçer
* saldırıları tespit eder
* XAI panelinde sonuçları raporlar

---

# 📂 Proje Yapısı

```
nullspacerf
│
├── bkzs.py
├── bkzs_v4_model.pkl
├── demo_attack_1.pcap
├── demo_attack_2.pcap
└── README.md
```

### Dosya Açıklamaları

**bkzs.py**

Streamlit tabanlı komuta merkezi ve XAI radar arayüzü.

**bkzs_v4_model.pkl**

39 milyon paket verisi ile eğitilmiş Random Forest modeli.

**.pcap dosyaları**

Demo ve test saldırı senaryoları.

---

<div align="center">

**Null Proof Ekibi Tarafından Kodlanmıştır**

</div>

