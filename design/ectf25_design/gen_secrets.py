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
from pathlib import Path
import secrets

from loguru import logger


# def gen_secrets(channels: list[int]) -> bytes:
#     """Generate secrets file with a key for each channel and an extra key (secret_key).

#     :param channels: List of channel numbers that will be valid in this deployment.
#         Channel 0 is the emergency broadcast, which will always be valid and will
#         NOT be included in this list.

#     :returns: Contents of the secrets file.
#     """
#     # Dictionary to store secrets
#     secrets_dict = {
#         "channels": channels,
#         "channel_keys": {},  # Store a unique key for each channel
#     }

#     logger.info(f"Generating secrets for channels: {channels}")

#     # Generate a unique 128-bit key for each channel
#     for channel in channels:
#         channel_key = secrets.token_bytes(16)  # Generate a 128-bit key
#         secrets_dict["channel_keys"][channel] = channel_key.hex()  # Store as hex string
#         logger.debug(f"Generated key for channel {channel}: {channel_key.hex()}")

#     # Generate an extra key (secret_key)
#     secret_key = secrets.token_bytes(16)
#     secrets_dict["secret_key"] = secret_key.hex()
#     logger.debug(f"Generated extra key (secret_key): {secret_key.hex()}")

#     return json.dumps(secrets_dict).encode()

def gen_secrets(channels: list[int]) -> bytes:
    """Generate secrets file with 10,000 channel keys and an extra secret_key."""
    secrets_dict = {
        "channels": channels,  # Retains original input for compatibility
        "channel_keys": {},
    }

    logger.info("Generating 10,008 channel keys")

    # Generate 10,000 keys with sequential channel IDs (1-10,000)
    for channel_id in range(1, 10008):
        channel_key = secrets.token_bytes(16)
        secrets_dict["channel_keys"][channel_id] = channel_key.hex()
        logger.debug(f"Generated key for channel {channel_id}: {channel_key.hex()}")

    # Generate extra secret_key
    secret_key = secrets.token_bytes(16)
    secrets_dict["secret_key"] = secret_key.hex()
    logger.debug(f"Generated extra key (secret_key): {secret_key.hex()}")

    return json.dumps(secrets_dict).encode()



# def generate_secrets_header(secrets_file: Path, header_file: Path):
#     """Generate the `secrets.h` header file from the secrets JSON file.

#     :param secrets_file: Path to the generated secrets JSON file.
#     :param header_file: Path to the output header file.
#     """
#     try:
#         # Read secrets JSON file
#         with open(secrets_file, "r") as f:
#             secrets = json.load(f)

#         # Extract keys
#         channel_keys = secrets.get("channel_keys", {})
#         secret_key = secrets.get("secret_key", "")

#         if not channel_keys or not secret_key:
#             logger.error("Error: Missing required keys in secrets file.")
#             return

#         # Convert keys to C-style array format
#         channel_keys_c = {
#             channel: ", ".join(f"0x{b:02X}" for b in bytes.fromhex(key))
#             for channel, key in channel_keys.items()
#         }

#         secret_key_hex = ", ".join(f"0x{b:02X}" for b in bytes.fromhex(secret_key))

#         # Ensure the output directory exists
#         header_file.parent.mkdir(parents=True, exist_ok=True)

#         # Write to `secrets.h`
#         with open(header_file, "w") as f:
#             f.write("#ifndef SECRETS_H\n")
#             f.write("#define SECRETS_H\n\n")
#             f.write("#include <stdint.h>\n\n")

#             # Write the channel keys
#             for channel, key_hex in channel_keys_c.items():
#                 f.write(f"static const uint8_t channel_{channel}_key[16] = {{ {key_hex} }};\n")

#             # Write the extra secret_key
#             f.write(f"\nstatic const uint8_t secret_key[16] = {{ {secret_key_hex} }};\n\n")

#             f.write("#endif // SECRETS_H\n")

#         logger.success(f"Generated {header_file}")

#     except Exception as e:
#         logger.error(f"Failed to generate secrets.h: {e}")


def generate_secrets_header(secrets_file: Path, header_file: Path):
    """Generate the `secrets.h` header file from the secrets JSON file."""
    try:
        # Read secrets JSON file
        with open(secrets_file, "r") as f:
            secrets = json.load(f)

        # Extract keys
        channel_keys = secrets.get("channel_keys", {})
        secret_key = secrets.get("secret_key", "")

        if not channel_keys or not secret_key:
            logger.error("Error: Missing required keys in secrets file.")
            return

        # Convert all channel keys to C-style array format
        all_keys_c = []
        for key in channel_keys.values():
            key_bytes = bytes.fromhex(key)
            key_hex = ", ".join(f"0x{b:02X}" for b in key_bytes)
            all_keys_c.append(f"{{ {key_hex} }}")

        secret_key_hex = ", ".join(f"0x{b:02X}" for b in bytes.fromhex(secret_key))

        # Ensure the output directory exists
        header_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to `secrets.h`
        with open(header_file, "w") as f:
            f.write("#ifndef SECRETS_H\n")
            f.write("#define SECRETS_H\n\n")
            f.write("#include <stdint.h>\n\n")

            # Write all channel keys as a single array
            f.write("static const uint8_t all_channel_keys[10007][16] = {\n")
            for row in all_keys_c:
                f.write(f"    {row},\n")
            f.write("};\n\n")

            # Write the secret_key
            f.write(f"static const uint8_t secret_key[16] = {{ {secret_key_hex} }};\n\n")

            f.write("#endif // SECRETS_H\n")

        logger.success(f"Generated {header_file}")

    except Exception as e:
        logger.error(f"Failed to generate secrets.h: {e}")



def parse_args():
    """Define and parse the command line arguments.

    NOTE: Your design must not change this function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force creation of secrets file, overwriting existing file",
    )
    parser.add_argument(
        "secrets_file",
        type=Path,
        help="Path to the secrets file to be created",
    )
    parser.add_argument(
        "channels",
        nargs="+",
        type=int,
        help="Supported channels. Channel 0 (broadcast) is always valid and will not"
        " be provided in this list",
    )
    return parser.parse_args()


def main():
    """Main function of gen_secrets."""
    # Parse the command line arguments
    args = parse_args()

    # Generate secrets
    secrets = gen_secrets(args.channels)

    # Print the generated secrets for debugging
    logger.debug(f"Generated secrets: {secrets}")

    # Write secrets to file
    with open(args.secrets_file, "wb" if args.force else "xb") as f:
        f.write(secrets)

    logger.success(f"Wrote secrets to {str(args.secrets_file.absolute())}")

    # Generate the `secrets.h` file in `decoder/inc/`
    secrets_header_path = Path("./decoder/inc/secrets.h")
    generate_secrets_header(args.secrets_file, secrets_header_path)


if __name__ == "__main__":
    main()
