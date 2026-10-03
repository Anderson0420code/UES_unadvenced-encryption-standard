import zlib
import hashlib
import random
import struct
import math
from PIL import Image

class MT19937_PRNG:
    """
    Mersenne Twister Engine providing exact compatibility 
    with standard pseudo-random number generator outputs.
    """
    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def next_byte(self) -> int:
        return self.rng.randint(0, 255)

    def shuffle(self, arr: list) -> None:
        self.rng.shuffle(arr)


class UESP01Cipher:
    """
    UES-P01 (Universal Envelope Steganography - Picture Variant)
    Provides pure Python encryption and decryption for image anti-AI scraping.
    """
    def __init__(self, key: str):
        self.key = key
        self.s1, self.s2, self.s3 = self._derive_seeds(key)

    def _derive_seeds(self, key: str):
        # Derive 32-bit integer seeds from SHA-256 digest
        sha = hashlib.sha256(key.encode('utf-8')).digest()
        s1 = struct.unpack(">I", sha[0:4])[0]
        s2 = struct.unpack(">I", sha[4:8])[0]
        s3 = struct.unpack(">I", sha[8:12])[0]
        return s1, s2, s3

    def encrypt_image(self, input_path: str, output_path: str) -> dict:
        """
        Encrypts an image file into a noise envelope matrix PNG image.
        """
        # 1. Load image and extract RGBA raw pixels
        img = Image.open(input_path).convert('RGBA')
        width, height = img.size
        raw_rgba = img.tobytes()

        # 2. Build header [uint32 width, uint32 height] and payload
        header = struct.pack(">II", width, height)
        payload = header + raw_rgba

        # 3. Zlib L9 Compression
        compressed = zlib.compress(payload, level=9)
        length = len(compressed)

        # 4. Calculate N x N matrix size
        N = math.ceil(math.sqrt(length))
        N2 = N * N

        # 5. Padding using PRNG s2
        rng2 = MT19937_PRNG(self.s2)
        padded = bytearray(compressed)
        for _ in range(N2 - length):
            padded.append(rng2.next_byte())

        # 6. Shuffle 1D array using PRNG s1
        rng1 = MT19937_PRNG(self.s1)
        indices = list(range(N2))
        rng1.shuffle(indices)

        shuffled = bytearray(N2)
        for i in range(N2):
            shuffled[indices[i]] = padded[i]

        # 7. Construct envelope matrix M = N + 2
        M = N + 2
        rng3 = MT19937_PRNG(self.s3)
        env_matrix = bytearray(M * M)

        shuffle_idx = 0
        for r in range(M):
            for c in range(M):
                if r == 0 or r == M - 1 or c == 0 or c == M - 1:
                    env_matrix[r * M + c] = rng3.next_byte()  # Boundary noise wall
                else:
                    env_matrix[r * M + c] = shuffled[shuffle_idx]
                    shuffle_idx += 1

        # 8. Save as protected noise image (Grayscale mode 'L')
        out_img = Image.frombytes('L', (M, M), bytes(env_matrix))
        out_img.save(output_path, 'PNG')

        return {
            "status": "success",
            "core_size": (N, N),
            "envelope_size": (M, M),
            "output_path": output_path
        }

    def decrypt_image(self, input_path: str, output_path: str) -> dict:
        """
        Decrypts a noise envelope PNG image back to the original image.
        """
        # 1. Load protected grayscale noise image
        img = Image.open(input_path).convert('L')
        M, _ = img.size
        N = M - 2
        N2 = N * N
        env_bytes = img.tobytes()

        # 2. Extract inner matrix payload
        shuffled = bytearray(N2)
        idx = 0
        for r in range(1, M - 1):
            for c in range(1, M - 1):
                shuffled[idx] = env_bytes[r * M + c]
                idx += 1

        # 3. Unshuffle payload using PRNG s1
        rng1 = MT19937_PRNG(self.s1)
        indices = list(range(N2))
        rng1.shuffle(indices)

        padded = bytearray(N2)
        for i in range(N2):
            padded[i] = shuffled[indices[i]]

        # 4. Decompress Zlib payload
        try:
            decompressed = zlib.decompress(bytes(padded))
            width, height = struct.unpack(">II", decompressed[0:8])
            raw_rgba = decompressed[8:]

            # 5. Restore original RGBA image
            restored_img = Image.frombytes('RGBA', (width, height), raw_rgba)
            restored_img.save(output_path, 'PNG')

            return {
                "status": "success",
                "restored_size": (width, height),
                "output_path": output_path
            }
        except Exception as err:
            return {
                "status": "error",
                "message": f"Decryption failed: invalid key or corrupted file. ({err})"
            }


def protect_image(input_file: str, output_file: str, secret_key: str):
    cipher = UESP01Cipher(secret_key)
    return cipher.encrypt_image(input_file, output_file)

def restore_image(input_file: str, output_file: str, secret_key: str):
    cipher = UESP01Cipher(secret_key)
    return cipher.decrypt_image(input_file, output_file)


if __name__ == "__main__":
    # Example direct function calls
    key = "UES-P01-Default-Key-2026"
    
    # encrypt_result = protect_image("original.png", "protected.png", key)
    # print(encrypt_result)
    
    # decrypt_result = restore_image("protected.png", "restored.png", key)
    # print(decrypt_result)
    pass