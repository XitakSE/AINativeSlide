# スライド情報構造 ＆ レイアウトパターン集 (Slide Layout & Information Patterns)

本書は、社内向けプレゼンテーション（提案・意思決定、認識合わせ、学習・ナレッジ共有）のスライド構成を自動生成・検証するAIエージェント向けのリファレンス仕様書です。

デザインテンプレート（フォント、配色、余白設計、CIロゴ）は [AINativeSlide-Template-Builder](../../AINativeSlide-Template-Builder/SKILL.md) および `assets/design_templates/` で別管理されている前提とし、エージェントは**「情報構造（ワイヤーフレーム）の選定」「メッセージの論理構築」「スロットへのテキスト配置」**に集中してください。

---

## 1. エージェント行動規範（Anti-AI-Smell Guardrails: 正本/SSOT）

> **📌 Anti-AI-Smell マスター定義（Single Source of Truth）**:
> 本セクションは、生成AI特有の「薄っぺらい整然さ（AIくささ）」を排除するための正本仕様です。
> `SKILL.md` の絶対禁止事項（項目10〜13）および出力前自己検証チェックリストは本書を基準としています。
> エージェントはスライド生成・修正時に以下の規範とリライト指針を厳守してください。

### 1.1 禁止事項（DO NOT）

1. **無意味な3均等カード化の禁止**
   - 3つ並ぶブロックの幅・文字量・強調度をすべて均等に配置してはならない。必ず「推奨案」「最重要課題」「最大のボトルネック」に視覚的アンカー（幅拡張、背景ハイライト、またはフラグ付け）を設定すること。
   - **NG例**: 3枚のカードすべてが同一の `w-1/3 p-4 bg-white border border-slate-200`
   - **OK例**: 推奨案のみ `w-[40%] bg-blue-50/80 border-2 border-blue-500 shadow-md`、他2つは `w-[30%] opacity-80`

2. **抽象バズワードの連呼禁止**
   - 「シナジーの最大化」「シームレスな連携」「DX推進の加速」「柔軟な対応」など、具体のアクションが想起できない語彙を出力してはならない。
   - **NG例**: 「シナジーの最大化により業務効率化とDXを加速」
   - **OK例**: 「受発注データを日次API同期し、月間80時間の手動転記をゼロ化」

3. **飾りアイコンの要求禁止**
   - 文脈と直結しないロケット、電球、握手、歯車などの汎用アイコン配置を指定してはならない。ステータス表示（チェック `✓`、アラート `✕` 等）または既定ロゴに限定すること。
   - **NG例**: アイデアの横に電球アイコン、成長の横にロケットアイコン、提携の横に握手アイコン
   - **OK例**: 状態を示す記号バッジ（`✓ 完了` / `! 要対応` / `✕ 却下`）、矢印（`➔`）、または企業公式ロゴ・実データ数値

4. **トピックタイトル（名詞止め見出し）のみの出力禁止**
   - 「〇〇について」「今後の展望」のようなラベルのみをスライドタイトルにしてはならない。必ずファクトと示唆を含む完全文（Action Title: 40〜60文字・動詞結び）を出力すること。
   - **NG例**: 「2024年度のシステム刷新について」
   - **OK例**: 「受発注基盤をクラウドへ移行し、障害復旧時間を従来の1/4に短縮する」

5. **中途半端な単語分断改行の禁止（Semantic Line Breaking）**
   - コンテナ端に到達した成り行きで、単語の途中や助詞・活用語尾で1〜2文字だけ次行に落ちる中途半端な改行（Bad Wrap）を厳禁とする。
   - 見出し（Action Title: H1/H2）や要約文では、文節（句読点や助詞「〜し、」「〜により、」「〜から、」の切れ目）で明示的に `<br>` を挿入するか、フォントサイズ・幅を微調整して自然な日本語リズムで改行すること。
   - **NG例**: 「破綻しない構造と自律検証でプロ品質を即座に量」/「産する」
   - **OK例**: 「破綻しない構造と自律検証で、」<br>「プロ品質のスライドを即座に量産する」

6. **右肩バッジの複数行折り返し ＆ ヘッダー下部余白ゼロの禁止**
   - 見出しが2行化した際、右肩のメタバッジが押しつぶされて複数行に分断されてはならない（必ず `shrink-0 whitespace-nowrap` を付与し、ヘッダーは `items-start gap-6` 構造とすること）。
   - 見出しが2行化したことで下のメインコンテンツとの余白がゼロ（または数px）になって密着してはならない。必ずヘッダー下部に十分な余白（`mb-5`〜`mb-6`）および視覚的区切り（`pb-3 border-b border-slate-800` 等）を設け、コンテンツとの間に適切な垂直余白（呼吸空間）を確保すること。

7. **外部画像ファイルパス・URL参照の禁止（Single-File純度の死守）**
   - `<img src="./images/..." >` や `<img src="https://..." >` などの外部パス・URL参照を行ってはならない。
   - スライドに画像を配置する場合は、必ず Base64 Data URI（`data:image/jpeg;base64,...` または `data:image/png;base64,...`）として直接インライン埋め込みし、HTMLファイル単体での完全な自己完結性を死守すること。

### 1.2 必須要件（MUST）

1. **リードメッセージ（Action Title）の原則**
   - スライド最上部には、そのスライドが主張する「ファクト＋示唆・結論」を完全な1文（40〜60文字程度、動詞結び）で記述すること。
2. **主語・数値・動作の明記**
   - 「誰が（対象組織・役職）」「何を（対象データ・業務）」「どうする（動詞）」「どれくらい（定量値・期間）」を具体化すること。
3. **対比とメリハリ**
   - 「現状 vs 理想」「自チーム vs 他チーム」「In Scope vs Out of Scope」「NG vs OK」など、比較軸を設けて境界線を引くこと。
4. **ヘッダーとコンテンツの垂直余白の確保**
   - ヘッダー見出しとメインコンテンツの間に `mb-5`〜`mb-6` および `pb-3 border-b border-slate-800` 相当の余白・境界線を設け、視覚的な階層とゆとりを維持すること。

### 1.3 出力前自己検証チェックリスト（詳細内省基準）

一般のエンタープライズ環境（ChatGPT Enterprise, Claude for Work等）では、開発用IDEや外部APIコールは使用できません。エージェント自身が出力直前に以下のチェックリストを用いて「雰囲気・解像度」を自律内省（Reflection）してください。完璧を求める必要はありませんが、現場で伝わる具体性を確保します（`SKILL.md` のクイックチェックリストと連動）。

- [ ] **リード文検証**: リード文は名詞止め（「〇〇について」）ではなく、動詞で終わる完全な文（40〜60文字のAction Title）になっているか？
- [ ] **雰囲気・解像度内省**: 現場担当者が読んだ際に「明日から誰が何をすればよいか」が想起できるか？「シナジー」「シームレス」「最適化」「推進」「共創」「伴走」等の空虚な語句を、具体的な物理動作（「手動入力の廃止」「夜間バッチ同期」「承認者2名体制」等）や定量数値に自律リライトしたか？
- [ ] **均等分割の回避**: 3列以上のレイアウトを採用する場合、強調対象（推奨、関門、最重要）に視覚的アンカー（幅拡張、バッジ、色枠）を設定したか？
- [ ] **余白保護**: テキストを詰め込みすぎていないか？（1スライドあたりの総文字数は日本語で200〜300字以内を推奨、最大700文字厳守）
- [ ] **不要装飾の排除**: 視覚的な飾りアイコン（ロケット、握手、電球等）を排除したか？

---

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

### Tailwind CSS による基本構造スニペット

```html
<section class="slide w-[1280px] h-[720px] p-12 justify-between flex flex-col overflow-hidden relative bg-white border border-slate-200" contenteditable="true">
  <!-- 1. ヘッダー: Kicker & Lead Message (Action Title) -->
  <div class="flex-shrink-0 border-b border-slate-100 pb-3">
    <div class="flex items-center justify-between">
      <span class="text-xs font-bold tracking-wider text-brand-600 uppercase">Kicker / Category Title</span>
      <span class="text-xs font-mono text-slate-400 bg-slate-100 px-2.5 py-0.5 rounded border border-slate-200">CONFIDENTIAL</span>
    </div>
    <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight leading-snug mt-1">
      【Lead Message】ファクトと具体的な示唆・結論を含む完全な1文をここに配置する（40〜60文字）
    </h2>
  </div>

  <!-- 2. メインコンテンツ: Main Content Body (flex-1 min-h-0 で伸縮) -->
  <div class="flex-1 min-h-0 flex flex-col justify-center my-auto py-2">
    <!-- パターン別ワイヤーフレームをここに挿入 -->
  </div>

  <!-- 3. フッター: Footer / Note -->
  <div class="flex-shrink-0 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
    <div class="truncate max-w-[900px]">※注記: 補足前提条件、データ出典、適用スコープ等を記載</div>
    <div class="font-mono text-slate-500 shrink-0">02 / 06</div>
  </div>
</section>
```

---

## 3. 社内資料向け6大情報構造パターン（6 Core Enterprise Wireframes）

### パターン1：課題・打ち手型（Problem & Solution）
- **識別子 (`pattern_id`)**: `problem_solution`
- **主用途**: 業務改善提案、ツール導入起案、施策優先順位の合意
- **目的**: 現状のペインと、そのボトルネックを解消する具体アクションの因果関係を示す。
- **比率**: 左右 40% : 60%（または 50% : 50%）

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: 月間40時間の重複入力を解消するため、マスタ同期スクリプトを導入する |
+---------------------------------+---------------------------------+
| 【現状の課題 / Bottleneck】     | 【解決策 / Action & Solution】  |
| ■ 発生事象 (Fact)               | ■ 実施内容 (To-Be)              |
|   ・スプレッドシートの手動転記   |   ・夜間バッチによる自動同期    |
|   ・月40hの工数ロス             |   ・手動入力フローの完全廃止    |
| ■ 根本原因 (Root Cause)         | ■ 期待効果 (Outcome)            |
|   ・DBと管理表の連携仕様が未策定 |   ・作業工数：月40h → 0h        |
|                                 |   ・転記ミス：月平均5件 → 0件   |
+---------------------------------+---------------------------------+
```

#### スロット定義
- `lead_message`: 施策の目的と導入対象を明記した完全文
- `col_problem`: `fact` (現場で起きている生々しい損失), `root_cause` (根本原因)
- `col_solution`: `action` (誰が何を実装するか), `outcome` (定量的成果指標)

#### HTML / Tailwind スニペット
```html
<div class="grid grid-cols-12 gap-6 my-auto items-stretch">
  <!-- 左: 現状の課題 (40% = cols-5) -->
  <div class="col-span-5 bg-rose-50/40 rounded-xl p-6 border border-rose-200/80 flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-rose-700 font-bold text-sm mb-4">
        <span class="w-6 h-6 rounded-full bg-rose-100 flex items-center justify-center text-xs font-bold text-rose-600">✕</span>
        <span>現状の課題 / Bottleneck</span>
      </div>
      <div class="space-y-4">
        <div>
          <div class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>発生事象 (Fact)
          </div>
          <ul class="space-y-1.5 text-xs text-slate-600 pl-3">
            <li>・スプレッドシートへの手動転記による二重管理</li>
            <li>・締め作業時の整合性確認に月40時間の工数ロス</li>
          </ul>
        </div>
        <div>
          <div class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-rose-400"></span>根本原因 (Root Cause)
          </div>
          <p class="text-xs text-slate-600 pl-3 leading-relaxed">
            基幹DBと現場管理表の連携仕様が未策定のまま個別運用が形骸化していること
          </p>
        </div>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-rose-200/60 text-xs font-bold text-rose-700">
      損失試算: 年間 480時間 / 人件費 約190万円相当
    </div>
  </div>

  <!-- 右: 解決策 (60% = cols-7) -->
  <div class="col-span-7 bg-emerald-50/40 rounded-xl p-6 border border-emerald-200/80 flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-emerald-700 font-bold text-sm mb-4">
        <span class="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center text-xs font-bold text-emerald-600">✓</span>
        <span>解決策 / Action & Solution</span>
      </div>
      <div class="space-y-4">
        <div>
          <div class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>実施内容 (To-Be)
          </div>
          <ul class="space-y-1.5 text-xs text-slate-600 pl-3">
            <li>・Webhookを用いた差分検知による自動同期バッチの常駐</li>
            <li>・手動入力フローの完全廃止とバリデーション機能の一元化</li>
          </ul>
        </div>
        <div>
          <div class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>期待効果 (Outcome)
          </div>
          <div class="grid grid-cols-2 gap-3 pl-3">
            <div class="p-2.5 bg-white rounded-lg border border-emerald-100 shadow-sm">
              <div class="text-[11px] text-slate-500">月間作業工数</div>
              <div class="text-base font-extrabold text-emerald-600">40h → 0h</div>
            </div>
            <div class="p-2.5 bg-white rounded-lg border border-emerald-100 shadow-sm">
              <div class="text-[11px] text-slate-500">転記ミス発生件数</div>
              <div class="text-base font-extrabold text-emerald-600">月5件 → 0件</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-emerald-200/60 text-xs font-bold text-emerald-700 flex justify-between items-center">
      <span>所要導入期間: 3週間</span>
      <span class="text-slate-500 font-normal">担当: データ統括チーム</span>
    </div>
  </div>
</div>
```

---

### パターン2：トレードオフ比較型（Comparison Matrix）
- **識別子 (`pattern_id`)**: `tradeoff_matrix`
- **主用途**: アーキテクチャ選定、ベンダー選定、施策オプションの意思決定
- **目的**: 複数選択肢のメリデリを公正に並べ、推奨案の採用論拠を示す。
- **比率**: 表形式（推奨案列を強調）

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: 運用保守の内製化を最優先とし、初期コスト増を許容して「案B」を採用する |
+--------------+------------------+------------------+--------------+
| 評価軸       | 案A: SaaS導入    | 【推奨】案B: 内製 | 案C: 既存改修 |
+--------------+------------------+------------------+--------------+
| 初期費用     | 低 (50万円)      | 高 (200万円)     | 極小 (10万円) |
| 月額ランコス | 高 (15万円/月)   | サーバー代のみ   | 0円          |
| カスタマイズ | 不可（仕様固定） | 完全自由         | 制限あり     |
| 保守体制     | ベンダー依存     | 自チーム完結     | 属人化継続   |
+--------------+------------------+------------------+--------------+
| 判定・総評   | △ コスト増リスク | ◎ 長期ROI最善    | × 課題未解決 |
+--------------+------------------+------------------+--------------+
```

#### スロット定義
- `lead_message`: 推奨案名と選択における最大のトレードオフ基準（何を捨てて何を取ったか）
- `criteria`: 評価軸リスト（最低3〜4軸）
- `options`: 各案の名称および属性値
- `recommended_option_id`: 強調対象となる列（背景ハイライト、推奨バッジ、色枠）
- `tradeoff_rationale`: 記号（◎◯△）＋ 具体的なデメリット許容理由

#### HTML / Tailwind スニペット
```html
<div class="my-auto overflow-hidden rounded-xl border border-slate-200 shadow-sm bg-white">
  <table class="w-full text-left text-xs border-collapse">
    <thead>
      <tr class="bg-slate-50/80 border-b border-slate-200 text-slate-600">
        <th class="p-3.5 font-bold w-1/4">評価軸</th>
        <th class="p-3.5 font-semibold text-slate-500 w-1/4">案A: SaaSツール導入</th>
        <!-- 推奨案列: 視覚的アンカー -->
        <th class="p-3.5 font-bold text-brand-700 bg-brand-50/70 border-x-2 border-t-2 border-brand-500 w-1/4 relative">
          <span class="absolute -top-2.5 right-3 bg-brand-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full shadow">本提案・推奨</span>
          案B: 基盤内製開発
        </th>
        <th class="p-3.5 font-semibold text-slate-500 w-1/4">案C: 既存システム改修</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-100 text-slate-700">
      <tr class="hover:bg-slate-50/50">
        <td class="p-3 font-bold text-slate-900 bg-slate-50/30">初期開発・導入費</td>
        <td class="p-3 text-slate-600">低 (50万円 / 初期設定のみ)</td>
        <td class="p-3 bg-brand-50/30 border-x-2 border-brand-500 font-medium text-slate-800">高 (200万円 / 開発工数要)</td>
        <td class="p-3 text-slate-600">極小 (10万円 / パッチ当て)</td>
      </tr>
      <tr class="hover:bg-slate-50/50">
        <td class="p-3 font-bold text-slate-900 bg-slate-50/30">月額運用コスト</td>
        <td class="p-3 text-rose-600 font-medium">高 (15万円/月 / アカウント課金)</td>
        <td class="p-3 bg-brand-50/30 border-x-2 border-brand-500 font-bold text-brand-900">極小 (インフラ実費のみ 約1.5万円)</td>
        <td class="p-3 text-slate-600">0円 (追加費用なし)</td>
      </tr>
      <tr class="hover:bg-slate-50/50">
        <td class="p-3 font-bold text-slate-900 bg-slate-50/30">要件適合性・拡張性</td>
        <td class="p-3 text-slate-500">不可 (仕様変更不可)</td>
        <td class="p-3 bg-brand-50/30 border-x-2 border-brand-500 font-bold text-emerald-700">完全自由 (社内独自フローに合致)</td>
        <td class="p-3 text-slate-500">制限あり (既存技術的負債に制約)</td>
      </tr>
      <tr class="hover:bg-slate-50/50">
        <td class="p-3 font-bold text-slate-900 bg-slate-50/30">保守・トラブル対応</td>
        <td class="p-3 text-slate-500">ベンダー依存 (SLA依存)</td>
        <td class="p-3 bg-brand-50/30 border-x-2 border-brand-500 font-semibold text-brand-900">自チーム完結 (即日修正可能)</td>
        <td class="p-3 text-rose-600">属人化継続 (担当退職リスク)</td>
      </tr>
      <tr class="bg-slate-50/60 font-semibold">
        <td class="p-3.5 font-bold text-slate-900">判定・トレードオフ総評</td>
        <td class="p-3 text-amber-700"><span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 text-[11px] font-bold mr-1">△</span> 累積コスト増大リスク</td>
        <td class="p-3 bg-brand-100/60 border-x-2 border-b-2 border-brand-500 text-brand-900 font-bold">
          <span class="px-2 py-0.5 rounded bg-brand-600 text-white text-[11px] font-bold mr-1">◎</span>
          初期費を許容し3年ROI最善
        </td>
        <td class="p-3 text-rose-700"><span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 text-[11px] font-bold mr-1">✕</span> 根本課題が未解決で再発</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

### パターン3：スコープ境界線型（Scope & Boundary）
- **識別子 (`pattern_id`)**: `scope_boundary`
- **主用途**: キックオフ、要件定義、タスク切り出し時の合意形成
- **目的**: 期待値のズレを防ぐため、「やること」以上に「今回はやらないこと」を明文化する。
- **比率**: 左右 50% : 50%

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: 今回リリースは基本機能に絞り、外部連携・一括処理はPhase 2へ送る  |
+---------------------------------+---------------------------------+
| 【対象範囲 / In Scope】         | 【対象外 / Out of Scope】       |
| 1. 単体レコードのCRUD操作       | 1. CSV一括インポート/エクスポート|
|    - 理由: コア業務の早期稼働   |    - 理由: Phase 2にて要件定義   |
| 2. 権限管理 (管理者/一般)       | 2. Slack/Teams通知連携          |
|    - 理由: セキュリティ必須要件 |    - 理由: 手動運用で代替可能    |
+---------------------------------+---------------------------------+
```

#### スロット定義
- `lead_message`: スコープ境界の基準（何を基準に切り分けたか）
- `in_scope_items`: `title` (対象項目名), `reason` (今回含める理由)
- `out_of_scope_items`: `title` (対象外項目名), `handling` (なぜ外すのか／いつ・誰が対応するか)

#### HTML / Tailwind スニペット
```html
<div class="grid grid-cols-2 gap-8 my-auto">
  <!-- In Scope (対象範囲) -->
  <div class="bg-white rounded-xl p-6 border-2 border-brand-500 shadow-sm flex flex-col justify-between relative">
    <div class="absolute -top-3 left-6 bg-brand-600 text-white text-[11px] font-extrabold px-3 py-0.5 rounded-full shadow">
      MUST: 今回リリース対象 (Phase 1)
    </div>
    <div class="mt-2 space-y-4">
      <div class="p-3.5 bg-slate-50 rounded-lg border border-slate-200">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-bold text-slate-900">1. 単体レコードのCRUD操作</span>
          <span class="text-[10px] font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded border border-brand-200">優先度: 高</span>
        </div>
        <p class="text-xs text-slate-600 leading-relaxed">
          <strong>採用理由:</strong> 現場の日常入力業務を即座に稼働させ、最低限のデータ蓄積を最速で開始するため。
        </p>
      </div>
      <div class="p-3.5 bg-slate-50 rounded-lg border border-slate-200">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-bold text-slate-900">2. ロール別アクセス権限管理（管理者/一般）</span>
          <span class="text-[10px] font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded border border-brand-200">優先度: 高</span>
        </div>
        <p class="text-xs text-slate-600 leading-relaxed">
          <strong>採用理由:</strong> 個人情報保護・セキュリティ監査要件を満たすための必須要件。
        </p>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-slate-100 text-xs font-bold text-brand-700">
      リリース目標: 2026年11月末
    </div>
  </div>

  <!-- Out of Scope (対象外) -->
  <div class="bg-slate-50/70 rounded-xl p-6 border border-slate-300 flex flex-col justify-between relative">
    <div class="absolute -top-3 left-6 bg-slate-600 text-white text-[11px] font-bold px-3 py-0.5 rounded-full">
      OUT: 今回は対応しない項目
    </div>
    <div class="mt-2 space-y-4">
      <div class="p-3.5 bg-white rounded-lg border border-slate-200">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-bold text-slate-700 line-through">1. CSV一括インポート / エクスポート</span>
          <span class="text-[10px] text-slate-500 bg-slate-100 px-2 py-0.5 rounded">Phase 2 検討</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed">
          <strong>除外理由 & 対応方針:</strong> データ移行は初回バッチで対応可能。差分取込仕様は次期フェーズ（2027年Q1）で策定。
        </p>
      </div>
      <div class="p-3.5 bg-white rounded-lg border border-slate-200">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-bold text-slate-700 line-through">2. Slack / Teams 通知連携</span>
          <span class="text-[10px] text-slate-500 bg-slate-100 px-2 py-0.5 rounded">手動運用で代替</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed">
          <strong>除外理由 & 対応方針:</strong> 初期はメール通知およびダッシュボード確認で実運用上代替可能なためカット。
        </p>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-slate-200 text-xs text-slate-500 font-medium">
      ※スコープ追加要望がある場合は要件変更申請（Change Request）を起案のこと
    </div>
  </div>
</div>
```

---

### パターン4：全体像・構造マッピング型（Architecture / Layering）
- **識別子 (`pattern_id`)**: `architecture_mapping`
- **主用途**: システム構成説明、業務フロー全体像、組織ロールの可視化
- **目的**: コンポーネント間の依存関係とデータ／情報の流れを俯瞰させる。
- **比率**: 左レイヤーラベル（25%） : 右ブロック構成（75%）

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: フロントエンドと基幹DBを疎結合化し、API層を中継して認証・ログを統合する |
+----------------+--------------------------------------------------+
| Client Layer   | [ Web UI (Next.js) ]      [ Mobile App ]         |
|                |              │                   │               |
|                |              ▼ (REST / HTTPS)    ▼               |
+----------------+--------------------------------------------------+
| Gateway / API  | [ API Gateway ] ─── 認証・認可 (Auth0)           |
|                |              │                                   |
|                |              ▼ (gRPC)                            |
+----------------+--------------------------------------------------+
| Data / Core    | [ Core Service ] ───▶ [ RDS (PostgreSQL) ]       |
+----------------+--------------------------------------------------+
```

#### スロット定義
- `lead_message`: アーキテクチャの変更点、または設計上最も留意すべき結合点
- `layers`: 上下に階層化されたカテゴリ定義
- `components`: 各階層に属する要素名
- `interactions`: 要素間のインターフェース・プロトコル（線やバッジに乗せるラベルテキスト）

#### HTML / Tailwind スニペット
```html
<div class="my-auto flex flex-col space-y-3.5">
  <!-- Layer 1: Client -->
  <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
    <div class="w-1/4 shrink-0 font-bold text-xs text-slate-700 tracking-wider uppercase border-r border-slate-200 pr-4">
      <div class="text-brand-600 font-extrabold">01. Client Layer</div>
      <div class="text-[11px] text-slate-500 font-normal">利用者インターフェース</div>
    </div>
    <div class="w-3/4 flex items-center gap-4">
      <div class="flex-1 p-3 bg-white rounded-lg border border-slate-200 text-center shadow-xs">
        <div class="text-xs font-bold text-slate-800">社内Webポータル (Next.js)</div>
        <div class="text-[10px] text-slate-500 font-mono">PCブラウザ操作</div>
      </div>
      <div class="text-slate-400 text-xs">/</div>
      <div class="flex-1 p-3 bg-white rounded-lg border border-slate-200 text-center shadow-xs">
        <div class="text-xs font-bold text-slate-800">現場モバイル端末</div>
        <div class="text-[10px] text-slate-500 font-mono">バーコード読取</div>
      </div>
      <span class="text-[10px] font-mono bg-slate-200 text-slate-700 px-2 py-1 rounded shrink-0">HTTPS / REST</span>
    </div>
  </div>

  <!-- Arrow Indicator -->
  <div class="flex justify-center -my-2 text-brand-500 font-bold text-xs">↓ 双方向通信</div>

  <!-- Layer 2: Gateway & Auth (CORE強調) -->
  <div class="flex items-center gap-4 bg-brand-50/60 p-4 rounded-xl border-2 border-brand-500 shadow-sm relative">
    <div class="absolute -top-2.5 right-4 bg-brand-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full">
      結合ポイント / CORE
    </div>
    <div class="w-1/4 shrink-0 font-bold text-xs text-brand-900 tracking-wider uppercase border-r border-brand-200 pr-4">
      <div class="text-brand-700 font-extrabold">02. Gateway & API</div>
      <div class="text-[11px] text-brand-600 font-normal">流量制御・認証統合</div>
    </div>
    <div class="w-3/4 flex items-center gap-4">
      <div class="flex-1 p-3 bg-white rounded-lg border border-brand-200 text-center shadow-xs">
        <div class="text-xs font-bold text-brand-900">API Gateway</div>
        <div class="text-[10px] text-slate-500">レートリミット / ルーティング</div>
      </div>
      <div class="text-brand-400 text-xs">⇄</div>
      <div class="flex-1 p-3 bg-white rounded-lg border border-brand-200 text-center shadow-xs">
        <div class="text-xs font-bold text-brand-900">認証・認可基盤 (SSO)</div>
        <div class="text-[10px] text-slate-500">SAML / OIDC / トークン検証</div>
      </div>
      <span class="text-[10px] font-mono bg-brand-200 text-brand-800 px-2 py-1 rounded shrink-0">gRPC / mTLS</span>
    </div>
  </div>

  <!-- Arrow Indicator -->
  <div class="flex justify-center -my-2 text-brand-500 font-bold text-xs">↓ 内部呼出</div>

  <!-- Layer 3: Data / Storage -->
  <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
    <div class="w-1/4 shrink-0 font-bold text-xs text-slate-700 tracking-wider uppercase border-r border-slate-200 pr-4">
      <div class="text-slate-700 font-extrabold">03. Data & Storage</div>
      <div class="text-[11px] text-slate-500 font-normal">永続化・監査ログ</div>
    </div>
    <div class="w-3/4 flex items-center gap-4">
      <div class="flex-1 p-3 bg-white rounded-lg border border-slate-200 text-center shadow-xs">
        <div class="text-xs font-bold text-slate-800">トランザクションDB (PostgreSQL)</div>
        <div class="text-[10px] text-slate-500">Multi-AZ高可用性</div>
      </div>
      <div class="text-slate-400 text-xs">+</div>
      <div class="flex-1 p-3 bg-white rounded-lg border border-slate-200 text-center shadow-xs">
        <div class="text-xs font-bold text-slate-800">監査ログ保管庫 (Object Storage)</div>
        <div class="text-[10px] text-slate-500">改ざん防止・10年保管</div>
      </div>
      <span class="text-[10px] font-mono bg-slate-200 text-slate-700 px-2 py-1 rounded shrink-0">暗号化保存</span>
    </div>
  </div>
</div>
```

---

### パターン5：ステップ・プロセス型（Sequential Workflow）
- **識別子 (`pattern_id`)**: `step_process`
- **主用途**: 業務運用手順、リリース手順、障害発生時対応、オンボーディング
- **目的**: 時系列の手順と、各ステップの入力・出力・関門（チェックポイント）を示す。
- **比率**: 3〜4ステップの横並び

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: Step 2のレビュー承認を完了するまで本番マージ・デプロイは不可 |
+-----------------+-----------------+-----------------+-------------+
| Step 1: 実装    | Step 2: レビュー| Step 3: ステージ | Step 4: 本番|
+-----------------+-----------------+-----------------+-------------+
| [作業]          | [作業]          | [作業]          | [作業]      |
| ブランチ作成    | PR作成・2名承認 | 自動テスト実行  | 手動承認    |
| ローカル検証    |                 | E2E確認         | デプロイ    |
+-----------------+-----------------+-----------------+-------------+
| [Output]        | [★Gate]        | [Output]        | [Goal]      |
| PRドラフト      | コード承認ログ  | 検証完了サイン  | 本番反映    |
+-----------------+-----------------+-----------------+-------------+
```

#### スロット定義
- `lead_message`: 所要時間目安、または最も留意すべき関門の明示
- `steps`: `step_number`, `title`, `tasks`, `gate_or_output`

#### HTML / Tailwind スニペット
```html
<div class="grid grid-cols-4 gap-4 my-auto">
  <!-- Step 1 -->
  <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
        <span class="text-xs font-mono font-bold text-slate-400">STEP 01</span>
        <span class="text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">開発担当</span>
      </div>
      <div class="text-xs font-bold text-slate-900 mb-2">実装 & 単体検証</div>
      <ul class="space-y-1.5 text-[11px] text-slate-600">
        <li>・featureブランチ作成</li>
        <li>・単体テストカバレッジ80%</li>
        <li>・静的解析ツールの通過</li>
      </ul>
    </div>
    <div class="mt-4 pt-2.5 border-t border-slate-100 text-[11px] font-medium text-slate-500">
      <span class="text-slate-400">成果物:</span> PRドラフト
    </div>
  </div>

  <!-- Step 2: Critical Gate (視覚的アンカー強調) -->
  <div class="bg-brand-50/60 rounded-xl p-4 border-2 border-brand-500 shadow-md flex flex-col justify-between relative">
    <div class="absolute -top-2.5 right-3 bg-brand-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full shadow">
      ★ 必須関門 (Gate)
    </div>
    <div>
      <div class="flex items-center justify-between border-b border-brand-200/80 pb-2 mb-3">
        <span class="text-xs font-mono font-bold text-brand-700">STEP 02</span>
        <span class="text-[10px] font-bold text-brand-700 bg-brand-100 px-2 py-0.5 rounded">レビュアー2名</span>
      </div>
      <div class="text-xs font-bold text-brand-900 mb-2">コードレビュー & 承認</div>
      <ul class="space-y-1.5 text-[11px] text-slate-700">
        <li>・設計整合性・セキュリティ確認</li>
        <li>・シニアエンジニア2名以上のApprove</li>
        <li>・差分コメント全解決</li>
      </ul>
    </div>
    <div class="mt-4 pt-2.5 border-t border-brand-200 text-[11px] font-bold text-brand-800">
      通過条件: 承認ログ ＋ CI通過
    </div>
  </div>

  <!-- Step 3 -->
  <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
        <span class="text-xs font-mono font-bold text-slate-400">STEP 03</span>
        <span class="text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">QAチーム</span>
      </div>
      <div class="text-xs font-bold text-slate-900 mb-2">ステージング検証</div>
      <ul class="space-y-1.5 text-[11px] text-slate-600">
        <li>・自動E2Eシナリオ実行</li>
        <li>・本番相当データでの負荷確認</li>
        <li>・ステークホルダー受入確認</li>
      </ul>
    </div>
    <div class="mt-4 pt-2.5 border-t border-slate-100 text-[11px] font-medium text-slate-500">
      <span class="text-slate-400">成果物:</span> 検証完了サイン
    </div>
  </div>

  <!-- Step 4 -->
  <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
        <span class="text-xs font-mono font-bold text-slate-400">STEP 04</span>
        <span class="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">リリース責任者</span>
      </div>
      <div class="text-xs font-bold text-slate-900 mb-2">本番適用 & 監視</div>
      <ul class="space-y-1.5 text-[11px] text-slate-600">
        <li>・カナリアデプロイ実施</li>
        <li>・エラートラッキング監視 (30分)</li>
        <li>・完了アナウンス発行</li>
      </ul>
    </div>
    <div class="mt-4 pt-2.5 border-t border-slate-100 text-[11px] font-bold text-emerald-700">
      Goal: 正常稼働サインオフ
    </div>
  </div>
</div>
```

---

### パターン6：落とし穴・FAQ型（Pitfalls & Best Practices）
- **識別子 (`pattern_id`)**: `pitfalls_faq`
- **主用途**: ガイドライン周知、トラブルシューティング、開発規約の定着
- **目的**: よくある失敗（アンチパターン）と推奨される正しい行動の対比。
- **比率**: 左右のNG/OK対比カード

#### ワイヤーフレーム
```text
+-------------------------------------------------------------------+
| Lead: 環境変数はコードにハードコードせず、必ず.env経由でSecrets管理に逃がす |
+---------------------------------+---------------------------------+
| × よくある誤り (Anti-Pattern)   | ○ 正しい実装 (Best Practice)    |
| const API_KEY = "xyz123...";   | const API_KEY = process.env...; |
| 【なぜNGか】                    | 【運用のポイント】              |
| ・リポジトリ公開時に流出する    | ・.envは.gitignoreに必須追加    |
| ・環境ごとの切替ができない      | ・CI/CD環境側のVariablesで注入  |
+---------------------------------+---------------------------------+
```

#### スロット定義
- `lead_message`: 最も周知したい原則的ルール
- `anti_pattern`: `snippet_or_fact`, `why_bad`
- `best_practice`: `correct_action`, `key_point`

#### HTML / Tailwind スニペット
```html
<div class="grid grid-cols-2 gap-8 my-auto">
  <!-- × Anti-Pattern (NG) -->
  <div class="bg-rose-50/30 rounded-xl p-6 border border-rose-200 flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-rose-700 font-bold text-sm mb-3">
        <span class="w-6 h-6 rounded-full bg-rose-100 flex items-center justify-center text-xs font-bold text-rose-600">✕</span>
        <span>よくある誤り (Anti-Pattern)</span>
      </div>
      <div class="p-3 bg-slate-900 text-rose-300 font-mono text-[11px] rounded-lg border border-slate-800 mb-4 overflow-x-auto">
        const API_KEY = "sk_live_9384729384...";<br>
        // ソースコード内に秘密鍵を直接ハードコード
      </div>
      <div class="space-y-2">
        <div class="text-xs font-bold text-rose-900">【なぜNGなのか】</div>
        <ul class="space-y-1 text-xs text-slate-600 pl-3">
          <li>・GitHubへの誤Push時に即座に全世界へクレデンシャルが流出</li>
          <li>・開発・検証・本番環境ごとのクレデンシャル切り替えが不可能</li>
          <li>・鍵ローテーション時に全アプリケーションの再ビルド・再デプロイが必須</li>
        </ul>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-rose-200/60 text-xs font-bold text-rose-700">
      リスク: インシデント発生・即時失効対応の発生
    </div>
  </div>

  <!-- ○ Best Practice (推奨) -->
  <div class="bg-emerald-50/30 rounded-xl p-6 border-2 border-emerald-500 shadow-sm flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2 text-emerald-700 font-bold text-sm">
          <span class="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center text-xs font-bold text-emerald-600">✓</span>
          <span>正しい実装 (Best Practice)</span>
        </div>
        <span class="text-[10px] font-extrabold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">社内標準</span>
      </div>
      <div class="p-3 bg-slate-900 text-emerald-300 font-mono text-[11px] rounded-lg border border-slate-800 mb-4 overflow-x-auto">
        const API_KEY = process.env.SERVICE_API_KEY;<br>
        if (!API_KEY) throw new Error("API_KEY missing");
      </div>
      <div class="space-y-2">
        <div class="text-xs font-bold text-emerald-900">【運用のポイント】</div>
        <ul class="space-y-1 text-xs text-slate-700 pl-3">
          <li>・ローカル環境では <code>.env.local</code> を使用し、必ず <code>.gitignore</code> に指定</li>
          <li>・CI/CD環境では Secret Manager / Vault より実行時に動的注入</li>
          <li>・起動時のNullチェックを徹底し、不整合状態での起動を即座にフェイル</li>
        </ul>
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-emerald-200/60 text-xs font-bold text-emerald-800">
      メリット: 安全な鍵運用 ＆ 環境差異の完全吸収
    </div>
  </div>
</div>
```

---

## 4. 表現強化コンポーネント（Visual Components）

### コンポーネント1：表紙・タイトルスライド (Cover Slide)
- **用途**: プレゼンテーション表紙、セクション扉
- **特徴**: 高級感のあるダークグラデーション背景、メタ情報（機密区分・日付・発表者）

```html
<section class="slide p-16 justify-between bg-gradient-to-br from-slate-900 via-brand-950 to-slate-950 text-white border border-slate-800" contenteditable="true">
  <div class="flex items-center justify-between z-10">
    <span class="text-xs font-semibold tracking-widest text-accent-400 uppercase">Category Title</span>
    <span class="text-xs font-mono text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full border border-slate-700">CONFIDENTIAL</span>
  </div>

  <div class="z-10 my-auto">
    <div class="inline-block px-3.5 py-1 rounded-md bg-brand-500/20 border border-brand-400/30 text-brand-300 text-xs font-semibold mb-4">
      PROJECT PROPOSAL
    </div>
    <h1 class="text-5xl font-extrabold tracking-tight text-white leading-tight mb-4">
      メインタイトルをここに記載<br>
      <span class="text-transparent bg-clip-text bg-gradient-to-r from-accent-400 to-indigo-200">サブキャッチコピー</span>
    </h1>
    <p class="text-lg text-slate-300 max-w-2xl font-light leading-relaxed">
      この企画が達成する目的、背景、および想定されるインパクトの要約文
    </p>
  </div>

  <div class="z-10 pt-6 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
    <div>発表部門: 〇〇部 | 日付: 2026年9月</div>
    <div class="font-mono">01 / 05</div>
  </div>
</section>
```

---

### コンポーネント2：純粋インラインSVGビジネスチャート (Inline SVG Chart & Metrics)
- **用途**: 投資対効果（ROI）推移、月次削減工数、業績予測
- **特徴**: 外部JSライブラリ不要（Pure Inline SVG）。CSS変数（`var(--brand-500)` 等）と完全同期。

```html
<div class="my-auto bg-slate-950/60 rounded-xl p-5 border border-slate-800/90 shadow-inner">
  <svg viewBox="0 0 800 240" class="w-full h-48 overflow-visible">
    <!-- グリッド線 -->
    <line x1="60" y1="30" x2="760" y2="30" stroke="#334155" stroke-dasharray="3 3" opacity="0.4" />
    <line x1="60" y1="90" x2="760" y2="90" stroke="#334155" stroke-dasharray="3 3" opacity="0.4" />
    <line x1="60" y1="150" x2="760" y2="150" stroke="#334155" stroke-dasharray="3 3" opacity="0.4" />
    <line x1="60" y1="210" x2="760" y2="210" stroke="#475569" stroke-width="1.5" />

    <!-- 棒グラフ (工数削減) -->
    <rect x="120" y="160" width="50" height="50" rx="4" fill="var(--brand-600)" opacity="0.8" />
    <text x="145" y="152" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">1.2k h</text>

    <rect x="270" y="125" width="50" height="85" rx="4" fill="var(--brand-500)" opacity="0.85" />
    <text x="295" y="117" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">2.4k h</text>

    <rect x="420" y="90" width="50" height="120" rx="4" fill="var(--brand-500)" opacity="0.9" />
    <text x="445" y="82" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">3.8k h</text>

    <rect x="570" y="60" width="50" height="150" rx="4" fill="var(--brand-400)" />
    <text x="595" y="52" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">5.2k h</text>

    <!-- 折れ線グラフ (累積ROI) -->
    <polyline points="145,190 295,140 445,85 595,45" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    <circle cx="145" cy="190" r="4" fill="#10b981" stroke="#fff" stroke-width="1.5" />
    <circle cx="295" cy="140" r="4" fill="#10b981" stroke="#fff" stroke-width="1.5" />
    <circle cx="445" cy="85" r="4" fill="#10b981" stroke="#fff" stroke-width="1.5" />
    <circle cx="595" cy="45" r="5" fill="#34d399" stroke="#fff" stroke-width="2" />

    <!-- X軸ラベル -->
    <text x="145" y="230" fill="#94a3b8" font-size="11" font-weight="semibold" text-anchor="middle">2026 (導入期)</text>
    <text x="295" y="230" fill="#94a3b8" font-size="11" font-weight="semibold" text-anchor="middle">2027 (展開期)</text>
    <text x="445" y="230" fill="#94a3b8" font-size="11" font-weight="semibold" text-anchor="middle">2028 (定着期)</text>
    <text x="595" y="230" fill="#94a3b8" font-size="11" font-weight="semibold" text-anchor="middle">2029 (自律運用期)</text>
  </svg>
</div>
```

---

### コンポーネント3：コンセプト・ビジュアルスプリット (AI生成画像 ＋ 概念解説)
- **用途**: 抽象概念・将来構想・世界観の提示
- **特徴**: 左側にアスペクト比固定のAI画像（D&D差し替え対応）、右側に要点解説カード。

```html
<div class="grid grid-cols-2 gap-8 items-center my-auto">
  <!-- AI画像枠 (ドラッグ＆ドロップ対応) -->
  <div class="image-dropzone relative aspect-video rounded-xl overflow-hidden border border-slate-700 shadow-2xl bg-slate-950 group">
    <!-- 画像はBase64 Data URIで直接インライン埋め込み（完全単一ファイル完結） -->
    <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/..." alt="Concept Imagery" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
    <div class="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-transparent to-transparent pointer-events-none"></div>
    <div class="absolute bottom-3 left-3 right-3 flex items-center justify-between text-[11px] text-slate-300">
      <span class="font-mono text-accent-400">Concept Art</span>
      <span class="bg-slate-900/80 px-2 py-0.5 rounded border border-slate-700 no-print text-[10px]">D&Dで画像変更</span>
    </div>
  </div>

  <!-- 右側テキスト解説 -->
  <div class="flex flex-col justify-center space-y-4">
    <p class="text-sm text-slate-300 leading-relaxed font-light">
      システム全体像や将来構想を直感的に提示するための解説文。
    </p>
    <div class="space-y-3">
      <div class="p-3.5 bg-slate-800/80 rounded-xl border border-slate-700/80">
        <div class="text-xs font-bold text-accent-400 mb-0.5">01. リアルタイム連携</div>
        <div class="text-xs text-slate-300">全社DBと各SaaSが即時ストリーミングで常時同期</div>
      </div>
      <div class="p-3.5 bg-slate-800/80 rounded-xl border border-slate-700/80">
        <div class="text-xs font-bold text-brand-400 mb-0.5">02. 自然言語インターフェース</div>
        <div class="text-xs text-slate-300">現場担当者が社内AIを通じて即座にインサイトを抽出</div>
      </div>
    </div>
  </div>
</div>
```

---

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
      "enum": [
        "problem_solution",
        "tradeoff_matrix",
        "scope_boundary",
        "architecture_mapping",
        "step_process",
        "pitfalls_faq"
      ],
      "description": "社内資料向け6大パターンのいずれかの識別子"
    },
    "kicker": {
      "type": "string",
      "description": "カテゴリまたは章タイトル（10〜20文字）"
    },
    "lead_message": {
      "type": "string",
      "description": "結論・示唆を含む完全文（40〜60文字、動詞結びのAction Title）"
    },
    "content_slots": {
      "type": "object",
      "description": "各パターンに定義されたスロットごとのキー・バリュー"
    },
    "footer_note": {
      "type": "string",
      "description": "前提、出典、対象バージョン等（省略可）"
    }
  },
  "required": ["pattern_id", "lead_message", "content_slots"]
}
```
