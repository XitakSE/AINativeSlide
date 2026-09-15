# デザインシステム & 堅牢ボックスモデル (IBM Carbon Design System 準拠)

<design_system_specs>
ビジネス・戦略コンサル・エンタープライズの意思決定プレゼンテーションとして即座に通用する品格（Executive Presentation Quality）と、**生成AI特有の安っぽさ（丸すぎる角、ぼやけた影、ネオングラデーション）を根絶する「IBM Carbon Design System」**に準拠した正本（SSOT）ガイドラインです。

---

<anti_ai_smell_visual_principles>
## 🎯 IBM Carbon による「視覚的アンチAI臭」の4大原則

1. **ハードエッジ（No Rounded-2XL）**:
   AIが好む丸っこいカード（`rounded-xl`, `rounded-2xl`）は幼稚・カジュアルな印象を与えます。本システムでは**完全な直角（`rounded-none`）**、または最小限（`rounded-xs: 2px` / `rounded-sm: 4px`）を絶対原則とします。
2. **アンチシャドウ ＆ レイヤリング（No Fake Drop Shadows）**:
   ぼやけたドロップシャドウ（`shadow-md`, `shadow-lg`, `shadow-xl`）を全廃します。立体感や区切りは、影ではなく**1pxの精密な境界線（`border border-gray-200` 等）**と**背景色のコントラスト階層（Gray 10 上の White）**のみで表現します。
3. **ソリッド直線アクセント（No Neon Gradients）**:
   紫〜ピンク等の安易なAIネオングラデーションを禁止し、重要カードや強調には**4pxの直線アクセントバー（`border-l-4 border-blue-600` または `border-t-4 border-blue-600`）**を用います。
4. **工業的精密タイポグラフィ（Engineered Typography）**:
   ポップなフォントを廃止し、人間工学と工学的厳密性に基づいて設計された **`IBM Plex Sans` + `IBM Plex Sans JP`** を正本フォントとします。
</anti_ai_smell_visual_principles>

---

<typography_hierarchy>
## 1. タイポグラフィ階層 (IBM Plex Family)

Google Fonts の `IBM Plex Sans`（欧文・数字・幾何学的でシャープなグロテスクサンセリフ）と `IBM Plex Sans JP`（明瞭で信頼性の高い和文フォント）を組み合わせます。

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+JP:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### フォントサイズ & ウェイト規定（A4横 / 16:9 ワイド共通・視認性基準）

スライドはWebサイトではなく「遠くから投影・印刷で読まれるプレゼンテーション資料」です。
`text-xs` (12px) や `text-[10px]` の乱用（豆粒フォント）は厳禁とし、以下の階層基準を死守してください。

| 役割 | 必須クラス指定 | サイズ/ウェイト | 意図・ガイドライン |
| :--- | :--- | :--- | :--- |
| **Hero Title (Cover)** | `text-5xl font-bold tracking-tight leading-tight` | 48px / Bold | 表紙の主タイトル（重厚な佇まい） |
| **Lead Message (Action Title)** | `text-2xl sm:text-3xl font-bold tracking-tight leading-snug` | 24〜28px / Bold | スライドの結論・主張（一瞬で目に飛び込む大きさ） |
| **サマリの結論・主要指標** | `text-lg sm:text-xl font-bold leading-snug` | 18〜20px / Bold | エグゼクティブサマリの右側結論、コアKPI |
| **巨大数値（Big Numbers）** | `text-3xl sm:text-4xl font-bold font-mono` | 30〜36px / Bold Mono | 定量ROI、削減率、主要実績値 |
| **Card Heading / サブ見出し** | `text-base sm:text-lg font-semibold text-gray-900` | 16〜18px / SemiBold | 各カード・ブロックのタイトル |
| **Body Text (スライド本文)** | `text-sm leading-relaxed text-gray-700` | 14px / Regular | **本文の絶対下限**（12pxは本文で使用禁止） |
| **Kicker / バッジ** | `text-xs font-semibold tracking-wider uppercase` | 12px / SemiBold | 章名バッジ、ステータスラベル |
| **Meta / Footer / Note** | `text-xs text-gray-500 font-mono` | 12px / Medium | 注記・出典・ページ番号（12px未満は使わない） |

> ⚠️ **文字数とフォントサイズの関係（Anti-Font-Shrink Rule）**:
> 「文字数が多すぎて枠に収まらないからフォントを小さくする」という縮小対応は禁止します。文字数を削って要約し（1スライド250〜350文字目安）、フォントサイズ（本文14px、見出し16〜18px）と余白を死守してください。
</typography_hierarchy>

---

<color_palette>
## 2. 推奨カラーパレット (IBM Carbon Color Tokens)

安っぽい原色や曖昧なグラデーションを避け、Carbon の精密なグレースケールと IBM Blue を基調とします。

- **Carbon Cool Gray (ベース・テキスト・背景)**:
  - `bg-gray-100` / `#f4f4f4`: スライド背景（Gray 10）
  - `bg-white` / `#ffffff`: カード・コンテナ地色（Layering Surface）
  - `border-gray-200` / `#e0e0e0`: 精密境界線・区切り線（Gray 20）
  - `text-gray-900` / `#161616`: 主見出し・結論（Gray 100）
  - `text-gray-700` / `#525252`: 本文・説明文（Gray 70）
  - `text-gray-500` / `#8d8d8d`: メタ情報・注記・枠線（Gray 50）
  - `bg-gray-900` / `#161616`: 表紙・ツールバー・重要反転スライド（Gray 100）
- **Brand / Primary (IBM Blue)**:
  - `brand-50: #edf5ff` (Blue 10: 重要カードの背景ハイライト)
  - `brand-100: #d0e2ff` (Blue 20: 選択バッジ背景)
  - `brand-500: #0f62fe` (Blue 60: 主要インタラクティブ色、キー数値)
  - `brand-600: #0043ce` (Blue 70: 直線アクセントライン、主要タグ、推奨枠)
  - `brand-900: #001d6c` (Blue 90: ディープブルー見出し)
- **Data Vis & Accents (Carbon Visualization Tokens)**:
  - `cyan-500: #1192e8` (Cyan 50: サブ指標、推移線)
  - `teal-500: #009d9a` (Teal 50: 効率化、自律機能)
  - `magenta-500: #ee538b` (Magenta 50: ハイライト、特殊アラート)
  - `purple-500: #a56eff` (Purple 50: カテゴリ区分)
- **Semantic (Status / Contrast)**:
  - `red-600: #da1e28` / `red-50: #fff1f1`: 課題・AS-IS・重大注意（Red 60）
  - `green-600: #198038` / `green-50: #defbe6`: 解決策・TO-BE・達成（Green 60）
</color_palette>

---

<robust_box_model>
## 3. 堅牢なボックスモデル（IBM Carbon 準拠ハードエッジ構造）

テキストの推敲によって文字数が2倍〜3倍に増減しても、**要素が重なったりスライド枠を突き抜けたりしない** ための鉄則です。

1. **スライド全体の縦構造**:
   ```html
   <section class="slide p-12 justify-between flex flex-col overflow-hidden relative bg-[#f4f4f4]">
     <!-- ヘッダー（固定） -->
     <div class="flex-shrink-0 border-b border-gray-300 pb-4">...</div>

     <!-- メインコンテンツ（伸縮可能） -->
     <div class="flex-1 min-h-0 flex flex-col justify-center my-auto">
       <div class="grid grid-cols-3 gap-6">...</div>
     </div>

     <!-- フッター（固定） -->
     <div class="flex-shrink-0 pt-3 border-t border-gray-300 flex justify-between">...</div>
   </section>
   ```
   - `flex-shrink-0`: ヘッダー・フッターがコンテンツに押しつぶされるのを防ぐ。
   - `flex-1 min-h-0`: メインコンテンツ領域がスライドの高さを超えないように自動収縮する。

2. **Carbon 標準カード構造（ハードエッジ・影ゼロ・1pxボーダー）**:
   ```html
   <div class="bg-white rounded-none p-5 border border-gray-300 shadow-none flex flex-col justify-between">
     <div>
       <!-- タイトル・本文 -->
       <div class="text-base font-semibold text-gray-900 mb-2">モジュール概要</div>
       <p class="text-sm text-gray-700 leading-relaxed">...</p>
     </div>
     <!-- カード内ボトム注記（固定位置に配置） -->
     <div class="mt-4 pt-3 border-t border-gray-200 text-xs font-mono text-gray-500">...</div>
   </div>
   ```

3. **推奨案・最重要カードの強調構造（直線アクセントバー）**:
   ```html
   <!-- ドロップシャドウを使わず、左端の4px太線で視線を引きつける -->
   <div class="bg-white rounded-none p-5 border border-gray-300 border-l-4 border-l-blue-600 shadow-none flex flex-col justify-between">
     ...
   </div>
   ```
</robust_box_model>
</design_system_specs>
