# スライド比率・印刷CSS仕様書 (Ratio & Print Specifications)

ブラウザ上での快適な閲覧・直接編集と、PDFエクスポート（印刷）時のピクセルパーフェクトな出力を両立するための厳格なCSS仕様です。

---

## 1. アスペクト比ごとの寸法仕様

| アスペクト比 | 用途・特徴 | 画面表示サイズ | 印刷 `@page size` | 印刷メディアクエリサイズ |
| :--- | :--- | :--- | :--- | :--- |
| **16:9**（デフォルト） | ワイド画面・モダンディスプレイ・Web投影 | `width: 1280px;`<br>`height: 720px;` | `@page { size: 16in 9in; margin: 0; }` | `.slide { width: 16in !important; height: 9in !important; }` |
| **4:3** | 既存資料踏襲・紙配布中心・正方形ディスプレイ | `width: 1024px;`<br>`height: 768px;` | `@page { size: 4in 3in; margin: 0; }` | `.slide { width: 4in !important; height: 3in !important; }` |

---

## 2. 印刷（PDF出力）CSSの必須ルール

Chromium系ブラウザ（Chrome, Edge等）において、**余白ゼロ・改ページずれゼロ・スライド1枚につきぴったり1ページ** でPDF化するために、以下のCSSルールを必ず含めます。

```css
/* 1. @page ルール（16:9 または 4:3 を指定） */
@page {
  size: 16in 9in; /* 4:3の場合は size: 4in 3in; */
  margin: 0;
}

/* 2. @media print ルール */
@media print {
  html, body {
    background-color: transparent !important;
    margin: 0 !important;
    padding: 0 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  /* 操作ツールバーや不要なUIを完全非表示 */
  .no-print {
    display: none !important;
  }

  /* スライドコンテナの余白やFlex/Gridの隙間をゼロ化 */
  .slide-viewport {
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
    display: block !important;
  }

  /* 各スライド要素の完全フィット & 強制改ページ */
  .slide {
    /* 16:9の場合: 16in / 9in。4:3の場合: 4in / 3in */
    width: 16in !important;
    height: 9in !important;
    max-width: none !important;
    max-height: none !important;
    margin: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    
    /* 改ページ制御（複数ブラウザ互換） */
    page-break-after: always !important;
    break-after: page !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
}
```

---

## 3. なぜ `size: 16in 9in` かつ `.slide { width: 16in; height: 9in; }` なのか？

- **インチ指定の利点**:
  Chromiumの印刷エンジンは、`size: 16in 9in` のような物理インチ単位に対して高精度なベクター解像度（72pt/in = 1152×648pt）でページを割り当てます。
  スライド自体の幅・高さを同じ `16in / 9in` に設定することで、ブラウザの自動スケーリング誤差による「ページの端に1pxの白い隙間ができる」「2ページ目に空行がはみ出す」といったトラブルを根本から防止します。

- **画面表示時のピクセル指定**:
  画面表示時はディスプレイの解像度に合わせて `1280px × 720px`（4:3なら `1024px × 768px`）の固定ボックスにし、`box-shadow` や角丸（`rounded-lg`）を付与することで、まるでFigmaやKeynoteのキャンバスを操作しているかのような快適な作業体験を提供します。
