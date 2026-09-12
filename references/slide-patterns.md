# スライドパターン集 (Slide Layout Patterns)

AI（LLM）がスライド内容に応じて選択すべき、代表的なスライドレイアウトのHTML/Tailwind構造パターン集です。

---

## 1. タイトルスライド (Cover Slide)
- **用途**: プレゼンテーション表紙、アジェンダ開始、セクション扉
- **特徴**: 高級感のあるダークグラデーション背景、光彩ブラー効果、信頼感を与えるメタ情報（機密区分・日付・発表者）

```html
<section class="slide p-16 justify-between bg-gradient-to-br from-slate-900 via-brand-950 to-slate-950 text-white border border-slate-800" contenteditable="true">
  <!-- 光彩装飾 -->
  <div class="absolute -right-24 -top-24 w-96 h-96 bg-brand-600/20 rounded-full blur-3xl pointer-events-none"></div>

  <!-- 上部メタ -->
  <div class="flex items-center justify-between z-10">
    <span class="text-xs font-semibold tracking-widest text-accent-400 uppercase">Category Title</span>
    <span class="text-xs font-mono text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full border border-slate-700">CONFIDENTIAL</span>
  </div>

  <!-- タイトル本文 -->
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

  <!-- フッター -->
  <div class="z-10 pt-6 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
    <div>発表部門: 〇〇部 | 日付: 2026年9月</div>
    <div class="font-mono">01 / 05</div>
  </div>
</section>
```

---

## 2. 課題と目指す姿 (Before vs After / 対比スライド)
- **用途**: AS-IS / TO-BE、従来手法と新手法の比較、競合優位性
- **特徴**: 16:9では左右2カラム、4:3では上下2段スタック。赤系（課題）と緑系（解決）のコントラスト。

```html
<div class="grid grid-cols-2 gap-8 my-auto">
  <!-- Before -->
  <div class="bg-white rounded-xl p-6 border border-rose-100 shadow-sm flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-rose-600 font-bold text-sm mb-4">
        <span class="w-6 h-6 rounded-full bg-rose-100 flex items-center justify-center text-xs">✕</span>
        <span>AS-IS: 現行の課題</span>
      </div>
      <ul class="space-y-3 text-sm text-slate-600">
        <li>• 課題項目1の説明テキスト</li>
        <li>• 課題項目2の説明テキスト</li>
      </ul>
    </div>
    <div class="mt-4 p-3 bg-rose-50/70 rounded-lg text-xs text-rose-700 font-medium">
      主要ボトルネックの要約
    </div>
  </div>

  <!-- After -->
  <div class="bg-white rounded-xl p-6 border border-emerald-100 shadow-sm flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-emerald-600 font-bold text-sm mb-4">
        <span class="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center text-xs">✓</span>
        <span>TO-BE: 導入後の姿</span>
      </div>
      <ul class="space-y-3 text-sm text-slate-600">
        <li>• 解決策1の説明テキスト</li>
        <li>• 解決策2の説明テキスト</li>
      </ul>
    </div>
    <div class="mt-4 p-3 bg-emerald-50/70 rounded-lg text-xs text-emerald-700 font-medium">
      期待される定性的効果
    </div>
  </div>
</div>
```

---

## 3. 3層アーキテクチャ / 3カラム機能カード
- **用途**: システム構成図、主要機能の紹介、サービス3つの柱
- **特徴**: 中央のキーカード（CORE）を強調し、視線誘導を行う。

```html
<div class="grid grid-cols-3 gap-6 my-auto">
  <div class="bg-slate-50 rounded-xl p-5 border border-slate-200 flex flex-col justify-between">
    <!-- レイヤー1 -->
  </div>
  <div class="bg-brand-50/50 rounded-xl p-5 border border-brand-200 flex flex-col justify-between relative shadow-sm">
    <div class="absolute -top-3 right-4 bg-brand-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">CORE</div>
    <!-- レイヤー2 (主軸) -->
  </div>
  <div class="bg-slate-50 rounded-xl p-5 border border-slate-200 flex flex-col justify-between">
    <!-- レイヤー3 -->
  </div>
</div>
```

---

## 4. 導入ロードマップ / タイムライン
- **用途**: スケジュール、マイルストーン、導入フェーズ（Phase 1〜4）
- **特徴**: 16:9では横4列、4:3では2×2グリッド。各フェーズのバッジ（M1, M2-3など）と完了指標。

---

## 5. KPI・投資対効果 (Impact & Metrics)
- **用途**: 導入効果、ROI試算、業績指標
- **特徴**: 3つの巨大数値（▲75%, 5倍速, 100%等）と定量的・定性的な補足解説。

---

## 6. コンセプト・ビジュアルスプリット (AI生成画像 ＋ 概念解説)
- **用途**: 抽象概念・将来構想・世界観・テクノロジー進化の提示
- **特徴**: 左側にアスペクト比固定のAI生成画像（DALL-E 3等）コンテナ、右側に洗練された見出し・キーメッセージ・3つの要点カード。画像はブラウザ上でドラッグ＆ドロップ差し替え可能。

```html
<section class="slide p-12 justify-between bg-slate-900 text-white border border-slate-800" contenteditable="true">
  <!-- ヘッダー -->
  <div class="flex items-start justify-between border-b border-slate-800 pb-4">
    <div>
      <div class="text-xs font-bold tracking-wider text-accent-400 uppercase">CONCEPT & VISION</div>
      <h2 class="text-2xl font-extrabold text-white mt-1">次世代データハブがもたらす自律型エコシステム</h2>
    </div>
    <div class="text-xs font-mono text-slate-400 bg-slate-800 px-3 py-1 rounded-md border border-slate-700">VISION</div>
  </div>

  <!-- 2カラムスプリット: 左AI画像 / 右解説 -->
  <div class="grid grid-cols-2 gap-8 items-center my-auto">
    <!-- AI画像枠 (ドラッグ＆ドロップ対応) -->
    <div class="image-dropzone relative aspect-video rounded-xl overflow-hidden border border-slate-700 shadow-2xl bg-slate-950 group">
      <!-- 抽象概念AI画像 (DALL-E 3 等で生成) -->
      <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80" 
           alt="Autonomous Data Hub Concept" 
           class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
      <div class="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-transparent to-transparent pointer-events-none"></div>
      <div class="absolute bottom-3 left-3 right-3 flex items-center justify-between text-[11px] text-slate-300">
        <span class="font-mono text-accent-400">Concept Art: Autonomous Integration</span>
        <span class="bg-slate-900/80 px-2 py-0.5 rounded border border-slate-700 no-print text-[10px]">D&Dで画像変更</span>
      </div>
    </div>

    <!-- 右側テキスト解説 -->
    <div class="flex flex-col justify-center space-y-4">
      <p class="text-sm text-slate-300 leading-relaxed font-light">
        データは単なる「蓄積物」から、現場とAIエージェントがリアルタイムに対話し、自律的な意思決定を導く「活動体」へと進化します。
      </p>
      <div class="space-y-3">
        <div class="p-3.5 bg-slate-800/80 rounded-xl border border-slate-700/80">
          <div class="text-xs font-bold text-accent-400 mb-0.5">01. リアルタイム・シナプス</div>
          <div class="text-xs text-slate-300">全社DBと各SaaSが双方向ストリーミングで常に同期</div>
        </div>
        <div class="p-3.5 bg-slate-800/80 rounded-xl border border-slate-700/80">
          <div class="text-xs font-bold text-brand-400 mb-0.5">02. 自然言語オーケストレーション</div>
          <div class="text-xs text-slate-300">非エンジニアでも社内AIを通じて即座に深層インサイトを抽出</div>
        </div>
      </div>
    </div>
  </div>

  <!-- フッター -->
  <div class="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-500">
    <div>全社次世代データ基盤導入計画</div>
    <div class="font-mono">03 / 05</div>
  </div>
</section>
```

