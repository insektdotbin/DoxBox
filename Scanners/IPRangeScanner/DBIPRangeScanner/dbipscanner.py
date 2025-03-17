from art import text2art
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import socket
import sys
import os

# Initialize colorama
init()

# Constants
MAX_WORKERS = 50  # Thread pool size
DEFAULT_TIMEOUT = 0.5  # Seconds

def print_banner():
    """Display program banner"""
    print(Fore.CYAN + text2art("DoxBox IP Scanner") + Style.RESET_ALL)
    print(Fore.YELLOW + "Warning: Only scan networks you're authorized to access!\n" + Style.RESET_ALL)

def validate_ip(ip: str) -> bool:
    """Validate IPv4 address format"""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def get_ip_range():
    """Get and validate IP range input"""
    while True:
        print(Fore.WHITE + "\nIP Input Options:")
        print("1. CIDR Notation (e.g., 192.168.1.0/24)")
        print("2. Start-End IP Range (e.g., 192.168.1.1-192.168.1.254)")
        choice = input("Choose input method (1/2): " + Style.RESET_ALL).strip()

        if choice == '1':
            cidr = input(Fore.WHITE + "Enter CIDR notation: " + Style.RESET_ALL).strip()
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                return [str(ip) for ip in network.hosts()]
            except ValueError:
                print(Fore.RED + "Invalid CIDR notation" + Style.RESET_ALL)

        elif choice == '2':
            start_ip = input(Fore.WHITE + "Enter starting IP: " + Style.RESET_ALL).strip()
            end_ip = input(Fore.WHITE + "Enter ending IP: " + Style.RESET_ALL).strip()
            
            if not validate_ip(start_ip) or not validate_ip(end_ip):
                print(Fore.RED + "Invalid IP format" + Style.RESET_ALL)
                continue
                
            start = list(map(int, start_ip.split('.')))
            end = list(map(int, end_ip.split('.')))
            
            if start > end:
                print(Fore.RED + "Start IP must be <= End IP" + Style.RESET_ALL)
                continue
                
            return generate_ip_range(start_ip, end_ip)

        else:
            print(Fore.RED + "Invalid choice" + Style.RESET_ALL)

def generate_ip_range(start_ip: str, end_ip: str) -> list:
    """Generate list of IPs between start and end addresses"""
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))
    ips = []
    
    while start <= end:
        ips.append('.'.join(map(str, start)))
        # Increment IP
        for i in reversed(range(4)):
            start[i] += 1
            if start[i] <= 255:
                break
            start[i] = 0
            if i == 0:
                break
    return ips

def get_ports():
    """Get and validate port input"""
    while True:
        ports_input = input(Fore.WHITE + "\nEnter ports (e.g., 80,443 or 1-100): " + Style.RESET_ALL).strip()
        try:
            if '-' in ports_input:
                start, end = map(int, ports_input.split('-'))
                if 1 <= start <= end <= 65535:
                    return list(range(start, end + 1))
                raise ValueError
            else:
                ports = [int(p) for p in ports_input.split(',')]
                if all(1 <= p <= 65535 for p in ports):
                    return ports
                raise ValueError
        except ValueError:
            print(Fore.RED + "Invalid port range (1-65535)" + Style.RESET_ALL)

def get_timeout():
    """Get connection timeout value"""
    while True:
        timeout = input(Fore.WHITE + f"Enter timeout [default {DEFAULT_TIMEOUT}s]: " + Style.RESET_ALL).strip()
        if not timeout:
            return DEFAULT_TIMEOUT
        try:
            timeout = float(timeout)
            if timeout > 0:
                return timeout
            raise ValueError
        except ValueError:
            print(Fore.RED + "Invalid timeout value" + Style.RESET_ALL)

def scan_port(ip: str, port: int, timeout: float):
    """Scan a single port on target IP"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"{Fore.GREEN}Port {port} open on {ip}{Style.RESET_ALL}")
                return (ip, port, 'Open')
            else:
                return (ip, port, 'Closed')
        except socket.timeout:
            return (ip, port, 'Filtered')
        except Exception as e:
            return (ip, port, f'Error: {str(e)}')

def scan_ip(ip: str, ports: list, timeout: float):
    """Scan multiple ports on a single IP"""
    print(f"\n{Fore.CYAN}Scanning {ip}...{Style.RESET_ALL}")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(scan_port, ip, port, timeout) for port in ports]
        return [f.result() for f in futures]

def main():
    print_banner()
    try:
        # Get user inputs
        ips = get_ip_range()
        ports = get_ports()
        timeout = get_timeout()
        
        # Scan configuration summary
        print(f"\n{Fore.YELLOW}Starting scan...")
        print(f"Targets: {len(ips)} IPs")
        print(f"Ports: {len(ports)} ports")
        print(f"Timeout: {timeout}s")
        print(f"Threads: {MAX_WORKERS}{Style.RESET_ALL}\n")
        
        # Perform scanning
        results = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(scan_ip, ip, ports, timeout) for ip in ips]
            for future in futures:
                results.extend(future.result())
        
        # Generate report
        print(f"\n{Fore.CYAN}=== Scan Results ===")
        open_hosts = set()
        for result in results:
            if result[2] == 'Open':
                open_hosts.add(result[0])
                print(f"{Fore.GREEN}{result[0]}:{result[1]} - {result[2]}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Summary:")
        print(f"Scanned {len(ips)} hosts")
        print(f"Found {len(open_hosts)} hosts with open ports")
        print(f"Total open ports found: {len([r for r in results if r[2] == 'Open'])}{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Scan aborted by user!{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    main()