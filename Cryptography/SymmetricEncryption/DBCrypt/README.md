# DoxBox Cryptography Tool
## Overview
The Cryptography Tool provides symmetric encryption and decryption using the Fernet module. It uses AES-128 encryption with PBKDF2 for key derivation.

## Features
+ Encrypts and decrypts text.
+ Password-based key derivation.
+ Secure token generation.

## Installation
1. Install Python 3.8+.
2. Install dependencies:

```bash
pip install art colorama
```
3. Download the Project:

```bash
git clone https://github.com/insektdotbin/DoxBox
```
# Usage
```bash
python dbcrypt.py
```
+ Choose to encrypt or decrypt text.
+ Enter the text and a password.

## Example:
```
Choose operation:
1. Encrypt Text
2. Decrypt Text
Enter choice (1/2): 1
Enter text to encrypt: Secret Message
Enter password: mypassword
```

# Ethical Guidelines
Only encrypt/decrypt data you own or have permission to access.
Keep passwords secure.
