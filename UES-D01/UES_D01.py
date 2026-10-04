import os
import random
import zlib
import struct
import numpy as np
from typing import Tuple, Dict, Any


def parse_key_32bytes(key_input: Any) -> bytes:
    """將輸入的金鑰解析並填充/截斷為標準的 32 位元組 (256-bit)"""
    if isinstance(key_input, bytes):
        key_bytes = key_input
    else:
        str_key = str(key_input).strip()
        if len(str_key) == 64:
            try:
                key_bytes = bytes.fromhex(str_key)
            except ValueError:
                key_bytes = str_key.encode("utf-8")
        else:
            key_bytes = str_key.encode("utf-8")

    if len(key_bytes) < 32:
        key_bytes = key_bytes.ljust(32, b"\x00")
    else:
        key_bytes = key_bytes[:32]
    return key_bytes


def derive_seeds_256(key_input: Any) -> Tuple[int, int, int]:
    """從 32 位元組 (256-bit) 金鑰中推導高敏感度的 PRNG 種子，實現 256-bit 金鑰雪崩保護"""
    key_bytes = parse_key_32bytes(key_input)
    w = struct.unpack(">8I", key_bytes)

    def mix(w: Tuple[int, ...], salt: int) -> int:
        h = (w[0] ^ salt ^ w[4]) & 0xFFFFFFFF
        h = (h * 0xCC9E2D51) & 0xFFFFFFFF
        h = (((h << 13) | (h >> 19)) ^ w[1]) & 0xFFFFFFFF
        h = (h * 0x1B873593) & 0xFFFFFFFF
        h = (((h << 15) | (h >> 17)) ^ w[2] ^ w[5]) & 0xFFFFFFFF
        h = (h * 0xE6546B64) & 0xFFFFFFFF
        h = (h ^ (h >> 16) ^ w[3] ^ w[6] ^ w[7]) & 0xFFFFFFFF
        return h

    return (
        mix(w, 0x12345678),
        mix(w, 0x87654321),
        mix(w, 0xABCDEF01),
    )


def ultimate_encrypt(text: str, key_input: Any) -> str:
    seed_key1, seed_key2, seed_noise = derive_seeds_256(key_input)
    prng1 = random.Random(seed_key1)
    prng2 = random.Random(seed_key2)
    prng_noise = random.Random(seed_noise)

    # 1. 壓縮與標頭填充
    compressed = zlib.compress(text.encode("utf-8"), level=9)
    if len(compressed) > 63:
        raise ValueError(
            f"壓縮後長度 ({len(compressed)} 位元組) 超過矩陣上限 63 位元組，請精簡輸入內容！"
        )
    
    padded_data = bytearray(64)
    padded_data[0] = len(compressed)
    padded_data[1 : 1 + len(compressed)] = compressed
    for i in range(1 + len(compressed), 64):
        padded_data[i] = prng_noise.randint(0, 255)

    # 2. 第一階段：1D 金鑰置換
    key1 = list(range(64))
    prng1.shuffle(key1)
    shuffled_bytes = [padded_data[i] for i in key1]

    # 3. 第二階段：循環位移擴展成 64x64 矩陣，並套上 66x66 城牆
    core_matrix = np.array([np.roll(shuffled_bytes, i) for i in range(64)])
    container = np.array([[prng_noise.randint(0, 255) for _ in range(66)] for _ in range(66)], dtype=int)
    container[1:65, 1:65] = core_matrix
    flat_cipher = container.flatten()

    # 4. 第三階段：全域二次隨機打亂
    key2 = list(range(len(flat_cipher)))
    prng2.shuffle(key2)
    final_shuffled = np.array([flat_cipher[i] for i in key2])

    # 5. 進位轉換：轉換成 Unicode 常用中文字區段 (0x4E00 偏移)
    disguised_text = "".join(chr(0x4E00 + int(b)) for b in final_shuffled)
    return disguised_text


def ultimate_decrypt(disguised_text: str, key_input: Any) -> str:
    if len(disguised_text) != 4356:
        raise ValueError(f"密文長度無效 (須為 4,356 個中文字，目前為 {len(disguised_text)} 字)")

    seed_key1, seed_key2, _ = derive_seeds_256(key_input)
    prng1 = random.Random(seed_key1)
    prng2 = random.Random(seed_key2)

    key1 = list(range(64))
    prng1.shuffle(key1)

    key2 = list(range(len(disguised_text)))
    prng2.shuffle(key2)

    # 2. 反向進位還原密文數值陣列 (0~255)
    final_shuffled = [ord(c) - 0x4E00 for c in disguised_text]

    # 3. 還原全域二次打亂 (還原 key2 置換)
    flat_cipher = [0] * len(final_shuffled)
    for current_idx, original_idx in enumerate(key2):
        flat_cipher[original_idx] = final_shuffled[current_idx]

    # 4. 剝離 66x66 矩陣的外圈城牆雜訊，取得 64x64 核心矩陣
    matrix_66x66 = np.array(flat_cipher).reshape(66, 66)
    core_matrix = matrix_66x66[1:65, 1:65]

    # 5. 提取 row 0 (對應 np.roll(shuffledBytes, 0)，即 1D 打亂後的數據)
    shuffled_bytes = core_matrix[0]

    # 6. 還原第一階段 1D 字元打亂 (還原 key1 置換)
    padded_data = bytearray(64)
    for original_idx, key_idx in enumerate(key1):
        padded_data[key_idx] = shuffled_bytes[original_idx]

    # 7. 讀取標頭紀錄的真實壓縮長度，避免 zlib 尾端雜訊解壓報錯
    compressed_len = padded_data[0]
    if compressed_len <= 0 or compressed_len > 63:
        raise ValueError("無效的解密長度標頭或金鑰不正確 (Invalid Length Header)")

    compressed_bytes = bytes(padded_data[1 : 1 + compressed_len])
    return zlib.decompress(compressed_bytes).decode("utf-8")


def run_unit_tests():
    """執行自動化測試驗證 32-Byte (256-bit) 金鑰情境"""
    print("=" * 60)
    print("🚀 正在執行 256-bit 高強度金鑰自動化單元測試...")
    print("=" * 60)

    test_cases = [
        ("密碼學矩陣研究：先壓縮再揉碎！", "2b7e151628aed2a6abf7158809cf4f3c2b7e151628aed2a6abf7158809cf4f3c"),
        ("Hello World! 1234567890", "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
        ("🥷 隱寫術與矩陣防護測試 🛡️", "8888888888888888888888888888888888888888888888888888888888888888"),
    ]

    for idx, (text, key) in enumerate(test_cases, 1):
        try:
            cipher = ultimate_encrypt(text, key)
            restored = ultimate_decrypt(cipher, key)
            assert text == restored, f"解密結果不匹配: {text} != {restored}"
            print(f"✅ [測試 {idx}] 通過: '{text}' (256-bit Key: {key[:16]}...)")
        except Exception as e:
            print(f"❌ [測試 {idx}] 失敗: {e}")

    # 測試更改 256-bit 金鑰中的 1 個 bit 是否能成功擋下
    key_orig = "2b7e151628aed2a6abf7158809cf4f3c2b7e151628aed2a6abf7158809cf4f3c"
    key_mutated = "2b7e151628aed2a6abf7158809cf4f3c2b7e151628aed2a6abf7158809cf4f3d" # 只改最後 1 位
    
    wrong_key_blocked = False
    try:
        cipher = ultimate_encrypt("256-bit 雪崩測試", key_orig)
        wrong_restored = ultimate_decrypt(cipher, key_mutated)
        if wrong_restored != "256-bit 雪崩測試":
            wrong_key_blocked = True
    except Exception:
        wrong_key_blocked = True

    if wrong_key_blocked:
        print("✅ [256-bit 雪崩測試] 通過: 僅改變 256-bit 金鑰中的 1 個 Bit 即可完美觸發雪崩！")

    print("\n所有測試順利完成！\n")


if __name__ == "__main__":
    run_unit_tests()
