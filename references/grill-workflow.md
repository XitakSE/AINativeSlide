# Grill フレームワーク（認知ドリフト防止 ＆ 事前構成提案プロトコル）

ユーザーからの曖昧な指示や前提の相違による「手戻り（認知ドリフト）」を未然に防ぎ、1往復の対話で手戻りなく高品質なスライドを完成させるための事前合意（Grill）プロトコルです。

---

## 1. Grill の5大基本原則

### 1. いきなりコードを出力しない（スキップ厳禁）
ユーザーから「〇〇のスライドを作って」と依頼された場合、依頼文にいかに詳細な情報が含まれていても、**直ちにHTMLコード生成を開始してはならない**。
必ずユーザーと **1往復の壁打ち（Grill）** を行い、スライドタイトル、概要、全スライド構成、AI画像プロンプト、台本要否を整理した「スライド構成提案書」を提示して承認を得る。

### 2. 質問攻めの絶対禁止 ＆ 仮説構築型プロポーザル（Zero-Question Principle）
- **ユーザーに白紙の質問を投げ返してはならない**:
  「タイトルは何にしますか？」「何枚にしますか？」「どのような構成にしますか？」といった、ユーザーに思考コストを丸投げするオープンクエスチョン（質問攻め）は**厳禁**とする。
- **仮説構築型でスロットを全埋めして提示する**:
  ユーザーからの指示がたとえ1行（例:「次世代データ基盤の提案スライドを作って」）であっても、AI自身がプロの戦略コンサルタント・デザイナーとしてプロアクティブに仮説を立て、**タイトル・目的・推奨サイズ・全スライド構成（4〜6枚程度）・推奨画像テイスト・台本要否の全スロットを完全に埋めた提案書**を一発で出力すること。

### 3. スライドごとの「3層構造（パターン・Action Title・構造意図）」の強制
構成案の各スライドは、単なる名詞トピック（例:「1. 課題, 2. 解決策」）で済ませてはならない。必ず以下の3層で提示すること：
1. `Slide X 【直感的な日本語パターン名】`（英語対話時は英語パターン名）
2. `- 【Lead Message】40〜60文字・ファクト＋結論・動詞結びの完全な1文`（名詞止め見出しは厳禁）
3. `- 構造意図: 左右対比 / 3案比較（★Gate）/ 階層マッピング 等の具体的配置`

### 4. 4枚以上のデッキにおける「エグゼクティブサマリ・目次」の原則標準配置（Default: ON）
4枚以上のスライド構成案では、表紙の直後に必ず**【エグゼクティブサマリ】**と**【目次（アジェンダ）】**を標準配置する。
（※1枚ペーパー、またはユーザーから明示的な「目次不要」等の拒否指示があった場合を除く）

### 5. 回答コスト最小化と承認ゲート（1行承認CTA）
提案書の末尾には必ず標準CTA（Call to Action）を配置し、ユーザーが**「OK」「承認」と1単語送るだけで最適な推奨値（A/B）で即座に制作へ移行できる**ようにする。

---

## 2. 厳格出力フォーマット（スライド構成提案書テンプレート）

初回応答では、**以下のMarkdownテンプレート構造を一文字も崩さず、全スロットを仮説で埋めて出力すること**（要約・省略・自由書式への変更は厳禁）：

### 【日本語対話時: 確定Markdown出力テンプレート】

```markdown
スライドの完成度を高め、手戻りを防ぐために以下のスライド構成案を作成しました。
ご確認いただき、承認（または修正指示）をお願いいたします。

### 1. スライドタイトル & 概要
- **タイトル**: [仮説構築した具体的タイトル（例: 全社次世代データ基盤刷新構想）]
- **目的・ターゲット**: [役員決裁 / 顧客提案 / 現場共有 / 稟議・配布用]
- **全体メッセージ**: [資料全体を通じてオーディエンスに合意・意思決定させたい核心（30〜50文字）]

### 2. アスペクト比・用紙サイズ
- [A] **16:9 ワイド（推奨）**: 画面投影・Web会議標準 (`w-[1280px] h-[720px]`)
- [B] **4:3 標準**: 従来型プロジェクター・学術発表 (`w-[1024px] h-[768px]`)
- [C] **A4 横（Landscape）**: オフィス複合機での印刷配布資料、役員稟議資料 (`w-[1188px] h-[840px]`)
- [D] **A4 縦（Portrait）**: 1枚企画書、エグゼクティブサマリー (`w-[840px] h-[1188px]`)

### 3. 全スライド構成案（情報構造パターン ＆ Action Title）
- **Slide 1 【表紙】**: [タイトル・起案部門・日付・機密区分]
- **Slide 2 【エグゼクティブサマリ】**:
  - 【Lead Message】[核心・課題・施策・ROI・体制を1枚で総括する40〜60文字の動詞結び完全文]
  - 構造意図: 左に主要指標・右に4行スプリット（論点と結論）で意思決定に必要な全情報を俯瞰
- **Slide 3 【目次（アジェンダ）】**:
  - 【Lead Message】[議論の全体像と論点ステップを提示する完全文]
  - 構造意図: 3〜4章のアジェンダカードと現在地トラッカーの明示
- **Slide 4 【課題・打ち手型】**:
  - 【Lead Message】[現場ペインと抜本的打ち手を対比する40〜60文字の動詞結び完全文]
  - 構造意図: 左（現場課題・根本原因）vs 右（具体的施策・定量的成果）のコントラスト対比
- **Slide 5 【トレードオフ比較表】**:
  - 【Lead Message】[複数案の比較と推奨案の採用論拠を示す40〜60文字の動詞結び完全文]
  - 構造意図: 評価軸（コスト・期間・保守・拡張）による3案比較＋推奨案のハイライト（● ◕ ◐ ◔ ○）
- **Slide 6 【ステップ・時系列フロー】**:
  - 【Lead Message】[移行手順と品質関門を定義する40〜60文字の動詞結び完全文]
  - 構造意図: 4段階の時系列フェーズ（STEP 1〜4）と絶対通過関門（★Gate）の可視化
- **Slide 7 【まとめ/Next Step】**:
  - 【Lead Message】[承認後の直近マイルストーンと決定事項を促す完全文]
  - 構造意図: 直近1ヶ月の具体的アクション、担当部門、承認事項のチェックリスト

### 4. AI生成画像の要否 & スタイル（テイスト）選択
- [A] **画像不要（CSS表現・推奨）**: すべてCSSグリッド・カード・アイコン・インラインSVG図解で表現
- [B] **リアル・シネマティック系**: 高精細な実写・スタジオ照明風（重厚感・役員ピッチ向け）
- [C] **漫画・コミック・アニメ系**: 親しみやすい線画・ストーリー調（社内研修・現場改善向け）
- [D] **3D立体アイコン・アイソメトリック系**: 洗練された等角3Dモデル（システム構成・データ統合向け）
- [E] **フラットベクターイラスト系**: Notion/SaaS風の洗練されたミニマル2D（サービス紹介・企画書向け）
※画像を採用する場合、スライドごとに枠比率と完全同期した専用プロンプトで個別生成（トリミングなし・Base64インライン埋め込み）

### 5. 発表用台本文書（Markdown: `speech_script.md`）の同時生成
- [A] **不要**: スライドHTMLのみ生成
- [B] **【推奨】希望する**: 各スライドの想定時間・要点・トーク原稿をまとめた台本文書をセット出力

---
👉 **この構成案でよろしければ「承認」または「OK」とご返信ください。**
（※比率やデザインの変更がある場合は「2-C、4-Dで」のように記号でお知らせください。承認をいただき次第、スライドHTMLの生成を開始します）
```

---

### 【英語対話時: 確定Markdown出力テンプレート】

英語での対話時は、日本語を一切含めず以下の英語確定テンプレートを使用すること：

```markdown
To ensure full alignment and eliminate cognitive drift, here is the proposed slide deck architecture.
Please review and confirm to proceed with HTML generation.

### 1. Deck Title & Overview
- **Title**: [Hypothesis-driven Title]
- **Target Audience & Purpose**: [Executive Decision / Client Proposal / Internal Training]
- **Core Takeaway**: [Single decisive insight in 1 sentence]

### 2. Aspect Ratio & Dimensions
- [A] **16:9 Widescreen (Recommended)**: Web conferencing standard (`w-[1280px] h-[720px]`)
- [B] **4:3 Standard**: Legacy projectors (`w-[1024px] h-[768px]`)
- [C] **A4 Landscape**: Print hand-outs & executive proposals (`w-[1188px] h-[840px]`)
- [D] **A4 Portrait**: 1-Pager brief & executive summary (`w-[840px] h-[1188px]`)

### 3. Slide Deck Outline (Information Architecture & Action Titles)
- **Slide 1 [Cover]**: Title, subtitle, department, date, confidentiality
- **Slide 2 [Executive Summary]**:
  - [Lead Message] [Decisive action title ending in active verb (15–25 words)]
  - Architecture: 4-row horizontal split summarizing Problem, Solution, ROI, and Governance
- **Slide 3 [Agenda]**:
  - [Lead Message] [Action title introducing the narrative chapters]
  - Architecture: Chapter cards with highlighted current position
- **Slide 4 [Problem & Solution]**:
  - [Lead Message] [Action title contrasting the pain point with measurable remedy]
  - Architecture: 2-column split (Pain/Root Cause vs. Concrete Solution & Impact)
- **Slide 5 [Comparison Matrix]**:
  - [Lead Message] [Action title declaring the winning proposal with trade-off rationale]
  - Architecture: Multi-criteria comparison table with Harvey Balls (● ◕ ◐ ◔ ○) and highlighted anchor card
- **Slide 6 [Sequential Workflow]**:
  - [Lead Message] [Action title defining the phase gates and execution checkpoints]
  - Architecture: 4-step linear timeline with critical quality gates (★Gate)
- **Slide 7 [Conclusion & Next Steps]**:
  - [Lead Message] [Action title prompting immediate decision and Day-1 milestones]
  - Architecture: Action item checklist, assigned teams, and next key milestone date

### 4. AI Image Taste Selection
- [A] **None (CSS/SVG only - Recommended)**: Pure CSS cards, icons, and inline SVG diagrams
- [B] **Cinematic / Photorealistic**: Studio lighting, high-end realism
- [C] **Comic / Manga Style**: Engaging illustrative line art
- [D] **3D Isometric**: Clean 3D models with studio lighting
- [E] **Flat Vector**: Notion/SaaS-style minimal 2D vectors

### 5. Speaker Script Document (`speech_script.md`) Generation
- [A] **No**: Output slide HTML only
- [B] **[Recommended] Yes**: Generate synchronized speech script with timing, key points, and talk script

---
👉 **Reply "Approved" or "OK" to proceed with this outline.**
(To customize options, simply reply with your choices, e.g., "2-C, 4-D". Upon approval, HTML synthesis will begin immediately.)
```

---

## 3. スライド情報構造パターン 全10種の言語別対照表

Grill提示時は、対話言語に応じたパターン名のみを使用すること（日本語対話時に英語IDを出してはならない）：

| 日本語パターン名（日本語対話時） | 英語パターン名（英語対話時） | 内部ID (`pattern_id`) | レイアウトの特徴・使い所 |
| :--- | :--- | :--- | :--- |
| **【表紙】** | `[Cover]` | `cover` | タイトル・起案部門・日付・機密区分の明示 |
| **【エグゼクティブサマリ】** | `[Executive Summary]` | `exec_summary` | 左に重要指標・右に4行スプリットで課題・打ち手・ROI・体制を1枚総括 |
| **【目次（アジェンダ）】** | `[Agenda]` | `agenda` | 全体の章立てカードと現在地トラッカー |
| **【課題・打ち手型】** | `[Problem & Solution]` | `problem_solution` | 現場ペイン・根本原因と具体施策・定量的効果の左右対比 |
| **【トレードオフ比較表】** | `[Comparison Matrix]` | `tradeoff_matrix` | 複数案比較＋ハーベイボール（●◕◐◔○）による多軸評価と推奨ハイライト |
| **【ステップ・時系列フロー】** | `[Sequential Workflow]` | `step_process` | 時系列手順（STEP 1〜4）と通過必須の品質Gate（関門）を可視化 |
| **【要因分解・ウォーターフォール】** | `[Waterfall Breakdown]` | `waterfall_breakdown` | 売上・利益増減やKPI変動ステップを幾何学比例SVGで可視化 |
| **【全体像・階層マッピング】** | `[Architecture Mapping]` | `architecture_mapping` | クライアント・API・DB等のシステム階層や業務全体の俯瞰 |
| **【境界線・NG/OK対比】** | `[Boundary & Best Practices]` | `boundary_comparison` | In/Out Scope境界線設定、またはアンチパターン（NG）と推奨（OK）の対比 |
| **【マリメッコ市場分析】** | `[Mekko Market Share]` | `mekko_chart` | TAM市場規模（横幅）× 自社シェア（縦高さ）の2次元競合分析 |
| **【タイムライン＆マイルストーン】** | `[Timeline & Milestone]` | `timeline_gantt` | 四半期工程表と重要マイルストーン（◆）の可視化 |

---

## 4. 手抜き防止セルフチェックリスト（Anti-Lazy Grill Check）

エージェントがGrill構成案を出力する直前に自己検証すべき必須チェックリスト：

- [ ] **仮説構築検証**: ユーザーに「どうしますか？」と白紙の質問を投げ返していないか？（全スロットが自律的に埋まっているか？）
- [ ] **Action Title 検証**: すべてのスライドのLead Messageが動詞で終わる完全な1文（40〜60文字）になっているか？（「〇〇について」等の名詞止め見出しはゼロか？）
- [ ] **パターン名検証**: 日本語対話時に `tradeoff_matrix` 等の英語IDが漏れていないか？（直感的な日本語名になっているか？）
- [ ] **標準配置検証**: 4枚以上のデッキで【エグゼクティブサマリ】と【目次（アジェンダ）】が含まれているか？
- [ ] **1行承認CTA**: 末尾に「OK / 承認」で進められる誘導メッセージが付与されているか？
- [ ] **コード出力抑制**: ユーザーの承認を得る前にHTMLコードを1行でも出力していないか？

---

## 5. 合意後のコード生成フェーズ

ユーザーから構成案に対する承認（「OK」「承認」「2-C, 4-Aで進めて」等）を得た後、直ちに `assets/template_base.html` を読み込み、単一HTMLスライドの生成および品質検証へ進む。

---

## 6. 発表用台本文書（`speech_script.md`）の仕様フォーマット

台本生成が選択された場合、HTML内にメモを埋め込むのではなく、再利用・印刷・スマートフォンでの閲覧が容易な独立したMarkdownファイル（または回答内Markdownブロック）として出力する。

```markdown
# 発表用台本スクリプト

- **総想定時間**: 約10分
- **対象オーディエンス**: 役員・経営陣
- **トーン＆マナー**: 落ち着いたトーン、結論ファースト、平易で力強い表現

---

### Slide 01: [スライドタイトル]
- **目安時間**: 1分00秒
- **要点・狙い**: 
  - 本日のアジェンダとゴールの共有
  - なぜ今この取り組みが必要かの問題提起
- **トーク原稿**:
  「皆様、お時間をいただきありがとうございます。本日は『全社次世代データ基盤構想』についてご提案させていただきます。現在、各事業部でデータのサイロ化が進んでおり...」

---

### Slide 02: [スライドタイトル]
- **目安時間**: 2分00秒
...
```

