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
import struct
from pathlib import Path
from loguru import logger
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def load_secrets(secrets: bytes) -> bytes:
    """Load encryption key from the secrets JSON."""
    secrets_dict = json.loads(secrets)
    return bytes.fromhex(secrets_dict["secret_key"])

def encrypt_data(key: bytes, data: bytes) -> bytes:
    """Encrypt data using AES-128 in ECB mode."""
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def add_padding(data: bytes) -> bytes:
    """Add padding to the data to make its length a multiple of 16 bytes."""
    padding_length = 16 - (len(data) % 16)
    return data + (b'\x00' * padding_length)

def gen_subscription(secrets: bytes, device_id: int, start: int, end: int, channel: int) -> bytes:
    """Generate and encrypt a subscription packet."""
    key = load_secrets(secrets)
    packet = struct.pack("<IQQI", device_id, start, end, channel)
    packet = add_padding(packet)
    return encrypt_data(key, packet)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", "-f", action="store_true", help="Force creation of subscription file, overwriting existing file")
    parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file created by ectf25_design.gen_secrets")
    parser.add_argument("subscription_file", type=Path, help="Output file for the encrypted subscription")
    parser.add_argument("device_id", type=lambda x: int(x, 0), help="Device ID of the update recipient.")
    parser.add_argument("start", type=lambda x: int(x, 0), help="Subscription start timestamp")
    parser.add_argument("end", type=int, help="Subscription end timestamp")
    parser.add_argument("channel", type=int, help="Channel to subscribe to")
    return parser.parse_args()

def main():
    """Main function to generate encrypted subscription files."""
    args = parse_args()
    subscription = gen_subscription(args.secrets_file.read(), args.device_id, args.start, args.end, args.channel)
    with open(args.subscription_file, "wb" if args.force else "xb") as f:
        f.write(subscription)
    logger.success(f"Subscription written to {str(args.subscription_file.absolute())}")

if __name__ == "__main__":
    main()
