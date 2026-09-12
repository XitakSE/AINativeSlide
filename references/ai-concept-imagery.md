# AI生成画像（Concept Imagery）設計 & 差し替え仕様書

抽象的な概念や世界観、未来ビジョン（例: データサイロの混乱、AIと人間の協調、セキュアな分散ネットワーク等）をスライド上で直感的に伝えるための、AI画像生成プロンプト設計とHTML内での実装仕様です。

---

## 1. 抽象概念を伝えるAI画像プロンプト設計の原則

ビジネススライドに馴染む洗練された画像を生成するために、以下の要素を英語プロンプトに必ず含めます。

### ① スタイルの指定（過剰なフォトリアルや稚拙なイラストを避ける）
- **3D Isometric Minimalist**: 等角投影の立体モデル。アーキテクチャやデータの流れに最適。
- **Abstract Glassmorphism & Neon Glow**: 暗めの背景に半透明ガラスと光のライン。テック・AI・サイバーセキュリティに最適。
- **Clean Vector / Corporate Flat Art**: ミニマルで知的。課題対比やビジネスシーンに最適。
- **Cinematic Conceptual 3D**: 重厚感と未来感。表紙やビジョン提示に最適。

### ② 文字入れ禁止指示 (No Text Rule)
- AI画像生成モデル（DALL-E 3, Midjourney, Imagen 等）に文字を描かせると崩れたり誤字になりがちです。
- **必ず `clean composition, no typography, no letters, no text watermark` を付加** し、文字はHTML側のTailwindで重ねるか隣接配置します。

### ③ プロンプトのテンプレート例
> **テーマ: サイロ化されたデータが1つのコアへ統合される抽象概念**  
> `Abstract 3D isometric visualization of fragmented glowing data cubes flowing through crystalline pipelines and unifying into a central radiant prism. Dark navy background, glowing violet and cyan neon accents, sleek glassmorphism textures, clean composition, minimalist tech aesthetic, 8k render, no text, no letters.`

---

## 2. HTMLスライド内での画像コンテナ仕様

画像のアスペクト比を固定し、文字との重なりや印刷時の崩れを防ぐためのCSS/Tailwind設計です。

### パターン A: 左右スプリット（左: AI画像 / 右: 概念解説）
```html
<div class="grid grid-cols-2 gap-8 items-center my-auto">
  <!-- AI画像コンテナ (ドラッグ＆ドロップ対応) -->
  <div class="image-dropzone relative aspect-video rounded-xl overflow-hidden border border-slate-700/50 shadow-xl bg-slate-900 group">
    <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80" 
         alt="AI Concept Art" 
         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
    <div class="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-transparent"></div>
    <span class="absolute bottom-3 left-3 text-[10px] font-mono text-slate-300 bg-slate-900/80 px-2 py-0.5 rounded border border-slate-700 no-print">
      画像をドラッグ＆ドロップで差し替え
    </span>
  </div>

  <!-- 右側テキスト解説 -->
  <div class="flex flex-col justify-center">
    <span class="text-xs font-bold text-brand-600 uppercase tracking-wider mb-2">Concept Vision</span>
    <h3 class="text-2xl font-extrabold text-slate-900 mb-4">自律型データハブ構想</h3>
    <p class="text-sm text-slate-600 leading-relaxed mb-4">...</p>
  </div>
</div>
```

---

## 3. ブラウザ直接画像差し替え機能（Drag & Drop JS）

職場のプレーンなブラウザ環境でも、デスクトップから画像をスライド上の枠にドラッグ＆ドロップするだけで、その場で画像が差し替わる軽量スクリプトを `template_base.html` に標準搭載します。

```javascript
// 画像ドラッグ＆ドロップ差し替えスクリプト
document.addEventListener('DOMContentLoaded', () => {
  const dropzones = document.querySelectorAll('.image-dropzone');
  
  dropzones.forEach(zone => {
    zone.addEventListener('dragover', (e) => {
      e.preventDefault();
      zone.classList.add('ring-2', 'ring-brand-500');
    });

    zone.addEventListener('dragleave', () => {
      zone.classList.remove('ring-2', 'ring-brand-500');
    });

    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('ring-2', 'ring-brand-500');
      
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
          const img = zone.querySelector('img');
          if (img) {
            img.src = event.target.result;
          }
        };
        reader.readAsDataURL(file);
      }
    });
  });
});
```
- **特徴**: サーバー通信なし。ローカルの `FileReader` で即座に DataURL に変換して `<img src="...">` を更新。
- 印刷（`window.print()`）時にもそのまま高解像度でPDFに埋め込まれます。
