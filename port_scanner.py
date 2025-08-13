import socket
import threading

# Mapping of common ports to service names
COMMON_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    123: 'NTP',
    143: 'IMAP',
    443: 'HTTPS',
    3389: 'RDP',
}

open_ports = []

def scan_port(ip, port):
    """
    Tries to connect to the given port on the target IP.
    If successful, adds port to open_ports list.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout in seconds
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = COMMON_PORTS.get(port, 'Unknown')
            print(f"Port {port} [OPEN] ({service})")
            open_ports.append((port, service))
    except Exception as e:
        pass  # Ignore exceptions for closed ports
    finally:
        sock.close()

def main():
    print("=== Basic Python Port Scanner ===")
    target = input("Enter target IP address (e.g. 192.168.1.1): ").strip()
    start_port = int(input("Enter start port (e.g. 20): ").strip())
    end_port = int(input("Enter end port (e.g. 1024): ").strip())
    print(f"\nScanning {target} from port {start_port} to {end_port} ...")

    threads = []

    # Create and start a thread for each port in range
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()
    
    print("\n--- Scan Complete ---")
    if open_ports:
        print("Open ports found:")
        for port, service in open_ports:
            print(f"Port {port} - {service}")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
