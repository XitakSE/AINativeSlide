# スライド情報構造 ＆ レイアウトパターン集 (Slide Layout & Information Patterns)

<slide_pattern_specifications>
本書は、社内向けプレゼンテーション（提案・意思決定、認識合わせ、学習・ナレッジ共有）のスライド構成を自動生成・検証するAIエージェント向けのリファレンス仕様書です。

デザインテンプレート（フォント、配色、余白設計、CIロゴ）は [AINativeSlide-Template-Builder](../../AINativeSlide-Template-Builder/SKILL.md) および `assets/corporate_default.html` で別管理されている前提とし、エージェントは**「情報構造（ワイヤーフレーム）の選定」「メッセージの論理構築」「スロットへのテキスト配置」**に集中してください。

---

<anti_ai_smell_guardrails>
## 1. エージェント行動規範（Anti-AI-Smell Guardrails: 正本/SSOT）

エージェントはスライド生成・推敲時に以下の絶対規範を厳守してください（`SKILL.md` 禁止事項と完全連動）：

1. **無意味な3均等カード化の禁止**: 3列以上並ぶ場合は必ず推奨案・関門に視覚的アンカー（幅拡張、ハイライト色枠等）を設定する。
2. **抽象バズワード連呼の禁止**: 「シナジー」「DX推進」等の空虚語句を廃止し、「月40h削減」「承認者2名体制」等の具体動作に直す。
3. **飾りアイコン要求の禁止**: 文脈と無関係なロケット・電球等のアイコンを廃止し、状態記号（`✓`/`!`）、矢印（`➔`）、実数値に限定する。
4. **トピックタイトル（名詞止め見出し）のみの禁止**: 「〇〇について」等の名詞止めを禁じ、結論を含む完全文（Action Title: 40〜60文字・動詞結び）を出力する。
5. **中途半端な単語分断改行の禁止 (Semantic Line Breaking)**: 単語や助詞の途中での不自然な改行を禁じ、文節で明示的に `<br>` を入れる。
6. **右肩バッジの折り返し＆ヘッダー余白ゼロの禁止**: バッジには `shrink-0 whitespace-nowrap` を付与し、ヘッダー下部に十分な余白（`mb-5`）を設ける。
7. **外部画像パス参照の禁止**: 画像は必ず Base64 Data URI（`data:image/...`）でインライン埋め込みし、単一ファイル完結を死守する。
8. **無意味な装飾AI画像の禁止（Anti-Decorative Imagery Rule）**: 単なる雰囲気出しのイメージ画像（アイキャッチ、意味のない3Dキューブ、抽象CG等）をスライド内に置くことを厳禁とする。画像は「UIモックアップ」「現場の実態」「物理製品」「AS-IS/TO-BEの構造的対比」等の不可欠な視覚証拠に限定する。
9. **豆粒フォント（text-xs / text-[10px]）乱用の禁止（Minimum Font Size Guardrails）**: スライド本文やカード内で `text-xs` (12px) や `text-[10px]` を多用することを禁止する（豆粒フォントの撲滅）。本文は最低 `text-sm` (14px) 以上、カード見出しは `text-base`〜`text-lg` (16〜18px)、Action Titleは `text-2xl`〜`text-3xl` (24〜28px) を厳守し、文字数を絞って余白を確保する。
10. **視覚的AI臭の根絶 ＆ IBM Carbon 原則の死守（Visual Anti-AI-Smell Rule）**:
    - **No Rounded-2XL (ハードエッジ)**: 丸すぎるカード（`rounded-xl`, `rounded-2xl`, `rounded-3xl`）を厳禁とし、完全な直角（`rounded-none`）または最小限（`rounded-sm: 4px`）を標準化する。
    - **No Drop Shadows (アンチシャドウ)**: ぼやけたドロップシャドウ（`shadow-md`, `shadow-lg`, `shadow-xl`）を全廃し、影ゼロ（`shadow-none`）＋ 1pxの精密境界線（`border border-gray-300`）および背景色のコントラスト階層（Gray 10 上の White）のみで面を構築する。
    - **No Neon Gradients (直線アクセントバー)**: 紫〜ピンク等の安易なAIネオングラデーションを禁止し、強調には 4px の直線アクセントバー（`border-l-4 border-blue-600` または `border-t-4 border-blue-600`）を用いる。
    - **IBM Plex Family の遵守**: フォントは `IBM Plex Sans` + `IBM Plex Sans JP` を標準とし、シャープで知的なエンジニアリング・エンタープライズ品質を担保する。

<self_reflection_checklist>
### 出力前自己内省チェックリスト
- [ ] リード文は動詞結びの完全な1文（40〜60文字のAction Title）になっているか？
- [ ] 現場担当者が読んだ時に「明日から誰が何をすべきか」の具体動作・数値が想起できるか？
- [ ] 本文フォントは `text-sm` (14px) 以上が確保されているか？（`text-xs` や `text-[10px]` を乱用していないか？）
- [ ] カードは IBM Carbon 準拠のハードエッジ（`rounded-none`）および影ゼロ（`shadow-none` + 1pxボーダー）になっているか？（`rounded-2xl` や `shadow-lg` 等の視覚的AI臭を出していないか？）
- [ ] 安易なネオングラデーションに頼らず、直線アクセントバー（`border-l-4`）で強調しているか？
- [ ] 配置された画像は単なる装飾ではなく、スライドの論理を証明する実質的意味を持っているか？
- [ ] エグゼクティブサマリに画像をねじ込んで標準の横スプリット4段構造を破壊していないか？
- [ ] `overflow-hidden` 親要素内で `-top-` バッジを使って見切れ（クリッピング）を発生させていないか？
- [ ] チャート類で `mb-[..%]` 等のパーセンテージマージンハックを使って要素重なり（コリジョン）を発生させていないか？
- [ ] ウォーターフォール図のバー高さ（height）は、表示数値に厳密比例しているか？（適当な手打ち値による「数値と高さの不一致」を防止）
- [ ] 1スライドあたりのテキスト量は適切か？（日本語200〜300文字推奨、最大700文字厳守）
</self_reflection_checklist>
</anti_ai_smell_guardrails>

---

<base_anatomy>
## 2. スライド共通骨格（Base Anatomy）

すべてのスライドは以下の基本階層でスロットを定義します。

```text
+-------------------------------------------------------------------+
| [Kicker / Category] (任意: カテゴリ・章名)                        |
| 【Lead Message】1スライド1主張を体現する完全な結論文 (Action Title)|
+-------------------------------------------------------------------+
|                                                                   |
|                       Main Content Body                           |
|                  (パターン別のワイヤーフレーム)                   |
|                                                                   |
+-------------------------------------------------------------------+
| [Footer / Note] 補足注記、データソース、前提条件、ページ番号      |
+-------------------------------------------------------------------+
```

```html
<section class="slide w-[1280px] h-[720px] p-12 justify-between flex flex-col overflow-hidden relative bg-white border border-slate-200" contenteditable="true">
  <!-- 1. ヘッダー (Action Title) -->
  <div class="flex-shrink-0 border-b border-slate-100 pb-3">
    <div class="flex items-center justify-between"><span class="text-xs font-bold text-brand-600 uppercase">Category</span><span class="text-xs font-mono text-slate-400 bg-slate-100 px-2 py-0.5 rounded">CONFIDENTIAL</span></div>
    <h2 class="text-xl font-extrabold text-slate-900 tracking-tight mt-1">【Lead Message】結論を含む完全な1文（40〜60文字）</h2>
  </div>
  <!-- 2. メインコンテンツ (flex-1 min-h-0) -->
  <div class="flex-1 min-h-0 flex flex-col justify-center my-auto py-2"><!-- パターンワイヤーフレーム --></div>
  <!-- 3. フッター -->
  <div class="flex-shrink-0 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
    <div class="truncate">※注記: 補足前提条件、データ出典等を記載</div><div class="font-mono text-slate-500">02 / 06</div>
  </div>
</section>
```
> 💡 **自動採番・メタボックスの決定論的注入**:
> フッターのスライド番号（`02 / 06`）の再計算や、スライド直下の修正指示入力欄（`.slide-meta-box`）の注入は、`scripts/assemble_deck.py` および `scripts/verify_slide.py --fix` が自動処理します。エージェントは各スライドの内部コンテンツ生成（Action Titleとワイヤーフレーム）に専念してください。
</base_anatomy>

---

<deck_meta_skeleton>
## 2.2 プレゼンテーション全体骨格（Deck Meta Skeleton）

複数枚で構成されるプレゼンテーション（提案書、稟議資料、ピッチデック等）では、**「表紙」の直後に「エグゼクティブサマリ」と「目次（アジェンダ）」を原則標準として配置**します。

> **📌 エグゼクティブサマリ＆目次の原則標準化ルール**:
> - **【原則標準（Default: ON）】**: 通常の複数枚スライド（4枚以上）。意思決定者が即座に判断できるよう、表紙直後にエグゼクティブサマリと目次を配置する。
>   - 構成順序: `[表紙]` ➔ `[エグゼクティブサマリ]` ➔ `[目次（アジェンダ）]` ➔ `[本文スライド群]` ➔ `[Next Steps/推進体制]`
> - **【除外条件（Exception: OFF）】**:
>   - 1枚ものの資料（A4縦・横の1-Pager、企画ペーパー、要約ペーパー）
>   - ユーザーから明示的な拒否・除外指示があった場合（「目次は不要」「3枚以内で作って」等）

### 骨格A：【エグゼクティブサマリ】（Executive Summary）
- **識別子 (`pattern_id`)**: `executive_summary`
- **絶対厳守ルール（画像完全禁止・聖域化）**: 
  - **本スライドへのAI生成画像・装飾イラストの挿入は一切禁止する（No Image Sanctuary Zone）**。画像を配置すると論理と数字の視認性が著しく破壊される。
  - 「左に論点・表題（25%）」「右に端的な事実・結論・巨大な主張フォント（75% / text-lg〜xl font-black）」の横スプリット4段構造を100%厳守する（※目次アジェンダの縦型カード列との混同を完全に防止）。
  - 各行の説明的な長文サブテキストは排除し、ファクト・数値・述語だけで言い切る。
- **実装**: 実稼働の完全なサンプルは `corporate_default.html` の Slide 2 を参照。

```html
<!-- エグゼクティブサマリ（左表題・右巨大事実/主張の横スプリット4段・サブ文章なし） -->
<div class="my-auto py-2 flex flex-col gap-4">
  <!-- Row 1: 課題 -->
  <div class="flex items-center gap-6 p-5 bg-white rounded-xl border border-slate-200 shadow-xs">
    <div class="w-56 shrink-0 border-r border-slate-100 pr-4">
      <div class="text-[11px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded uppercase">01. 直面する課題</div>
      <div class="text-sm font-extrabold text-slate-800 mt-1">現場ボトルネック</div>
    </div>
    <div class="flex-1 min-w-0">
      <div class="text-lg font-black text-slate-900 leading-relaxed">手動転記に年間4,800時間。<span class="text-rose-600 underline decoration-rose-300">1,920万円の年間機会損失</span> が発生</div>
    </div>
  </div>
  <!-- Row 2: 推奨解決策（視覚的アンカー強調） -->
  <div class="flex items-center gap-6 p-5 bg-brand-50/80 rounded-xl border-2 border-brand-500 shadow-sm relative">
    <div class="absolute -top-2.5 right-6 px-2.5 py-0.5 rounded-full bg-brand-600 text-white text-[10px] font-extrabold">★ 推奨アプローチ</div>
    <div class="w-56 shrink-0 border-r border-brand-200 pr-4">
      <div class="text-[11px] font-bold text-brand-800 bg-brand-100 px-2 py-0.5 rounded uppercase">02. 抜本的解決策</div>
      <div class="text-sm font-extrabold text-brand-950 mt-1">自律AI基盤の全社導入</div>
    </div>
    <div class="flex-1 min-w-0">
      <div class="text-lg font-black text-brand-950 leading-relaxed">API連携と自動描画を直結し、定常工数を <span class="text-brand-600 bg-white px-2.5 py-0.5 rounded border border-brand-300 font-black">92% 削減</span> してゼロ化</div>
    </div>
  </div>
  <!-- Row 3: 定量ROI -->
  <div class="flex items-center gap-6 p-5 bg-white rounded-xl border border-slate-200 shadow-xs">
    <div class="w-56 shrink-0 border-r border-slate-100 pr-4">
      <div class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded uppercase">03. 投資対効果 (ROI)</div>
      <div class="text-sm font-extrabold text-slate-800 mt-1">初年度ROI 152%</div>
    </div>
    <div class="flex-1 min-w-0">
      <div class="text-lg font-black text-slate-900 leading-relaxed">初期投資1,200万に対し人件費1,820万削減。<span class="text-emerald-600 underline decoration-emerald-300">8ヶ月で原価回収</span> を完了</div>
    </div>
  </div>
  <!-- Row 4: 計画・体制 -->
  <div class="flex items-center gap-6 p-5 bg-white rounded-xl border border-slate-200 shadow-xs">
    <div class="w-56 shrink-0 border-r border-slate-100 pr-4">
      <div class="text-[11px] font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded uppercase">04. 推進体制・計画</div>
      <div class="text-sm font-extrabold text-slate-800 mt-1">2026年Q4 全社展開</div>
    </div>
    <div class="flex-1 min-w-0">
      <div class="text-lg font-black text-slate-900 leading-relaxed">10月PoC、11月パイロットを経て <span class="bg-slate-100 px-2.5 py-0.5 rounded font-black">12月に全社本番稼働</span> を完遂</div>
    </div>
  </div>
</div>
```

---

### 骨格B：【目次・アジェンダ】（Table of Contents / Agenda）
- **識別子 (`pattern_id`)**: `agenda`
- **目的**: プレゼンテーション全体の論理展開（章立て）を俯瞰させ、聞き手が現在地を常に把握できるようにする。
- **章ガイド**: ヘッダー上部に戦略コンサル型章トラッカー（Breadcrumbs）を配置し、`✓ Summary › [1] 01. 目次` をアクティブ表示する。
- **実装**: 実稼働サンプルは `corporate_default.html` の Slide 3 を参照。

```html
<!-- 目次・アジェンダ（4章グリッド） -->
<div class="grid grid-cols-4 gap-6 my-auto">
  <div class="bg-slate-50 p-6 rounded-xl border border-slate-200 flex flex-col justify-between">
    <div><div class="font-mono text-2xl font-black text-slate-300 mb-2">01</div><h3 class="text-sm font-bold text-slate-800 mb-1">背景と事業課題</h3><p class="text-xs text-slate-500">運用ペインと工数増大要因の分析</p></div>
    <div class="mt-4 text-[11px] font-mono text-slate-400">P. 04 - 05</div>
  </div>
  <!-- 注目章（ハイライト） -->
  <div class="bg-brand-50/60 p-6 rounded-xl border-2 border-brand-400 shadow-sm flex flex-col justify-between">
    <div><div class="font-mono text-2xl font-black text-brand-400 mb-2">02</div><h3 class="text-sm font-bold text-brand-900 mb-1">刷新方針と打ち手</h3><p class="text-xs text-brand-700">自律化アーキテクチャと推奨案</p></div>
    <div class="mt-4 text-[11px] font-mono text-brand-600 font-bold">P. 06 - 08</div>
  </div>
  <div class="bg-slate-50 p-6 rounded-xl border border-slate-200 flex flex-col justify-between">
    <div><div class="font-mono text-2xl font-black text-slate-300 mb-2">03</div><h3 class="text-sm font-bold text-slate-800 mb-1">投資対効果と検証</h3><p class="text-xs text-slate-500">PoC成果、定量ROI、リスクヘッジ</p></div>
    <div class="mt-4 text-[11px] font-mono text-slate-400">P. 09 - 10</div>
  </div>
  <div class="bg-slate-50 p-6 rounded-xl border border-slate-200 flex flex-col justify-between">
    <div><div class="font-mono text-2xl font-black text-slate-300 mb-2">04</div><h3 class="text-sm font-bold text-slate-800 mb-1">ロードマップ・体制</h3><p class="text-xs text-slate-500">導入工程、必須Gate、推進体制</p></div>
    <div class="mt-4 text-[11px] font-mono text-slate-400">P. 11 - 12</div>
  </div>
</div>
```
</deck_meta_skeleton>

---

<wireframe_catalog>
## 3. 社内資料向け厳選6大情報構造パターン（6 Core Enterprise Wireframes）

| 日本語対話時 | 英語対話時 | 内部識別子 (`pattern_id`) | レイアウトの特徴・使い所 |
| :--- | :--- | :--- | :--- |
| **【課題・打ち手型】** | `[Problem & Solution]` | `problem_solution` | 左右対比で「現場ペイン・原因」と「施策・定量的効果」を対比 |
| **【トレードオフ比較表】** | `[Comparison Matrix]` | `tradeoff_matrix` | 複数案比較＋**ハーベイボール（●◕◐◔○）** で多軸評価。推奨列を強調 |
| **【ステップ・時系列フロー】** | `[Sequential Workflow]` | `step_process` | 時系列の運用手順（STEP 1〜4）と、通過必須の品質Gate（関門）を可視化 |
| **【要因分解・ウォーターフォール】** | `[Waterfall Breakdown]` | `waterfall_breakdown` | 売上・利益増減、コスト構造、KPIドライバーの変動ステップを戦略コンサル型増減ステップで可視化 |
| **【全体像・階層マッピング】** | `[Architecture Mapping]` | `architecture_mapping` | クライアント・API・DBなどのシステム階層や業務フロー全体の構造を俯瞰 |
| **【境界線・NG/OK対比】** | `[Boundary & Best Practices]` | `boundary_comparison` | In/Out Scope境界線設定、またはアンチパターン（NG）と推奨（OK）の対比 |

---

### パターン1：【課題・打ち手型】（problem_solution）
- **主用途**: 業務改善提案、ツール導入起案、施策優先順位の合意（左右 40% : 60%）

#### ワイヤーフレーム＆スロット
```text
[Lead: 月間40時間の重複入力を解消するため、マスタ同期スクリプトを導入する]
┌─ 【現状の課題 / Bottleneck (40%)】 ─┬─ 【解決策 / Action & Solution (60%)】 ─┐
│ ● 発生事象: 手動転記による二重管理  │ ● 実施内容: 差分検知バッチによる自動同期 │
│ ● 根本原因: DB連携仕様の未策定      │ ● 期待効果: 工数40h→0h / ミス5件→0件     │
│ [損失試算: 年間480時間 / 約190万円]  │ [所要期間: 3週間 / 担当: データ統括]    │
└─────────────────────────────────────┴─────────────────────────────────────────┘
スロット: lead_message, col_problem (fact, root_cause), col_solution (action, outcome)
```

#### 骨格HTML構造スニペット
```html
<!-- 左右4:6分割（左: 課題・損失試算 / 右: 施策・定量的効果） -->
<div class="grid grid-cols-12 gap-6 my-auto items-stretch">
  <!-- 左: 現状の課題 (cols-5) -->
  <div class="col-span-5 bg-rose-50/40 rounded-xl p-6 border border-rose-200/80 flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-rose-700 font-bold text-sm mb-3">
        <span class="w-5 h-5 rounded-full bg-rose-100 flex items-center justify-center text-xs text-rose-600">✕</span>
        <span>現状の課題 / Bottleneck</span>
      </div>
      <div class="space-y-3 text-xs text-slate-600">
        <div><span class="font-bold text-slate-700">● 発生事象:</span> スプレッドシート手動転記による二重管理</div>
        <div><span class="font-bold text-slate-700">● 根本原因:</span> 基幹DB連携の仕様未策定・個別運用の形骸化</div>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-rose-200/60 text-xs font-bold text-rose-700">損失試算: 年間480時間 / 人件費 約190万円</div>
  </div>

  <!-- 右: 解決策 (cols-7) -->
  <div class="col-span-7 bg-emerald-50/40 rounded-xl p-6 border border-emerald-200/80 flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-emerald-700 font-bold text-sm mb-3">
        <span class="w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center text-xs text-emerald-600">✓</span>
        <span>解決策 / Action & Solution</span>
      </div>
      <div class="space-y-3">
        <div class="text-xs text-slate-600">・Webhookによる差分検知自動同期バッチ常駐<br>・手動入力フローの完全廃止</div>
        <div class="grid grid-cols-2 gap-3">
          <div class="p-2.5 bg-white rounded-lg border border-emerald-100 text-xs">
            <div class="text-[10px] text-slate-500">作業工数</div><div class="text-base font-extrabold text-emerald-600">40h → 0h</div>
          </div>
          <div class="p-2.5 bg-white rounded-lg border border-emerald-100 text-xs">
            <div class="text-[10px] text-slate-500">転記ミス</div><div class="text-base font-extrabold text-emerald-600">月5件 → 0件</div>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-emerald-200/60 text-xs font-bold text-emerald-700 flex justify-between">
      <span>所要期間: 3週間</span><span class="text-slate-500 font-normal">担当: データ統括チーム</span>
    </div>
  </div>
</div>
```

---

### パターン2：【トレードオフ比較表】（tradeoff_matrix / Comparison Matrix）
- **識別子 (`pattern_id`)**: `tradeoff_matrix`
- **主用途**: アーキテクチャ選定、ベンダー選定、施策オプションの意思決定
- **目的**: 複数選択肢のメリデリを公正に並べ、推奨案の採用論拠を示す。
- **比率**: 表形式（推奨案列を強調）
- **示唆アノテーション**: 多軸評価には記号（◎/◯/△）に加え、**ハーベイボール（● ◕ ◐ ◔ ○）** を積極的に活用する。
- **実装**: 実稼働の完全なサンプルは `corporate_default.html` の Slide 4 を参照。

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: 運用保守の内製化を最優先とし、初期コスト増を許容して「案B」を採用する |
+--------------+------------------+------------------+--------------+
| 評価軸       | 案A: SaaS導入    | 【推奨】案B: 内製 | 案C: 既存改修 |
+--------------+------------------+------------------+--------------+
| 初期費用     | ● 低 (50万円)    | ○ 高 (200万円)   | ● 極小 (10万) |
| 月額ランコス | ○ 高 (15万円/月) | ● サーバ実費のみ | ◐ 0円        |
| 拡張性       | ◔ 不可           | ● 完全自由       | ◐ 制限あり   |
| 保守内製度   | ◔ ベンダー依存   | ● 自チーム完結   | ○ 属人化継続 |
+--------------+------------------+------------------+--------------+
| 判定・総評   | △ コスト増リスク | ◎ 長期ROI最善    | × 課題未解決 |
+--------------+------------------+------------------+--------------+
```

#### スロット定義
- `lead_message`: 推奨案名と選択における最大のトレードオフ基準（何を捨てて何を取ったか）
- `criteria`: 評価軸リスト（最低3〜4軸）
- `options`: 各案の名称および属性値
- `recommended_option_id`: 強調対象となる列（背景ハイライト、推奨バッジ、色枠）
- `tradeoff_rationale`: ハーベイボール／判定記号 ＋ 具体的なデメリット許容理由

#### 骨格HTML構造スニペット
```html
<!-- トレードオフ比較テーブル（推奨列ハイライト枠＆ハーベイボール） -->
<div class="my-auto overflow-hidden rounded-xl border border-slate-200 shadow-sm bg-white">
  <table class="w-full text-left text-xs border-collapse">
    <thead>
      <tr class="bg-slate-50/80 border-b border-slate-200 text-slate-600">
        <th class="p-3 font-bold w-1/4">評価軸</th>
        <th class="p-3 font-semibold text-slate-500 w-1/4">案A: SaaS導入</th>
        <!-- 推奨列（視覚的アンカー・バッジ安全内包） -->
        <th class="p-3 font-bold text-white bg-brand-600 border-x-2 border-t-2 border-brand-500 w-1/4">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-brand-200 font-normal">本命案</span>
            <span class="bg-amber-400 text-slate-950 text-[10px] font-black px-2 py-0.5 rounded-full shadow-xs">★ 推奨</span>
          </div>
          案B: 内製開発
        </th>
        <th class="p-3 font-semibold text-slate-500 w-1/4">案C: 既存改修</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-100 text-slate-700">
      <tr>
        <td class="p-2.5 font-bold text-slate-900 bg-slate-50/30">初期開発費</td>
        <td class="p-2.5">● 低 (50万)</td>
        <td class="p-2.5 bg-brand-50/30 border-x-2 border-brand-500 font-medium">○ 高 (200万)</td>
        <td class="p-2.5">● 極小 (10万)</td>
      </tr>
      <tr>
        <td class="p-2.5 font-bold text-slate-900 bg-slate-50/30">月額運用費</td>
        <td class="p-2.5 text-rose-600">○ 高 (15万/月)</td>
        <td class="p-2.5 bg-brand-50/30 border-x-2 border-brand-500 font-bold text-brand-900">● 実費のみ (~1.5万)</td>
        <td class="p-2.5">◐ 0円</td>
      </tr>
      <tr class="bg-slate-50/60 font-semibold">
        <td class="p-3 font-bold text-slate-900">判定・総評</td>
        <td class="p-3 text-amber-700">△ コスト増リスク</td>
        <td class="p-3 bg-brand-100/60 border-x-2 border-b-2 border-brand-500 text-brand-900 font-bold">◎ 3年ROI最善</td>
        <td class="p-3 text-rose-700">✕ 根本課題未解決</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

### パターン3：【ステップ・時系列フロー】（step_process / Sequential Workflow）
- **主用途**: 業務運用手順、リリース手順、障害対応、オンボーディング（3〜4ステップ）

#### ワイヤーフレーム＆スロット
```text
[Lead: Step 2のレビュー承認を完了するまで本番マージ・デプロイは不可]
┌─ STEP 01 (実装) ──┬─ ★ STEP 02 (Gate) ──┬─ STEP 03 (QA) ────┬─ STEP 04 (本番) ──┐
│ ・ブランチ作成     │ ・シニア2名承認     │ ・自動E2E検証     │ ・カナリアデプロイ│
│ [成果物: PR]       │ [通過条件: 承認ログ] │ [成果物: サイン]  │ [Goal: 稼働確認]  │
└───────────────────┴─────────────────────┴───────────────────┴───────────────────┘
スロット: lead_message, steps (step_number, title, tasks, gate_or_output)
```

#### 骨格HTML構造スニペット
```html
<!-- 4ステップ横並びプロセス（Gate強調＆マイルストーン：実稼働サンプルは corporate_default.html Slide 6 参照） -->
<div class="grid grid-cols-4 gap-4 my-auto">
  <!-- 通常Step -->
  <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-xs font-mono"><span>STEP 01</span><span class="text-slate-400">10月上旬</span></div>
      <div class="text-xs font-bold text-slate-900 mb-1">基盤構築</div>
      <ul class="text-[11px] text-slate-600 space-y-1"><li>・API連携</li><li>・疎通テスト</li></ul>
    </div>
    <div class="pt-2 border-t border-slate-100 text-[10px] text-slate-400">成果物: PoCレポート</div>
  </div>

  <!-- 必須Gate Step (視覚的アンカー強調) -->
  <div class="bg-brand-50/70 rounded-xl p-4 border-2 border-brand-500 shadow-sm flex flex-col justify-between relative">
    <div class="absolute -top-2.5 right-3 bg-brand-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full shadow flex items-center gap-1">
      <span class="w-2 h-2 rotate-45 bg-amber-400"></span>必須関門 (Gate)
    </div>
    <div>
      <div class="flex justify-between border-b border-brand-200 pb-2 mb-2 text-xs font-mono font-bold text-brand-700"><span>STEP 02</span><span>10月下旬</span></div>
      <div class="text-xs font-bold text-brand-900 mb-1">セキュリティ監査</div>
      <ul class="text-[11px] text-slate-700 space-y-1"><li>・暗号化監査</li><li>・脆弱性診断</li></ul>
    </div>
    <div class="pt-2 border-t border-brand-200 text-[10px] font-bold text-brand-800">通過条件: 監査承認必須</div>
  </div>

  <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-xs font-mono"><span>STEP 03</span><span class="text-slate-400">11月中旬</span></div>
      <div class="text-xs font-bold text-slate-900 mb-1">パイロット運用</div>
      <ul class="text-[11px] text-slate-600 space-y-1"><li>・2部署実務投入</li><li>・FB回収</li></ul>
    </div>
    <div class="pt-2 border-t border-slate-100 text-[10px] text-slate-400">成果物: 評価報告</div>
  </div>

  <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-xs font-mono"><span>STEP 04</span><span class="text-emerald-700 font-bold">12月1日</span></div>
      <div class="text-xs font-bold text-slate-900 mb-1">全社本番展開</div>
      <ul class="text-[11px] text-slate-600 space-y-1"><li>・全アカウント有効化</li><li>・24h監視体制</li></ul>
    </div>
    <div class="pt-2 border-t border-slate-100 text-[10px] font-bold text-emerald-700">Goal: 自律化完了</div>
  </div>
</div>
```

---

### パターン4：【要因分解・ウォーターフォール】（waterfall_breakdown / Waterfall Breakdown）
- **識別子 (`pattern_id`)**: `waterfall_breakdown`
- **主用途**: 売上・利益増減、コスト削減内訳、工数・業務時間削減（人月/h）、人員変動（名）、顧客・ユーザー増減（社/人）、粗利率・KPI率(pt/%)、システム性能(ms)など、**金額スケールの大小（数千円〜数千億円）や単位を問わず「開始値 ＋ 各増減要因 ＋ 着地値」を持つあらゆる定量的指標**
- **目的**: 開始値（Base）から終了値（Target）に至るまでのプラス要因・マイナス要因の累積インパクトを戦略コンサル標準の増減ステップで可視化する。
- **示唆アノテーション**: 単なる棒グラフではなく、**ステップごとの増減差分と最終着地、およびCAGR・成長率矢印**で示唆（So What?）を語る。
- **数値・高さ厳格比例原則**: 各バーの描画高さ（`height`）は単位・スケールに関わらず表示数値の絶対値に厳密比例（`scale = max_height / max_val`）させ、手打ちの不自然な高さを厳禁とする。コネクタ破線は前ステップのバー端点と同一 `y` 座標に接続する。
- **実装**: 実稼働の完全なサンプルは `corporate_default.html` の Slide 5 を参照。

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: 新機能投入と解約防止により、単価減を吸収してARR +35%成長を達成する |
+-------------------------------------------------------------------+
| [前期ARR: 10.0億]                                                  |
|   └── (+) 新規獲得: +2.8億 (大型エンタープライズ成約)               |
|   └── (+) 解約防止: +1.2億 (CS体制刷新)                            |
|   └── (-) 単価改定影響: -0.5億 (一部ディスカウント)                 |
|   └── [当期目標ARR: 13.5億] (★差分: +3.5億 / CAGR +35%)             |
+-------------------------------------------------------------------+
```

#### スロット定義
- `lead_message`: 全体変動の最大要因と着地数値の完全文
- `base_metric`: 起点数値（名称・金額・比率）
- `breakdown_steps`: 各増減要因（プラス/マイナスの別、要因名、増減数値、背景要因）
- `final_metric`: 着地目標数値、および全体成長率・差分（Difference / CAGR）

#### 骨格HTML構造スニペット
```html
<!-- ウォーターフォール要因分解（完全インラインSVG：要素重なりゼロ保証） -->
<div class="my-auto bg-slate-50/80 rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
  <!-- 決定論的インラインSVG（座標・バー・コネクタ・ラベルが絶対に重ならない） -->
  <div class="w-full">
    <svg viewBox="0 0 960 190" class="w-full h-44">
      <line x1="30" y1="150" x2="930" y2="150" stroke="#cbd5e1" stroke-width="1.5" />
      <line x1="140" y1="80" x2="230" y2="80" stroke="#94a3b8" stroke-dasharray="3,3" />
      <line x1="330" y1="60" x2="430" y2="60" stroke="#94a3b8" stroke-dasharray="3,3" />
      <line x1="530" y1="64" x2="820" y2="64" stroke="#94a3b8" stroke-dasharray="3,3" />
      <!-- Bar 1: 起点 (10.0億 / 70px) -->
      <rect x="40" y="80" width="100" height="70" rx="6" fill="#94a3b8" />
      <text x="90" y="72" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#334155">10.0億</text>
      <text x="90" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">前期</text>
      <text x="90" y="170" text-anchor="middle" font-size="10" fill="#64748b">2025実績</text>
      <!-- Bar 2: 増分 1 (+2.8億 / 20px: y=60〜80) -->
      <rect x="230" y="60" width="100" height="20" rx="6" fill="#10b981" />
      <text x="280" y="52" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#059669">+2.8億</text>
      <text x="280" y="75" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">新規獲得</text>
      <text x="280" y="170" text-anchor="middle" font-size="10" fill="#059669">エンタープライズ</text>
      <!-- Bar 3: 減分 (-0.5億 / 4px: y=60〜64) -->
      <rect x="430" y="60" width="100" height="4" rx="2" fill="#f43f5e" />
      <text x="480" y="52" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#e11d48">-0.5億</text>
      <text x="480" y="170" text-anchor="middle" font-size="10" fill="#64748b">値引影響</text>
      <!-- 境界線 -->
      <line x1="680" y1="20" x2="680" y2="150" stroke="#818cf8" stroke-width="2" stroke-dasharray="4,4" />
      <!-- Bar 4: 着地目標 (12.3億 / 86px: y=64〜150) -->
      <rect x="820" y="64" width="100" height="86" rx="6" fill="#4f46e5" />
      <text x="870" y="54" text-anchor="middle" font-family="monospace" font-size="14" font-weight="900" fill="#4f46e5">12.3億</text>
      <text x="870" y="110" text-anchor="middle" font-size="12" font-weight="black" fill="#ffffff">当期目標</text>
      <text x="870" y="170" text-anchor="middle" font-size="10" font-weight="bold" fill="#4f46e5">+23% YoY</text>
    </svg>
  </div>
  <!-- 下部示唆サマリ -->
  <div class="grid grid-cols-3 gap-3 pt-3 border-t border-slate-100 text-xs">
    <div class="bg-white p-2.5 rounded border border-slate-200"><strong>① 新規獲得:</strong> セキュリティ監査機能で成約率1.8倍</div>
    <div class="bg-white p-2.5 rounded border border-slate-200"><strong>② チャーン低減:</strong> CS自動化で離脱率4.2%→1.1%</div>
    <div class="bg-brand-50 p-2.5 rounded border border-brand-200 text-brand-900 font-medium"><strong>③ So What:</strong> 単価減を量で相殺、利益率78%維持</div>
  </div>
</div>
```

---

### パターン5：【全体像・階層マッピング】（architecture_mapping / Architecture & Layering）
- **主用途**: システム構成説明、業務フロー全体像、組織ロールの可視化（上中下3層）

#### ワイヤーフレーム＆スロット
```text
[Lead: フロントエンドと基幹DBを疎結合化し、API層を中継して認証・ログを統合する]
┌─ 01. Client Layer (利用者UI) ───────▶ Web UI / 現場端末 (HTTPS) ──────────┐
│                                   ▼ (双方向通信)                         │
├─ ★ 02. Gateway & API (CORE結合部) ─▶ API Gateway ⇄ 認証基盤 (gRPC) ──────┤
│                                   ▼ (内部呼出)                           │
└─ 03. Data & Storage (永続化) ──────▶ DB (PostgreSQL) ＋ 監査ログ保管庫 ────┘
スロット: lead_message, layers (name, description), components, interactions
```

#### 骨格HTML構造スニペット
```html
<!-- 3層スタックアーキテクチャ（左: レイヤー定義 / 右: コンポーネント群 ＆ 結合強調） -->
<div class="my-auto flex flex-col space-y-3">
  <!-- Layer 1: Client -->
  <div class="flex items-center gap-4 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
    <div class="w-1/4 shrink-0 font-bold text-xs text-slate-700 uppercase border-r border-slate-200 pr-3">
      <div class="text-brand-600 font-extrabold">01. Client Layer</div>
      <div class="text-[10px] text-slate-500 font-normal">利用者UI</div>
    </div>
    <div class="w-3/4 flex items-center gap-3">
      <div class="flex-1 p-2 bg-white rounded border border-slate-200 text-center text-xs font-bold">社内Webポータル</div>
      <div class="flex-1 p-2 bg-white rounded border border-slate-200 text-center text-xs font-bold">現場端末</div>
      <span class="text-[10px] font-mono bg-slate-200 px-2 py-0.5 rounded">HTTPS</span>
    </div>
  </div>

  <!-- Layer 2: Gateway & Auth (CORE強調) -->
  <div class="flex items-center gap-4 bg-brand-50/60 p-3.5 rounded-xl border-2 border-brand-500 shadow-sm relative">
    <div class="absolute -top-2 right-4 bg-brand-600 text-white text-[9px] font-extrabold px-2 py-0.5 rounded-full">CORE 結合部</div>
    <div class="w-1/4 shrink-0 font-bold text-xs text-brand-900 uppercase border-r border-brand-200 pr-3">
      <div class="text-brand-700 font-extrabold">02. Gateway & API</div>
      <div class="text-[10px] text-brand-600 font-normal">流量制御・認証統合</div>
    </div>
    <div class="w-3/4 flex items-center gap-3">
      <div class="flex-1 p-2 bg-white rounded border border-brand-200 text-center text-xs font-bold text-brand-900">API Gateway</div>
      <div class="flex-1 p-2 bg-white rounded border border-brand-200 text-center text-xs font-bold text-brand-900">認証基盤 (SSO)</div>
      <span class="text-[10px] font-mono bg-brand-200 text-brand-800 px-2 py-0.5 rounded">gRPC</span>
    </div>
  </div>

  <!-- Layer 3: Data -->
  <div class="flex items-center gap-4 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
    <div class="w-1/4 shrink-0 font-bold text-xs text-slate-700 uppercase border-r border-slate-200 pr-3">
      <div class="text-slate-700 font-extrabold">03. Data & Storage</div>
      <div class="text-[10px] text-slate-500 font-normal">永続化・監査ログ</div>
    </div>
    <div class="w-3/4 flex items-center gap-3">
      <div class="flex-1 p-2 bg-white rounded border border-slate-200 text-center text-xs font-bold">トランザクションDB</div>
      <div class="flex-1 p-2 bg-white rounded border border-slate-200 text-center text-xs font-bold">監査ログ保管庫</div>
      <span class="text-[10px] font-mono bg-slate-200 px-2 py-0.5 rounded">暗号化</span>
    </div>
  </div>
</div>
```

---

### パターン6：【境界線・NG/OK対比】（boundary_comparison / Boundary & Best Practices）
- **主用途**: スコープ境界線（In Scope vs Out of Scope）、ポリシー（NG vs OK）、アンチパターン対比（50% : 50%）

#### ワイヤーフレーム＆スロット
```text
[Lead: 今回リリースは基本機能に絞り、外部連携・一括処理はPhase 2へ送る]
┌─ 【対象外 / NG / Out of Scope (50%)】 ─┬─ 【MUST対象 / OK / In Scope (50%)】 ──┐
│ ✕ CSV一括入出力 (Phase 2にて定義)       │ ✓ 単体CRUD操作 (最優先で業務稼働)      │
│ ✕ 外部SaaS・Slack連携 (手動代替可能)    │ ✓ ロール別権限管理 (セキュリティ必須)  │
│ [※追加要望は要件変更申請起案必須]      │ [リリース目標: 2026年11月末本番反映]    │
└────────────────────────────────────────┴────────────────────────────────────────┘
スロット: lead_message, left_items (type, title, reason), right_items (type, title, reason)
```

#### 骨格HTML構造スニペット
```html
<!-- 左右50:50対比（左: 対象外NG / 右: MUST対象OK強調） -->
<div class="grid grid-cols-2 gap-8 my-auto">
  <!-- 左: 対象外 (Out of Scope) -->
  <div class="bg-rose-50/30 rounded-xl p-5 border border-rose-200 flex flex-col justify-between">
    <div>
      <div class="flex justify-between mb-3 text-xs font-bold text-rose-700">
        <span>✕ 対象外 / 今回やらないこと</span><span class="bg-rose-100 px-2 py-0.5 rounded text-[10px]">Phase 2以降</span>
      </div>
      <div class="space-y-3 text-xs">
        <div class="p-2.5 bg-white rounded border border-rose-100">
          <div class="font-bold line-through text-slate-400">1. CSV一括インポート/エクスポート</div>
          <p class="text-[11px] text-slate-500 mt-1">DB直結バッチで暫定対応可能。差分取込は次期策定。</p>
        </div>
        <div class="p-2.5 bg-white rounded border border-rose-100">
          <div class="font-bold line-through text-slate-400">2. 外部SaaS・Slack連携</div>
          <p class="text-[11px] text-slate-500 mt-1">初期は管理画面メール通知で運用代替可能なためカット。</p>
        </div>
      </div>
    </div>
    <div class="mt-3 pt-2 border-t border-rose-200 text-[11px] text-rose-700">※追加要望は要件変更申請（CR）起案のこと</div>
  </div>

  <!-- 右: 対象 (In Scope: 強調) -->
  <div class="bg-white rounded-xl p-5 border-2 border-brand-500 shadow-sm flex flex-col justify-between relative">
    <div class="absolute -top-2.5 left-5 bg-brand-600 text-white text-[10px] font-extrabold px-2.5 py-0.5 rounded-full shadow">
      MUST: 今回コミット対象 (In Scope)
    </div>
    <div class="mt-1 space-y-3 text-xs">
      <div class="p-2.5 bg-brand-50/40 rounded border border-brand-200">
        <div class="flex justify-between font-bold text-brand-900"><span>1. 単体CRUD操作 ＆ 入力バリデーション</span><span class="text-[10px] bg-brand-100 text-brand-700 px-1.5 py-0.5 rounded">最優先</span></div>
        <p class="text-[11px] text-slate-600 mt-1">現場の日常オペレーションを最速で稼働させデータ蓄積を開始。</p>
      </div>
      <div class="p-2.5 bg-brand-50/40 rounded border border-brand-200">
        <div class="flex justify-between font-bold text-brand-900"><span>2. ロール別アクセス権限管理</span><span class="text-[10px] bg-brand-100 text-brand-700 px-1.5 py-0.5 rounded">セキュリティ必須</span></div>
        <p class="text-[11px] text-slate-600 mt-1">個人情報保護・監査ログ要件を満たすための必須要件。</p>
      </div>
    </div>
    <div class="mt-3 pt-2 border-t border-brand-100 text-xs font-bold text-brand-700">リリース目標: 2026年11月末本番反映</div>
  </div>
</div>
```
</wireframe_catalog>

---

<consulting_components_summary>
## 4. 表現強化コンポーネント ＆ 戦略コンサル型 高度パーツ

スライドの表現力を高める各種パーツは、保守性とトークン効率を高めるためモジュール化されています。

### 4.1 基本コンポーネント（Core Components）

#### コンポーネント1：表紙・タイトルスライド (Cover Slide)
- **用途**: プレゼンテーション表紙、セクション扉
- **特徴**: 高級感のあるグラデーション背景、メタ情報（機密区分・日付・発表者）、Action Title
- **実装**: `assets/corporate_default.html` の Slide 1 を正本として参照。

#### コンポーネント2：コンセプト・ビジュアルスプリット (AI生成画像 ＋ 概念解説)
- **用途**: 抽象概念・将来構想・世界観の提示
- **特徴**: 左側にアスペクト比固定のAI画像（Base64インライン埋め込み）、右側に要点解説カード。

```html
<!-- コンセプト画像枠 (Base64インライン埋め込み) ＋ 解説カード -->
<div class="grid grid-cols-2 gap-8 items-center my-auto">
  <div class="image-dropzone relative aspect-video rounded-xl overflow-hidden border border-slate-700 shadow-2xl bg-slate-950">
    <img src="data:image/jpeg;base64,/9j/..." alt="Concept" class="w-full h-full object-cover">
    <div class="absolute bottom-2 left-3 right-3 flex justify-between text-[10px] text-slate-300 font-mono">
      <span class="text-accent-400">Concept Art</span><span class="bg-slate-900/80 px-1.5 py-0.5 rounded no-print">D&Dで変更</span>
    </div>
  </div>
  <div class="space-y-3 text-xs">
    <p class="text-slate-300 leading-relaxed font-light">システム全体像や将来構想を直感提示する要約文。</p>
    <div class="p-3 bg-slate-800/80 rounded border border-slate-700 font-bold text-accent-400">01. リアルタイム連携</div>
    <div class="p-3 bg-slate-800/80 rounded border border-slate-700 font-bold text-brand-400">02. 自然言語IF</div>
  </div>
</div>
```

---

### 4.2 戦略コンサル型 高度示唆コンポーネント（Advanced Visuals）

> 📖 **詳細実装スニペット（Tailwind & SVG）は以下を参照してください**:  
> 👉 [components-consulting.md](./components-consulting.md)

| コンポーネント | 用途・ビジネス意図 | 構文要点 |
| :--- | :--- | :--- |
| **差分矢印・CAGR** | 2指標間の成長率・削減率を直結 | `difference_arrow` |
| **ハーベイボール** | 多軸評価（●◕◐◔○）で優劣可視化 | `harvey_balls` |
| **章トラッカー** | アジェンダ現在地を常時提示 | `agenda_breadcrumbs` |
| **実績 vs 予測境界線** | 過去確定値とシミュレーションを区分 | `actual_forecast_divider` |
| **軸ブレイク波線** | 突出外れ値による縮退を防止 | `axis_break` |
| **2次元マリメッコ** | 横幅（TAM）× 縦高さ（シェア） | `mekko_chart` |
| **ガント・タイムライン** | WBS、工程、Gate関門（◆） | `timeline_milestones` |
| **純粋SVG複合チャート** | 棒（工数）＋ 折れ線（ROI） | Pure Inline SVG |
</consulting_components_summary>

---

<json_schema_spec>
## 5. エージェント用 出力生成フォーマット（JSON Schema）

エージェントが思考プロセスや中間表現としてスライド構造を定義する際は、以下の構造化スキーマに従ってください。

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SlideData",
  "type": "object",
  "properties": {
    "pattern_id": {
      "type": "string",
      "enum": ["executive_summary", "agenda", "problem_solution", "tradeoff_matrix", "step_process", "waterfall_breakdown", "architecture_mapping", "boundary_comparison", "mekko_chart", "timeline_gantt"],
      "description": "社内資料向け骨格パターンの識別子"
    },
    "kicker": { "type": "string", "description": "カテゴリまたは章タイトル" },
    "lead_message": { "type": "string", "description": "結論を含む完全文（Action Title）" },
    "content_slots": { "type": "object", "description": "各パターンのスロット" },
    "footer_note": { "type": "string", "description": "前提、出典等" }
  },
  "required": ["pattern_id", "lead_message", "content_slots"]
}
```
</json_schema_spec>

---

<data_visual_binding_summary>
## 6. データ表からの直接ビジュアル化プロトコル (Data-to-Visual Binding)

> 📖 **詳細変換レシピと実例は以下を参照してください**:  
> 👉 [data-visual-binding.md](./data-visual-binding.md)

ユーザーがプロンプトで数値データ（CSV、TSV、Markdown表、Excelコピー等）を提示した場合、エージェントは手動での再入力を求めず、以下の決定論的ルールで最適パターンへ自動変換してください：

1. **時系列推移・要因データ（開始値、各期増減、着地値）**: ➔ `waterfall_breakdown`（ウォーターフォール型）へ自動バインド
2. **2軸のセグメントデータ（市場規模・シェア構成比）**: ➔ `mekko_chart`（マリメッコ型）へ自動バインド
3. **複数案の採点表・メリデリデータ**: ➔ `tradeoff_matrix`（ハーベイボール付き比較表）へ自動バインド
4. **月次・四半期別タスク・工程データ**: ➔ `timeline_gantt`（マイルストーン付きガント）へ自動バインド
</data_visual_binding_summary>
</slide_pattern_specifications>
