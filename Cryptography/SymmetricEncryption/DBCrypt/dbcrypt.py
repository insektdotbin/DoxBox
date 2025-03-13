from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from art import text2art
from colorama import init, Fore, Style
import base64
import os

# Initialize colorama
init()

# Constants
KDF_ITERATIONS = 480000
SALT_LENGTH = 16


def print_banner():
    """Print the program banner with colored ASCII art"""
    print(Fore.BLUE + text2art("DoxBox") + Style.RESET_ALL)
    print(Fore.CYAN + "== Secure Encryption & Decryption Tool ==" + Style.RESET_ALL)
    print(
        Fore.YELLOW
        + "Warning: Keep your password secure! It cannot be recovered.\n"
        + Style.RESET_ALL
    )


def generate_key(password: str, salt: bytes) -> bytes:
    """Derive a secure key from password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_text(text: str, password: str) -> str:
    """Encrypt text with password-based key"""
    salt = os.urandom(SALT_LENGTH)
    key = generate_key(password, salt)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(text.encode())
    return base64.urlsafe_b64encode(salt + encrypted_data).decode()


def decrypt_text(encrypted_text: str, password: str) -> str:
    """Decrypt text with password-based key"""
    try:
        combined_data = base64.urlsafe_b64decode(encrypted_text.encode())
        salt, encrypted_data = combined_data[:SALT_LENGTH], combined_data[SALT_LENGTH:]
        key = generate_key(password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data).decode()
    except (InvalidToken, ValueError, TypeError):
        return None


def get_password() -> str:
    """Securely get password from user with validation"""
    while True:
        password = input(Fore.WHITE + "Enter password: " + Style.RESET_ALL).strip()
        if len(password) >= 8:
            return password
        print(
            Fore.RED + "Error: Password must be at least 8 characters" + Style.RESET_ALL
        )


def get_input(prompt: str) -> str:
    """Get validated user input"""
    while True:
        user_input = input(Fore.WHITE + prompt + Style.RESET_ALL).strip()
        if user_input:
            return user_input
        print(Fore.RED + "Error: Input cannot be empty" + Style.RESET_ALL)


def display_result(message: str, success: bool = True):
    """Display formatted results with color coding"""
    color = Fore.GREEN if success else Fore.RED
    print(color + "\n" + "=" * 50)
    print(f"{message}")
    print("=" * 50 + "\n" + Style.RESET_ALL)


def main_menu():
    """Display main menu interface"""
    print("\nOptions:")
    print(Fore.CYAN + "1. Encrypt Text")
    print("2. Decrypt Text")
    print("3. Exit" + Style.RESET_ALL)


def main():
    print_banner()
    while True:
        main_menu()
        choice = get_input("Enter choice (1-3): ")

        if choice == "1":
            text = get_input("Enter text to encrypt: ")
            password = get_password()
            encrypted = encrypt_text(text, password)
            display_result(f"ENCRYPTED TEXT:\n{encrypted}")

        elif choice == "2":
            encrypted_text = get_input("Enter encrypted text: ")
            password = get_password()
            decrypted = decrypt_text(encrypted_text, password)

            if decrypted:
                display_result(f"DECRYPTED TEXT:\n{decrypted}")
            else:
                display_result("DECRYPTION FAILED! Invalid password or data", False)

        elif choice == "3":
            print(Fore.YELLOW + "\nExiting DoxBox... Stay secure!" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "\nInvalid choice. Please enter 1-3" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
