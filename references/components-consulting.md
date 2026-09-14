# 戦略コンサル型 示唆・高度コンポーネント集 (Executive & Strategic Visual Components)

本書は、スライドに「コンサルティング・ファーム水準の示唆（So What?）」と「高い情報密度」を与えるための高度なUI・ビジュアルコンポーネント集です。
すべて **外部ライブラリ（Chart.js等）を一切使わず、Tailwind CSS ＋ インラインSVG のみ** で単一ファイル完結（Single-File Architecture）する仕様になっています。

---

## 1. コンポーネント一覧と用途

| コンポーネント | 用途・ビジネス意図 | 実装技術 |
| :--- | :--- | :--- |
| **1. 差分矢印・CAGR** | 2指標間の成長率・削減率（So What）を直結 | インラインSVG破線矢印 ＋ バッジ |
| **2. ハーベイボール** | 多軸評価（●◕◐◔○）で全体優劣を一目で可視化 | インラインSVG（満ち欠け円） |
| **3. 章トラッカー** | 全体アジェンダの現在地をヘッダー上部に常時提示 | Flexパンくず ＋ 番号バッジ |
| **4. 実績 vs 予測境界線** | 過去確定値と将来シミュレーションを誠実に区分 | 垂直破線 ＋ To-Beバッジ |
| **5. 軸ブレイク（省略波線）** | 突出した外れ値でグラフ全体が潰れるのを防ぐ | SVG波線 ＋ 分割バー |
| **6. 2次元マリメッコ** | 横幅（TAM規模）× 縦高さ（シェア）の2次元比較 | Tailwind Flex (`w-[..%]`) ＋ スタック |
| **7. ガント・タイムライン** | WBS、四半期工程、重要Gateマイルストーン（◆） | CSS Grid 12分割 ＋ 回転ダイヤ（◆） |
| **8. 純粋SVG複合チャート** | 棒グラフ（工数削減）＋ 折れ線（ROI推移） | Pure Inline SVG (`viewBox`) |

---

## 2. 各コンポーネントのHTML / Tailwindスニペット

### 1. 差分矢印・CAGRアノテーション (Difference & CAGR Arrows)
2つのメトリクスカードや棒グラフの間を繋ぎ、増減率（%）や絶対額差分を明示します。

```html
<div class="flex items-center justify-between gap-4 p-6 bg-slate-50 rounded-xl border border-slate-200">
  <!-- 起点メトリクス -->
  <div class="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex-1 text-center">
    <div class="text-xs font-semibold text-slate-500 mb-1">2024年度 実績</div>
    <div class="font-mono text-2xl font-extrabold text-slate-700">12,400 <span class="text-xs font-normal">時間</span></div>
  </div>

  <!-- 差分アノテーション (Difference Arrow) -->
  <div class="flex flex-col items-center justify-center shrink-0 px-2">
    <span class="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-bold border border-emerald-300 shadow-xs mb-1">
      ▲ -72.5% (削減)
    </span>
    <svg class="w-24 h-4 text-emerald-600 overflow-visible" viewBox="0 0 100 16" fill="none">
      <line x1="0" y1="8" x2="90" y2="8" stroke="currentColor" stroke-width="2" stroke-dasharray="4 2" />
      <polygon points="88,3 98,8 88,13" fill="currentColor" />
    </svg>
    <span class="text-[10px] font-mono text-slate-400 mt-0.5">年次工数差分</span>
  </div>

  <!-- 目標メトリクス (推奨強調) -->
  <div class="p-4 bg-brand-50/70 rounded-lg border-2 border-brand-500 shadow-sm flex-1 text-center">
    <div class="text-xs font-bold text-brand-700 mb-1">2026年度 導入後</div>
    <div class="font-mono text-2xl font-black text-brand-900">3,400 <span class="text-xs font-normal">時間</span></div>
  </div>
</div>
```

---

### 2. ハーベイボール (Harvey Balls / 多軸成熟度評価)
表形式の比較で、満ち欠け（● ◕ ◐ ◔ ○）を用いて評価レベルを直感的に伝えます。

```html
<div class="inline-flex items-center gap-6 p-4 bg-white rounded-xl border border-slate-200 text-xs">
  <!-- 100% / 達成・満点 -->
  <div class="flex items-center gap-2">
    <svg class="w-4 h-4 text-emerald-600" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" /></svg>
    <span class="font-bold text-slate-700">● 100% (完全適合)</span>
  </div>
  <!-- 75% / 高水準 -->
  <div class="flex items-center gap-2">
    <svg class="w-4 h-4 text-brand-600" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" />
      <path d="M12 2 A10 10 0 1 1 2 12 L12 12 Z" fill="currentColor" />
    </svg>
    <span class="font-semibold text-slate-700">◕ 75% (概ね適合)</span>
  </div>
  <!-- 50% / 中間 -->
  <div class="flex items-center gap-2">
    <svg class="w-4 h-4 text-amber-500" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" />
      <path d="M12 2 A10 10 0 0 1 12 22 L12 12 Z" fill="currentColor" />
    </svg>
    <span class="font-medium text-slate-700">◐ 50% (一部対応)</span>
  </div>
  <!-- 25% / 初歩 -->
  <div class="flex items-center gap-2">
    <svg class="w-4 h-4 text-orange-400" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" />
      <path d="M12 2 A10 10 0 0 1 22 12 L12 12 Z" fill="currentColor" />
    </svg>
    <span class="text-slate-600">◔ 25% (要改善)</span>
  </div>
  <!-- 0% / 非対応 -->
  <div class="flex items-center gap-2">
    <svg class="w-4 h-4 text-slate-300" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" /></svg>
    <span class="text-slate-400">○ 0% (非対応)</span>
  </div>
</div>
```

---

### 3. 章トラッカー・進行バー (Agenda Breadcrumbs)
ヘッダー直上に配置し、全体アジェンダの現在地を示します。

```html
<div class="flex items-center gap-2 text-[11px] font-medium text-slate-400 mb-2 border-b border-slate-100 pb-2">
  <span class="flex items-center gap-1 text-slate-500">
    <span class="w-3.5 h-3.5 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center text-[9px] font-bold">✓</span>
    01. 背景・課題
  </span>
  <span class="text-slate-300">›</span>
  <span class="flex items-center gap-1.5 font-bold text-brand-600 bg-brand-50 px-2 py-0.5 rounded border border-brand-200">
    <span class="w-3.5 h-3.5 rounded-full bg-brand-600 text-white flex items-center justify-center text-[9px] font-bold">2</span>
    02. 刷新方針と推奨案
  </span>
  <span class="text-slate-300">›</span>
  <span class="flex items-center gap-1 text-slate-400 opacity-60">
    <span class="w-3.5 h-3.5 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center text-[9px]">3</span>
    03. 投資対効果
  </span>
  <span class="text-slate-300">›</span>
  <span class="flex items-center gap-1 text-slate-400 opacity-60">
    <span class="w-3.5 h-3.5 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center text-[9px]">4</span>
    04. ロードマップ
  </span>
</div>
```

---

### 4. 実績 vs 予測の境界線 (Actuals vs Forecast Divider)
時系列推移やウォーターフォールにおいて、過去確定実績と将来目標シミュレーションを明確に線引きします。

```html
<div class="relative flex items-center justify-between p-6 bg-slate-50 rounded-xl border border-slate-200 overflow-hidden">
  <!-- 左: 実績エリア -->
  <div class="w-1/2 pr-6 flex flex-col justify-between">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs font-bold text-slate-700 bg-slate-200 px-2.5 py-0.5 rounded">実績 (〜FY2025)</span>
      <span class="text-[11px] font-mono text-slate-400">確定監査済み</span>
    </div>
    <div class="flex items-end gap-3 h-32">
      <div class="flex-1 bg-slate-400 rounded-t-lg h-[60%] flex items-center justify-center text-white text-xs font-bold">4.2億</div>
      <div class="flex-1 bg-slate-500 rounded-t-lg h-[80%] flex items-center justify-center text-white text-xs font-bold">5.8億</div>
    </div>
  </div>

  <!-- 中央: 垂直境界線 (Divider) -->
  <div class="absolute left-1/2 top-0 bottom-0 -ml-px w-0 border-l-2 border-dashed border-brand-400 flex flex-col items-center justify-start pt-2 z-10">
    <span class="bg-brand-600 text-white text-[9px] font-black px-2 py-0.5 rounded-full shadow whitespace-nowrap">
      境界線 (To-Be)
    </span>
  </div>

  <!-- 右: 予測エリア -->
  <div class="w-1/2 pl-6 flex flex-col justify-between bg-brand-50/40 -my-6 py-6 border-l border-brand-100">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs font-bold text-brand-700 bg-brand-100 px-2.5 py-0.5 rounded border border-brand-200">目標予測 (FY2026〜)</span>
      <span class="text-[11px] font-mono text-brand-600 font-bold">CAGR +32% 計画</span>
    </div>
    <div class="flex items-end gap-3 h-32">
      <div class="flex-1 bg-brand-500 rounded-t-lg h-[100%] flex items-center justify-center text-white text-xs font-black shadow-sm">8.5億</div>
      <div class="flex-1 bg-gradient-to-t from-brand-600 to-accent-500 rounded-t-lg h-[130%] flex items-center justify-center text-white text-xs font-black shadow-md relative">
        <span class="absolute -top-5 text-brand-700 font-mono font-bold text-xs">11.2億</span>
        ★ Target
      </div>
    </div>
  </div>
</div>
```

---

### 5. 軸ブレイク波線 (Axis Break / Scale Break)
突出した異常値（外れ値）を波線で中途省略し、他指標の比較スケールを保護します。

```html
<div class="flex items-end gap-6 p-6 bg-white rounded-xl border border-slate-200 h-64">
  <!-- 通常バー -->
  <div class="flex flex-col items-center flex-1 h-full justify-end">
    <span class="font-mono text-xs font-bold text-slate-600 mb-1">45時間</span>
    <div class="w-full bg-slate-400 rounded-t-md h-[25%] flex items-center justify-center text-white text-xs font-semibold">通常業務</div>
    <span class="text-[11px] text-slate-400 mt-2">他部署平均</span>
  </div>

  <!-- 外れ値（軸ブレイクバー） -->
  <div class="flex flex-col items-center flex-1 h-full justify-end relative">
    <span class="font-mono text-sm font-black text-rose-600 mb-1">4,800時間 (外れ値)</span>
    <div class="w-full bg-rose-500 rounded-t-md h-[25%] flex items-center justify-center text-white text-xs font-bold shadow-xs">手動転記ロス</div>
    <!-- 省略波線SVG -->
    <div class="w-full h-4 my-0.5 flex items-center justify-center overflow-hidden bg-rose-50">
      <svg class="w-full h-3 text-rose-400" viewBox="0 0 100 12" preserveAspectRatio="none">
        <path d="M0,6 Q25,0 50,6 T100,6" fill="none" stroke="currentColor" stroke-width="2" />
        <path d="M0,10 Q25,4 50,10 T100,10" fill="none" stroke="currentColor" stroke-width="2" />
      </svg>
    </div>
    <div class="w-full bg-rose-500 h-[35%] flex items-center justify-center text-white text-[11px] font-medium">基幹手作業</div>
    <span class="text-[11px] font-bold text-rose-700 mt-2">当部門ボトルネック</span>
  </div>

  <!-- 改善後 -->
  <div class="flex flex-col items-center flex-1 h-full justify-end">
    <span class="font-mono text-xs font-black text-emerald-600 mb-1">0時間</span>
    <div class="w-full bg-emerald-500 rounded-t-md h-[8%] flex items-center justify-center text-white text-[10px] font-bold">自動化</div>
    <span class="text-[11px] font-bold text-emerald-700 mt-2">AINative導入後</span>
  </div>
</div>
```

---

### 6. 2次元マリメッコチャート (Mekko Chart)
横幅（TAM規模）× 縦高さ（シェア構成比）を純粋Tailwindで表現します。

```html
<div class="my-auto bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
  <div class="flex items-center justify-between text-xs mb-3">
    <span class="font-bold text-slate-700">市場セグメント別規模（横幅） ＆ 自社シェア（縦高さ）</span>
    <div class="flex items-center gap-3">
      <span class="flex items-center gap-1 text-[11px]"><span class="w-2.5 h-2.5 rounded bg-brand-600"></span> 自社</span>
      <span class="flex items-center gap-1 text-[11px] text-slate-500"><span class="w-2.5 h-2.5 rounded bg-slate-400"></span> 競合A</span>
      <span class="flex items-center gap-1 text-[11px] text-slate-400"><span class="w-2.5 h-2.5 rounded bg-slate-300"></span> その他</span>
    </div>
  </div>

  <div class="flex items-stretch gap-3 h-52 bg-white p-3 rounded-lg border border-slate-200">
    <!-- カラム1: 50%幅 (500億) -->
    <div class="w-[50%] flex flex-col justify-end h-full relative">
      <div class="absolute -top-5 left-0 right-0 text-center font-mono text-[11px] font-bold text-slate-600">500億円 (50%)</div>
      <div class="h-[60%] bg-brand-600 rounded-t text-white flex flex-col items-center justify-center text-xs font-bold">自社 60%</div>
      <div class="h-[25%] bg-slate-400 text-white flex items-center justify-center text-[10px]">競合A 25%</div>
      <div class="h-[15%] bg-slate-300 text-slate-700 flex items-center justify-center text-[10px]">他 15%</div>
      <span class="text-[11px] font-bold text-slate-700 text-center mt-2">大企業 (成熟)</span>
    </div>

    <!-- カラム2: 30%幅 (300億) -->
    <div class="w-[30%] flex flex-col justify-end h-full relative">
      <div class="absolute -top-5 left-0 right-0 text-center font-mono text-[11px] font-bold text-slate-600">300億円 (30%)</div>
      <div class="h-[30%] bg-brand-500 rounded-t text-white flex flex-col items-center justify-center text-xs font-bold">自社 30%</div>
      <div class="h-[50%] bg-slate-400 text-white flex items-center justify-center text-[10px]">競合A 50%</div>
      <div class="h-[20%] bg-slate-300 text-slate-700 flex items-center justify-center text-[10px]">他 20%</div>
      <span class="text-[11px] font-bold text-slate-700 text-center mt-2">中堅 (激戦)</span>
    </div>

    <!-- カラム3: 20%幅 (200億) - 攻め所強調 -->
    <div class="w-[20%] flex flex-col justify-end h-full relative bg-brand-50/60 rounded p-1 border-2 border-dashed border-brand-400">
      <div class="absolute -top-5 left-0 right-0 text-center font-mono text-[11px] font-black text-brand-700">200億円 (20%)</div>
      <div class="h-[15%] bg-brand-400 rounded-t text-white flex items-center justify-center text-[10px] font-bold">自社 15%</div>
      <div class="h-[15%] bg-slate-400 text-white flex items-center justify-center text-[10px]">競合 15%</div>
      <div class="h-[70%] bg-amber-100 text-amber-900 flex flex-col items-center justify-center text-[10px] font-bold">未開拓 70%</div>
      <span class="text-[11px] font-black text-brand-900 text-center mt-2">SMB (★本提案目標)</span>
    </div>
  </div>
</div>
```

---

### 7. タイムライン＆マイルストーン (Timeline & Milestone)
CSS Grid 12列で四半期スケジュールとトラック、ダイヤマーク（◆）の必須Gateを表現します。

```html
<div class="my-auto bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
  <div class="grid grid-cols-12 text-xs font-bold border-b border-slate-200 pb-2 mb-3 text-slate-600">
    <div class="col-span-3 text-slate-800">推進トラック</div>
    <div class="col-span-2 text-center border-l border-slate-100">Q1</div>
    <div class="col-span-2 text-center border-l border-slate-100">Q2</div>
    <div class="col-span-2 text-center border-l border-slate-100">Q3</div>
    <div class="col-span-3 text-center border-l border-slate-100">Q4</div>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Track 1 -->
    <div class="grid grid-cols-12 items-center gap-1">
      <div class="col-span-3 font-semibold text-slate-800 flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-brand-600"></span>基盤開発
      </div>
      <div class="col-span-9 grid grid-cols-9 h-8 items-center bg-slate-50 rounded-md p-1 relative">
        <div class="col-span-5 bg-brand-600 rounded text-white text-[10px] font-bold flex items-center justify-between px-2 h-6 shadow-xs">
          <span>API統合 ＆ 自律エンジン</span>
          <span class="font-mono">v1.0</span>
        </div>
        <div class="col-span-1 flex justify-center">
          <span class="w-3.5 h-3.5 bg-amber-400 rotate-45 border border-white shadow flex items-center justify-center text-[8px] font-black text-slate-900">◆</span>
        </div>
        <div class="col-span-3 bg-brand-400/80 rounded text-brand-900 text-[10px] font-medium flex items-center px-2 h-6">監視拡充</div>
      </div>
    </div>

    <!-- Track 2 (Gate強調) -->
    <div class="grid grid-cols-12 items-center gap-1">
      <div class="col-span-3 font-semibold text-slate-800 flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-rose-500"></span>セキュリティ監査
      </div>
      <div class="col-span-9 grid grid-cols-9 h-8 items-center bg-slate-50 rounded-md p-1 relative">
        <div class="col-start-4 col-span-3 bg-rose-500 rounded text-white text-[10px] font-bold flex items-center justify-between px-2 h-6 shadow-xs">
          <span>脆弱性診断・審査</span>
        </div>
        <div class="col-span-1 flex justify-center">
          <span class="w-3.5 h-3.5 bg-rose-600 rotate-45 border-2 border-white shadow-md flex items-center justify-center text-[8px] font-black text-white">◆</span>
        </div>
      </div>
    </div>
  </div>

  <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
    <div class="flex items-center gap-4">
      <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-amber-400 rotate-45 inline-block"></span> 開発M</span>
      <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-rose-600 rotate-45 inline-block"></span> ★ 必須品質Gate</span>
    </div>
    <span class="font-bold text-brand-700">12月1日: 全社本番移行完了</span>
  </div>
</div>
```

---

### 8. 純粋SVG複合ビジネスチャート (Inline SVG Combined Chart)
棒グラフ（工数削減量）と折れ線グラフ（累積ROI推移）を外部ライブラリなしで描画します。

```html
<div class="my-auto bg-slate-950/60 rounded-xl p-5 border border-slate-800/90 shadow-inner">
  <svg viewBox="0 0 800 240" class="w-full h-48 overflow-visible">
    <line x1="60" y1="30" x2="760" y2="30" stroke="#334155" stroke-dasharray="3 3" opacity="0.4" />
    <line x1="60" y1="90" x2="760" y2="90" stroke="#334155" stroke-dasharray="3 3" opacity="0.4" />
    <line x1="60" y1="150" x2="760" y2="150" stroke="#334155" stroke-dasharray="3 3" opacity="0.4" />
    <line x1="60" y1="210" x2="760" y2="210" stroke="#475569" stroke-width="1.5" />

    <!-- 棒グラフ -->
    <rect x="120" y="160" width="50" height="50" rx="4" fill="var(--brand-600)" opacity="0.8" />
    <text x="145" y="152" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">1.2k h</text>
    <rect x="270" y="125" width="50" height="85" rx="4" fill="var(--brand-500)" opacity="0.85" />
    <text x="295" y="117" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">2.4k h</text>
    <rect x="420" y="90" width="50" height="120" rx="4" fill="var(--brand-500)" opacity="0.9" />
    <text x="445" y="82" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">3.8k h</text>
    <rect x="570" y="60" width="50" height="150" rx="4" fill="var(--brand-400)" />
    <text x="595" y="52" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">5.2k h</text>

    <!-- 折れ線グラフ -->
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
