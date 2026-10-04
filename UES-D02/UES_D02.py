import math
import random
import zlib
import hashlib
import struct
from typing import Tuple, Dict, Any

def derive_seeds_sha256(key_input: str) -> Tuple[random.Random, random.Random, random.Random]:
    """
    從金鑰導出三個獨立且強韌的 PRNG 實例。
    修復 Python 原生 hash() 在跨系統與重啟程序後隨機種子不一致的問題。
    """
    key_bytes = key_input.encode("utf-8")
    digest = hashlib.sha256(key_bytes).digest()
    
    # 將 SHA-256 的 32 位元組切分為三個 32 位元整數種子
    s1, s2, s3 = struct.unpack(">III", digest[:12])
    
    return random.Random(s1), random.Random(s2), random.Random(s3)

def ues_dynamic_encrypt(text: str, key_input: str) -> Dict[str, Any]:
    """
    UES-D02 動態矩陣加密演算法
    根據壓縮後數據長度，自動計算最小 N x N 核心矩陣與精準 1 圈外圍城牆 (M = N + 2)
    """
    prng_core, prng_pad, prng_wall = derive_seeds_sha256(key_input)
    
    # 1. 資料壓縮
    raw_bytes = text.encode("utf-8")
    compressed = zlib.compress(raw_bytes, level=9)
    L = len(compressed)
    
    # 2. 計算最小平方核心維度 N x N (需容納 1-Byte 長度標頭 + L 位元組壓縮數據)
    N = math.ceil(math.sqrt(L + 1))
    core_cells = N * N
    
    # 3. 核心填充 (長度標頭 + 壓縮內容 + 隨機填充)
    padded_core = bytearray(core_cells)
    padded_core[0] = L
    padded_core[1 : 1 + L] = compressed
    for i in range(1 + L, core_cells):
        padded_core[i] = prng_pad.randint(0, 255)
        
    # 4. 1D 核心打亂置換
    core_key = list(range(core_cells))
    prng_core.shuffle(core_key)
    shuffled_core = [padded_core[i] for i in core_key]
    
    # 將 1D 排列轉為 N x N 核心矩陣
    core_matrix = [shuffled_core[i * N : (i + 1) * N] for i in range(N)]
    
    # 5. 生成精準 1 圈外圍城牆 (總邊長 M = N + 2)
    M = N + 2
    final_shuffled = []
    
    for r in range(M):
        for c in range(M):
            if 1 <= r < M - 1 and 1 <= c < M - 1:
                # 內圍核心區域
                final_shuffled.append(core_matrix[r - 1][c - 1])
            else:
                # 外圍城牆雜訊 (使用獨立 prng_wall)
                final_shuffled.append(prng_wall.randint(0, 255))
                
    # 6. 中文 Unicode 隱寫偽裝轉換 (0x4E00 偏移)
    disguised_text = "".join(chr(0x4E00 + b) for b in final_shuffled)
    
    return {
        "disguised_text": disguised_text,
        "raw_bytes_len": len(raw_bytes),
        "compressed_len": L,
        "core_dimension_N": N,
        "total_dimension_M": M,
        "total_chars": len(disguised_text)
    }

def ues_dynamic_decrypt(disguised_text: str, key_input: str) -> str:
    """
    UES-D02 動態矩陣解密演算法
    自動推導動態邊長 M 與核心邊長 N，完美剝離城牆並還原內容
    """
    prng_core, prng_pad, prng_wall = derive_seeds_sha256(key_input)
    total_cells = len(disguised_text)
    
    # 推導總邊長 M 與核心邊長 N
    M = int(math.isqrt(total_cells))
    if M * M != total_cells:
        raise ValueError("密文長度無效，無法構成完美的平方城牆矩陣！")
    N = M - 2
    core_cells = N * N
    
    # 1. 還原中文字為 Byte 陣列 (0~255)
    final_shuffled = [ord(c) - 0x4E00 for c in disguised_text]
    
    # 2. 剝離 1 圈城牆，提取 N x N 核心內容
    shuffled_core = []
    idx = 0
    for r in range(M):
        for c in range(M):
            if 1 <= r < M - 1 and 1 <= c < M - 1:
                shuffled_core.append(final_shuffled[idx])
            else:
                # 消耗掉 prng_wall 隨機步數以保持 PRNG 同步
                _ = prng_wall.randint(0, 255)
            idx += 1
            
    # 3. 還原 1D 核心打亂置換
    core_key = list(range(core_cells))
    prng_core.shuffle(core_key)
    
    padded_core = bytearray(core_cells)
    for original_idx, key_idx in enumerate(core_key):
        padded_core[key_idx] = shuffled_core[original_idx]
        
    # 4. 讀取長度標頭並解壓縮
    compressed_len = padded_core[0]
    if compressed_len <= 0 or compressed_len >= core_cells:
        raise ValueError("解密長度標頭異常，可能是金鑰錯誤或密文損毀！")
        
    compressed_bytes = bytes(padded_core[1 : 1 + compressed_len])
    
    try:
        decompressed = zlib.decompress(compressed_bytes)
        return decompressed.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Zlib 解壓縮失敗 (金鑰錯誤或資料損毀): {e}")

def run_dynamic_unit_tests():
    """執行 UES-D02 動態矩陣單元測試"""
    print("=" * 65)
    print("🚀 執行 UES-D02 Dynamic Matrix Cipher 演算法驗證...")
    print("=" * 65)
    
    test_cases = [
        ("短文本測試", "key123"),
        ("自研動態平方矩陣，精準 1 圈城牆防禦！中長度訊息動態調整測試。", "ues2026_secret_key"),
        ("A" * 150, "long_text_key_hash"),
        ("🥷 隱寫術 Emoji 與幾何城牆測試 🏰 Matrix Dynamic Dimension Test", "crypto_key_2026")
    ]
    
    for idx, (text, key) in enumerate(test_cases, 1):
        res = ues_dynamic_encrypt(text, key)
        restored = ues_dynamic_decrypt(res["disguised_text"], key)
        
        assert restored == text, f"測試 {idx} 失敗！"
        print(f"✅ [測試 {idx}] 通過:")
        print(f"   明文: '{text[:20]}...' ({len(text)} 字)")
        print(f"   核心邊長 (N): {res['core_dimension_N']} | 城牆總邊長 (M): {res['total_dimension_M']}")
        print(f"   動態密文長度: {res['total_chars']} 個中文字 (壓縮率: {res['compressed_len']} B / 核心: {res['core_dimension_N']**2} 格)")
        print("-" * 65)

if __name__ == "__main__":
    run_dynamic_unit_tests()
```eoc
