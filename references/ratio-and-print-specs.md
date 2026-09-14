# スライド比率・印刷CSS仕様書 (Ratio & Print Specifications)

<ratio_and_print_specifications>
ブラウザ上での快適な閲覧・直接編集と、PDFエクスポート（印刷）時のピクセルパーフェクトな出力を両立するための厳格なCSS仕様です。

---

<aspect_ratio_dimensions>
## 1. アスペクト比ごとの寸法仕様

| アスペクト比 / 用紙サイズ | 用途・特徴 | 画面表示サイズ | 印刷 `@page size` | 印刷メディアクエリサイズ |
| :--- | :--- | :--- | :--- | :--- |
| **16:9**（デフォルト） | ワイド画面・モダンディスプレイ・Web投影 | `width: 1280px;`<br>`height: 720px;` | `@page { size: 16in 9in; margin: 0; }` | `.slide { width: 16in !important; height: 9in !important; }` |
| **4:3** | 既存資料踏襲・正方形ディスプレイ・学術発表 | `width: 1024px;`<br>`height: 768px;` | `@page { size: 4in 3in; margin: 0; }` | `.slide { width: 4in !important; height: 3in !important; }` |
| **A4 横 (Landscape)** | **印刷配布用スライド、役員稟議、提案企画書** | `width: 1188px;`<br>`height: 840px;` | `@page { size: A4 landscape; margin: 0; }` | `.slide { width: 297mm !important; height: 210mm !important; }` |
| **A4 縦 (Portrait)** | **1枚企画書、エグゼクティブサマリー、白書** | `width: 840px;`<br>`height: 1188px;` | `@page { size: A4 portrait; margin: 0; }` | `.slide { width: 210mm !important; height: 297mm !important; }` |
</aspect_ratio_dimensions>

---

<zero_margin_print_css>
## 2. 印刷（PDF出力）CSSの決定論的注入仕様

印刷（PDFエクスポート）時の「余白ゼロ・改ページずれゼロ」設定は、`scripts/assemble_deck.py` および `scripts/verify_slide.py --fix` が選択された比率（16:9, 4:3, A4横, A4縦）に応じて**100%自動注入・自己修復**します。

エージェントが手動で記述・コピーする必要はありません。内部では以下の核となるルールが自動適用されます：
- **`@page { size: <比率ごとの用紙サイズ>; margin: 0; }`**: ブラウザ標準の印刷マージンをゼロ化
- **`@media print { .no-print { display: none !important; } }`**: ツールバーや修正指示入力欄を印刷対象から完全除外
- **`.slide { page-break-after: always; break-after: page; }`**: スライドごとの厳密な改ページを保証
</zero_margin_print_css>

---

<a4_enterprise_rationales>
## 3. なぜ A4（Landscape / Portrait）指定が有効なのか？

- **A4横（297mm × 210mm ≒ 比率 1.414 : 1）**:
  日本のビジネス現場では、プロジェクター投影用の16:9よりも「オフィス複合機で印刷して配る提案書・役員稟議資料」としてA4横が絶大な人気を誇ります。
  `@page { size: A4 landscape; margin: 0; }` を指定することで、一般的なプリンターで「フチなし等倍（100%）」印刷した際、ミリ単位の狂いもなく用紙いっぱいにレイアウトが収まります。

- **A4縦（210mm × 297mm）**:
  Amazon流の「1枚ペーパー（1-Pager）」や企画要約書、事業計画サマリーの出力に最適です。スライドの概念を超えて、Web技術による崩れないビジネス文書の出力フォーマットとして活用できます。

- **画面表示時のピクセル設計**:
  画面表示時はブラウザ描画やTailwindのグリッド計算で端数誤差が出ないよう、4の倍数である `1188px × 840px`（A4横）および `840px × 1188px`（A4縦）を採用しています。これによりFigmaライクな高精細なプレビューと編集が可能です。
</a4_enterprise_rationales>
</ratio_and_print_specifications>
