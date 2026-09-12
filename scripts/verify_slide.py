#!/usr/bin/env python3
"""
AINativeSlide Automated Slide Deck Verifier (Python 3)

外部依存なし (Pure Python 3 標準ライブラリのみ) で動作するスライド品質自動テストツール。
AIエージェントが生成したHTMLスライドの構造、スライド番号の連続性、
メタボックスの整合性、文字溢れ（Overflow）リスク、印刷設定を厳格に検査し、
不備がある場合はAIが自律修正するための具体的な指示を出力して終了コード1を返します。

使用法:
    python3 scripts/verify_slide.py <path_to_slide.html> [--strict]
"""

import sys
import os
import re
from pathlib import Path

def main():
    args = sys.argv[1:]
    is_strict = '--strict' in args
    file_args = [a for a in args if not a.startswith('--')]

    if not file_args:
        print('[USAGE] python3 scripts/verify_slide.py <path_to_html_file> [--strict]', file=sys.stderr)
        sys.exit(2)

    target_file = Path(file_args[0]).resolve()

    if not target_file.exists():
        print(f'[ERROR] File not found: {target_file}', file=sys.stderr)
        sys.exit(2)

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f'[ERROR] Failed to read file: {e}', file=sys.stderr)
        sys.exit(2)

    errors = []
    warnings = []

    # ========================================================
    # 1. スライド要素（.slide）とメタボックスの抽出
    # ========================================================
    slide_pattern = re.compile(r'<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>([\s\S]*?)</section>', re.IGNORECASE)
    slides = list(slide_pattern.finditer(html))

    # メタボックスの抽出
    metabox_pattern = re.compile(
        r'<div[^>]*class=["\'][^"\']*\bslide-meta-box\b[^"\']*["\'][^>]*>([\s\S]*?)</div>\s*(?=(?:<!--\s*==|<section\s*class=["\'][^"\']*\bslide\b|</main>|$))',
        re.IGNORECASE
    )
    meta_boxes = list(metabox_pattern.finditer(html))

    slide_count = len(slides)
    metabox_count = len(meta_boxes)

    if slide_count == 0:
        errors.append('スライド要素 (<section class="slide ...">) が1枚も見つかりません。')

    # スライド数とメタボックス数の完全一致チェック
    if slide_count > 0 and slide_count != metabox_count:
        errors.append(f'スライド枚数 ({slide_count}枚) とメタ情報ボックス数 ({metabox_count}個) が一致していません。各スライドの直下に必ず1つの .slide-meta-box を配置してください。')

    # ========================================================
    # 2. スライド番号・フッター・メタバッジの連番チェック
    # ========================================================
    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        slide_num_str = f"{slide_num:02d}"
        expected_total_str = f"{slide_count:02d}"
        inner_html = slide.group(1)

        # フッターの番号パターン: "01 / 08", "1 / 8", "01/08" 等（Tailwindの /20 等を拾わないよう末尾付近またはタグ内の数値を優先）
        footer_exact_pattern = re.compile(rf'(?:>|\s|\b)0?{slide_num}\s*/\s*0?{slide_count}(?:<|\s|\b)', re.IGNORECASE)
        if not footer_exact_pattern.search(inner_html):
            # 誤ったスライド番号表記がないか探索 (例: "01 / 06")
            any_number_match = re.search(r'(?:>|\s|\b)0?(\d{1,2})\s*/\s*0?(\d{1,2})(?:<|\s|\b)', inner_html)
            if any_number_match:
                detected = any_number_match.group(0).strip('<> ')
                errors.append(f'Slide {slide_num}: フッター番号が誤っています (検出: "{detected}" -> 正しくは "{slide_num_str} / {expected_total_str}")')
            else:
                errors.append(f'Slide {slide_num}: フッターのスライド番号表記 ("{slide_num_str} / {expected_total_str}") が見つかりません。')

        # アスペクト比・用紙サイズの検出と文字数ヒューリスティック検査
        text_content = inner_html
        text_content = re.sub(r'<style[\s\S]*?</style>', '', text_content, flags=re.IGNORECASE)
        text_content = re.sub(r'<script[\s\S]*?</script>', '', text_content, flags=re.IGNORECASE)
        text_content = re.sub(r'<svg[\s\S]*?</svg>', '', text_content, flags=re.IGNORECASE)
        text_content = re.sub(r'<[^>]+>', ' ', text_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()

        # A4縦（高さ1188px）か横長（高さ720px〜840px）かでテキスト上限を調整
        is_portrait = 'h-[1188px]' in slide.group(0) or 'h-[1123px]' in slide.group(0) or 'portrait' in html.lower()
        max_chars = 1100 if is_portrait else 700
        warn_chars = 850 if is_portrait else 520

        if len(text_content) > max_chars:
            errors.append(f'Slide {slide_num}: 本文テキスト量が多すぎます ({len(text_content)}文字 > 上限{max_chars}文字)。枠外はみ出し防止のため要約または箇条書きを短縮してください。')
        elif len(text_content) > warn_chars:
            warnings.append(f'Slide {slide_num}: テキスト量が多めです ({len(text_content)}文字)。要素がスライド枠に収まっているか確認してください。')

    # メタボックス内のバッジ番号チェック
    for idx, box in enumerate(meta_boxes):
        slide_num = idx + 1
        inner_html = box.group(1)
        expected_badge = re.compile(rf'Slide\s*0?{slide_num}\s*/\s*0?{slide_count}', re.IGNORECASE)
        if not expected_badge.search(inner_html):
            any_badge_match = re.search(r'Slide\s*0?\d+\s*/\s*0?\d+', inner_html, re.IGNORECASE)
            if any_badge_match:
                errors.append(f'メタボックス {slide_num}: バッジ番号が誤っています (検出: "{any_badge_match.group(0)}" -> 正しくは "Slide {slide_num} / {slide_count}")')
            else:
                warnings.append(f'メタボックス {slide_num}: バッジ表記 ("Slide {slide_num} / {slide_count}") が見つかりません。')

    # ========================================================
    # 3. ヘッダー表記と必須コンポーネントの検証
    # ========================================================
    header_count_match = re.search(r'id=["\']deckSlideCountText["\'][^>]*>(.*?)</span>', html, re.IGNORECASE)
    if header_count_match:
        header_count_text = header_count_match.group(1).strip()
        expected_header_count = f'全{slide_count}スライド'
        if slide_count > 0 and str(slide_count) not in header_count_text:
            errors.append(f'ヘッダー総スライド数表記が誤っています (検出: "{header_count_text}" -> 正しくは "{expected_header_count}")')
    else:
        errors.append('ヘッダーに id="deckSlideCountText" の要素が見つかりません。')

    required_ids = [
        'deckTitleText',
        'deckRatioText',
        'deckSlideCountText',
        'toggleEditBtn',
        'copyCommentsBtn',
        'presentationModal'
    ]

    for rid in required_ids:
        if not re.search(rf'id=["\']{rid}["\']', html, re.IGNORECASE):
            errors.append(f'必須要素 id="{rid}" がHTML内に存在しません。')

    # ========================================================
    # 4. 印刷・PDF余白ゼロ設定（16:9, 4:3, A4 landscape, A4 portrait）
    # ========================================================
    if not re.search(r'@page\s*\{[^}]*margin\s*:\s*0', html, re.IGNORECASE):
        errors.append('CSSに印刷用の余白ゼロ設定 (@page { margin: 0; }) が定義されていません。')

    if not re.search(r'@media\s*print', html, re.IGNORECASE):
        errors.append('印刷用メディアクエリ (@media print) が定義されていません。')

    if not re.search(r'\.no-print', html, re.IGNORECASE):
        warnings.append('印刷除外用クラス (.no-print) の定義が見当たりません。')

    # ========================================================
    # 5. JavaScript ランタイム整合性 (基本プレゼン・推敲機能)
    # ========================================================
    required_js_functions = [
        'toggleEditMode',
        'startPresentation',
        'stopPresentation',
        'copySlideComments'
    ]

    for fn in required_js_functions:
        if not re.search(rf'function\s+{fn}\b', html, re.IGNORECASE):
            errors.append(f'必須JavaScript関数 {fn}() が定義されていません。')

    # ========================================================
    # 6. 結果の集計とAI向け出力
    # ========================================================
    print('----------------------------------------------------')
    print(f'🔍 AINativeSlide スライド自動検証レポート: {target_file.name}')
    print(f'📊 スライド枚数: {slide_count}枚 | メタ情報ボックス: {metabox_count}個')
    print('----------------------------------------------------')

    if errors:
        print(f'\n❌ [TEST FAILED] {len(errors)}件のエラーが検出されました。\nAIは以下の指示に従って直ちにHTMLを修正してください:\n')
        for i, err in enumerate(errors, 1):
            print(f'  {i}. [ERROR] {err}')

    if warnings:
        print(f'\n⚠️ [WARNINGS] {len(warnings)}件の警告があります:')
        for i, warn in enumerate(warnings, 1):
            print(f'  {i}. [WARN] {warn}')

    if not errors:
        if warnings and is_strict:
            print('\n❌ [STRICT MODE FAILED] 警告が存在するため終了コード1を返します。')
            sys.exit(1)
        print('\n✅ [TEST PASSED] すべての品質テストに合格しました！')
        print('   ・スライド数・番号の完全一致')
        print('   ・メタ情報ボックスの整合性')
        print('   ・文字数・はみ出しヒューリスティッククリア')
        print('   ・必須UI & 印刷用ゼロマージン設定確認済み')
        print('🚀 成果物をユーザーに納品可能です。\n')
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
