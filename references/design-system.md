# デザインシステム & 堅牢ボックスモデル (Design System & Box Model)

<design_system_specs>
ビジネスプレゼンテーションとして即座に通用する品格（Executive Presentation Quality）と、テキスト推敲時のレイアウト崩れを防ぐ構造設計のガイドラインです。

---

<typography_hierarchy>
## 1. タイポグラフィ階層

Google Fonts の `Plus Jakarta Sans`（欧文・数字・幾何学的で洗練されたサンセリフ）と `Noto Sans JP`（読みやすく信頼性の高い和文フォント）を組み合わせます。

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

### フォントサイズ & ウェイト規定（A4横 / 16:9 ワイド共通・視認性基準）

スライドはWebサイトではなく「遠くから投影・印刷で読まれるプレゼンテーション資料」です。
`text-xs` (12px) や `text-[10px]` の乱用（豆粒フォント）は厳禁とし、以下の階層基準を死守してください。

| 役割 | 必須クラス指定 | サイズ/ウェイト | 意図・ガイドライン |
| :--- | :--- | :--- | :--- |
| **Hero Title (Cover)** | `text-5xl font-black tracking-tight leading-tight` | 48px / Black | 表紙の主タイトル（圧倒的な重厚感） |
| **Lead Message (Action Title)** | `text-2xl sm:text-3xl font-bold tracking-tight leading-snug` | 24〜28px / Bold | スライドの結論・主張（一瞬で目に飛び込む大きさ） |
| **サマリの結論・主要指標** | `text-lg sm:text-xl font-black leading-snug` | 18〜20px / Black | エグゼクティブサマリの右側結論、コアKPI |
| **巨大数値（Big Numbers）** | `text-3xl sm:text-4xl font-black` | 30〜36px / Black | 定量ROI、削減率、主要実績値 |
| **Card Heading / サブ見出し** | `text-base sm:text-lg font-bold text-slate-900` | 16〜18px / Bold | 各カード・ブロックのタイトル |
| **Body Text (スライド本文)** | `text-sm leading-relaxed text-slate-600` | 14px / Regular | **本文の絶対下限**（12pxは本文で使用禁止） |
| **Kicker / バッジ** | `text-xs font-bold tracking-wider` | 12px / Bold | 章名バッジ、ステータスラベル |
| **Meta / Footer / Note** | `text-xs text-slate-400 font-mono` | 12px / Medium | 注記・出典・ページ番号（12px未満は使わない） |

> ⚠️ **文字数とフォントサイズの関係（Anti-Font-Shrink Rule）**:
> 「文字数が多すぎて枠に収まらないからフォントを小さくする」という縮小対応は禁止します。文字数を削って要約し（1スライド250〜350文字目安）、フォントサイズ（本文14px、見出し16〜18px）と余白を死守してください。
</typography_hierarchy>

---

<color_palette>
## 2. 推奨カラーパレット

単調な原色を避け、Slateをベースとした深みのあるカラーリングを採用します。

- **Slate (ベース・テキスト・背景)**:
  - `bg-slate-50`（スライド本文背景、カード背景）
  - `bg-slate-900 / 950`（表紙、ツールバー、重要スライド）
  - `text-slate-900`（主見出し）
  - `text-slate-600`（本文）
  - `text-slate-400`（メタ情報・補足）
- **Brand / Primary (Indigo / Violet)**:
  - `brand-600: #4f46e5`（アクセントライン、主要タグ、プライマリカード枠）
  - `brand-50: #eef2ff`（重要カードの背景ハイライト）
- **Accent (Sky / Cyan)**:
  - `accent-500: #0ea5e9`（グラデーション、サブアクセント）
- **Semantic (Status / Contrast)**:
  - `rose-600 / rose-50`: 課題・AS-IS・注意（✕アイコン）
  - `emerald-600 / emerald-50`: 解決策・TO-BE・達成（✓アイコン）
</color_palette>

---

<robust_box_model>
## 3. 堅牢なボックスモデル（文字崩れ防止ルール）

テキストの推敲によって文字数が2倍〜3倍に増減しても、**要素が重なったりスライド枠を突き抜けたりしない** ための鉄則です。

1. **スライド全体の縦構造**:
   ```html
   <section class="slide p-12 justify-between flex flex-col overflow-hidden relative">
     <!-- ヘッダー（固定） -->
     <div class="flex-shrink-0 border-b border-slate-200 pb-4">...</div>

     <!-- メインコンテンツ（伸縮可能） -->
     <div class="flex-1 min-h-0 flex flex-col justify-center my-auto">
       <div class="grid grid-cols-3 gap-6">...</div>
     </div>

     <!-- フッター（固定） -->
     <div class="flex-shrink-0 pt-3 border-t border-slate-200 flex justify-between">...</div>
   </section>
   ```
   - `flex-shrink-0`: ヘッダー・フッターがコンテンツに押しつぶされるのを防ぐ。
   - `flex-1 min-h-0`: メインコンテンツ領域がスライドの高さを超えないように自動収縮する。

2. **カード内部の構造**:
   ```html
   <div class="bg-white rounded-xl p-5 border border-slate-200 flex flex-col justify-between">
     <div>
       <!-- タイトル・本文 -->
     </div>
     <!-- カード内ボトム注記（固定位置に配置） -->
     <div class="mt-4 pt-3 border-t border-slate-100 text-xs font-medium">...</div>
   </div>
   ```
   - `flex flex-col justify-between` により、カード内の高さが揃い、下部の注記やマイルストーン情報が常に底面に整列します。
</robust_box_model>
</design_system_specs>
