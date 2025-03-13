from art import text2art
from colorama import Fore, Style, init
import hashlib
import sys

# Initialize colorama
init()

# Supported hash algorithms
HASH_ALGORITHMS = {
    "1": "md5",
    "2": "sha1",
    "3": "sha256",
    "4": "sha384",
    "5": "sha512",
    "6": "sha3_256",
    "7": "sha3_512",
    "8": "blake2s",
    "9": "blake2b",
}


def print_banner():
    """Display program banner"""
    print(Fore.CYAN + text2art("Hash Tool") + Style.RESET_ALL)
    print(
        Fore.YELLOW
        + "Warning: Avoid using MD5/SHA1 for sensitive data!\n"
        + Style.RESET_ALL
    )


def display_menu():
    """Show hash algorithm options"""
    print(Fore.WHITE + "Available Hash Algorithms:")
    print(f"{Fore.CYAN}1. MD5{Style.RESET_ALL} (Insecure)")
    print(f"{Fore.CYAN}2. SHA-1{Style.RESET_ALL} (Insecure)")
    print(f"{Fore.GREEN}3. SHA-256")
    print("4. SHA-384")
    print("5. SHA-512")
    print("6. SHA3-256")
    print("7. SHA3-512")
    print("8. BLAKE2s")
    print(f"9. BLAKE2b{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}0. Exit{Style.RESET_ALL}\n")


def get_algorithm_choice():
    """Get and validate algorithm selection"""
    while True:
        choice = input(
            Fore.WHITE + "Choose algorithm (1-9, 0 to exit): " + Style.RESET_ALL
        ).strip()
        if choice == "0":
            print(Fore.YELLOW + "\nExiting..." + Style.RESET_ALL)
            sys.exit(0)
        if choice in HASH_ALGORITHMS:
            return HASH_ALGORITHMS[choice]
        print(
            Fore.RED
            + "Invalid choice. Please select 1-9 or 0 to exit."
            + Style.RESET_ALL
        )


def get_input_text():
    """Get text input with validation"""
    while True:
        text = input(Fore.WHITE + "\nEnter text to hash: " + Style.RESET_ALL).strip()
        if text:
            return text
        print(Fore.RED + "Error: Input cannot be empty" + Style.RESET_ALL)


def compute_hash(text: str, algorithm: str):
    """Compute hash value with error handling"""
    try:
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode("utf-8"))
        return hasher.hexdigest()
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)
        return None


def display_result(text: str, algorithm: str, digest: str):
    """Display formatted hash result"""
    print(f"\n{Fore.GREEN}=== Hash Result ===")
    print(f"{Fore.WHITE}Algorithm: {Fore.CYAN}{algorithm.upper()}")
    print(f"{Fore.WHITE}Input: {Fore.YELLOW}{text}")
    print(f"{Fore.WHITE}Digest: {Fore.GREEN}{digest}")
    print("===================" + Style.RESET_ALL)


def main():
    print_banner()
    while True:
        try:
            display_menu()
            algorithm = get_algorithm_choice()
            text = get_input_text()

            if algorithm in ["md5", "sha1"]:
                print(
                    Fore.RED
                    + "Warning: This algorithm is considered cryptographically weak!"
                    + Style.RESET_ALL
                )

            digest = compute_hash(text, algorithm)

            if digest:
                display_result(text, algorithm, digest)
            else:
                print(Fore.RED + "Failed to compute hash" + Style.RESET_ALL)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nOperation cancelled by user" + Style.RESET_ALL)
            sys.exit(1)


if __name__ == "__main__":
    main()
