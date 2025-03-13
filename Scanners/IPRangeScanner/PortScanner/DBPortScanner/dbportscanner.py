import socket
import sys
import time
import errno
from colorama import Fore, Style, init
from art import text2art

# Initialize colorama for cross-platform colored output
init()


def print_banner():
    print(Fore.BLUE + text2art("DoxBox") + Style.RESET_ALL)
    print(Fore.CYAN + "=== DoxBox Port Scanner ===" + Style.RESET_ALL)


def get_target_host():
    while True:
        host = input("Enter target host (IP or domain name): ").strip()
        try:
            ip = socket.gethostbyname(host)
            return ip
        except socket.gaierror:
            print(
                Fore.RED
                + "Error: Invalid host. Please enter a valid IP or domain name."
                + Style.RESET_ALL
            )


def get_port_range():
    while True:
        try:
            start_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
            if 1 <= start_port <= end_port <= 65535:
                return start_port, end_port
            print(
                Fore.RED
                + "Error: Ports must be between 1-65535 and start <= end."
                + Style.RESET_ALL
            )
        except ValueError:
            print(Fore.RED + "Error: Please enter valid integers." + Style.RESET_ALL)


def get_specific_ports():
    while True:
        try:
            ports_input = input(
                "Enter specific ports (comma-separated, e.g., 80,443,8080): "
            ).strip()
            ports = [int(port.strip()) for port in ports_input.split(",")]
            if all(1 <= port <= 65535 for port in ports):
                return ports
            print(Fore.RED + "Error: Ports must be between 1-65535." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Error: Please enter valid integers." + Style.RESET_ALL)


def get_timeout():
    while True:
        try:
            timeout = float(input("Enter connection timeout (seconds, e.g., 0.5): "))
            if timeout > 0:
                return timeout
            print(Fore.RED + "Error: Timeout must be positive." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Error: Please enter a valid number." + Style.RESET_ALL)


def scan_ports(host, ports, timeout):
    open_ports = []
    print(Fore.CYAN + f"\nStarting scan on {host}..." + Style.RESET_ALL)
    print(Fore.YELLOW + "Press Ctrl+C to abort the scan.\n" + Style.RESET_ALL)
    start_time = time.time()

    try:
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                try:
                    result = s.connect_ex((host, port))
                    if result == 0:
                        print(Fore.GREEN + f"Port {port}: Open" + Style.RESET_ALL)
                        open_ports.append(port)
                    else:
                        if result == errno.ECONNREFUSED:
                            print(Fore.RED + f"Port {port}: Closed" + Style.RESET_ALL)
                        else:
                            print(
                                Fore.YELLOW
                                + f"Port {port}: Filtered/Error (code {result})"
                                + Style.RESET_ALL
                            )
                except socket.timeout:
                    print(
                        Fore.YELLOW
                        + f"Port {port}: Filtered (timeout)"
                        + Style.RESET_ALL
                    )
                except Exception as e:
                    print(Fore.RED + f"Port {port}: Error - {str(e)}" + Style.RESET_ALL)

    except KeyboardInterrupt:
        print(Fore.RED + "\nScan aborted by user!" + Style.RESET_ALL)
        sys.exit(1)

    duration = time.time() - start_time
    print(Fore.CYAN + f"\nScan completed in {duration:.2f} seconds" + Style.RESET_ALL)
    return open_ports


def main():
    print_banner()
    host = get_target_host()
    timeout = get_timeout()

    while True:
        choice = input(
            "\nChoose scanning mode:\n1. Scan a range of ports\n2. Scan specific ports\nEnter your choice (1 or 2): "
        ).strip()
        if choice == "1":
            start_port, end_port = get_port_range()
            ports = range(start_port, end_port + 1)
            break
        elif choice == "2":
            ports = get_specific_ports()
            break
        else:
            print(
                Fore.RED
                + "Error: Invalid choice. Please enter 1 or 2."
                + Style.RESET_ALL
            )

    open_ports = scan_ports(host, ports, timeout)

    if open_ports:
        print(Fore.GREEN + "\nOpen ports found:" + Style.RESET_ALL)
        for port in sorted(open_ports):
            print(Fore.GREEN + f" - Port {port}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo open ports found." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
