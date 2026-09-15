from flask import Flask, render_template, request, jsonify
import socket
import threading
import uuid

app = Flask(__name__)

COMMON_SERVICES = {
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
    8000: "HTTP Development Server",
    8080: "HTTP Proxy"
}

scans = {}


def scan_ports(scan_id, target, start_port, end_port):
    try:
        target_ip = socket.gethostbyname(target)

        total_ports = end_port - start_port + 1

        scans[scan_id]["target_ip"] = target_ip
        scans[scan_id]["status"] = "scanning"

        for current, port in enumerate(
            range(start_port, end_port + 1),
            start=1
        ):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            result = sock.connect_ex((target_ip, port))

            if result == 0:
                service = COMMON_SERVICES.get(port, "Unknown")

                scans[scan_id]["results"].append({
                    "port": port,
                    "state": "OPEN",
                    "service": service
                })

            sock.close()

            scans[scan_id]["current_port"] = port
            scans[scan_id]["progress"] = int(
                (current / total_ports) * 100
            )

        scans[scan_id]["status"] = "completed"

    except socket.gaierror:
        scans[scan_id]["status"] = "error"
        scans[scan_id]["error"] = "Hostname could not be resolved."

    except Exception as e:
        scans[scan_id]["status"] = "error"
        scans[scan_id]["error"] = str(e)


@app.route("/", methods=["GET", "POST"])
def index():

    results = []
    target = ""
    error = ""

    if request.method == "POST":

        target = request.form.get("target", "").strip()

        try:
            start_port = int(request.form.get("start_port"))
            end_port = int(request.form.get("end_port"))

            if not target:
                error = "Please enter a target."

            elif start_port < 1 or end_port > 65535:
                error = "Ports must be between 1 and 65535."

            elif start_port > end_port:
                error = "Starting port cannot be greater than ending port."

            else:

                # JavaScript request
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":

                    scan_id = str(uuid.uuid4())

                    scans[scan_id] = {
                        "target": target,
                        "target_ip": "",
                        "progress": 0,
                        "current_port": start_port,
                        "status": "starting",
                        "results": [],
                        "error": ""
                    }

                    thread = threading.Thread(
                        target=scan_ports,
                        args=(scan_id, target, start_port, end_port)
                    )

                    thread.start()

                    return jsonify({
                        "scan_id": scan_id
                    })

                # Normal form submission
                else:
                    target_ip, results = scan_ports_sync(
                        target,
                        start_port,
                        end_port
                    )

        except ValueError:
            error = "Port numbers must be integers."

        except socket.gaierror:
            error = "Hostname could not be resolved."

    return render_template(
        "index.html",
        results=results,
        target=target,
        error=error
    )


def scan_ports_sync(target, start_port, end_port):
    results = []

    target_ip = socket.gethostbyname(target)

    for port in range(start_port, end_port + 1):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            service = COMMON_SERVICES.get(port, "Unknown")

            results.append({
                "port": port,
                "state": "OPEN",
                "service": service
            })

        sock.close()

    return target_ip, results


@app.route("/progress/<scan_id>")
def progress(scan_id):

    scan = scans.get(scan_id)

    if not scan:
        return jsonify({
            "error": "Scan not found."
        }), 404

    return jsonify(scan)


if __name__ == "__main__":
    app.run(debug=True)