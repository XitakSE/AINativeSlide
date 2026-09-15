---
name: ainativeslide
description: >-
  承認済みのスライド構成仕様（deck_manifest.json または確定構成案）とテーマ設定（themes/theme.json）を受け取り、
  Single-File HTMLプレゼンテーションスライドの生成、完全インラインSVGチャート描画、
  およびPython自動品質検証スクリプト（verify_slide.py）による自律修正ループを実行する実装・ビルドエンジン。
  16:9ワイド、4:3標準、A4横（印刷・稟議用）、A4縦（企画書用）の全比率に対応。
  (Triggers: build slides, generate HTML slides, deck_manifest.json, スライド生成, スライドHTML出力)
---

# AINativeSlide エージェント実行仕様書（Agent Execution Contract）

<execution_contract>
本スキルは、スライド制作における **「Single-File HTML合成・インラインSVG描画・自律品質検証（verify_slide.py）」に特化した実装エンジン** です。
確定したスライド構成仕様書（`deck_manifest.json`）およびテーマ定義（`themes/theme.json`）を入力とし、決定論的スクリプトを用いて完全動作する高品質スライドを出力します。

---

<execution_sequence>
## 1. 必須実行シーケンス（MANDATORY SEQUENCE）

```
[入力: deck_manifest.json ＆ theme.json] ➔ [手順1: 仕様受付（※未指定時のみ簡易Grill）] ➔ [手順2: ベース骨格読込] ➔ [手順3: 単一HTML生成] ➔ [手順4: 自律検証・自動修復] ➔ [手順5: 納品・反復対応]
```

<step id="1_manifest_input">
### 手順1: スライド構成仕様（`deck_manifest.json`）の受付 ＆ フォールバック
本スキルは、確定したスライド構成仕様（`deck_manifest.json`）およびデザイントークン（`themes/theme.json`）を入力として受け取り、決定論的にHTMLを実装・ビルドするエンジンである。

- **正規ルート（マニフェスト指定時・推奨）**:
  `deck_manifest.json`（または企画スキル `@ainativeslide-planner` で合意済みの構成案）が提供されている場合、**Grill等の対話を挟まず、直ちに手順2（ベース骨格読込）および手順3（HTML生成）へ進むこと**。
- **フォールバック（マニフェスト未指定の直接依頼時のみ）**:
  ユーザーから構成案なしで直接「スライドを作って」と依頼された場合のみ、いきなりコードを出力せず、仮説構築型でタイトル・比率・全スライド構成（パターン・Action Title）を提示し、ユーザーの「OK」承認を得てから生成へ移行すること（詳細仕様: [references/grill-workflow.md](./references/grill-workflow.md)）。
</step>

<step id="2_skeleton">
### 手順2: ベース骨格の読み込み（ゼロからの自作禁止）
- **環境に応じたアプローチ**:
  - **CLI / Python実行環境（最優先推奨・Token節約 & 完全動作保証）**: LLMが `template_base.html` を読み込む必要はない。LLMはスライド断片（`<section class="slide ...">...</section>`）のHTML出力に専念し、全体の骨格・メタボックス・番号再計算・印刷CSSの統合は `scripts/assemble_deck.py` で決定論的に処理する。
  - **プレーンチャット環境（ChatGPT Enterprise, Claude Web等）**: `view_file` またはプロンプト参照で `template_base.html` をベースとし、中略（`// ...` 等）することなく完全な単一コードブロックとして出力する。
- 自社公式デザイン（CIカラー・ロゴ枠）が指定されている場合は、[assets/corporate_default.html](./assets/corporate_default.html) を参照すること。
</step>

<step id="3_single_file_html">
### 手順3: 単一HTML（Single-File HTML）の生成規則

#### 方式A: 決定論的Pythonスクリプトによる合成（CLI/Python実行環境向け・推奨）
1. スライド要素群（各スライドの `<section class="slide ...">...</section>`）のみをファイルまたは標準入力に記述。
2. 以下の合体スクリプトを実行し、完全なSingle-File HTMLを自動生成する：
   ```bash
   python3 scripts/assemble_deck.py <スライド断片ファイル> --title "<スライドタイトル>" -r 16:9 -o deck.html
   ```
   - スライド番号の再計算（`01 / 05`, `02 / 05`...）、メタ情報ボックス（`.slide-meta-box`）の1:1注入、印刷用 `@page` CSSの同期、ヘッダータイトルの同期が決定論的に実行され、末尾で自動品質検証（`verify_slide.py`）まで一括実行される。

#### 方式B: 単一HTMLの手動/プロンプト生成（プレーンチャット環境向けフォールバック）
自己完結した単一のHTMLコードブロック（`<!DOCTYPE html>...</html>`）を生成する。以下の規約を厳守すること：

<generation_rules>
1. **編集機能のフェイルセーフ保証（Fail-safe Editability）**:
   - `<body class="... is-editable">`: `body` タグには必ず初期クラスとして `is-editable` を含め、ロード直後から即座に編集可能状態にする。
   - `<section class="slide ... contenteditable="true">`: 全スライド要素に静的に `contenteditable="true"` を必ず付与する。これによりJavaScriptが万が一遅延・停止してもブラウザネイティブで即座にテキスト編集できる安全網を死守する。
   - `pointer-events: none` の禁止: CSSにおいてスライド要素（`main .slide`）へのマウス操作・クリックを遮断する `pointer-events: none` を記述してはならない。
2. **固定ヘッダーツールバー**: `[📝 編集: ON]`, `[📋 指示をコピー]`, `[▶ 全画面発表]`, `[🖨 PDF保存]` の4ボタン構造をそのまま維持する。
3. **堅牢スライドボックス**: 全スライド要素は `<section class="slide ...">` とし、固定幅・固定高・`overflow-hidden` を付与する。
4. **スライド共通骨格（Base Anatomy）の厳守**:
   - `[Kicker / Category]`（任意: カテゴリ・章名）
   - `【Lead Message】` 1スライド1主張を体現する完全な結論文（Action Title: 40〜60文字・動詞結び）
   - `Main Content Body`（パターン別のワイヤーフレーム・`flex-1 min-h-0`）
   - `[Footer / Note]` 補足注記、データソース、前提条件、スライド番号
5. **メタ情報枠の 1:1 配置**: すべての `<section class="slide ...">` の直下に、同番の `<div class="slide-meta-box no-print ...">` を必ず1つ対で配置する。
6. **文字溢れの物理的抑止**: 本文コンテンツは `<div class="ai-content">` で囲み、見出し（`h2`, `h3`）、段落（`p`）、箇条書き（`ul`, `li`）を使用する。Tailwindの `line-clamp` により枠外突き抜けを完全に遮断する。
7. **画像生成・配置の厳格ルール（完全Base64インライン化 ＆ Zero-Cropping）**:
   - 画像を配置する場合、**必ず1スライドにつき1枚ずつ専用プロンプトで個別に生成し、スライド枠のアスペクト比（16:9等）と完全同期させてトリミングなし（Zero-Cropping）で配置すること**（1枚の画像をCSSトリミングして使い回す手抜きは厳禁）。
   - **完全単一ファイル完結（Single-File Complete Architecture）の死守**: 外部画像フォルダ（`./images/...` や `./demo_assets/...`）や外部CDN URLへの参照は一切禁止する。AIが生成した画像やユーザー提供画像は、**必ず Base64 Data URI（`data:image/jpeg;base64,...` または `data:image/png;base64,...`）に変換して `<img src="...">` に直接インライン埋め込みすること**。これにより、HTMLファイル単体のみをダウンロード・共有・オフライン閲覧しても画像リンク切れ（404）が絶対に発生しない完全なポータビリティを保証する。
   - ※ユーザーから素材画像が提供された場合も、同様にBase64エンコードしてインライン埋め込むこと。
8. **完全インラインSVG**: グラフやチャートは外部JSライブラリ（Chart.js等）をロードせず、純粋なインライン `<svg>` で描画する。
9. **言語の自動同期**: 依頼文が日本語の場合は `<html lang="ja">`、英語の場合は `<html lang="en">` を設定する。テンプレート内のJSがヘッダー文言やプレースホルダーを自動的に完全同期する。
</generation_rules>
</step>

<step id="4_verification_repair">
### 手順4: 自律品質検証 ＆ 自動修復ループ（Self-Repair Loop）
HTMLコードをユーザーに提示する前に、環境に応じた品質チェックを実施すること：

- **Python / CLI実行が可能な環境の場合（Antigravity, Cursor, Claude Code, Code Interpreter等）**:
  検証スクリプトを実行して静的テストを実施する：
  ```bash
  python3 scripts/verify_slide.py <スライドHTMLのパス>
  ```
  - **終了コード 0 の場合**: テスト合格。手順5へ進む。
  - **終了コード 1 の場合**:
    1. まず自動修復フラグ `--fix` を付けて実行する：
       ```bash
       python3 scripts/verify_slide.py <スライドHTMLのパス> --fix
       ```
       スライド番号、メタボックスの対配置、印刷用 `@page` CSS、ヘッダー総数表示、`is-editable` クラスが自動修復され、ファイルに保存された上で再検証される。
    2. テキスト文字数超過やAnti-AI-Smell警告、CSSリスクなど、LLMによるリライトが必要な残存エラーがある場合は、エラー指示に従って該当スライドのコンテンツを修正し、コード0になるまで検証する。
- **Python / CLI実行ができない環境の場合（プレーンチャット等）**:
  スクリプトの実行は行わず、自律的なコード内セルフチェック（スライド数とメタボックス数の1:1一致、ページ番号整合性、文字数・はみ出し確認）を実施する。
  **※重要（幻覚予防）**: スクリプトを実行できない環境であるにもかかわらず、「スクリプトを実行しました」「テストに合格しました」といった架空のコマンド実行報告や捏造ログを出力してはならない（実行できないなら単に実行しない）。

<reflection_checklist>
- **全環境共通: 出力前自己検証チェックリスト（AI自律セマンティック内省: Anti-AI-Smell Reflection）**:
  ※エンタープライズ環境（ChatGPT Enterprise, Claude for Work等）ではIDEや外部APIは使用できません。エージェント自身がスライド出力直前に「雰囲気・解像度」を内省してください（詳細規範・リライト指針は [references/slide-patterns.md §1](./references/slide-patterns.md#1-エージェント行動規範anti-ai-smell-guardrails) 参照）：
  - [ ] **リード文検証**: 動詞で終わる完全な1文（40〜60字のAction Title）か？（名詞止め見出し禁止）
  - [ ] **解像度・動作内省**: 「シナジー」「推進」等の空虚語を、現場の具体的物理動作や定量数値にリライトしたか？
  - [ ] **均等分割の回避**: 3列以上の構成で、推奨案や重要カードに視覚的アンカー（色枠・バッジ）を設定したか？
  - [ ] **余白保護**: テキスト過密を回避したか？（1スライド200〜300字推奨、上限700字厳守）
  - [ ] **不要装飾排除**: 文脈と無関係な飾りアイコン（ロケット、電球等）を排除したか？
</reflection_checklist>
</step>

<step id="5_delivery_iteration">
### 手順5: 成果物の提示 ＆ 反復推敲の処理
- 完成した完全なHTMLを、単一のコードブロック（```html ... ```）で出力する。
- 手順1で台本生成を希望された場合は、[assets/speech_script_example.md](./assets/speech_script_example.md) に準拠した台本文書（`speech_script.md`）を併せて出力する。
- **ユーザーからの反復フィードバック対応**:
  - ユーザーが「📋 指示をコピー」から修正要望テキストを貼り付けて指示してきた場合、指示のないスライドはユーザーによる推敲内容を100%維持し、指示のあったスライドのみを的確に改修すること。
</step>
</execution_sequence>

---

<strictly_forbidden>
## 2. 絶対禁止事項（STRICTLY FORBIDDEN）

1. **未承認でのコード生成開始の禁止**: 手順1のGrillで構成案・画像プロンプトを提示し、ユーザーの承認を得る前にHTMLコードを出力してはならない。
2. **実行不能環境での検証偽装・幻覚ログ捏造の禁止（幻覚予防）**: CLI/Pythonを実行できない環境において、「テストを実行し全合格しました」「verify_slide.py を実行しました」などの架空の実行報告や、偽のターミナル出力ログを捏造してはならない。実行できない環境ではスクリプトを実行せずセルフチェックのみで納品すること。
3. **画像のトリミング使い回し禁止**: 1枚の生成画像をCSSトリミングして複数スライドに使い回してはならない。画像枠のあるスライドには、必ず1スライドにつき1枚ずつ個別に画像を生成し、トリミングなしで使用すること（ユーザー提供画像を除く）。
4. **ゼロからのHTML独自記述の禁止**: 必ず [assets/template_base.html](./assets/template_base.html) を複製・ベースとすること。
5. **外部重量級JSライブラリの読み込み禁止**: Chart.js, D3, Reveal.js, Mermaid CDN, React, Vue 等を勝手に読み込んではならない。
6. **スライド内HTMLダウンロードボタンの再導入禁止**: `downloadHtmlWithComments` などのブラウザ内Blob保存ボタンを設置してはならない（AI環境自体の保存機能および「指示をコピー」に集約済み）。
7. **スライド枠とメタボックスの 1:1 不一致の禁止**: `.slide` の数と `.slide-meta-box` の数は常に完全一致させること（CLI環境では `scripts/assemble_deck.py` が100%自動対配置し、`scripts/verify_slide.py --fix` が自動修復）。
8. **余白ゼロ印刷CSSの改変・破壊の禁止**: トップレベル `@page { margin: 0; }` および `@media print` の余白ゼロ・改ページ設定を削除・改変してはならない（CLI環境では `scripts/assemble_deck.py` が比率に合わせて自動注入し、`scripts/verify_slide.py --fix` が自動修復）。
9. **テキスト許容量超過の禁止**: 横長スライドでは推奨目安500〜600文字・絶対上限700文字（A4縦の場合は推奨目安約850文字・絶対上限1,100文字）を超えてはならない（`scripts/verify_slide.py` の警告・エラー判定基準と完全連動）。
10. **無意味な3均等カード化の禁止 (Anti-AI-Smell)**: 3つ並ぶブロックの幅・文字量・強調度を均等にしてはならない。必ず推奨案や重要カードに視覚的アンカーを設定すること（詳細: [slide-patterns.md §1.1](./references/slide-patterns.md#11-禁止事項do-not)）。
11. **抽象バズワード連呼の禁止 (Anti-AI-Smell)**: 「シナジー」「推進」等、具体的動作が想起できない空虚な語彙を出力してはならない（詳細: [slide-patterns.md §1.1](./references/slide-patterns.md#11-禁止事項do-not)）。
12. **飾りアイコン要求の禁止 (Anti-AI-Smell)**: 文脈と無関係な汎用装飾アイコン（ロケット、電球等）を配置してはならない（詳細: [slide-patterns.md §1.1](./references/slide-patterns.md#11-禁止事項do-not)）。
13. **トピックタイトル（名詞止め見出し）のみの出力禁止 (Anti-AI-Smell)**: 「〇〇について」等の名詞ラベルのみをスライド見出しにしてはならない。必ず完全文（Action Title）を出力すること（詳細: [slide-patterns.md §1.1](./references/slide-patterns.md#11-禁止事項do-not)）。
14. **中途半端な単語分断改行の禁止 (Anti-AI-Smell / Semantic Line Breaking)**: コンテナ端に到達した成り行きで単語の途中や助詞で1〜2文字だけ次行に落ちる改行を厳禁とする。見出しや本文では文節・意味の切れ目で明示的に `<br>` を挿入するか幅・文字サイズを調整して自然なリズムで改行すること（詳細: [slide-patterns.md §1.1](./references/slide-patterns.md#11-禁止事項do-not)）。
15. **右肩バッジの折り返し ＆ ヘッダー下部余白ゼロの禁止 (Header Spacing & Badge Protection)**: 見出しが2行化した際、右肩バッジが押しつぶされて複数行に分断されてはならない（必ず `shrink-0 whitespace-nowrap` を付与し、ヘッダーは `items-start gap-6` 構造とすること）。また、見出しとメインコンテンツが密着して余白がゼロにならないよう、必ずヘッダー下部に十分な余白（`mb-5`〜`mb-6`）および視覚的境界線（`pb-3 border-b border-slate-800` 等）を設けること（詳細: [slide-patterns.md §1.1](./references/slide-patterns.md#11-禁止事項do-not)）。
16. **外部画像ファイルパス・URL参照の禁止 (Single-File純度の死守)**: `<img src="./images/..." >` や `<img src="https://..." >` などの外部パス参照を行ってはならない。画像は必ず Base64 Data URI（`data:image/jpeg;base64,...` または `data:image/png;base64,...`）として HTML 内に直接インライン埋め込みし、HTMLファイル単体での完全動作を死守すること。
17. **スライドへの `contenteditable="true"` および `body` への `is-editable` 欠落の禁止 (Fail-safe Editability)**: スライドへの静的編集属性付与（`<section class="slide ... contenteditable="true">`）や初期クラス（`<body class="... is-editable">`）を省略してはならない。万が一スクリプトが停止しても、ブラウザ標準機能による直接編集を常に担保すること。
18. **スライド全域への `pointer-events: none` 适用の禁止**: スライド要素へのマウスクリックやテキスト選択を完全遮断するような CSS（`pointer-events: none`）をスライドや body に適用してはならない。
19. **マニフェスト未指定時の白紙質問攻め禁止 (Fallback Grill Rule)**: マニフェスト未指定で直接作成を求められた場合、ユーザーに白紙のオープンクエスチョンを投げ返してはならない。必ず仮説構築型で全スロットを埋めた提案書を提示し、承認を得てから生成へ移行すること。
</strictly_forbidden>

---

<dimension_specifications>
## 3. 用紙サイズ・アスペクト比 寸法仕様一覧

| 形式・サイズ | 主な用途・利用シーン | 画面表示クラス | 印刷用CSS `@page` |
| :--- | :--- | :--- | :--- |
| **16:9 ワイド** | Web会議プレゼン、PCディスプレイ投影 | `w-[1280px] h-[720px]` | `@page { size: 16in 9in; margin: 0; }` |
| **4:3 標準** | 従来型プロジェクター、学術発表 | `w-[1024px] h-[768px]` | `@page { size: 4in 3in; margin: 0; }` |
| **A4 横（Landscape）** | オフィス複合機での印刷配布資料、役員稟議・企画提案書 | `w-[1188px] h-[840px]` | `@page { size: A4 landscape; margin: 0; }` |
| **A4 縦（Portrait）** | Amazon流 1枚ペーパー（1-Pager）、エグゼクティブサマリー | `w-[840px] h-[1188px]` | `@page { size: A4 portrait; margin: 0; }` |
</dimension_specifications>

---

<progressive_disclosure_references>
## 4. 詳細リファレンス（段階的開示: Progressive Disclosure）

必要に応じて以下のリファレンスを `view_file` で参照し、詳細な設計仕様を取得すること：

- [references/slide-patterns.md](./references/slide-patterns.md): スライド情報構造＆レイアウトパターン集（Anti-AI-Smell ガードレール、Base Anatomy、Deck全体骨格、厳選6大パターン、JSON Schema）
- [references/components-consulting.md](./references/components-consulting.md): 戦略コンサル型 示唆・高度コンポーネント集（差分矢印、ハーベイボール、章トラッカー、実績/予測境界線、軸ブレイク、マリメッコ、ガント）
- [references/data-visual-binding.md](./references/data-visual-binding.md): データ表（CSV/Markdown）からの直接ビジュアル化プロトコル（決定論的パターン変換マトリクス）
- [references/grill-workflow.md](./references/grill-workflow.md): Grill詳細フロー、構成提案書テンプレート、台本文書仕様
- [references/ratio-and-print-specs.md](./references/ratio-and-print-specs.md): 各比率の寸法計算、余白ゼロ印刷CSS、解像度換算
- [references/ai-concept-imagery.md](./references/ai-concept-imagery.md): 4大テイスト別プロンプト構文、D&D差し替えJS仕様
- [references/design-system.md](./references/design-system.md): タイポグラフィ階層、堅牢ボックスモデル、カラーパレット
</progressive_disclosure_references>
</execution_contract>

