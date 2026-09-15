# CyberScan - Python Network Port Scanner

CyberScan is a beginner-friendly cybersecurity tool built with **Python and Flask** that scans TCP ports on a target system and identifies commonly associated network services.

The project includes both a command-line scanner and a web-based dashboard with live scan progress.

## Features

- TCP port scanning using Python socket programming
- Custom target IP address or hostname
- Custom starting and ending port
- Detection of open TCP ports
- Basic identification of commonly associated services
- Input validation and error handling
- Hostname resolution
- Flask-based web dashboard
- Background scanning to keep the web interface responsive
- Live scan progress percentage
- Current port tracking
- Open-port counter
- Keyboard interrupt handling in the command-line scanner
- Responsible security-testing guidance

## Technologies Used

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- Socket Programming
- TCP/IP Networking
- Git & GitHub

## Project Structure

```text
python-network-port-scanner/
│
├── app.py
├── scanner.py
├── README.md
├── scanner-output.png
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
