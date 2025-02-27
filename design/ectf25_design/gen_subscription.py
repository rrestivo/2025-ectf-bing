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
from cryptography.hazmat.primitives import padding


class SubscriptionGenerator:
    """Handles subscription encryption with proper padding (mod 16 for AES).

        This class provides functionality to generate and encrypt subscription 
    updates for a specific decoder device. It ensures that the encrypted 
    subscriptions conform to the system's security requirements.

    Attributes:
        key (bytes): The master encryption key loaded from the secrets file.
    
    """

    def __init__(self, secrets: bytes):
        """
        Initializes the subscription generator with the required encryption key.

        Args:
            secrets (bytes): JSON-encoded secrets file containing encryption keys.

        Raises:
            ValueError: If the secrets file is missing required keys.
        """
        # Load secrets from JSON file
        secrets_dict = json.loads(secrets)

        # Extract the AES encryption key (stored as a hex string)
        self.key = bytes.fromhex(secrets_dict["secret_key"])

        logger.debug(f"Loaded AES encryption key: {self.key.hex()}")

    def _encrypt(self, data: bytes) -> bytes:
        """
       Encrypts the given data using AES-128 in ECB mode.

        Args:
            data (bytes): The plaintext data to encrypt.

        Returns:
            bytes: The encrypted data.
        """
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return encrypted_data

    # def _pad_data(self, data: bytes) -> bytes:
    #     """
    #    Applies PKCS7 padding to ensure the input data is a multiple of 16 bytes.

    #     Args:
    #         data (bytes): The unpadded data.

    #     Returns:
    #         bytes: The padded data.
    #     """
    #     padder = padding.PKCS7(128).padder()  # 128-bit (16 bytes) block size
    #     padded_data = padder.update(data) + padder.finalize()
    #     return padded_data

    def gen_subscription(self, device_id: int, start: int, end: int, channel: int) -> bytes:
        """
      Generates and encrypts a subscription update packet.

        The subscription packet contains a device ID, subscription validity timestamps, 
        and the channel number. It is then encrypted using AES-128.

        Args:
            device_id (int): Unique identifier of the decoder device.
            start (int): Subscription start timestamp.
            end (int): Subscription end timestamp.
            channel (int): Channel number to grant access to.

        Returns:
            bytes: The encrypted subscription packet.
        """

        # Pack subscription fields into a binary format (little-endian order)
        packet = struct.pack("<IQQI", device_id, start, end, channel)

        padding_length = 16 - (len(packet) % 16)
        packet += b'\x00' * padding_length

        # Encrypt the padded subscription packet
        encrypted_packet = self._encrypt(packet)
        logger.debug(f"Encrypted subscription packet: {encrypted_packet.hex()}")

        return encrypted_packet


def parse_args():
    """
   Parses command-line arguments for generating subscriptions.

    This function provides the command-line interface for generating encrypted 
    subscription updates.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force creation of subscription file, overwriting existing file",
    )
    parser.add_argument(
        "secrets_file",
        type=argparse.FileType("rb"),
        help="Path to the secrets file created by ectf25_design.gen_secrets",
    )
    parser.add_argument("subscription_file", type=Path, help="Output file for the encrypted subscription")
    parser.add_argument("device_id", type=lambda x: int(x, 0), help="Device ID of the update recipient.")
    parser.add_argument("start", type=lambda x: int(x, 0), help="Subscription start timestamp")
    parser.add_argument("end", type=int, help="Subscription end timestamp")
    parser.add_argument("channel", type=int, help="Channel to subscribe to")

    return parser.parse_args()


def main():
    """Main function for generating encrypted subscription files.
    
    This function:
    1. Parses command-line arguments.
    2. Loads encryption secrets.
    3. Generates and encrypts a subscription packet.
    4. Saves the encrypted subscription to the specified file.
    
    """
    args = parse_args()

    # Initialize the subscription generator with secrets
    generator = SubscriptionGenerator(args.secrets_file.read())

    # Generate encrypted subscription packet
    subscription = generator.gen_subscription(args.device_id, args.start, args.end, args.channel)

    # Save encrypted subscription packet to file
    with open(args.subscription_file, "wb" if args.force else "xb") as f:
        f.write(subscription)

    logger.success(f"Subscription written to {str(args.subscription_file.absolute())}")


if __name__ == "__main__":
    main()