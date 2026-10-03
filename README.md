# UES_unadvenced-encryption-standard
A system for anti ai crawling If bugs/problems found, please contact andersonlilife@icloud.com or make a branch
 # unadvanced-encryption-standard (UES) Technical & Web GUI Documentation

`unadvanced-encryption-standard` is a data steganography and camouflage protection system implemented via Python and modern browser-native JavaScript (Web GUI). The primary design goal of this system is **anti-AI web crawling and unauthorized data harvesting**. By employing data compression, Pseudo-Random Number Generator (PRNG) permutations, matrix transformations, and character/image encoding, raw text, confidential files, or images are transformed into text or grayscale noise images that AI crawlers cannot parse or extract semantic features from, preventing data from being ingested into AI model training sets.

---

## System Design Goals & Principles

Traditional text and images on the public web are easily analyzed by automated crawlers and utilized to train Large Language Models (LLMs) or vision models. This system disrupts this process through the following mechanisms:

1. **Semantic Structure Destruction**: Compresses text, subjects it to dual/dynamic chaotic permutations, and maps it to semantically unrelated Unicode Chinese character blocks (`0x4E00` offset), ensuring text crawlers only extract meaningless character combinations.
2. **Image Data Noisification**: Extracts raw RGBA image pixel data, compresses and permutes it, and repackages it into single-channel grayscale (Mode 'L') or pixel noise images, blinding image crawlers to original visual features.
3. **Dynamic Boundary Noise**: Wraps outer pseudo-random generated walls around the core data matrix to interfere with automated feature extraction algorithms.
4. **Zero-Backend Pure Frontend (Web GUI)**: Provides a serverless web workbench based on HTML5 Canvas, Tailwind CSS, and JavaScript (Pako Zlib, Web Crypto API), ensuring total local privacy protection inside the browser.

---

## Module Architecture

The system comprises three core modules, each featuring a Python backend engine and an independent pure-frontend Web GUI tool.

```
UES System Architecture
│
├── 1. D-Series (Text & Document Protection)
│   ├── UES-D01: Fixed 66x66 Matrix (For short text/passwords) [Python & HTML GUI]
│   └── UES-D02: Adaptive Dynamic N×N Matrix + Precise M=N+2 Wall (For arbitrary length text) [Python & HTML GUI]
│
└── 2. P-Series (Image Data Protection)
    └── UES-P01: RGBA Pixel Compression/Obfuscation + Grayscale Noise Wall Image [Python & HTML GUI]
```

---

### 1. D-Series: Text & Document Protection Modules

#### UES-D01 (Fixed-Size Text Cipher - 66×66 Matrix)
* **Applicable Scenarios**: Short texts, passwords, or fixed-length data protection.
* **Technical Details**:
  * **Key Processing**: Processes input key into 32 bytes (256-bit) and derives PRNG seed via `SHA-256`.
  * **Capacity Limit**: Raw text length $L$ after `zlib` (Level 9) compression must not exceed 63 bytes.
  * **Matrix Transformation**:
    1. Perform 1D key permutation on 64 bytes.
    2. Expand into a $64 \times 64$ core matrix via circular shift (`np.roll`).
    3. Wrap 1 layer of pseudo-random noise walls around the core matrix to construct a $66 \times 66$ matrix (4,356 elements total).
    4. Perform global secondary shuffling on the $66 \times 66$ array.
  * **Output Encoding**: Mapped to Unicode common Chinese character section (`0x4E00`), outputting exactly 4,356 Chinese characters.
* **GUI Tool**: `UES-D01.html` (Featuring 66×66 Canvas heatmap rendering, data probes, and avalanche testing).

#### UES-D02 (Dynamic-Size Text Cipher - Adaptive Matrix)
* **Applicable Scenarios**: Arbitrary-length text or document content protection.
* **Technical Details**:
  * **Key Processing**: Uses `SHA-256` to derive three independent 32-bit integer seeds (`prng_core`, `prng_pad`, `prng_wall`).
  * **Dynamic Dimension Calculation**:
    Let $L$ be the byte length of text after `zlib` compression. The minimum core square matrix side length $N$ is calculated as:
    $$N = \lceil \sqrt{L + 1} \rceil$$
  * **Wall Structure**: Adds 1 layer of noise wall around the $N \times N$ core, forming a matrix of side length $M = N + 2$ (total elements $M^2$).
  * **Output Encoding**: Dynamically generates a Unicode Chinese string of length $M^2$ (`0x4E00` offset).
* **GUI Tool**: `UES-D02.html` (Supports dynamic N×N / M×M visualization and 5-step pipeline dissection).

---

### 2. P-Series: Image Protection Module

#### UES-P01 (Image Data Steganography Protection)
* **Applicable Scenarios**: Anti-AI crawler protection for PNG, JPEG, and other image formats.
* **Technical Details**:
  * **Data Extraction & Header Construction**: Reads raw RGBA pixel data of the image, establishing an 8-byte Header containing 32-bit width and height.
  * **Data Compression & Obfuscation**: Compresses payload using `zlib` (Level 9), applying bitwise XOR and position permutation on pixel arrays via MT19937 PRNG.
  * **Wall Encapsulation & Image Output**: Wraps defensive noise around the perimeter, exporting the array into a grayscale noise map or pixel-obfuscated image resistant to AI feature extraction.
* **GUI Tool**: `UES-P01.html` (Provides single-page drag-and-drop upload, real-time preview, and local restoration).

---

## Frontend GUI Interface Usage

The project provides three serverless Single Page Applications (SPAs):

1. **`UES-D01.html`**: Open directly in a browser to perform encryption, decryption, and heatmap probe analysis on a fixed 66×66 matrix.
2. **`UES-D02.html`**: Supports long-text adaptive dynamic matrix encryption, featuring visual Canvas matrix scaling and key avalanche testing.
3. **`UES-P01.html`**: Provides browser-native anti-crawler image encryption and reverse decryption, ensuring images are never transmitted to third-party servers.

---

## Python Script Usage Examples

### 1. UES-D02 Dynamic Text Encryption & Decryption

```python
from UES_D02 import ues_dynamic_encrypt, ues_dynamic_decrypt

key = "secret-key-2026"
text = "這是一段需要防止被 AI 爬蟲抓取的機密文件內容。"

# Encryption
result = ues_dynamic_encrypt(text, key)
disguised_text = result["disguised_text"]
print("Encrypted Result (Unicode Chinese String):", disguised_text)

# Decryption
restored_text = ues_dynamic_decrypt(disguised_text, key)
print("Decrypted Result:", restored_text)
```

### 2. UES-P01 Image Protection & Restoration

```python
from UES_P01 import protect_image, restore_image

key = "image-protection-key"

# Convert original image into an anti-crawler grayscale noise map
protect_result = protect_image("input.png", "protected.png", key)

# Restore noise map back to original RGBA image
restore_result = restore_image("protected.png", "restored.png", key)
```

---

## Technical Limitations & Notes

1. **D01 Capacity Limit**: `UES-D01` requires text compressed via `zlib` to not exceed 63 bytes. For longer data, please use `UES-D02`.
2. **Key Precision**: Encryption and decryption heavily rely on the PRNG seed derived from the key. If the key differs by even 1 bit, decompression will fail.
3. **Cryptographic Security Positioning**: The core purpose of this project is **data steganography, obfuscation, and anti-AI automated harvesting**. System randomness relies on Mersenne Twister (MT19937) / 
Pseudo-RNG algorithms and should not replace standard cryptographic algorithms like AES for high-security financial transmission.


# unadvanced-encryption-standard (UES) 技術與 Web GUI 說明文件

`unadvanced-encryption-standard` 是一套基於 Python 與 現代瀏覽器原生 JS（Web GUI）實現的數據隱寫與偽裝保護系統。本系統設計目標為**反 AI 網絡爬蟲與未授權數據抓取**，透過數據壓縮、偽隨機數生成器（PRNG）置換、矩陣轉換與字符/圖像編碼，將原始文字、機密文件或圖像轉化為無法被 AI 爬蟲解析與提取語意特徵的文本或灰階噪點圖像，防止數據被納入 AI 模型訓練集。

---

## 系統設計目標與原理

傳統的文字與圖像在公開網絡上易被自動化爬蟲分析並用於訓練大型語言模型（LLM）或視覺模型。本系統透過以下幾項機制進行阻斷：

1. **破壞文本語意結構**：將文字壓縮並經過雙重/動態亂序置換後，映射至無語意關聯的 Unicode 中文字符區段（`0x4E00` 偏移），使文本爬蟲僅能擷取出無意義的字元組合。
2. **圖像數據噪點化**：提取圖像 RGBA 原始像素數據，經壓縮與置換後，重新打包為單通道灰階（Mode 'L'）圖像或像素噪點圖，使圖像爬蟲無法獲得原始視覺特徵。
3. **動態邊界雜訊**：在數據核心矩陣外圍加入偽隨機生成的外牆雜訊，干擾自動化特徵提取演算法。
4. **零後端純前端（Web GUI）**：提供基於 HTML5 Canvas, Tailwind CSS 與 JavaScript (Pako Zlib, Web Crypto API) 的無伺服器網頁工作臺，保障數據在瀏覽器本機完全隱私保護。

---

## 模組說明與架構

本系統包含三個核心模組，各自具備 Python 後端引擎與獨立的純前端 Web GUI 工具。

```
UES 系統架構
│
├── 1. D 系列 (文字與文件隱寫 protection)
│   ├── UES-D01: 固定尺寸 66x66 矩陣 (適用短文本/密碼) [Python & HTML GUI]
│   └── UES-D02: 自適應動態 N×N 矩陣 + 精準 M=N+2 城牆 (適用任意長文本) [Python & HTML GUI]
│
└── 2. P 系列 (圖像數據保護)
    └── UES-P01: RGBA 像素壓縮/混淆 + 灰階噪聲城牆圖 [Python & HTML GUI]
```

---

### 1. D 系列：文字與文件數據保護模組

#### UES-D01 (固定尺寸文字加密 - 66×66 矩陣)
* **適用場景**：短文本、密碼或固定長度資料保護。
* **技術細節**：
  * **金鑰處理**：將輸入金鑰處理為 32 位元組（256-bit），並透過 `SHA-256` 導出 PRNG 種子。
  * **容量限制**：原始文字經 `zlib`（Level 9）壓縮後的長度 $L$ 不得超過 63 位元組。
  * **矩陣轉換**：
    1. 對 64 位元組進行一維金鑰置換。
    2. 利用循環位移（`np.roll`）擴展為 $64 \times 64$ 核心矩陣。
    3. 在核心矩陣外圍包裹 1 圈偽隨機雜訊城牆，構建 $66 \times 66$ 矩陣（共 4,356 個元素）。
    4. 對 $66 \times 66$ 陣列進行全域二次打亂。
  * **輸出編碼**：映射至 Unicode 常用中文字區段（`0x4E00`），固定輸出 4,356 個中文字元。
* **GUI 工具**：`UES-D01.html`（具備 66×66 Canvas 熱力圖繪製、數據探針與雪崩測試）。

#### UES-D02 (動態尺寸文字加密 - 自適應矩陣)
* **適用場景**：任意長度文本或文件內容保護。
* **技術細節**：
  * **金鑰處理**：使用 `SHA-256` 導出三組獨立 32 位元整數種子（`prng_core`, `prng_pad`, `prng_wall`）。
  * **動態維度計算**：
    設文字經 `zlib` 壓縮後的長度為 $L$ 位元組，最小核心平方矩陣邊長 $N$ 計算如下：
    $$N = \lceil \sqrt{L + 1} \rceil$$
  * **城牆結構**：在 $N \times N$ 核心外圍加入 1 圈雜訊城牆，形成邊長 $M = N + 2$ 的矩陣（總元素數 $M^2$）。
  * **輸出編碼**：動態生成長度為 $M^2$ 的 Unicode 中文字串（`0x4E00` 偏移）。
* **GUI 工具**：`UES-D02.html`（支援動態 N×N / M×M 視覺化繪製與五大步驟管道剖析）。

---

### 2. P 系列：圖像保護模組

#### UES-P01 (圖像數據隱寫保護)
* **適用場景**：PNG、JPEG 等圖像檔案之抗 AI 爬蟲保護。
* **技術細節**：
  * **數據提取與標頭構建**：讀取圖像 RGBA 原始像素數據，建立包含 32 位元寬高的 8 位元組 Header。
  * **數據壓縮與混淆**：使用 `zlib`（Level 9）壓縮 Payload，透過 MT19937 偽隨機生成器對像素陣列進行位元異或（XOR）與位置置換。
  * **城牆封裝與圖像輸出**：外圍加上防護噪聲，將陣列導出為抗 AI 特徵提取之灰階噪點圖或像素混淆圖。
* **GUI 工具**：`UES-P01.html`（提供單頁拖曳上傳、即時預覽與本機還原功能）。

---

## 前端 GUI 介面使用方式

本專案提供三款無須安裝後端環境的 Web 單頁應用程式（Single Page Applications）：

1. **UES-D01.html**：直接於瀏覽器開啟即可進行 66×66 固定矩陣之加密、解密與熱力圖探針分析。
2. **UES-D02.html**：支援長篇文字自適應動態矩陣加密，具備視覺化 Canvas 矩陣縮放與金鑰雪崩測試。
3. **UES-P01.html**：提供純瀏覽器本機端圖像抗爬蟲加密與反向解密，保障影像不被傳輸至第三方伺服器。

---

## Python 腳本使用範例

### 1. UES-D02 文字動態加解密

```python
from UES_D02 import ues_dynamic_encrypt, ues_dynamic_decrypt

key = "secret-key-2026"
text = "這是一段需要防止被 AI 爬蟲抓取的機密文件內容。"

# 加密
result = ues_dynamic_encrypt(text, key)
disguised_text = result["disguised_text"]
print("加密結果 (Unicode 中文字串):", disguised_text)

# 解密
restored_text = ues_dynamic_decrypt(disguised_text, key)
print("解密結果:", restored_text)
```

### 2. UES-P01 圖像保護與還原

```python
from UES_P01 import protect_image, restore_image

key = "image-protection-key"

# 將原始圖像轉換為抗爬蟲灰階噪點圖
protect_result = protect_image("input.png", "protected.png", key)

# 將噪點圖還原為原始 RGBA 圖像
restore_result = restore_image("protected.png", "restored.png", key)
```

---

## 技術限制與說明

1. **D01 容量限制**：`UES-D01` 要求文字經 `zlib` 壓縮後不可超過 63 位元組。若數據較長，請選用 `UES-D02`。
2. **金鑰精確度**：加解密過程高度依賴金鑰導出的 PRNG 種子，若金鑰相差 1 個位元，將無法解壓縮。
3. **密碼學安全定位**：本專案之核心目的為**數據隱寫、混淆與反 AI 自動化採集**。系統隨機數依賴 Mersenne Twister (MT19937) / Pseudo-RNG 演算法，不應替代 AES 等標準加密演算法用於高資安等級之金融傳輸。
