**eCTF Encoder**


```python
import argparse
import struct
import json
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
```

- `argparse`: Handles command-line arguments.
- `struct`: Helps in binary data formatting.
- `json`: Parses JSON data (secrets file).
- `os`: Generates random values (IV for encryption).
- `cryptography.hazmat.primitives.ciphers`: Implements AES encryption.

---

## **2. AES S-Box Definition**
The AES S-Box (Substitution Box) is a predefined table used for byte substitution in encryption:

```python
AES_SBOX = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, ...] 
```

Each byte in the data is replaced using this S-box transformation to enhance security.

---

## **3. Encoder Class**
The `Encoder` class initializes the encryption system using a secret key from a JSON file.

### **3.1 Initialization**

```python
class Encoder:
    def __init__(self, secrets: bytes):
        secrets = json.loads(secrets)
        self.key = bytes.fromhex(secrets["some_secrets"])
        self.some_secrets = secrets["some_secrets"]
```

- `secrets` is a JSON file containing encryption keys.
- `self.key` extracts and stores a 128-bit AES key.
- `self.some_secrets` retains the original hex string for reference.

### **Example:**
**Input (JSON file `test.secrets`)**
```json
{"some_secrets": "2b7e151628aed2a6abf7158809cf4f3c"}
```
**Stored in `self.key`**:
```
b"+~\x15\x16(\xae\xd2\xa6\xab\xf7\x15\x88\t\xcfO<)"
```

---

## **4. AES Encryption Helper Function**

```python
def _aes_encrypt(self, data: bytes, key: bytes, iv: bytes, prepend_iv: bool = False) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    return (iv + ct) if prepend_iv else ct
```

- Encrypts data using **AES-128 in CFB mode**.
- Uses an **Initialization Vector (IV)** for randomness.
- If `prepend_iv=True`, IV is added to the ciphertext for decryption.

### **Example:**
**Input:**
```python
key = b"1234567890abcdef"
iv = b"0000000000000000"
data = b"Hello, world!"
```
**Output (Ciphertext):**
```
b'\xd4\xc1\x89\xfa...'
```

---

## **5. Applying AES S-Box Substitution**

```python
def _apply_sbox(self, data: bytes) -> bytes:
    return bytes(AES_SBOX[b] for b in data)
```

- Each byte in `data` is substituted using the AES S-Box table.

### **Example:**
**Input:** `b"AB" (ASCII: 65, 66)`
**Output:** `[AES_SBOX[65], AES_SBOX[66]] = b"\xa5\xe5"`

---

## **6. Encoding Function**

```python
def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
```
### **6.1 Frame Preparation**
```python
if len(frame) > 64:
    raise ValueError("Frame size must not exceed 64 bytes.")
frame = frame.ljust(64, b'\x00')
```
- **Ensures frame size is at most 64 bytes**, padding with zeros if needed.

### **6.2 Inner Encryption (for non-channel 0)**
```python
if channel == 0:
    processed_frame = frame
else:
    fixed_iv = b'\x00' * 16
    inner_encrypted = self._aes_encrypt(frame, self.key, fixed_iv)
    processed_frame = self._apply_sbox(inner_encrypted)
```
- Encrypts frame with a **fixed IV** (all zeros) for consistency.
- Applies **AES S-box substitution**.

### **6.3 Adding Headers and Final Encryption**
```python
header = struct.pack("<IQ", channel, timestamp)
packet = header + processed_frame
random_iv = os.urandom(16)
final_encrypted = self._aes_encrypt(packet, self.key, random_iv, prepend_iv=True)
return final_encrypted
```
- **Header (12 bytes):**
  - `channel` (4 bytes, little-endian `I` format)
  - `timestamp` (8 bytes, little-endian `Q` format)
- **Outer AES-128-CFB encryption** with a **random IV** (16 bytes).

### **Example:**
**Input:**
```python
channel = 1
frame = b"Test Frame"
timestamp = 1678901234
```
**Output:**
```
b'\x8f\xe3\xaf\xbd... (92 encrypted bytes)'
```

---

## **7. Command-Line Interface (CLI)**
The script provides a command-line interface to test encoding:

```python
def main():
    parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
    parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file")
    parser.add_argument("channel", type=int, help="Channel to encode for")
    parser.add_argument("frame", help="Contents of the frame")
    parser.add_argument("timestamp", type=int, help="64b timestamp to use")
    args = parser.parse_args()
    encoder = Encoder(args.secrets_file.read())
    print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))
```

### **Running the Script:**
```sh
python3 encoder.py test.secrets 1 "Hello" 100
```
**Output:**
```
b'\xa5\x87\xd1\xf9...'  # Encrypted frame
```


##  -----------------------------------------  ** Explanation for Adav_Enocder  logic ** -------------------------------------------

raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ python3 Adv_enoder.py  my_secrets.json 1 "hello" 2
2025-02-06 22:10:08.782 | INFO     | __main__:__init__:44 - Encoder initialized with allowed channels: [0, 1, 2, 3, 4, 5, 6, 7, 8]
2025-02-06 22:10:08.788 | INFO     | __main__:encode:102 - Encoding started for Channel 1 at Timestamp 2
2025-02-06 22:10:08.893 | INFO     | __main__:_derive_session_key:65 - Derived session key for Channel 1: 460a4b75756ffdc76bef46f10043be5c
2025-02-06 22:10:08.899 | INFO     | __main__:encode:124 - Encoded frame for Channel 1 | Timestamp: 2 | Encrypted Data: 00000000000000000000000000000000b9facc0f64b809a8f32318ec8406013d45543ed755b02ec22545141206cb0c688ab76dc65fef36c925c3ecef66830863d68bb3851009aa02d42df5edadba1c0dc51ad234397b9a3e8efc259a
Encoded Data: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb9\xfa\xcc\x0fd\xb8\t\xa8\xf3#\x18\xec\x84\x06\x01=ET>\xd7U\xb0.\xc2%E\x14\x12\x06\xcb\x0ch\x8a\xb7m\xc6_\xef6\xc9%\xc3\xec\xeff\x83\x08c\xd6\x8b\xb3\x85\x10\t\xaa\x02\xd4-\xf5\xed\xad\xba\x1c\r\xc5\x1a\xd249{\x9a>\x8e\xfc%\x9a'
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ python3 Adv_enoder.py  my_secrets.json 2 "hello" 2
2025-02-06 22:10:17.641 | INFO     | __main__:__init__:44 - Encoder initialized with allowed channels: [0, 1, 2, 3, 4, 5, 6, 7, 8]
2025-02-06 22:10:17.642 | INFO     | __main__:encode:102 - Encoding started for Channel 2 at Timestamp 2
2025-02-06 22:10:17.683 | INFO     | __main__:_derive_session_key:65 - Derived session key for Channel 2: 7983b6c3122a15f04966bf8442bc425f
2025-02-06 22:10:17.686 | INFO     | __main__:encode:124 - Encoded frame for Channel 2 | Timestamp: 2 | Encrypted Data: 00000000000000000000000000000000ff36466d3071c810a0644deba38dc70a7a50d0e6f4835094454eced498c9664c34e1aad67d568ce937ec8d554d097ce14f200739e53dc73a88f10ff767a792e28375c6c15811ae7e62d9d5ba
Encoded Data: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff6Fm0q\xc8\x10\xa0dM\xeb\xa3\x8d\xc7\nzP\xd0\xe6\xf4\x83P\x94EN\xce\xd4\x98\xc9fL4\xe1\xaa\xd6}V\x8c\xe97\xec\x8dUM\t|\xe1O \x079\xe5=\xc7:\x88\xf1\x0f\xf7g\xa7\x92\xe2\x83u\xc6\xc1X\x11\xae~b\xd9\xd5\xba'
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ python3 Adv_enoder.py  my_secrets.json 3 "hello" 3
2025-02-06 22:10:27.054 | INFO     | __main__:__init__:44 - Encoder initialized with allowed channels: [0, 1, 2, 3, 4, 5, 6, 7, 8]
2025-02-06 22:10:27.055 | INFO     | __main__:encode:102 - Encoding started for Channel 3 at Timestamp 3
2025-02-06 22:10:27.094 | INFO     | __main__:_derive_session_key:65 - Derived session key for Channel 3: 6d65adca7ba1dd18911b311826d05cfa
2025-02-06 22:10:27.096 | INFO     | __main__:encode:124 - Encoded frame for Channel 3 | Timestamp: 3 | Encrypted Data: 0000000000000000000000000000000096c6c107c2432ad1e39d5c8df97b6152f4b4545a1ab63908e83574d39bb79c5c362843cbc3074fd91c19d85ed60ec1974882016dd134daa49f76dbbc280a403157343d73c68ec88b73c88469
Encoded Data: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x96\xc6\xc1\x07\xc2C*\xd1\xe3\x9d\\\x8d\xf9{aR\xf4\xb4TZ\x1a\xb69\x08\xe85t\xd3\x9b\xb7\x9c\\6(C\xcb\xc3\x07O\xd9\x1c\x19\xd8^\xd6\x0e\xc1\x97H\x82\x01m\xd14\xda\xa4\x9fv\xdb\xbc(\n@1W4=s\xc6\x8e\xc8\x8bs\xc8\x84i'
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ python3 Adv_enoder.py  my_secrets.json 3 "hello" 3
2025-02-06 22:10:33.446 | INFO     | __main__:__init__:44 - Encoder initialized with allowed channels: [0, 1, 2, 3, 4, 5, 6, 7, 8]
2025-02-06 22:10:33.447 | INFO     | __main__:encode:102 - Encoding started for Channel 3 at Timestamp 3
2025-02-06 22:10:33.486 | INFO     | __main__:_derive_session_key:65 - Derived session key for Channel 3: 6d65adca7ba1dd18911b311826d05cfa
2025-02-06 22:10:33.492 | INFO     | __main__:encode:124 - Encoded frame for Channel 3 | Timestamp: 3 | Encrypted Data: 0000000000000000000000000000000096c6c107c2432ad1e39d5c8df97b6152f4b4545a1ab63908e83574d39bb79c5c362843cbc3074fd91c19d85ed60ec1974882016dd134daa49f76dbbc280a403157343d73c68ec88b73c88469
Encoded Data: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x96\xc6\xc1\x07\xc2C*\xd1\xe3\x9d\\\x8d\xf9{aR\xf4\xb4TZ\x1a\xb69\x08\xe85t\xd3\x9b\xb7\x9c\\6(C\xcb\xc3\x07O\xd9\x1c\x19\xd8^\xd6\x0e\xc1\x97H\x82\x01m\xd14\xda\xa4\x9fv\xdb\xbc(\n@1W4=s\xc6\x8e\xc8\x8bs\xc8\x84i'
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ python3 Adv_enoder.py  my_secrets.json 100 "hello" 3
2025-02-06 22:10:39.688 | INFO     | __main__:__init__:44 - Encoder initialized with allowed channels: [0, 1, 2, 3, 4, 5, 6, 7, 8]
2025-02-06 22:10:39.690 | INFO     | __main__:encode:102 - Encoding started for Channel 100 at Timestamp 3
2025-02-06 22:10:39.691 | ERROR    | __main__:_derive_session_key:50 - Unauthorized channel 100 attempted!
Traceback (most recent call last):
  File "/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design/Adv_enoder.py", line 146, in <module>
    main()
  File "/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design/Adv_enoder.py", line 140, in main
    encrypted_data = encoder.encode(args.channel, args.frame.encode(), args.timestamp)
  File "/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design/Adv_enoder.py", line 109, in encode
    session_key = self._derive_session_key(channel)
  File "/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design/Adv_enoder.py", line 51, in _derive_session_key
    raise ValueError(f"Unauthorized channel {channel}. Not in allowed list.")
ValueError: Unauthorized channel 100. Not in allowed list.
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ 

