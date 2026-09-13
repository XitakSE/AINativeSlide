# AI生成画像（Concept Imagery）設計 & 差し替え仕様書

抽象的な概念や世界観、未来ビジョン（例: データサイロの混乱、AIと人間の協調、セキュアな分散ネットワーク等）をスライド上で直感的に伝えるための、AI画像生成プロンプト設計とHTML内での実装仕様です。

---

## 1. 抽象概念を伝えるAI画像プロンプト設計の原則

ビジネススライドに馴染む洗練された画像を生成するために、以下の要素を英語プロンプトに必ず含めます。

### ① 4大スタイル（テイスト）の選択肢とプロンプト設計規約

プレゼンの目的やターゲット読者層に合わせて、以下の4つの主要テイストから選択します。

1. **リアル・実写・シネマティック系 (Photorealistic / Cinematic 3D)**
   - **特徴**: 高精細な実写写真風、スタジオライティング、重厚なビジネス空間・人物・未来都市。
   - **最適な用途**: 役員・経営会議決裁、投資家ピッチ、重厚なビジョン提示。
   - **プロンプト構文**: `Photorealistic cinematic shot of [主題], dramatic studio lighting, shallow depth of field, high-end corporate aesthetic, 8k resolution, clean composition, no typography, no letters, no text`
   - **例**: `Photorealistic cinematic shot of a modern enterprise executive board reviewing holographic real-time business telemetry, soft ambient lighting, ultra-sharp detail, clean composition, no text`

2. **漫画・コミック・アニメ系 (Manga / Anime / Comic Art)**
   - **特徴**: 親しみやすい線画・ストーリー調、表情豊かなキャラクター、感情や課題の共感を誘う表現。
   - **最適な用途**: 社内研修、現場向け業務改善、採用説明会、ストーリー仕立ての課題・解決策提示。
   - **プロンプト構文**: `Modern Japanese manga comic art style, clean expressive line art, vibrant cel-shaded color palette, relatable business storytelling scene of [主題], modern corporate anime aesthetic, no typography, no letters, no text`
   - **例**: `Modern Japanese manga comic art style, clean expressive line art, vibrant cel-shaded color palette, office team collaborating happily around a simplified smart workflow board, no text`

3. **3D立体アイコン・アイソメトリック系 (3D Isometric / Minimalist 3D Icons)**
   - **特徴**: 粘土・ガラス・プラスチック質感の等角投影3Dモデル、抽象的で洗練された形状。
   - **最適な用途**: システム構成、データパイプライン、クラウド連携、機能一覧の視覚化。
   - **プロンプト構文**: `Minimalist 3D isometric illustration of [主題], smooth clay and frosted glass textures, glowing tech blue and cyan neon accents, dark navy background, clean isometric perspective, 8k render, no typography, no letters, no text`
   - **例**: `Minimalist 3D isometric illustration of fragmented glowing data cubes flowing through crystalline pipelines and unifying into a central radiant prism, deep navy background, sleek glassmorphism, no text`

4. **フラットベクター・ビジネスイラスト系 (Flat Vector / Corporate Art)**
   - **特徴**: シンプルな2D線画・面構成、Notion風やSaaSウェブサイト風の洗練されたミニマルアート。
   - **最適な用途**: サービス紹介、対比図、マーケティング資料、クイック企画書。
   - **プロンプト構文**: `Clean modern flat vector illustration of [主題], minimalist corporate editorial art, bold geometry, elegant subtle color palette, generous negative space, no typography, no letters, no text`
   - **例**: `Clean modern flat vector illustration of interconnected modular gears and analytical graphs, elegant indigo and slate palette, minimalist corporate style, no text`

### ② 文字入れ禁止指示 (No Text Rule)
- AI画像生成モデル（DALL-E 3, Midjourney, Imagen 等）に文字を描かせると崩れたり誤字になりがちです。
- **必ず `clean composition, no typography, no letters, no text watermark` を付加** し、文字はHTML側のTailwindで重ねるか隣接配置します。

### ③ 1スライド1枚の個別生成原則（トリミング使い回しの厳禁）
- 1枚の大きな概念画像を生成し、CSSのトリミング（`object-fit: cover` 等）で複数のスライドに分割・使い回す手抜きは禁止します。
- 画像を配置するスライドには、**必ず1スライドにつき1枚ずつ個別に専用プロンプトで画像を生成し、トリミングなしで配置**します。
- ※ただし、ユーザーからすでに参考画像や製品スクリーンショット等の素材が直接提供された場合は、その画像を優先して配置します。

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
