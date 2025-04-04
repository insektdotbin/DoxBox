# DoxBox Hash Cracking Tool
## Overview
The Hash Cracking Tool is a multi-threaded Python application designed to crack hashed passwords using a wordlist. It supports multiple hash algorithms, including MD5, SHA-1, SHA-256, SHA-512, SHA3, and BLAKE2. The tool is optimized for performance and includes ethical use warnings.

## Features
Supports 8 hash algorithms.

Multi-threaded for fast cracking.

Validates hash formats and wordlist inputs.

Warns against using weak algorithms (MD5/SHA1).

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
python dbhashcrack.py
```
1. Select an algorithm (e.g., SHA-256).

2. Enter the hash to crack.

3. Provide a wordlist file path.

Example:

```
Select algorithm (1-8): 3
Enter hash to crack: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
Enter wordlist path: passwords.txt
```

# Ethical Guidelines
Only use this tool on systems you own or have permission to test.
Do not use it for malicious purposes.
