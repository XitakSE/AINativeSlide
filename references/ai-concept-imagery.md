# AI生成画像（Concept Imagery）設計 & 差し替え仕様書

抽象的な概念や世界観、未来ビジョン（例: データサイロの混乱、AIと人間の協調、セキュアな分散ネットワーク等）をスライド上で直感的に伝えるための、AI画像生成プロンプト設計とHTML内での実装仕様です。

---

## 1. 抽象概念を伝えるAI画像プロンプト設計の原則

ビジネススライドに馴染む洗練された画像を生成するために、以下の要素をプロンプトに含めます。

### ⓪ 依頼言語へのプロンプト適応規約（Language Adaptation Rule）
- **日本語での依頼時**: ユーザーのレビュー負荷を下げ、意図通りの構図を直感的に合意できるよう、ビジュアル方針の画像生成プロンプトは必ず**日本語**で記述・提示します（Midjourney, DALL-E 3, Imagen 等の日本語入力に対応）。
- **英語での依頼時（または明示的な英語指定時）**: 英語構文を使用します。

### ① 4大スタイル（テイスト）の選択肢とプロンプト設計規約

プレゼンの目的やターゲット読者層に合わせて、以下の4つの主要テイストから選択します。

1. **リアル・実写・シネマティック系 (Photorealistic / Cinematic 3D)**
   - **特徴**: 高精細な実写写真風、スタジオライティング、重厚なビジネス空間・人物・未来都市。
   - **最適な用途**: 役員・経営会議決裁、投資家ピッチ、重厚なビジョン提示。
   - **日本語プロンプト構文**: `[主題]の実写映画風シネマティックショット、ドラマチックなスタジオ照明、浅い被写界深度、洗練された企業美学、超高解像度、すっきりした構図、文字入れなし、テキストなし、タイポグラフィなし`
   - **英語プロンプト構文**: `Photorealistic cinematic shot of [主題], dramatic studio lighting, shallow depth of field, high-end corporate aesthetic, 8k resolution, clean composition, no typography, no letters, no text`
   - **例（日本語）**: `最新の企業役員会がホログラムでリアルタイムの経営数値を視覚化して審議している実写映画風シネマティックショット、柔らかい環境光、超高精細、すっきりした構図、文字入れなし、テキストなし`

2. **漫画・コミック・アニメ系 (Manga / Anime / Comic Art)**
   - **特徴**: 親しみやすい線画・ストーリー調、表情豊かなキャラクター、感情や課題の共感を誘う表現。
   - **最適な用途**: 社内研修、現場向け業務改善、採用説明会、ストーリー仕立ての課題・解決策提示。
   - **日本語プロンプト構文**: `現代の日本のビジネス漫画・コミック調アートスタイル、明瞭で表情豊かな線画、鮮やかなセル画風カラーパレット、[主題]の共感を呼ぶビジネスシーン、文字入れなし、吹き出し文字なし、テキストなし`
   - **英語プロンプト構文**: `Modern Japanese manga comic art style, clean expressive line art, vibrant cel-shaded color palette, relatable business storytelling scene of [主題], modern corporate anime aesthetic, no typography, no letters, no text`
   - **例（日本語）**: `現代の日本のビジネス漫画スタイル、明瞭で表情豊かな線画、スマートな業務改善ボードの前でチームメンバーが笑顔でハイタッチしている親しみやすいオフィスシーン、文字入れなし、テキストなし`

3. **3D立体アイコン・アイソメトリック系 (3D Isometric / Minimalist 3D Icons)**
   - **特徴**: 粘土・ガラス・プラスチック質感の等角投影3Dモデル、抽象的で洗練された形状。
   - **最適な用途**: システム構成、データパイプライン、クラウド連携、機能一覧の視覚化。
   - **日本語プロンプト構文**: `[主題]のミニマルな3Dアイソメトリックイラスト、滑らかなフロストガラスとクレイの質感、光るテックブルーとシアンのアクセント、すっきりした等角投影構図、超高解像度レンダリング、文字入れなし、テキストなし`
   - **英語プロンプト構文**: `Minimalist 3D isometric illustration of [主題], smooth clay and frosted glass textures, glowing tech blue and cyan neon accents, clean isometric perspective, 8k render, no typography, no letters, no text`
   - **例（日本語）**: `散在するデータブロックが透明なガラスパイプラインを通り中央の光り輝く統合ハブへと集約されるミニマルな3Dアイソメトリックイラスト、クリーンな白スタジオ背景、滑らかな質感、文字入れなし、テキストなし`

4. **フラットベクター・ビジネスイラスト系 (Flat Vector / Corporate Art)**
   - **特徴**: シンプルな2D線画・面構成、Notion風やSaaSウェブサイト風の洗練されたミニマルアート。
   - **最適な用途**: サービス紹介、対比図、マーケティング資料、クイック企画書。
   - **日本語プロンプト構文**: `[主題]の洗練されたモダンフラットベクターイラスト、ミニマルな企業エディトリアルアート、明確な幾何学形状、上品で落ち着いたカラーパレット、贅沢な余白、文字入れなし、テキストなし`
   - **英語プロンプト構文**: `Clean modern flat vector illustration of [主題], minimalist corporate editorial art, bold geometry, elegant subtle color palette, generous negative space, no typography, no letters, no text`
   - **例（日本語）**: `相互に連携するモジュール型歯車と分析ダッシュボードを描いた洗練されたモダンフラットベクターイラスト、上品なインディゴとスレート基調、ミニマルなコーポレート調、文字入れなし、テキストなし`

### ② 文字入れ禁止指示 (No Text Rule)
- AI画像生成モデル（DALL-E 3, Midjourney, Imagen 等）に文字を描かせると崩れたり誤字になりがちです。
- **日本語では `文字入れなし、テキストなし、タイポグラフィなし、ウォーターマークなし`**、**英語では `clean composition, no typography, no letters, no text watermark`** を必ず付加し、文字情報はHTML側のTailwindで重ねるか隣接配置します。

### ③ アスペクト比の事前同期による完全ノーカット原則（Zero-Cropping Rule）
- 画像生成プロンプトには、スライドコンテナの表示比率に合わせたアスペクト比を必ず明記します：
  - **16:9 ワイド（左右スプリット / 全画面）**: `widescreen 16:9 composition, landscape aspect ratio`
  - **4:3 標準**: `standard 4:3 composition, landscape aspect ratio`
  - **A4 横 / A4 縦**: `balanced composition matching container ratio`
- コンテナ枠と生成画像のアスペクト比を事前に完全一致させることで、CSSトリミングによる意図しない構図の切り落としを一切発生させず、生成された構図を100%そのまま美しく表示します（※ブラウザレンダリング時の微小な端数丸め誤差による白隙間を防ぐため、コンテナCSSには保険として `object-cover` を指定しますが、比率が完全一致しているため実質的な切り落としは生じません）。

### ④ デッキ全体の一貫性を保つ「シードスタイル記述子（Seed Style）」
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
