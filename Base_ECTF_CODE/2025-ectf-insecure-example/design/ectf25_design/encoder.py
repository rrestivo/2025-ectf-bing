import struct
import os
import json
#from sbox import AES_SBOX
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


AES_SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

# class Encoder:
    
#     def __init__(self, secrets: bytes):
#         """
#         Initializes the encoder with the secret encryption key.
#         """
#         secrets = json.loads(secrets)
#         self.key = bytes.fromhex(secrets["some_secrets"])

#     def _aes_encrypt(self, data: bytes, key: bytes) -> bytes:
#         """
#         Encrypt data using AES-128 in CFB mode WITHOUT an IV.
#         """
#         cipher = Cipher(algorithms.AES(key), modes.CFB(b'\x00' * 16), backend=default_backend())
#         encryptor = cipher.encryptor()
#         return encryptor.update(data) + encryptor.finalize()

#     def _apply_sbox(self, data: bytes) -> bytes:
#         """
#         Apply the AES S-box substitution to each byte of the data.
#         """
#         return bytes(AES_SBOX[b] for b in data)

#     def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
#         """Encodes the frame without an IV to match expected decoder size."""

#         print(f"\n[LOG] Encoding frame for channel {channel} with timestamp {timestamp}")

#         if len(frame) > 64:
#             raise ValueError("Frame size must not exceed 64 bytes.")

#         print(f"[LOG] Initial frame size: {len(frame)} bytes")

#         # Pad frame to exactly 64 bytes
#         frame = frame.ljust(64, b'\x00')
#         print(f"[LOG] Frame after padding: {len(frame)} bytes")

#         # Process the frame based on channel type
#         if channel == 0:
#             processed_frame = frame
#             print(f"[LOG] Frame remains unchanged for emergency channel (size: {len(processed_frame)})")
#         else:
#             encrypted_frame = self._aes_encrypt(frame, self.key)
#             print(f"[LOG] Frame after AES encryption: {len(encrypted_frame)} bytes")

#             processed_frame = self._apply_sbox(encrypted_frame)
#             print(f"[LOG] Frame after S-box substitution: {len(processed_frame)} bytes")

#         # Construct the header (4-byte channel, 8-byte timestamp)
#         header = struct.pack("<IQ", channel, timestamp)
#         print(f"[LOG] Header size: {len(header)} bytes")

#         # Create the final packet (header + encrypted frame)
#         packet = header + processed_frame
#         print(f"[LOG] Final packet size: {len(packet)} bytes")

#         return packet


# def main():
#     """Test main function to encode a frame."""
#     import argparse
#     parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
#     parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file")
#     parser.add_argument("channel", type=int, help="Channel to encode for")
#     parser.add_argument("frame", help="Contents of the frame")
#     parser.add_argument("timestamp", type=int, help="64-bit timestamp to use")
#     args = parser.parse_args()

#     encoder = Encoder(args.secrets_file.read())
#     print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))


# if __name__ == "__main__":
#     main()

# class Encoder:
    
#     def __init__(self, secrets: bytes):
#         """
#         Initializes the encoder with the secret encryption key.
#         """
#         secrets = json.loads(secrets)
#         self.key = bytes.fromhex(secrets["some_secrets"])

#     def _aes_encrypt(self, data: bytes, key: bytes) -> bytes:
#         """
#         Encrypt data using AES-128 in ECB mode.
#         """
#         cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
#         encryptor = cipher.encryptor()
#         return encryptor.update(data) + encryptor.finalize()

#     def _apply_sbox(self, data: bytes) -> bytes:
#         """
#         Apply the AES S-box substitution to each byte of the data.
#         """
#         return bytes(AES_SBOX[b] for b in data)

#     def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
#         """Encodes the frame using AES-ECB mode to match the expected decoder size."""

#         print(f"\n[LOG] Encoding frame for channel {channel} with timestamp {timestamp}")

#         if len(frame) > 64:
#             raise ValueError("Frame size must not exceed 64 bytes.")

#         print(f"[LOG] Initial frame size: {len(frame)} bytes")

#         # Pad frame to exactly 64 bytes
#         frame = frame.ljust(64, b'\x00')
#         print(f"[LOG] Frame after padding: {len(frame)} bytes")

#         # Process the frame based on channel type
#         if channel == 0:
#             processed_frame = frame
#             print(f"[LOG] Frame remains unchanged for emergency channel (size: {len(processed_frame)})")
#         else:
#             encrypted_frame = self._aes_encrypt(frame, self.key)
#             print(f"[LOG] Frame after AES-ECB encryption: {len(encrypted_frame)} bytes")

#             processed_frame = self._apply_sbox(encrypted_frame)
#             print(f"[LOG] Frame after S-box substitution: {len(processed_frame)} bytes")

#         # Construct the header (4-byte channel, 8-byte timestamp)
#         header = struct.pack("<IQ", channel, timestamp)
#         print(f"[LOG] Header size: {len(header)} bytes")

#         # Create the final packet (header + encrypted frame)
#         packet = header + processed_frame
#         print(f"[LOG] Final packet size: {len(packet)} bytes")

#         return packet


# def main():
#     """Test main function to encode a frame."""
#     import argparse
#     parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
#     parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file")
#     parser.add_argument("channel", type=int, help="Channel to encode for")
#     parser.add_argument("frame", help="Contents of the frame")
#     parser.add_argument("timestamp", type=int, help="64-bit timestamp to use")
#     args = parser.parse_args()

#     encoder = Encoder(args.secrets_file.read())
#     print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))


# if __name__ == "__main__":
#     main()

class Encoder:
    
    def __init__(self, secrets: bytes):
        """
        Initializes the encoder with the secret encryption key.
        """
        secrets = json.loads(secrets)
        self.key = bytes.fromhex(secrets["some_secrets"])

    def _aes_encrypt(self, data: bytes, key: bytes) -> bytes:
        """
        Encrypt data using AES-128 in ECB mode.
        """
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
        """Encodes the frame using AES-ECB mode to match the expected decoder size."""

        print(f"\n[LOG] Encoding frame for channel {channel} with timestamp {timestamp}")

        if len(frame) > 64:
            raise ValueError("Frame size must not exceed 64 bytes.")

        print(f"[LOG] Initial frame size: {len(frame)} bytes")

        # Pad frame to exactly 64 bytes
        frame = frame.ljust(64, b'\x00')
        print(f"[LOG] Frame after padding: {len(frame)} bytes")

        # Process the frame based on channel type
        if channel == 0:
            processed_frame = frame
            print(f"[LOG] Frame remains unchanged for emergency channel (size: {len(processed_frame)})")
        else:
            processed_frame = self._aes_encrypt(frame, self.key)
            print(f"[LOG] Frame after AES-ECB encryption: {len(processed_frame)} bytes")

        # Construct the header (4-byte channel, 8-byte timestamp)
        header = struct.pack("<IQ", channel, timestamp)
        print(f"[LOG] Header size: {len(header)} bytes")

        # Create the final packet (header + encrypted frame)
        packet = header + processed_frame
        print(f"[LOG] Final packet size: {len(packet)} bytes")

        return packet


def main():
    """Test main function to encode a frame."""
    import argparse
    parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
    parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file")
    parser.add_argument("channel", type=int, help="Channel to encode for")
    parser.add_argument("frame", help="Contents of the frame")
    parser.add_argument("timestamp", type=int, help="64-bit timestamp to use")
    args = parser.parse_args()

    encoder = Encoder(args.secrets_file.read())
    print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))


if __name__ == "__main__":
    main()
"""
Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

# import argparse
# import struct
# import json
# #from sbox import AES_SBOX
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend


# class Encoder:
#     def __init__(self, secrets: bytes):
#         """
#         You **may not** change the arguments or returns of this function!

#         :param secrets: Contents of the secrets file generated by
#             ectf25_design.gen_secrets
#         """
#         # TODO: parse your secrets data here and run any necessary pre-processing to
#         #   improve the throughput of Encoder.encode

#         # Load the json of the secrets file
#         secrets = json.loads(secrets)

#         # Load the example secrets for use in Encoder.encode
#         # This will be "EXAMPLE" in the reference design"
#         self.some_secrets = secrets["some_secrets"]

#     def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
#         """The frame encoder function

#         This will be called for every frame that needs to be encoded before being
#         transmitted by the satellite to all listening TVs

#         You **may not** change the arguments or returns of this function!

#         :param channel: 16b unsigned channel number. Channel 0 is the emergency
#             broadcast that must be decodable by all channels.
#         :param frame: Frame to encode. Max frame size is 64 bytes.
#         :param timestamp: 64b timestamp to use for encoding. **NOTE**: This value may
#             have no relation to the current timestamp, so you should not compare it
#             against the current time. The timestamp is guaranteed to strictly
#             monotonically increase (always go up) with subsequent calls to encode

#         :returns: The encoded frame, which will be sent to the Decoder
#         """
#         # TODO: encode the satellite frames so that they meet functional and
#         #  security requirements

#         return struct.pack("<IQ", channel, timestamp) + frame


# def main():
#     """A test main to one-shot encode a frame

#     This function is only for your convenience and will not be used in the final design.

#     After pip-installing, you should be able to call this with:
#         python3 -m ectf25_design.encoder path/to/test.secrets 1 "frame to encode" 100
#     """
#     parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
#     parser.add_argument(
#         "secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file"
#     )
#     parser.add_argument("channel", type=int, help="Channel to encode for")
#     parser.add_argument("frame", help="Contents of the frame")
#     parser.add_argument("timestamp", type=int, help="64b timestamp to use")
#     args = parser.parse_args()

#     encoder = Encoder(args.secrets_file.read())
#     print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))


# if __name__ == "__main__":
#     main()