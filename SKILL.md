---
name: ainativeslide
description: >-
  ユーザーがプレゼンテーションスライド、ピッチデック、企画書、提案書、稟議資料、1枚ペーパー（ワンページャー）、
  またはPDF印刷用HTMLスライドの作成・デザイン・修正・推敲を求めた際に必ず本スキル（AINativeSlide）を起動する。
  16:9ワイド、4:3標準、A4横（印刷・稟議用）、A4縦（企画書用）の全比率に対応し、単一HTML（Single-File HTML）、
  完全インラインSVGチャート、Python自動品質検証スクリプト（verify_slide.py）による自律修正ループを実行する。
  (Triggers: presentation slides, pitch deck, proposal, HTML slides, A4 landscape, 1-Pager)
---

# AINativeSlide エージェント実行仕様書（Agent Execution Contract）

<execution_contract>
本スキルが呼び出された場合、AIエージェントは以下の決定論的シーケンスを順序厳守で実行すること。逸脱は一切認められない。

---

<execution_sequence>
## 1. 必須実行シーケンス（MANDATORY SEQUENCE）

```
[手順1: 必須Grill＆構成案承認] ➔ (ユーザー承認) ➔ [手順2: ベース骨格読込] ➔ [手順3: 単一HTML生成] ➔ [手順4: 自律検証・自動修復] ➔ [手順5: 納品・反復対応]
```

<step id="1_grill">
### 手順1: 必須スマートGrill ＆ 構成案の事前承認（スキップ厳禁・必ず1往復実施）
**※いかに依頼文が詳細であっても、いきなりHTMLコード生成を開始してはならない。必ずユーザーと1往復の壁打ちを行い、構成案の承認を得てから生成を開始すること。**

- **必須事前読込（Mandatory Reading）**:
  初回応答をユーザーへ出力する前に、**必ず `view_file` ツールを用いて [references/grill-workflow.md](./references/grill-workflow.md) を読み込み**、そこに定義された確定Markdownテンプレート（スライド構成提案書）の枠組みを100%遵守して出力すること。

- **質問攻めの絶対禁止 ＆ 仮説構築型プロポーザル（Zero-Question Principle）**:
  「何枚にしますか？」「どのような目的ですか？」「サイズはどうしますか？」といった、ユーザーに思考コストを丸投げする白紙の質問（オープンクエスチョン）を**厳禁**とする。
  ユーザーからの依頼文がたとえ1行（例:「新規事業ピッチのスライドを作って」）であっても、AI自身がプロの戦略コンサルタント・デザイナーとしてプロアクティブに仮説を立て、**タイトル・目的・推奨比率・全スライド構成（4〜6枚程度）・推奨画像テイスト・台本要否の全スロットを完全に埋めた提案書**を一発で提示すること。

- **スライドごとの「3層構造」の徹底**:
  各スライドの構成案は、単なる名詞トピック（例:「1. 課題, 2. 解決策」）で済ませてはならない。必ず以下の3要素を明示すること：
  1. `Slide X 【直感的な日本語パターン名】`（英語対話時は英語パターン名）
     - 4枚以上の複数スライドでは、表紙直後に**【エグゼクティブサマリ】**と**【目次（アジェンダ）】**を標準配置する。
     - 日本語対話時は開発用英語ID（`tradeoff_matrix` 等）を出さず、【課題・打ち手型】【トレードオフ比較表】【ステップ・時系列フロー】【要因分解・ウォーターフォール】【全体像・階層マッピング】【境界線・NG/OK対比】等の直感的な日本語名を使用する。
  2. `- 【Lead Message】40〜60文字・ファクト＋結論・動詞結びの完全な1文`（名詞止め見出しは厳禁）
  3. `- 構造意図: 左右対比 / 3案比較（★Gate）/ 階層マッピング 等の具体的配置`

- **データ直接ビジュアル化プロトコル（Data-to-Visual Binding）**:
  ユーザーからCSV、TSV、Markdown表、数値データが提示された場合は、手動再入力を求めず、自動で差分・CAGRを計算してウォーターフォール、マリメッコ、または比較表へ直接バインドして構成案を提示すること（詳細: [references/data-visual-binding.md](./references/data-visual-binding.md)）。

- **回答コスト最小化と1行承認誘導CTA**:
  提案書の末尾には必ず標準CTA（Call to Action）を付与し、ユーザーが「OK」「承認」と1単語送るだけで最適な推奨値（A/B）で即座に制作へ移行できるようにする。

<approval_gate>
> **絶対遵守ゲート**:
> ユーザーから構成案に対する「承認」「OK」「これで進めて」等の合意を得るまで、手順2（HTMLコード生成）を開始してはならない。
</approval_gate>
</step>

<step id="2_skeleton">
### 手順2: ベース骨格の読み込み（ゼロからの自作禁止）
- **必須手順**: ユーザーの承認を得た後、必ずベース骨格（[assets/template_base.html](./assets/template_base.html)）を取得し、検証済みのヘッダーツールバー、モーダル、JavaScriptエンジンをスケルトンとして使用すること。
  - **ツールが使える環境（Antigravity, Claude Code等）**: `view_file` ツールを用いて `assets/template_base.html` を読み込む。
  - **CLI / Python実行環境（Antigravity, Cursor, Claude Code, Code Interpreter等 - 最優先推奨）**:
    - **決定論的合体パイプライン（Token節約 & 100%完全動作保証）**: LLMはスライドコンテンツの断片（`<section class="slide ...">...</section>`）のHTML出力に集中し、全体の骨格・メタボックス・番号再計算・印刷CSSの統合は `scripts/assemble_deck.py` で決定論的に処理する。
  - **プレーンチャット環境（ChatGPT Enterprise, Claude Web等）**:
    - `template_base.html` の軽量化スクリプト（約210行）を中略（`// ...` 等）することなく、完全な単一コードブロックとして出力する。
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
7. **スライド枠とメタボックスの 1:1 不一致の禁止**: `.slide` の数と `.slide-meta-box` の数は常に完全一致させること。
8. **余白ゼロ印刷CSSの破壊禁止**: 以下の印刷用CSSブロック（トップレベル `@page` および `@media print`）を改変・削除してはならない：
   ```css
   @page {
     size: 16in 9in; /* 比率に応じて 4in 3in / A4 landscape / A4 portrait */
     margin: 0;
   }
   @media print {
     body { background: transparent !important; margin: 0 !important; padding: 0 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
     .no-print { display: none !important; }
     .slide-viewport { padding: 0 !important; gap: 0 !important; display: block !important; }
     .slide {
       width: 16in !important; height: 9in !important; max-width: none !important; max-height: none !important;
       page-break-after: always !important; break-after: page !important;
       page-break-inside: avoid !important; break-inside: avoid !important;
       margin: 0 auto !important; border-radius: 0 !important; box-shadow: none !important; border: none !important;
     }
   }
   ```
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
19. **Grill時の質問攻め・手抜き名詞トピック箇条書きの禁止**: ユーザーに白紙のオープンクエスチョンを投げ返したり（丸投げ質問）、スライド構成案を単なる名詞トピックの箇条書き（例:「1. 課題, 2. 解決策」）で済ませてはならない。初回応答前に必ず [references/grill-workflow.md](./references/grill-workflow.md) を読み込み、仮説構築型で全スロットを埋めた確定Markdownテンプレート（3層構造：日本語パターン名・40〜60字の完全文Action Title・構造意図）を出力すること。
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

