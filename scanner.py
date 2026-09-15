import socket

common_services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP Proxy",
    8000: "HTTP Development Server"
}

print("=" * 50)
print("       Python Network Port Scanner")
print("=" * 50)

try:
    target = input("Enter target IP or hostname: ").strip()

    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    if start_port < 1 or end_port > 65535:
        print("Error: Ports must be between 1 and 65535.")
        exit()

    if start_port > end_port:
        print("Error: Starting port cannot be greater than ending port.")
        exit()

    target_ip = socket.gethostbyname(target)

    print(f"\nTarget: {target}")
    print(f"IP Address: {target_ip}")
    print(f"Scanning ports {start_port}-{end_port}")
    print("-" * 50)

    open_ports = 0

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            service = common_services.get(port, "Unknown")
            print(f"[OPEN] Port {port} - {service}")
            open_ports += 1

        sock.close()

    print("-" * 50)
    print(f"Scan completed. Open ports found: {open_ports}")

except ValueError:
    print("Error: Port numbers must be integers.")

except socket.gaierror:
    print("Error: Hostname could not be resolved.")

except KeyboardInterrupt:
    print("\nScan cancelled by user.")