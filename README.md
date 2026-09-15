# Python Network Port Scanner

A beginner-friendly cybersecurity project written in Python that scans TCP ports on a target host and identifies commonly associated services.

## Features

- TCP port scanning
- Custom target IP or hostname
- Custom port range
- Open-port detection
- Basic service identification
- Input validation
- Hostname resolution
- Keyboard interrupt handling

## Technologies Used

- Python 3
- Socket Programming
- TCP/IP Networking

## How It Works

The scanner attempts to establish a TCP connection to each port in the specified range.

If the connection succeeds, the port is reported as open.

Common port numbers are mapped to their commonly associated services, such as:

- 22 → SSH
- 80 → HTTP
- 443 → HTTPS
- 3306 → MySQL
- 8000 → HTTP Development Server

## How to Run

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
