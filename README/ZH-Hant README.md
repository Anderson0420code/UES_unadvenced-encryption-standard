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