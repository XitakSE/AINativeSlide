# AINativeSlide (生成AIのための安定・高精度なHTMLスライド出力フレームワーク)

<p align="left">
  <strong>🌐 Language:</strong>
  <a href="README_EN.md">English</a> | 
  <a href="README.md"><strong>日本語</strong></a>
</p>

> **AIにスライドを作らせるなら、PPTXではなくHTML** —— LLMが最も得意とするHTML/Tailwind CSSを中間フォーマットとして活用し、レイアウト崩れや文字溢れのない堅牢なスライドを安定生成。最終的には余白ゼロのピクセルパーフェクトなPDFとしてエクスポートする、AI出力安定化フレームワークです。

<p align="left">
  <a href="https://xitakse.github.io/AINativeSlide/">
    <img src="https://img.shields.io/badge/Live%20Demo-%E3%83%96%E3%83%A9%E3%82%A6%E3%82%B6%E3%81%A7%E4%BB%8A%E3%81%99%E3%81%90%E8%A9%A6%E3%81%99%EF%BC%88%E7%99%BB%E9%8C%B2%E4%B8%8D%E8%A6%81%EF%BC%89-4f46e5?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Demo" />
  </a>
  <a href="https://github.com/XitakSE/AINativeSlide/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-slate?style=for-the-badge" alt="License" />
  </a>
</p>

---

## 📖 目次
1. [従来手法との比較](#従来手法との比較)
2. [主要機能一覧](#主要機能一覧)
3. [スキルの導入方法（インストール）](#スキルの導入方法インストール)
4. [使い方ガイド](#使い方ガイド)
5. [キーボードショートカット一覧](#キーボードショートカット一覧)
6. [ディレクトリ・ファイル構成](#ディレクトリ・ファイル構成)
7. [Pull Request 自動レビュー](#pull-request-自動レビュー-gemini-code-assist)
8. [ライセンス](#ライセンス)

---

## 従来手法との比較

| 比較項目 | 従来のPPTX直接生成<br>*(python-pptx 等)* | Markdownスライド<br>*(Marp 等)* | **AINativeSlide**<br>*(HTML + Tailwind)* |
| :--- | :--- | :--- | :--- |
| **文字溢れ耐性** | ❌ 頻繁にはみ出し・重なり発生 | ⚠️ 縦スクロールまたは見切れ | ⭕ **CSS line-clamp で物理的にはみ出し不能** |
| **レイアウト表現力** | ❌ 座標指定がシビアで崩れやすい | ⚠️ 箇条書き主体で構図が固定 | ⭕ **Flexbox/Grid でカード・表・SVGを自在配置** |
| **自律品質検証** | ❌ 人間がPowerPointで手動修正 | ⚠️ 手動でMarkdownを推敲 | ⭕ **Pythonテスト（標準lib）でAIが納品前に自己修復** |
| **印刷・用紙対応** | ⚠️ OS/フォント環境依存でズレる | ⭕ PDF出力可能 | ⭕ **16:9 / 4:3 / A4横・縦の余白ゼロPDF** |
| **外部依存性** | Python環境・Officeソフト | Node.js / CLI ツール | ⭕ **外部依存ゼロ（ブラウザで開くだけで完結）** |

---

## 主要機能一覧

| 分野 | 機能 | 概要 |
| :--- | :--- | :--- |
| **AI出力安定化** | **CSS物理文字溢れ防止 (`line-clamp`)** | 本文を `<div class="ai-content">` で囲み、見出し2行/本文6行/リスト3行で強制三点リーダー化 |
| | **Python自律品質テスト (`verify_slide.py`)** | 外部依存ゼロ（標準libのみ）。文字数・連番・印刷CSSを検査し、AIが自律修正してから納品 |
| | **幻覚予防ガードレール (Anti-Hallucination)** | CLIのないプレーンチャット環境での架空テスト実行ログ捏造を厳禁化 |
| **用紙・印刷** | **4大アスペクト比・用紙サポート** | 16:9（Web投影）、4:3（従来型）、**A4横（印刷配布・稟議）**、**A4縦（1-Pager）** |
| | **余白ゼロ印刷CSS (`@page`)** | ブラウザの「印刷（PDFに保存）」で改ページずれゼロ・余白ゼロのPDFを出力 |
| **デザイン統制** | **Anti-AI-Smell ガードレール** | 均等3分割を禁止し推奨案を強調。抽象バズワードを排除し、完全文のAction Title（動詞結び）義務化 |
| | **社内向け6大情報構造パターン** | 課題打ち手、トレードオフ比較、スコープ境界線、全体像、ステップ手順、落とし穴FAQ |
| | **企業公式デザインテンプレート** | CIカラー、公式ロゴ、機密区分バッジ、定位置フッターを固定化（[Template-Builder](https://github.com/XitakSE/AINativeSlide-Template-Builder) 連携） |
| | **インラインSVGビジネスチャート** | 外部JS不使用の複合チャート（棒・折れ線）＆ 推奨列ハイライト付き比較テーブル |
| **AIビジュアル** | **AI生成画像 (Concept Imagery)** | 4大テイスト（リアル／漫画／3Dアイコン／フラット）の日本語プロンプト設計 |
| | **Zero-Cropping 構図同期** | スライド枠比率とプロンプト比率を事前同期し、CSSトリミング切り落としをゼロ化（D&D差し替え対応） |
| | **Base64 完全インライン化** | 生成画像やCIロゴをData URIとしてHTML内に直接埋め込み、単一ファイル（Single-File）で完全完結 |
| **推敲・発表** | **事前スマートGrill（承認ゲート）** | いきなりコードを出力せず、スライド構成提案書で合意を得る認知ドリフト防止策 |
| | **発表用台本文書（MD）セット生成** | スライドHTMLと口語体トーク原稿（`speech_script.md`）を同時出力（Grill選択制） |
| | **ブラウザ直接推敲 & ミニ書式バー** | スライド文字をクリック編集。太字・文字色・マーカー・個別フォントサイズ調整 |
| | **全画面スライドショー & 閲覧モード** | キーボード **`F`** で投影、**`E`** で閲覧専用（誤操作防止）、**`Esc`** で復帰 |
| | **修正指示の一括コピー ＆ 保存** | 各スライドの要望を整形プロンプトとしてクリップボードへ集約。`localStorage` 自動保存 |

---

## スキルの導入方法（インストール）

AINativeSlideは、オープンな **Agent Skills規格（`SKILL.md`）** に準拠しています。**Codex**, **Claude Code**, **Cursor**, **Antigravity** などの対応エージェント環境に本スキルを配置するだけで、自動的に認識されます。

### 手順A. Git Clone による導入（推奨）
作業プロジェクトまたはワークスペースのルートで以下を実行します：

```bash
git clone https://github.com/XitakSE/AINativeSlide.git .agents/skills/ainativeslide
```

### 手順B. ZIPダウンロードによる直接配置（社内プロキシ制限環境・Git CLI不要）
1. GitHubリポジトリの **「<> Code」➔「Download ZIP」** からZIPファイルを保存。
2. 解凍したフォルダを `ainativeslide` にリネーム。
3. 作業スペースの `.agents/skills/ainativeslide` に直接配置します（フォルダ直下に `SKILL.md` がある状態）。

---

## 使い方ガイド

### ① スライド作成の依頼（プロンプト例）

AIチャット欄に、テーマと要件を入力します。

```markdown
以下の要件で、AINativeSlide規格の「Single-File HTMLプレゼンテーション」を作成してください。
いきなりコードを出力せず、まずはスライド構成案を提示して承認を得てください（Grill実施）。

【テーマ】
全社次世代データ基盤 Modern Data Stack 導入計画

【ターゲット】
経営陣・役員向け（投資回収ROIとガバナンス統制の納得感を重視）

【スライド要件】
1. 用紙比率: 16:9 ワイド（または A4横）
2. 枚数: 全6〜8枚
3. Anti-AI-Smell規約に準拠し、各スライドの見出しは動詞結びの完全文（Action Title）にすること
4. 主要構成:
   - 表紙（CIロゴ・機密区分バッジ）
   - 現状課題と目指す姿（AS-IS vs TO-BE 対比カード）
   - 3案の評価マトリクス（推奨案を枠線とバッジで強調）
   - 4カ年の投資回収ROI推移（インラインSVGチャート）
   - 段階的導入ロードマップ（4フェーズ）
5. 発表用台本文書（speech_script.md）もセットで出力してください。
```

### ② 生成・自律修復フロー
エージェント環境では、AIが内部で自律テストを実行し、全合格（Exit Code 0）にしてから納品します。

```mermaid
flowchart LR
    A[ユーザー依頼] --> B[AIが構成案を提示 (Grill)]
    B --> C{ユーザー承認}
    C --> D[HTMLコード生成]
    D --> E[verify_slide.py 自動実行]
    E --> F{テスト合否}
    F -- エラー検出 --> G[AIが自律修正]
    G --> E
    F -- 全合格 --> H[🚀 完成HTMLを納品]
```

### ③ ブラウザ推敲と反復修正（Iteration）
出力されたHTMLをブラウザで開きます。
1. **直接編集**: スライド上の文字をクリックして直接推敲（`localStorage` に自動保存）。範囲選択でミニ書式バーが出現。
2. **修正指示の入力**: 各スライド下の「💬 修正指示」欄に要望を入力。
3. **指示の一括コピー**: ツールバーの **「📋 指示をコピー」** をクリックし、AIチャットへ貼り付けて送信するだけで、推敲内容を維持したまま改訂版が再生成されます。

### ④ プレゼンテーション本番 & PDF保存
- **全画面発表**: **`F`** キーで全画面スライドショー開始（`Esc` で通常画面へ復帰）。
- **PDF保存**: ツールバーの「PDF保存」をクリック（または `Ctrl+P` / `Cmd+P`）。送信先を「PDFに保存」、**余白「なし」**、**「背景のグラフィックス」をオン** に設定して保存すると、改ページずれゼロのPDFが出力されます。

---

## キーボードショートカット一覧

| キー | 対象モード | 動作内容 |
| :--- | :--- | :--- |
| **`F`** / **`F5`** | 通常 / 投影 | 全画面プレゼンテーションモードの開始 / 終了 |
| **`E`** | 通常 / 投影 | 編集モードのON / OFF切り替え（OFF時は誤操作を防ぐ選択禁止モード） |
| **`Esc`** | 投影 | スライドショーの終了（通常編集モードへ復帰） |
| **`→`** / **`↓`** / **`Space`** / **`PageDown`** | 投影 | 次のスライドへ進む |
| **`←`** / **`↑`** / **`PageUp`** | 投影 | 前のスライドへ戻る |
| **`Home`** / **`End`** | 投影 | 最初 / 最後のスライドへジャンプ |

※テキスト入力欄や `contenteditable` の編集にフォーカス中は、誤動作を防ぐためプレゼンテーションショートカットは安全に無効化されます。

---

## ディレクトリ・ファイル構成

```
AINativeSlide/
├── AGENTS.md                # AIコーディングエージェント向け指示書
├── SKILL.md                 # スキル仕様書（スマートGrill・自律検証ループ・パターン規約）
├── README.md                # 本ドキュメント（日本語）
├── README_EN.md             # 英語ドキュメント
├── index.html               # GitHub Pages ルート & 16:9 実動ショーケース
├── scripts/
│   ├── verify_slide.py      # 【外部依存ゼロ】自動品質検証＆自律修正Pythonスクリプト
│   └── gemini_pr_review.py  # 【外部依存ゼロ】Gemini API 自動PRレビュー実行スクリプト
├── resources/
│   ├── template_base.html   # 汎用HTMLベーステンプレート（機能エンジン）
│   ├── speech_script_example.md # 発表台本文書サンプル
│   └── design_templates/    # 企業公式デザインテンプレート群（CI/VI統一）
└── references/              # 詳細技術リファレンス
    ├── slide-patterns.md    # スライド情報構造＆レイアウトパターン集（Anti-AI-Smell・6大構成）
    ├── grill-workflow.md    # 認知ドリフト防止 Grill仕様
    ├── ratio-and-print-specs.md # 16:9 / 4:3 / A4 比率・印刷CSS仕様
    ├── ai-concept-imagery.md # コンセプト画像プロンプト設計仕様
    └── design-system.md     # タイポグラフィ・堅牢ボックスモデル仕様
```

※自社PPTXテンプレートからの移行は、初期セットアップ専用スキル [ainativeslide-template-builder](https://github.com/XitakSE/AINativeSlide-Template-Builder) で実行できます。

---

## Pull Request 自動レビュー (Gemini Code Assist)

本リポジトリでは、GitHub Actions を通じて **Gemini Code Assist による自動コードレビュー** が常時稼働しています。Pull Request が作成されると、`scripts/verify_slide.py` の検証結果および設計規約を読み込み、PRコメント欄に品質レポートが自動投稿されます。

---

## ライセンス

MIT License © 2026 AINativeSlide Contributors. 商用・非商用問わず自由にご利用いただけます。
