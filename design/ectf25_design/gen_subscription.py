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
import secrets
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from loguru import logger

# Constants
CHANNEL_MIN = 0
CHANNEL_MAX = 8
NONCE_SIZE = 8  # 8-byte nonce to prevent replay attacks
DECODER_ID_MAX = 0xFFFFFFFF  # Max for 4-byte unsigned integer

def load_secrets(secrets_file: str) -> bytes:
    """Load AES key from the global secrets file."""
    try:
        with open(secrets_file, "rb") as f:
            secrets_data = json.loads(f.read())
    except FileNotFoundError:
        logger.error("Error: secrets.json file not found!")
        raise
    except json.JSONDecodeError:
        logger.error("Error: Invalid secrets.json format!")
        raise

    return bytes.fromhex(secrets_data["some_secrets"])

def validate_inputs(decoder_id: int, start: int, end: int, channel: int):
    """Validate all input parameters before generating a subscription."""
    
    # Validate channel range
    if channel < CHANNEL_MIN or channel > CHANNEL_MAX:
        logger.error(f"Invalid channel {channel}! Must be between {CHANNEL_MIN} and {CHANNEL_MAX}.")
        raise ValueError("Invalid channel! Must be between 0 and 8.")

    # Validate decoder ID
    if decoder_id < 0 or decoder_id > DECODER_ID_MAX:
        logger.error(f"Invalid Decoder ID {decoder_id}! Must be a 4-byte unsigned integer.")
        raise ValueError("Invalid Decoder ID! Must be a valid 4-byte unsigned integer.")

    # Validate time range
    if start >= end:
        logger.error(f"Invalid time range: Start ({start}) >= End ({end}).")
        raise ValueError("Invalid time range! Start time must be less than end time.")

def encrypt_subscription(aes_key: bytes, subscription_data: bytes) -> bytes:
    """Encrypt subscription data using AES-128-CFB."""
    iv = os.urandom(16)  # Generate a random IV (16 bytes)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(subscription_data) + encryptor.finalize()
    
    return iv + encrypted_data  # Store IV at the beginning of the file



def gen_subscription(aes_key: bytes, decoder_id: int, start: int, end: int, channel: int) -> bytes:
    """Generate an encrypted subscription file for a decoder."""
    
    # Validate inputs before processing
    validate_inputs(decoder_id, start, end, channel)

    # Generate a nonce (random 8-byte value)
    nonce = secrets.randbits(NONCE_SIZE * 8)  # Correct usage of secrets module

    # Pack the subscription data (Before encryption)
    subscription_data = struct.pack("<IQQIQ", decoder_id, start, end, channel, nonce)

    logger.debug(f"Subscription Data (Before Encryption): {subscription_data.hex()}")

    # Encrypt subscription file using AES-128-CFB
    encrypted_subscription = encrypt_subscription(aes_key, subscription_data)

    return encrypted_subscription  # Return the encrypted subscription


def parse_args():
    """Define and parse the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite")
    parser.add_argument("secrets_file", type=Path, help="Path to the global secrets file")
    parser.add_argument("subscription_file", type=Path, help="Subscription output file")
    parser.add_argument("decoder_id", type=lambda x: int(x, 0), help="Decoder ID (4 bytes)")
    parser.add_argument("start", type=lambda x: int(x, 0), help="Subscription start timestamp")
    parser.add_argument("end", type=int, help="Subscription end timestamp")
    parser.add_argument("channel", type=int, help="Channel to subscribe to")
    return parser.parse_args()

def main():
    """Main function for generating encrypted subscriptions."""
    args = parse_args()

    # Load AES key from secrets file
    aes_key = load_secrets(args.secrets_file)

    try:
        # Generate encrypted subscription
        encrypted_subscription = gen_subscription(aes_key, args.decoder_id, args.start, args.end, args.channel)

        # Save encrypted subscription file
        with open(args.subscription_file, "wb" if args.force else "xb") as f:
            f.write(encrypted_subscription)

        logger.success(f"Wrote encrypted subscription to {str(args.subscription_file.absolute())}")
    
    except ValueError as e:
        logger.error(f"Subscription generation failed: {e}")

if __name__ == "__main__":
    main()