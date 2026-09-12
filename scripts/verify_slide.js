#!/usr/bin/env node

/**
 * NativeSlide Automated Slide Deck Verifier
 * 
 * 外部依存なし (Pure Node.js) で動作するスライド品質自動テストツール。
 * AIエージェントが生成したHTMLスライドの構造、スライド番号の連続性、
 * メタボックスの整合性、文字溢れ（Overflow）リスク、印刷設定を厳格に検査し、
 * 不備がある場合はAIが自律修正するための具体的な指示を出力して終了コード1を返します。
 * 
 * 使用法:
 *   node scripts/verify_slide.js <path_to_slide.html> [--strict]
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const isStrict = args.includes('--strict');
const fileArgs = args.filter(a => !a.startsWith('--'));

if (fileArgs.length === 0) {
  console.error('[USAGE] node scripts/verify_slide.js <path_to_html_file> [--strict]');
  process.exit(2);
}

const targetFile = path.resolve(process.cwd(), fileArgs[0]);

if (!fs.existsSync(targetFile)) {
  console.error(`[ERROR] File not found: ${targetFile}`);
  process.exit(2);
}

const html = fs.readFileSync(targetFile, 'utf8');

const errors = [];
const warnings = [];

// ========================================================
// 1. スライド要素（.slide）とメタボックスの抽出
// ========================================================
const slideRegex = /<section[^>]*class=["'][^"']*\bslide\b[^"']*["'][^>]*>([\s\S]*?)<\/section>/gi;
const slides = [];
let match;
while ((match = slideRegex.exec(html)) !== null) {
  slides.push({
    fullMatch: match[0],
    innerHtml: match[1],
    startIndex: match.index
  });
}

const metaBoxRegex = /<div[^>]*class=["'][^"']*\bslide-meta-box\b[^"']*["'][^>]*>([\s\S]*?)<\/div>\s*(?=(?:<!--\s*==|<section\s*class=["'][^"']*\bslide\b|<\/main>|$))/gi;
const metaBoxes = [];
while ((match = metaBoxRegex.exec(html)) !== null) {
  metaBoxes.push({
    fullMatch: match[0],
    innerHtml: match[1],
    startIndex: match.index
  });
}

const slideCount = slides.length;
const metaBoxCount = metaBoxes.length;

if (slideCount === 0) {
  errors.push('スライド要素 (<section class="slide ...">) が1枚も見つかりません。');
}

// スライド数とメタボックス数の完全一致チェック
if (slideCount > 0 && slideCount !== metaBoxCount) {
  errors.push(`スライド枚数 (${slideCount}枚) とメタ情報ボックス数 (${metaBoxCount}個) が一致していません。各スライドの直下に必ず1つの .slide-meta-box を配置してください。`);
}

// ========================================================
// 2. スライド番号・フッター・メタバッジの連番チェック
// ========================================================
slides.forEach((slide, idx) => {
  const slideNum = idx + 1;
  const slideNumStr = String(slideNum).padStart(2, '0');
  const expectedTotalStr = String(slideCount).padStart(2, '0');

  // フッターの番号パターン: "01 / 08", "1 / 8", "01/08" 等
  const footerPattern = new RegExp(`(\\b0?${slideNum}\\s*\\/\\s*0?${slideCount}\\b)`, 'i');
  if (!footerPattern.test(slide.innerHtml)) {
    const anyNumberMatch = slide.innerHtml.match(/\b0?(\d+)\s*\/\s*0?(\d+)\b/);
    if (anyNumberMatch) {
      errors.push(`Slide ${slideNum}: フッター番号が誤っています (検出: "${anyNumberMatch[0]}" -> 正しくは "${slideNumStr} / ${expectedTotalStr}")`);
    } else {
      errors.push(`Slide ${slideNum}: フッターのスライド番号表記 ("${slideNumStr} / ${expectedTotalStr}") が見つかりません。`);
    }
  }

  // 文字数・はみ出しヒューリスティック検査 (16:9スライド 720pxの高さ基準)
  const textContent = slide.innerHtml
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<svg[\s\S]*?<\/svg>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  // 日本語スライドの場合、700文字以上は縦スクロール・枠外はみ出しの危険度が極めて高い
  if (textContent.length > 700) {
    errors.push(`Slide ${slideNum}: 本文テキスト量が多すぎます (${textContent.length}文字 > 上限700文字)。縦幅720pxから文字がはみ出すため、要約または箇条書きを短縮してください。`);
  } else if (textContent.length > 520) {
    warnings.push(`Slide ${slideNum}: テキスト量が多めです (${textContent.length}文字)。要素がスライド枠（720px）に収まっているか確認してください。`);
  }
});

// メタボックス内のバッジ番号チェック
metaBoxes.forEach((box, idx) => {
  const slideNum = idx + 1;
  const expectedBadge = new RegExp(`Slide\\s*0?${slideNum}\\s*\\/\\s*0?${slideCount}`, 'i');
  if (!expectedBadge.test(box.innerHtml)) {
    const anyBadgeMatch = box.innerHtml.match(/Slide\s*0?\d+\s*\/\s*0?\d+/i);
    if (anyBadgeMatch) {
      errors.push(`メタボックス ${slideNum}: バッジ番号が誤っています (検出: "${anyBadgeMatch[0]}" -> 正しくは "Slide ${slideNum} / ${slideCount}")`);
    } else {
      warnings.push(`メタボックス ${slideNum}: バッジ表記 ("Slide ${slideNum} / ${slideCount}") が見つかりません。`);
    }
  }
});

// ========================================================
// 3. ヘッダー表記と必須コンポーネントの検証
// ========================================================
const headerCountMatch = html.match(/id=["']deckSlideCountText["'][^>]*>(.*?)<\/span>/i);
if (headerCountMatch) {
  const headerCountText = headerCountMatch[1].trim();
  const expectedHeaderCount = `全${slideCount}スライド`;
  if (slideCount > 0 && !headerCountText.includes(String(slideCount))) {
    errors.push(`ヘッダー総スライド数表記が誤っています (検出: "${headerCountText}" -> 正しくは "${expectedHeaderCount}")`);
  }
} else {
  errors.push('ヘッダーに id="deckSlideCountText" の要素が見つかりません。');
}

const requiredIds = [
  'deckTitleText',
  'deckRatioText',
  'deckSlideCountText',
  'tabBtnEdit',
  'tabBtnPresent',
  'headerControlsEdit',
  'headerControlsPresent',
  'tocDrawer',
  'presentationModal'
];

requiredIds.forEach(id => {
  const idRegex = new RegExp(`id=["']${id}["']`, 'i');
  if (!idRegex.test(html)) {
    errors.push(`必須要素 id="${id}" がHTML内に存在しません。`);
  }
});

// ========================================================
// 4. 印刷・PDF余白ゼロ設定
// ========================================================
if (!/@page\s*\{[^}]*margin\s*:\s*0/i.test(html)) {
  errors.push('CSSに印刷用の余白ゼロ設定 (@page { margin: 0; }) が定義されていません。');
}

if (!/@media\s*print/i.test(html)) {
  errors.push('印刷用メディアクエリ (@media print) が定義されていません。');
}

if (!/\.no-print/i.test(html)) {
  warnings.push('印刷除外用クラス (.no-print) の定義が見当たりません。');
}

// ========================================================
// 5. JavaScript ランタイム整合性
// ========================================================
const requiredJsFunctions = [
  'switchHeaderTab',
  'toggleEditMode',
  'toggleTocDrawer',
  'openSpeakerView',
  'startPresentation',
  'stopPresentation',
  'copySlideComments'
];

requiredJsFunctions.forEach(fn => {
  const fnRegex = new RegExp(`function\\s+${fn}\\b`, 'i');
  if (!fnRegex.test(html)) {
    errors.push(`必須JavaScript関数 ${fn}() が定義されていません。`);
  }
});

// ========================================================
// 6. 結果の集計とAI向け出力
// ========================================================
console.log('----------------------------------------------------');
console.log(`🔍 NativeSlide スライド自動検証レポート: ${path.basename(targetFile)}`);
console.log(`📊 スライド枚数: ${slideCount}枚 | メタ情報ボックス: ${metaBoxCount}個`);
console.log('----------------------------------------------------');

if (errors.length > 0) {
  console.log(`\n❌ [TEST FAILED] ${errors.length}件のエラーが検出されました。\nAIは以下の指示に従って直ちにHTMLを修正してください:\n`);
  errors.forEach((err, i) => {
    console.log(`  ${i + 1}. [ERROR] ${err}`);
  });
}

if (warnings.length > 0) {
  console.log(`\n⚠️ [WARNINGS] ${warnings.length}件の警告があります:`);
  warnings.forEach((warn, i) => {
    console.log(`  ${i + 1}. [WARN] ${warn}`);
  });
}

if (errors.length === 0) {
  if (warnings.length > 0 && isStrict) {
    console.log('\n❌ [STRICT MODE FAILED] 警告が存在するため終了コード1を返します。');
    process.exit(1);
  }
  console.log('\n✅ [TEST PASSED] すべての品質テストに合格しました！');
  console.log('   ・スライド数・番号の完全一致');
  console.log('   ・メタ情報ボックスの整合性');
  console.log('   ・文字数・はみ出しヒューリスティッククリア');
  console.log('   ・必須UI & 印刷用ゼロマージン設定確認済み');
  console.log('🚀 成果物をユーザーに納品可能です。\n');
  process.exit(0);
} else {
  process.exit(1);
}
