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
import struct
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding



class Encoder:
    """Handles encryption-based encoding of data frames for secure transmission.

    This class encrypts frames using a two-layer encryption process:
    1. First encryption layer with a channel-specific key.
    2. Second encryption layer with a master secret key.

    Attributes:
        channel_keys (dict[int, bytes]): A dictionary mapping channel IDs to AES keys.
        secret_key (bytes): The master AES encryption key used for final encryption.
    """

    def __init__(self, secrets: bytes):
        """Initializes the Encoder with encryption keys.

        Args:
            secrets (bytes): The JSON-encoded secrets file containing encryption keys.

        Raises:
            ValueError: If the secrets file is improperly formatted or missing required keys.

       
        """
        secrets = json.loads(secrets)
        self.channel_keys = {
            int(c): bytes.fromhex(k) for c, k in secrets["channel_keys"].items()
        }
        self.secret_key = bytes.fromhex(secrets["secret_key"])
        
        

    def _encrypt(self, data: bytes, key: bytes) -> bytes:
        """Encrypts data using AES-ECB mode.

        Args:
            data (bytes): The data to be encrypted.
            key (bytes): The AES key used for encryption.

        Returns:
            bytes: The encrypted data.

       
        """
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return encrypted_data
    
    

    def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
        """Encodes and encrypts a frame for transmission.

        This method performs the following steps:
        1. Validates the frame size.
        2. Computes the effective channel ID.
        3. Retrieves the appropriate channel key or uses the master secret key.
        4. Pads the frame to a multiple of 16 bytes.
        5. Encrypts the frame using the channel key.
        6. Constructs a packet header with channel, timestamp, and frame size.
        7. Encrypts the entire packet using the master secret key.

        Args:
            channel (int): The channel number for which the frame is encoded.
            frame (bytes): The raw frame data. Must not exceed 64 bytes.
            timestamp (int): A 64-bit timestamp.

        Returns:
            bytes: The fully encrypted packet.

        Raises:
            ValueError: If the frame exceeds the allowed size or if no encryption key is found.

    
        """
    
        if len(frame) > 64:
            raise ValueError("Frame size must not exceed 64 bytes.")

        effective_channel = channel % 10007

        if effective_channel == 0:
            channel_key = self.secret_key
        else:
            if effective_channel not in self.channel_keys:
                raise ValueError(
                    f"No key found for effective channel {effective_channel}"
                )
            channel_key = self.channel_keys[effective_channel]

        frame_size = len(frame)

        
        if frame_size % 16 != 0:
            frame_padding = 16 - (frame_size % 16)
            frame += b"\x80" + b"\x00" * (frame_padding - 1)  

        encrypted_frame = self._encrypt(frame, channel_key)

        header = struct.pack("<IQI", channel, timestamp, frame_size)

        full_packet = header + encrypted_frame

        
        if len(full_packet) % 16 != 0:
            padding_length = 16 - (len(full_packet) % 16)
            full_packet += b"\x80" + b"\x00" * (padding_length - 1) 

        encrypted_packet = self._encrypt(full_packet, self.secret_key)

        return encrypted_packet



def main():
    
    """Main function to encode a frame using command-line arguments.

    This function:
    1. Parses command-line arguments for the secrets file, channel, frame, and timestamp.
    2. Initializes the Encoder with the provided secrets.
    3. Encodes the frame using the Encoder class.
    4. Prints the encoded packet in byte format.

    Command-line Arguments:
        secrets_file (str): Path to the JSON secrets file.
        channel (int): Channel ID for encoding.
        frame (str): Raw frame data (string format).
        timestamp (int): 64-bit timestamp.

  
    """
    parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
    parser.add_argument(
        "secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file"
    )
    parser.add_argument("channel", type=int, help="Channel to encode for")
    parser.add_argument("frame", help="Contents of the frame")
    parser.add_argument("timestamp", type=int, help="64b timestamp to use")
    args = parser.parse_args()

    encoder = Encoder(args.secrets_file.read())
    print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))


if __name__ == "__main__":
    main()