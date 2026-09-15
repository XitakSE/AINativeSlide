#!/usr/bin/env python3
"""
AINativeSlide Theme Application Engine (Python 3 Standard Library Only)

theme.json に定義された企業CIデザイントークン（カラーパレット、フォント、ロゴ、固定要素）を
ベーステンプレートHTMLに決定論的に流し込み、カスタマイズされたSingle-File HTMLを出力します。

使用法:
    python3 scripts/apply_theme.py --theme themes/default_theme.json --template assets/template_base.html -o custom_base.html
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path

# アスペクト比・用紙サイズの仕様定義
RATIO_SPECS = {
    '16:9': {
        'page_size': '16in 9in',
        'width': '1280px',
        'height': '720px',
        'label': '16:9 ワイド'
    },
    '4:3': {
        'page_size': '4in 3in',
        'width': '1024px',
        'height': '768px',
        'label': '4:3 スタンダード'
    },
    'a4_landscape': {
        'page_size': 'A4 landscape',
        'width': '1188px',
        'height': '840px',
        'label': 'A4 横 (Landscape)'
    },
    'a4_portrait': {
        'page_size': 'A4 portrait',
        'width': '840px',
        'height': '1188px',
        'label': 'A4 縦 (Portrait)'
    }
}
# エイリアスマッピング
RATIO_ALIASES = {
    '16-9': '16:9',
    '4-3': '4:3',
    'a4': 'a4_landscape',
    'a4_l': 'a4_landscape',
    'a4-landscape': 'a4_landscape',
    'a4_p': 'a4_portrait',
    'a4-portrait': 'a4_portrait'
}


class ThemeApplier:
    def __init__(self, theme_data: dict, html_content: str):
        self.theme = theme_data
        self.html = html_content

    def apply_all(self) -> str:
        html = self.html

        # 1. タイポグラフィ適用
        html = self._apply_typography(html)

        # 2. カラーパレット適用 (CSS変数 & Tailwind config)
        html = self._apply_colors(html)

        # 3. アスペクト比・用紙サイズ適用
        html = self._apply_ratio(html)

        # 4. 固定要素適用 (ロゴ、機密区分バッジ、フッター)
        html = self._apply_fixed_elements(html)

        return html

    def _apply_typography(self, html: str) -> str:
        typo = self.theme.get('typography', {})
        if not typo:
            return html

        # Google Fonts URL 置換
        fonts_url = typo.get('google_fonts_url')
        if fonts_url:
            html = re.sub(
                r'<link\s+href=["\']https://fonts\.googleapis\.com/css2\?[^"\']*["\']\s+rel=["\']stylesheet["\']>',
                f'<link href="{fonts_url}" rel="stylesheet">',
                html,
                count=1,
                flags=re.IGNORECASE
            )

        # Tailwind fontFamily 置換
        font_en = typo.get('font_family_en', 'Plus Jakarta Sans')
        font_ja = typo.get('font_family_ja', 'Noto Sans JP')
        font_family_code = f'sans: [\'"{font_en}"\', \'"{font_ja}"\', \'sans-serif\'],'

        html = re.sub(
            r'sans:\s*\[[^\]]+\]\s*,?',
            font_family_code,
            html,
            count=1
        )

        return html

    def _apply_colors(self, html: str) -> str:
        colors = self.theme.get('colors', {})
        if not colors:
            return html

        brand = colors.get('brand', {})
        accent = colors.get('accent', {})

        # 1. CSS変数 (:root { --brand-XX: ...; }) の置換・同期
        def replace_css_var(var_name: str, color_val: str, content: str) -> str:
            pattern = re.compile(rf'(--{re.escape(var_name)}\s*:\s*)([^;]+)(;)', re.IGNORECASE)
            if pattern.search(content):
                return pattern.sub(rf'\g<1>{color_val}\g<3>', content)
            return content

        for key, val in brand.items():
            html = replace_css_var(f'brand-{key}', val, html)

        for key, val in accent.items():
            html = replace_css_var(f'accent-{key}', val, html)

        # 2. Tailwind config の brand オブジェクト置換（直値定義の場合に対応）
        if 'tailwind.config' in html:
            # brand 定義の更新
            for key, val in brand.items():
                # '50: #eef2ff' または '50: "var(--brand-50, #eef2ff)"' などのパターン
                pattern = re.compile(rf'(\b{key}\s*:\s*)(["\'][^"\']*["\'])', re.IGNORECASE)
                # brand ブロック内のみを置換するのが理想だが、CSS変数参照パターンを直値または更新
                html = re.sub(
                    rf"(\b{key}\s*:\s*)'var\(--brand-{key},\s*[^']+\)'",
                    rf"\1'var(--brand-{key}, {val})'",
                    html
                )

        return html

    def _apply_ratio(self, html: str) -> str:
        raw_ratio = self.theme.get('ratio', '16:9').lower()
        ratio_key = RATIO_ALIASES.get(raw_ratio, raw_ratio)
        spec = RATIO_SPECS.get(ratio_key)
        if not spec:
            return html

        # @page CSS 置換
        page_pattern = re.compile(r'(@page\s*\{[^}]*size\s*:\s*)([^;]+)(;)', re.IGNORECASE)
        if page_pattern.search(html):
            html = page_pattern.sub(rf'\g<1>{spec["page_size"]}\g<3>', html, count=1)

        # .slide 幅・高さ置換
        slide_pattern = re.compile(r'(\.slide\s*\{[^}]*width\s*:\s*)[^;]+(;[^}]*height\s*:\s*)[^;]+(;)', re.IGNORECASE)
        if slide_pattern.search(html):
            html = slide_pattern.sub(rf'\g<1>{spec["width"]}\g<2>{spec["height"]}\g<3>', html, count=1)

        # .slide-meta-box 幅置換
        meta_pattern = re.compile(r'(\.slide-meta-box\s*\{[^}]*width\s*:\s*)[^;]+(;)', re.IGNORECASE)
        if meta_pattern.search(html):
            html = meta_pattern.sub(rf'\g<1>{spec["width"]}\g<2>', html, count=1)

        # ヘッダーのアスペクト比表記更新
        ratio_span_pattern = re.compile(r'(id=["\']deckRatioText["\'][^>]*>)(.*?)(</span>)', re.IGNORECASE)
        if ratio_span_pattern.search(html):
            html = ratio_span_pattern.sub(rf'\g<1>{spec["label"]}\g<3>', html, count=1)

        return html

    def _apply_fixed_elements(self, html: str) -> str:
        fixed = self.theme.get('fixed_elements', {})
        if not fixed:
            return html

        # 1. 企業ロゴ
        logo_info = fixed.get('logo', {})
        if logo_info:
            logo_content = logo_info.get('content', '')
            if logo_content:
                # 既存のロゴコンテナを置換
                logo_pattern = re.compile(r'(<!--\s*企業ロゴ\s*-->\s*<div[^>]*>)([\s\S]*?)(</div>)', re.IGNORECASE)
                if logo_pattern.search(html):
                    html = logo_pattern.sub(rf'\1{logo_content}\3', html)

        # 2. 会社名・コピーライト
        company_name = fixed.get('company_name')
        if company_name:
            # フッターの会社名表記置換
            html = re.sub(
                r'(<span[^>]*class=["\'][^"\']*company-name[^"\']*["\'][^>]*>).*?(</span>)',
                rf'\g<1>{company_name}\g<2>',
                html
            )

        copyright_text = fixed.get('copyright')
        if copyright_text:
            html = re.sub(
                r'(<span[^>]*class=["\'][^"\']*copyright[^"\']*["\'][^>]*>).*?(</span>)',
                rf'\g<1>{copyright_text}\g<2>',
                html
            )

        return html


def apply_theme_to_file(theme_path: Path, template_path: Path, output_path: Path = None) -> str:
    """テーマJSONをテンプレートHTMLに適用し、結果を返す（出力先指定時はファイル保存）"""
    with open(theme_path, 'r', encoding='utf-8') as f:
        theme_data = json.load(f)

    with open(template_path, 'r', encoding='utf-8') as f:
        template_html = f.read()

    applier = ThemeApplier(theme_data, template_html)
    result_html = applier.apply_all()

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result_html)

    return result_html


def main():
    parser = argparse.ArgumentParser(
        description='AINativeSlide Theme Applier: theme.json のデザイントークンをテンプレートHTMLへ決定論的に適用します。'
    )
    parser.add_argument('--theme', '-t', required=True, help='テーマ定義JSONファイルのパス')
    parser.add_argument('--template', '-i', default=None, help='ベーステンプレートHTMLパス (デフォルト: assets/template_base.html)')
    parser.add_argument('-o', '--output', default=None, help='出力先HTMLファイルパス (省略時は標準出力)')

    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    theme_path = Path(args.theme).resolve()
    if not theme_path.exists():
        print(f'❌ [ERROR] テーマJSONファイルが見つかりません: {theme_path}', file=sys.stderr)
        sys.exit(1)

    if args.template:
        template_path = Path(args.template).resolve()
    else:
        template_path = repo_root / 'assets' / 'template_base.html'

    if not template_path.exists():
        print(f'❌ [ERROR] テンプレートHTMLが見つかりません: {template_path}', file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output).resolve() if args.output else None

    try:
        result = apply_theme_to_file(theme_path, template_path, output_path)
        if output_path:
            print(f'✅ [SUCCESS] テーマ "{theme_path.name}" を適用したテンプレートを生成しました: {output_path}')
        else:
            print(result)
    except Exception as e:
        print(f'❌ [ERROR] テーマ適用中にエラーが発生しました: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
