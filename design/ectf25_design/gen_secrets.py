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


def gen_secrets(channels: list[int]) -> bytes:
    """Generate the contents secrets file

    This will be passed to the Encoder, ectf25_design.gen_subscription, and the build
    process of the decoder

    :param channels: List of channel numbers that will be valid in this deployment.
        Channel 0 is the emergency broadcast, which will always be valid and will
        NOT be included in this list

    :returns: Contents of the secrets file
    """
    # TODO: Update this function to generate any system-wide secrets needed by
    #   your design

    # Generate a **secure random 128-bit key**
    random_key = secrets.token_bytes(16)  # 16 bytes = 128 bits

    # Convert the key to a hex string (matches the format of the hardcoded example)
    key_hex_string = random_key.hex()

    # Store the channels and generated key in the secrets dictionary
    secrets_dict = {
        "channels": channels,
        "some_secrets": key_hex_string,  # Store the key as a hex string
    }

    logger.debug(f"Generated random secret key: {key_hex_string}")

    # NOTE: if you choose to use JSON for your file type, you will not be able to
    # store binary data, and must either use a different file type or encode the
    # binary data to hex, base64, or another type of ASCII-only encoding
    return json.dumps(secrets_dict).encode()


def generate_secrets_header(secrets_file: Path, header_file: Path):
    """Generate the `secrets.h` header file from the secrets JSON file.

    :param secrets_file: Path to the generated secrets JSON file.
    :param header_file: Path to the output header file.
    """
    try:
        # Read secrets JSON file
        with open(secrets_file, "r") as f:
            secrets = json.load(f)

        # Extract the key
        secret_value = secrets.get("some_secrets", "")
        if not secret_value:
            logger.error("Error: 'some_secrets' key is missing in secrets file.")
            return

        # Convert hex string to an actual byte array
        try:
            key_bytes = bytes.fromhex(secret_value)
        except ValueError:
            logger.error("Error: 'some_secrets' is not a valid hex string.")
            return

        # Convert byte array to C-style array format
        key_hex = ", ".join(f"0x{b:02X}" for b in key_bytes)

        # Ensure the output directory exists
        header_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to `secrets.h`
        with open(header_file, "w") as f:
            f.write("#ifndef SECRETS_H\n")
            f.write("#define SECRETS_H\n\n")
            f.write("#include <stdint.h>\n\n")
            f.write(f"static const uint8_t secret_key[16] = {{ {key_hex} }};\n\n")
            f.write("#endif // SECRETS_H\n")

        logger.success(f"Generated {header_file}")

    except Exception as e:
        logger.error(f"Failed to generate secrets.h: {e}")


def parse_args():
    """Define and parse the command line arguments

    NOTE: Your design must not change this function
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
    """Main function of gen_secrets

    You will likely not have to change this function
    """
    # Parse the command line arguments
    args = parse_args()

    secrets = gen_secrets(args.channels)

    # Print the generated secrets for your own debugging
    # Attackers will NOT have access to the output of this, but feel free to remove
    #
    # NOTE: Printing sensitive data is generally not good security practice
    logger.debug(f"Generated secrets: {secrets}")

    # Open the file, erroring if the file exists unless the --force arg is provided
    with open(args.secrets_file, "wb" if args.force else "xb") as f:
        # Dump the secrets to the file
        f.write(secrets)

    # For your own debugging. Feel free to remove
    logger.success(f"Wrote secrets to {str(args.secrets_file.absolute())}")
    # Generate the `secrets.h` file in `inc/`
    secrets_header_path = Path("./decoder/inc/secrets.h")
    generate_secrets_header(args.secrets_file, secrets_header_path)

if __name__ == "__main__":
    main()
