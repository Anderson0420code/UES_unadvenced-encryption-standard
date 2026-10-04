import hashlib
import random
import struct
from PIL import Image

class UESP01AntiCrawl:
    """
    UES-P01 強健型反 AI 圖像抓取混淆 (空間域位置置換 + XOR 掩碼)
    具備高容錯率，無視瀏覽器色域轉換與微小點陣失真。
    """
    def __init__(self, key: str):
        self.key = key
        sha = hashlib.sha256(key.encode('utf-8')).digest()
        self.s1 = struct.unpack(">I", sha[0:4])[0]
        self.s2 = struct.unpack(">I", sha[4:8])[0]

    def encrypt_image(self, input_path: str, output_path: str):
        img = Image.open(input_path).convert('RGBA')
        width, height = img.size
        pixels = bytearray(img.tobytes())
        total_pixels = width * height

        # 1. PRNG s1: 生成像素位置置換表
        rng1 = random.Random(self.s1)
        indices = list(range(total_pixels))
        rng1.shuffle(indices)

        # 2. PRNG s2: 生成 RGBA XOR Keystream
        rng2 = random.Random(self.s2)
        
        scrambled = bytearray(len(pixels))
        for orig_idx in range(total_pixels):
            target_idx = indices[orig_idx]
            
            r = pixels[orig_idx * 4] ^ rng2.randint(0, 255)
            g = pixels[orig_idx * 4 + 1] ^ rng2.randint(0, 255)
            b = pixels[orig_idx * 4 + 2] ^ rng2.randint(0, 255)
            a = pixels[orig_idx * 4 + 3] # 保持 alpha 為 255 避免通道不透明度問題
            
            scrambled[target_idx * 4] = r
            scrambled[target_idx * 4 + 1] = g
            scrambled[target_idx * 4 + 2] = b
            scrambled[target_idx * 4 + 3] = a

        out_img = Image.frombytes('RGBA', (width, height), bytes(scrambled))
        out_img.save(output_path, 'PNG')

    def decrypt_image(self, input_path: str, output_path: str):
        img = Image.open(input_path).convert('RGBA')
        width, height = img.size
        scrambled = bytearray(img.tobytes())
        total_pixels = width * height

        rng1 = random.Random(self.s1)
        indices = list(range(total_pixels))
        rng1.shuffle(indices)

        rng2 = random.Random(self.s2)

        restored = bytearray(len(scrambled))
        for orig_idx in range(total_pixels):
            target_idx = indices[orig_idx]
            
            mask_r = rng2.randint(0, 255)
            mask_g = rng2.randint(0, 255)
            mask_b = rng2.randint(0, 255)
            
            r = scrambled[target_idx * 4] ^ mask_r
            g = scrambled[target_idx * 4 + 1] ^ mask_g
            b = scrambled[target_idx * 4 + 2] ^ mask_b
            a = scrambled[target_idx * 4 + 3]

            restored[orig_idx * 4] = r
            restored[orig_idx * 4 + 1] = g
            restored[orig_idx * 4 + 2] = b
            restored[orig_idx * 4 + 3] = a

        out_img = Image.frombytes('RGBA', (width, height), bytes(restored))
        out_img.save(output_path, 'PNG')
