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

### ④ アスペクト比の事前同期による完全ノーカット原則（Zero-Cropping Rule）
- 画像生成プロンプトには、スライドコンテナの表示比率に合わせたアスペクト比を必ず明記します：
  - **16:9 ワイド（左右スプリット / 全画面）**: `widescreen 16:9 composition, landscape aspect ratio`
  - **4:3 標準**: `standard 4:3 composition, landscape aspect ratio`
  - **A4 横 / A4 縦**: `balanced composition matching container ratio`
- コンテナ枠と生成画像のアスペクト比を事前に完全一致させることで、CSSトリミング（`object-cover` による上下左右の切り落とし）を一切発生させず、生成された構図を100%そのまま美しく表示します。

### ⑤ デッキ全体の一貫性を保つ「シードスタイル記述子（Seed Style）」
複数スライドで画像を生成する際、画風のブレを防ぐため、全スライドの画像プロンプトに共通のシードスタイル（基調色・照明・質感）を一貫して注入します：
- 例（3Dアイソメトリックの場合）:
  `[各スライド固有の主題], consistent sleek 3D isometric style, deep slate navy background (#0f172a), indigo (#6366f1) and sky blue glowing accents, frosted glass textures, clean composition, no text, no letters`

---

## 2. HTMLスライド内での画像コンテナ仕様（CSP完全適合・外部CDN排除）

最新のAIサンドボックスや企業環境の厳格なCSP（Content Security Policy）に適合するため、外部画像URL（Unsplash等）への依存を排除し、AIが生成したセッションアセット（またはData URI）を直接 `<img src="...">` に配置します。

### パターン A: 左右スプリット（左: AI生成画像 / 右: 概念解説）
```html
<div class="grid grid-cols-2 gap-8 items-center my-auto">
  <!-- AIネイティブ生成画像コンテナ (アスペクト比同期 16:9 / ドラッグ＆ドロップ再差し替え対応) -->
  <div class="image-dropzone relative aspect-video rounded-xl overflow-hidden border border-slate-700/60 shadow-xl bg-slate-900 group">
    <!-- AIが生成した画像アセットを直接埋め込み（Zero-Cropping: アスペクト比完全一致） -->
    <img src="./images/slide_3_concept.png" 
         alt="自律型データハブの概念図" 
         class="w-full h-full object-cover transition-transform duration-500">
    <div class="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-transparent pointer-events-none"></div>
    <span class="absolute bottom-3 left-3 text-[10px] font-mono text-slate-300 bg-slate-900/80 px-2 py-0.5 rounded border border-slate-700 no-print">
      画像をドラッグ＆ドロップで再差し替え可能
    </span>
  </div>

  <!-- 右側テキスト解説 -->
  <div class="flex flex-col justify-center">
    <span class="text-xs font-bold text-brand-400 uppercase tracking-wider mb-2">Concept Vision</span>
    <h3 class="text-2xl font-extrabold text-slate-100 mb-4">自律型データハブ構想</h3>
    <p class="text-sm text-slate-400 leading-relaxed mb-4">...</p>
  </div>
</div>
```

---

## 3. ブラウザ直接画像差し替え機能（Drag & Drop JS）

納品後にユーザー自身が別の画像へ手動で差し替えたい場合のために、ブラウザ上でローカル画像を枠にドラッグ＆ドロップするだけで即時反映される軽量スクリプトを `template_base.html` に標準搭載しています。

```javascript
// 画像ドラッグ＆ドロップ再差し替えスクリプト
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
- **特徴**: 外部通信ゼロ。ブラウザのローカル `FileReader` で即座に DataURL に変換して差し替え。
- 印刷（`window.print()`）時にも高解像度のままPDFへ埋め込まれます。
