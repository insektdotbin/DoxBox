from art import text2art
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import os
import sys

# Initialize colorama
init()

# Supported algorithms and their hash lengths
HASH_INFO = {
    "1": ("md5", 32),
    "2": ("sha1", 40),
    "3": ("sha256", 64),
    "4": ("sha512", 128),
    "5": ("sha3_256", 64),
    "6": ("sha3_512", 128),
    "7": ("blake2b", 128),
    "8": ("blake2s", 64),
}


def print_banner():
    """Display program banner with warnings"""
    print(Fore.RED + text2art("DoxBox") + Style.RESET_ALL)
    print(
        Fore.YELLOW
        + "Ethical Use Warning: Only crack hashes you own or have permission to crack!\n"
        + Style.RESET_ALL
    )


def display_algorithms():
    """Show supported hashing algorithms"""
    print(Fore.CYAN + "Available Algorithms:")
    print(f"{Fore.WHITE}1. MD5 (Insecure)\n2. SHA-1 (Insecure)\n3. SHA-256\n4. SHA-512")
    print("5. SHA3-256\n6. SHA3-512\n7. BLAKE2b\n8. BLAKE2s" + Style.RESET_ALL)


def validate_hash(target_hash: str, algorithm: str) -> bool:
    """Validate hash format against selected algorithm"""
    expected_length = HASH_INFO[algorithm][1]
    return len(target_hash) == expected_length and all(
        c in "0123456789abcdef" for c in target_hash
    )


def load_wordlist(path: str) -> list:
    """Load and validate wordlist file"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Wordlist '{path}' not found")
    if os.path.getsize(path) > 100 * 1024 * 1024:  # 100MB limit
        raise ValueError("Wordlist too large (>100MB)")

    with open(path, "r", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def crack_hash(target_hash: str, algorithm: str, wordlist: list) -> str:
    """Multi-threaded hash cracking function"""
    algo_name = HASH_INFO[algorithm][0]
    target_hash = target_hash.lower()

    def test_password(password: str) -> bool:
        try:
            hasher = hashlib.new(algo_name)
            hasher.update(password.encode("utf-8"))
            return hasher.hexdigest() == target_hash
        except:
            return False

    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        futures = {executor.submit(test_password, pwd): pwd for pwd in wordlist}

        for future in as_completed(futures):
            if future.result():
                executor.shutdown(wait=False, cancel_futures=True)
                return futures[future]

    return None


def main():
    print_banner()
    try:
        # Algorithm selection
        display_algorithms()
        algorithm = input("\nSelect algorithm (1-8): ").strip()
        if algorithm not in HASH_INFO:
            print(Fore.RED + "Invalid algorithm selection" + Style.RESET_ALL)
            return

        # Hash input
        target_hash = input("Enter hash to crack: ").strip().lower()
        if not validate_hash(target_hash, algorithm):
            print(
                Fore.RED
                + "Invalid hash format for selected algorithm"
                + Style.RESET_ALL
            )
            return

        # Wordlist handling
        wordlist_path = input("Enter wordlist path: ").strip()
        try:
            wordlist = load_wordlist(wordlist_path)
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)
            return

        print(
            f"\n{Fore.YELLOW}Starting crack attempt with {len(wordlist)} passwords...{Style.RESET_ALL}"
        )

        # Attempt crack
        result = crack_hash(target_hash, algorithm, wordlist)

        if result:
            print(f"\n{Fore.GREEN}Success! Password found: {result}{Style.RESET_ALL}")
        else:
            print(
                f"\n{Fore.RED}Failed to crack hash. Try a different wordlist.{Style.RESET_ALL}"
            )

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    main()
