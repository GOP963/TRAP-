

***

# 🕸️ TRAP v8.0 | Multi-Vector Auditing Framework

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-red.svg)
![Type](https://img.shields.io/badge/Security-Auditing-critical.svg)

**TRAP v8.0** is an advanced social engineering and security auditing framework designed to demonstrate vulnerabilities in browser-based permissions. It utilizes deceptive, high-fidelity user interfaces to collect environmental data, including precise geolocation, visual snapshots, and ambient audio.

---

## 💎 Key Modules

### 📍 1. Waze Navigation Auditor
*   **Deceptive Scenario:** Mimics a live Waze traffic update page.
*   **Mechanism:** Utilizes the Geolocation API to retrieve high-accuracy coordinates.
*   **Visuals:** Integrated with OpenStreetMap (Leaflet.js) to display a real-time map, reducing user suspicion.

### 📸 2. Instagram/Snapchat AR Lens
*   **Deceptive Scenario:** A "Filter Preview" page for social media.
*   **Features:** Includes **5 custom real-time filters**:
    *   **Normal:** Raw feed.
    *   **Grayscale & Sepia:** Classic aesthetic looks.
    *   **Hue-Rotate:** Cyberpunk color cycling.
    *   **Rabbit Mask:** An overlay AR filter to maximize engagement.
*   **Mechanism:** Periodically captures snapshots and transmits them to the C2 server.

### 🎵 3. Shazam Audio Sync
*   **Deceptive Scenario:** A song identification service.
*   **Mechanism:** Captures high-frequency audio streams via the MediaRecorder API.
*   **Visuals:** Features a pulsing "Shazam" logo and CSS3 animations to simulate a real audio analysis process.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Flask
- Colorama

### Quick Start
```bash
# Clone the repository
git clone https://github.com/charon/trap-v8.git

# Navigate to the directory
cd trap-v8

# Install dependencies
pip install flask colorama
```

---

## 🚀 Execution

To launch the command-line interface and start the server:

```bash
python trap.py
```

### 🌐 Deployment (Remote Access)
To test the framework outside of a local network, use a tunnel like **Ngrok** to provide a secure HTTPS link (Required for Camera/GPS permissions):

```bash
ngrok http 5000
```

---

## 📂 Project Structure

| Directory | Description |
| :--- | :--- |
| `captured_photos/` | Stores all incoming JPG snapshots from the AR module. |
| `recordings/` | Stores raw audio streams (.wav) from the Shazam module. |
| `coordinates.txt` | Logs timestamps and precise Latitude/Longitude data. |
| `trap.py` | The core Python backend and CLI controller. |

---

## 🛡️ Disclaimer
**TRAP v8.0** is intended for **Authorized Security Auditing** and **Educational Purposes** only. Unauthorized use of this tool for data collection without explicit consent is illegal. The developer (**Charon**) is not responsible for any misuse or damage caused by this software. Use it ethically and responsibly.

---

## 👨‍💻 Author
**Developed by [Charon]**  
*Building tools for the next generation of security research.*

***

