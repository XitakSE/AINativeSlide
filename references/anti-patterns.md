# HTML生成アンチパターン集 (Anti-Patterns)

AINativeSlide の HTML 生成において、LLM が陥りやすい失敗例（アンチパターン）と、その正しい実装（正解例）をまとめました。
`verify_slide.py` でエラーや警告が出た場合は、このリストを参照して修正してください。

## ❌ アンチパターン1: 編集機能の遮断 (`pointer-events: none`)

スライド要素を「触れないようにする（表示専用）」目的で、CSS に `pointer-events: none` を付与してしまう失敗です。
これをやると、AINativeSlideの最大の強みである「ブラウザ上での直接テキスト編集」が完全に死亡します。

**NGなコード (生成してはいけない)**:
```css
.slide-viewport {
    pointer-events: none; /* 絶対に禁止 */
}
```

**OKなコード**:
（`pointer-events` は一切指定せず、デフォルトのままにするか、親要素に `is-editable` クラスを付与して制御します）

## ❌ アンチパターン2: 外部画像参照 (Single-File 制約違反)

プロジェクトの制約として「全ての要素は単一のHTMLファイル内で完結させる（Zero-Dependency）」必要があります。
外部のURLやローカルの相対パスを `img` タグの `src` に指定すると検証エラーになります。

**NGなコード**:
```html
<!-- 外部URLはエラー -->
<img src="https://example.com/logo.png" alt="Logo">

<!-- ローカルファイル参照もエラー -->
<img src="./assets/images/logo.png" alt="Logo">
```

**OKなコード**:
```html
<!-- SVGのインライン埋め込み (推奨) -->
<svg class="w-8 h-8 text-brand-600" fill="none" viewBox="0 0 24 24">
    <path stroke="currentColor" d="..." />
</svg>

<!-- Base64 Data URI -->
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." alt="Logo">
```

## ❌ アンチパターン3: メタボックスの配置ミス

`slide-meta-box` は、AIへの修正指示を入力するためのUIですが、これをスライド本体（`<section class="slide">`）の内側に配置してしまう失敗です。
これをやると、スライドとして表示した際や印刷時にメタボックスまで見えてしまいます。

**NGなコード**:
```html
<section class="slide p-12">
    <h1>スライドタイトル</h1>
    
    <!-- ❌ スライドの中に入れてはいけない -->
    <div class="slide-meta-box no-print">
        <span>Slide 01 / 01</span>
    </div>
</section>
```

**OKなコード**:
```html
<section class="slide p-12">
    <h1>スライドタイトル</h1>
</section>
<!-- ✅ スライドの直下（外側）に配置する -->
<div class="slide-meta-box no-print">
    <span>Slide 01 / 01</span>
</div>
```

## ❌ アンチパターン4: body から `is-editable` を消去

HTMLの骨格を再生成する際、`body` タグの初期クラスである `is-editable` を書き落としてしまう失敗です。

**NGなコード**:
```html
<body class="bg-slate-50">
```

**OKなコード**:
```html
<body class="bg-slate-50 is-editable text-slate-900 antialiased overflow-hidden flex flex-col h-screen">
```

## ❌ アンチパターン5: 印刷用の余白ゼロ設定の欠落

スライドをPDFとして印刷（保存）する際、ブラウザのデフォルト余白が入らないようにするための設定を消してしまう失敗です。

**NGなコード**:
```css
/* メディアクエリのみで @page がない */
@media print {
    body { background: white; }
}
```

**OKなコード**:
```css
@media print {
    @page {
        size: 16in 9in; /* アスペクト比に合わせる */
        margin: 0;      /* 必須 */
    }
    html, body {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
    }
}
```
