# 🛰️ NullSpace RF | Zero-Trust GNSS Radar

![Python](https://img.shields.io/badge/Python-3.10-blue)
![AI](https://img.shields.io/badge/AI-RandomForest-green)
![License](https://img.shields.io/badge/License-MIT-orange)
![Status](https://img.shields.io/badge/Status-Research-red)

<div align="center">
<img src="https://images.seeklogo.com/logo-png/45/2/turkiye-uzay-ajansi-tua-logo-png_seeklogo-453642.png" width="150">

<h1>🛰️ NullSpace RF | Zero-Trust GNSS Radar</h1>

<p><b>An Open-Source, Multi-Orbit Cyber Defense Shield for the Regional Positioning and Timing System (BKZS)</b></p>

<p><i>TUA Astro Hackathon 2026 - Developer: <b>Team Null Proof</b></i></p>
</div>

---

# 🚀 Project Vision and the Problem Solved

Today, UAVs/UCAVs, autonomous marine vehicles, and critical infrastructure are absolutely dependent on **GNSS (Global Navigation Satellite Systems)** signals to find their way. However, these signals are extremely weak by the time they reach the ground (approximately **−160 dBW**) and are highly fragile against **Electronic Warfare (EW)** attacks.

**NullSpace RF** is designed to detect and block two lethal attacks against GNSS receivers directly on the **edge device (Edge Computing)**.

Supported systems:

* GPS
* GLONASS
* Galileo
* BeiDou
* Türkiye's future **BKZS** satellites

Detected attack types:

### 1️⃣ Spoofing (Signal Deception)

Generating fake satellite signals to steer autonomous vehicles off their route.

### 2️⃣ Jamming (Signal Blinding)

Rendering the GNSS receiver unable to receive signals using high-power white noise.

---

# 🧠 Artificial Intelligence and Data

Our project's AI model was trained not with synthetic data, but with **real network traffic (PCAP) obtained from the MARSIM dataset published on Zenodo over CERN infrastructure**.

### Big Data

The system uses a **Random Forest** model trained on **39,000,000 rows of refined network packets**.

- https://zenodo.org/records/8202936

### Zero False Alarms

The **Precision metric**, which is critical for defense systems, has been optimized.

* Precision: **99%**
* False attack alarms: **below 1%**

### Explainable Artificial Intelligence (XAI)

NullSpace RF is **not a black-box system**.

Thanks to the XAI panel:

* the reason for the attack
* the features used
* physical anomalies

are reported in real time.

---

# 📐 Physical Mathematics and Detection Vectors

NullSpace RF does not use machine learning alone.

It also analyzes **space physics and RF behaviors**.

---

## 1️⃣ Ionospheric Variance Collapse (Spoofing Detection)

GNSS signals arriving from space **generate natural noise and variance as they pass through the ionosphere**.

However, a ground-based **SDR spoofing device** cannot replicate this natural variance.

The system performs the following variance calculation:

```
σ² = (1 / N) Σ (xi − μ)²
```

If the variance drops below the natural atmospheric distribution limits, the system concludes:

**"This signal is not coming from space"**

and it isolates the connection.

---

## 2️⃣ RF Choking and Satellite Dropout (Jamming Detection)

The system continuously monitors the average signal power (**μ**).

During a jamming attack:

* the bandwidth is filled with white noise
* the SNR drops rapidly
* the minimum satellite count requirement is violated

The minimum number of satellites required for a position solution:

```
N ≥ 4
```

If this condition is violated, the system **generates a jamming alarm.**

---

# 💻 Installation and Usage

The system is optimized for low-hardware devices.

Supported platforms:

* Raspberry Pi
* UAV onboard computers
* Edge AI devices
* standard Linux machines

Approximate model size:

**~436 KB**

---

# 1️⃣ Clone the Repository

```bash
git clone https://github.com/burakdevelopment/nullspacerf.git

cd nullspacerf
```

---

# 2️⃣ Install Dependencies

Python 3.10+ is required.

```bash
pip install scikit-learn streamlit pandas numpy plotly joblib
```

---

# 3️⃣ Launch

To run the radar interface:

```bash
streamlit run bkzs.py
```

---

# 4️⃣ Live Analysis

In the interface that opens in your browser:

1️⃣ Upload the `.pcap` file
2️⃣ Click the **Start Live Analysis** button

Within milliseconds, the system:

* analyzes the network packets
* measures signal behaviors
* detects attacks
* reports the results in the XAI panel

---

# 📂 Project Structure

```
nullspacerf
│
├── bkzs.py
├── bkzs_v4_model.pkl
├── demo_attack_1.pcap
├── demo_attack_2.pcap
└── README.md
```

### File Descriptions

**bkzs.py**

Streamlit-based command center and XAI radar interface.

**bkzs_v4_model.pkl**

Random Forest model trained on 39 million packets of data.

**.pcap files**

Demo and test attack scenarios.

---

<div align="center">

**Coded by the Null Proof Team**

</div>
