"""
Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import argparse
import json
import os
import struct
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from loguru import logger



# Load the AES key from (e.g. secrets.json)
def load_secrets(secrets_file: str) -> bytes:
    """Load AES key from the global secrets file."""
    with open(secrets_file, "rb") as f:
        secrets = json.loads(f.read())
    return bytes.fromhex(secrets["some_secrets"])  # Convert hex key to bytes




# Encrypt the subscription data using AES-128-CFB with a random IV.
def encrypt_subscription(aes_key: bytes, subscription_data: bytes) -> bytes:
    """Encrypt subscription data using AES-128-CFB."""
    iv = os.urandom(16)  # Generate a random IV (16 bytes)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(subscription_data) + encryptor.finalize()
    
    return iv + encrypted_data  # Store IV at the beginning of the file




# Save the encrypted subscription file with the IV prepended
def gen_subscription(secrets: bytes, device_id: int, start: int, end: int, channel: int) -> bytes:
    """Generate an encrypted subscription file for a decoder."""
    # Create raw subscription data (before encryption)
    subscription_data = struct.pack("<IQQI", device_id, start, end, channel)

    # Encrypt subscription file using AES-128-CFB
    encrypted_subscription = encrypt_subscription(secrets, subscription_data)
    
    return encrypted_subscription  # Return the encrypted subscription




def parse_args():
    """Define and parse the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite")
    parser.add_argument("secrets_file", type=Path, help="Path to the global secrets file")
    parser.add_argument("subscription_file", type=Path, help="Subscription output file")
    parser.add_argument("device_id", type=lambda x: int(x, 0), help="Decoder ID")
    parser.add_argument("start", type=lambda x: int(x, 0), help="Subscription start timestamp")
    parser.add_argument("end", type=int, help="Subscription end timestamp")
    parser.add_argument("channel", type=int, help="Channel to subscribe to")
    return parser.parse_args()


def main():
    """Main function of gen_subscription

    You will likely not have to change this function
    """
    # Parse the command line arguments
    args = parse_args()
    
    
    aes_key = load_secrets(args.secrets_file)

    # Generate encrypted subscription
    encrypted_subscription = gen_subscription(aes_key, args.device_id, args.start, args.end, args.channel)


    # Save encrypted subscription file
    with open(args.subscription_file, "wb" if args.force else "xb") as f:
        f.write(encrypted_subscription)

    # For your own debugging. Feel free to remove
    logger.success(f"Wrote encrypted subscription to {str(args.subscription_file.absolute())}")


if __name__ == "__main__":
    main()
