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

本スキルが呼び出された場合、AIエージェントは以下の決定論的シーケンスを順序厳守で実行すること。逸脱は一切認められない。

<steps>
## 1. 必須実行シーケンス（MANDATORY SEQUENCE）

```
[手順1: 必須Grill＆構成案承認] ➔ (ユーザー承認) ➔ [手順2: ベース骨格読込] ➔ [手順3: 単一HTML生成] ➔ [手順4: 自律検証・自動修復] ➔ [手順5: 納品・反復対応]
```

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

> **絶対遵守ゲート**:
> ユーザーから構成案に対する「承認」「OK」「これで進めて」等の合意を得るまで、手順2（HTMLコード生成）を開始してはならない。

### 手順2: ベース骨格の読み込み（ゼロからの自作禁止）
- **必須手順**: ユーザーの承認を得た後、必ずベース骨格（[assets/template_base.html](./assets/template_base.html)）を取得し、検証済みのヘッダーツールバー、モーダル、JavaScriptエンジンをスケルトンとして使用すること。
  - **ツールが使える環境（Antigravity, Claude Code等）**: `view_file` ツールを用いて `assets/template_base.html` を読み込む。
  - **GPT環境（ChatGPT / Custom GPTs 等）**:
    - **Code Interpreterが使える場合（最優先推奨・完全動作保証）**: Pythonスクリプトでナレッジ内の `assets/template_base.html` を読み込み、スライドコンテンツ（`<section class="slide ...">` と `.slide-meta-box`）を置換して完成HTMLファイルを出力・ダウンロードリンクを提供する。
    - **チャット出力環境**: `template_base.html` の軽量化スクリプトを中略することなく出力する。
- 自社公式デザインが指定されている場合は、[assets/corporate_default.html](./assets/corporate_default.html) を参照すること。

### 手順3: 単一HTML（Single-File HTML）の生成規則
自己完結した単一のHTMLコードブロック（`<!DOCTYPE html>...</html>`）を生成する。
1. **編集機能のフェイルセーフ保証**: `<body class="... is-editable">`、`<section class="slide ... contenteditable="true">` を死守。`pointer-events: none` は禁止。
2. **固定ヘッダーツールバー維持**: `[📝 編集: ON]`, `[📋 指示をコピー]`, `[▶ 全画面発表]`, `[🖨 PDF保存]`。
3. **堅牢スライドボックス**: `<section class="slide ...">` とし固定幅・固定高・`overflow-hidden`。
4. **スライド共通骨格**: `[Kicker]` ➔ `【Lead Message】` ➔ `Main Content Body` ➔ `[Footer]`。
5. **メタ情報枠の 1:1 配置**: 各 `.slide` の直下に1つの `.slide-meta-box` を必ず配置。
6. **文字溢れの物理的抑止**: `<div class="ai-content">` と Tailwind `line-clamp` の活用。
7. **画像生成・完全Base64インライン化**: 外部画像参照(`src="./images/..."`)は完全禁止。AI生成画像や提供画像は必ずBase64 Data URI (`data:image/jpeg;base64,...`) にし、スライド枠比率と同期させてトリミングなしで配置。
8. **完全インラインSVG**: 外部JSライブラリを使用せず純粋なインライン `<svg>` でグラフ描画。
9. **言語の自動同期**: `lang="ja"` または `lang="en"` の設定。

### 手順4: 自律品質検証 ＆ 自動修復ループ（Self-Repair Loop）
- **Python実行が可能な環境の場合**:
  必ず `python3 scripts/verify_slide.py <スライドHTMLのパス>` を実行し、終了コードが 0 になるまで自律修正ループを回す。
- **Python実行ができない環境の場合（プレーンチャット等）**:
  セルフチェックのみ実施。**※重要: 実行できない環境で「テストを実行しました」などの架空の実行報告や捏造ログを出力してはならない。**
- **出力前自己検証チェックリスト（Anti-AI-Smell Reflection）**:
  - [ ] リード文検証（完全な1文・動詞結びか）
  - [ ] 解像度・動作内省（バズワードを具体アクションにリライトしたか）
  - [ ] 均等分割の回避（推奨案への視覚的アンカー）
  - [ ] 余白保護（テキスト上限厳守）

### 手順5: 成果物の提示 ＆ 反復推敲の処理
- 完成した完全なHTMLを出力する。
- 台本希望の場合は `speech_script.md` も出力。
- 反復フィードバック時は、指示のないスライドは100%維持し、指示箇所のみ改修すること。
</steps>

<rules>
## 2. 絶対禁止事項（STRICTLY FORBIDDEN）

1. **未承認でのコード生成開始の禁止**: 手順1のGrill完了前にHTMLを出力しないこと。
2. **実行不能環境での検証偽装・幻覚ログ捏造の禁止**: 実行できない環境で検証スクリプトの架空実行報告を行わないこと。
3. **画像のトリミング使い回し禁止**: 1スライドにつき1枚の画像を個別に生成し、CSSトリミングで使い回さないこと。
4. **ゼロからのHTML独自記述の禁止**: 必ず `template_base.html` をベースとすること。
5. **外部重量級JSライブラリの読み込み禁止**: Chart.js, Mermaid CDN等は使用不可。
6. **スライド内HTMLダウンロードボタンの再導入禁止**: ブラウザ内Blob保存ボタンは設置不可。
7. **スライド枠とメタボックスの 1:1 不一致の禁止**: 数を常に完全一致させること。
8. **余白ゼロ印刷CSSの破壊禁止**: トップレベル `@page` および `@media print` ブロックを改変・削除しないこと。
9. **テキスト許容量超過の禁止**: 横長700文字（推奨500~600）、A4縦1100文字（推奨850）を超えないこと。
10. **無意味な3均等カード化の禁止**: 推奨案には必ず視覚的アンカー（色枠等）を設定すること。
11. **抽象バズワード連呼の禁止**: 「シナジー」「推進」等を出力しないこと。
12. **飾りアイコン要求の禁止**: 文脈と無関係なアイコンを配置しないこと。
13. **名詞止め見出しのみの出力禁止**: 必ずAction Title（完全文）にすること。
14. **中途半端な単語分断改行の禁止**: 文節・意味の切れ目で `<br>` または幅調整を行い自然に改行すること。
15. **右肩バッジの折り返し ＆ ヘッダー下部余白ゼロの禁止**: バッジには `shrink-0 whitespace-nowrap` を付与し、ヘッダー下部には十分な余白(`mb-5`等)を設けること。
16. **外部画像ファイルパス・URL参照の禁止**: 画像は必ず Base64 Data URI で直接インライン埋め込みすること。
17. **静的編集属性の欠落禁止**: `<section class="slide ... contenteditable="true">` および `<body class="... is-editable">` を省略しないこと。
18. **`pointer-events: none` の適用禁止**: スライド要素へのマウスクリックやテキスト選択を完全遮断しないこと。
19. **Grill時の質問攻め・手抜き箇条書きの禁止**: 初回応答時に白紙の質問をしたり、名詞トピックだけの構成案を出さないこと。
</rules>

## 3. 用紙サイズ・アスペクト比 寸法仕様一覧

| 形式・サイズ | 主な用途・利用シーン | 画面表示クラス | 印刷用CSS `@page` |
| :--- | :--- | :--- | :--- |
| **16:9 ワイド** | Web会議プレゼン、PCディスプレイ投影 | `w-[1280px] h-[720px]` | `@page { size: 16in 9in; margin: 0; }` |
| **4:3 標準** | 従来型プロジェクター、学術発表 | `w-[1024px] h-[768px]` | `@page { size: 4in 3in; margin: 0; }` |
| **A4 横（Landscape）** | オフィス複合機での印刷配布資料、役員稟議・企画提案書 | `w-[1188px] h-[840px]` | `@page { size: A4 landscape; margin: 0; }` |
| **A4 縦（Portrait）** | Amazon流 1枚ペーパー（1-Pager）、エグゼクティブサマリー | `w-[840px] h-[1188px]` | `@page { size: A4 portrait; margin: 0; }` |

## 4. 詳細リファレンス（段階的開示: Progressive Disclosure）

必要に応じて以下のリファレンスを `view_file` で参照し、詳細な設計仕様を取得すること：

- [references/slide-patterns.md](./references/slide-patterns.md): スライド情報構造＆レイアウトパターン集
- [references/components-consulting.md](./references/components-consulting.md): 戦略コンサル型 示唆・高度コンポーネント集
- [references/data-visual-binding.md](./references/data-visual-binding.md): データ表からの直接ビジュアル化プロトコル
- [references/grill-workflow.md](./references/grill-workflow.md): Grill詳細フロー、構成提案書テンプレート
- [references/ratio-and-print-specs.md](./references/ratio-and-print-specs.md): 各比率の寸法計算、余白ゼロ印刷CSS
- [references/ai-concept-imagery.md](./references/ai-concept-imagery.md): 画像プロンプト構文
- [references/design-system.md](./references/design-system.md): タイポグラフィ階層、ボックスモデル
