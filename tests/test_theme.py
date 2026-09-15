import unittest
import sys
import json
from pathlib import Path

# パスを追加して scripts モジュールをインポート可能にする
sys.path.append(str(Path(__file__).resolve().parent.parent))
from scripts.apply_theme import ThemeApplier, RATIO_SPECS
from scripts.assemble_deck import DeckAssembler

class TestThemeApplier(unittest.TestCase):
    def setUp(self):
        self.sample_html = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP&family=Plus+Jakarta+Sans&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', '"Noto Sans JP"', 'sans-serif'],
          },
          colors: {
            brand: {
              50: 'var(--brand-50, #eef2ff)',
              600: 'var(--brand-600, #4f46e5)',
            }
          }
        }
      }
    }
  </script>
  <style>
    :root {
      --brand-50: #eef2ff;
      --brand-600: #4f46e5;
    }
    @page { size: 16in 9in; margin: 0; }
    .slide { width: 1280px; height: 720px; }
    .slide-meta-box { width: 1280px; }
  </style>
</head>
<body>
  <span id="deckRatioText">16:9 ワイド</span>
  <span class="company-name">Original Corp</span>
  <span class="copyright">Original Copyright</span>
</body>
</html>'''

    def test_default_theme_json_validity(self):
        theme_path = Path(__file__).resolve().parent.parent / 'themes' / 'default_theme.json'
        self.assertTrue(theme_path.exists(), "default_theme.json does not exist")

        with open(theme_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn('theme_id', data)
        self.assertIn('colors', data)
        self.assertIn('brand', data['colors'])
        self.assertIn('50', data['colors']['brand'])
        self.assertIn('600', data['colors']['brand'])
        self.assertIn('typography', data)
        self.assertEqual(data['typography']['font_family_en'], 'IBM Plex Sans')
        self.assertEqual(data['components']['card_radius'], 'rounded-none')
        self.assertEqual(data['components']['card_shadow'], 'shadow-none')
        self.assertIn('ratio', data)

    def test_apply_custom_colors(self):
        custom_theme = {
            "colors": {
                "brand": {
                    "50": "#f0fdf4",
                    "600": "#16a34a"
                }
            }
        }
        applier = ThemeApplier(custom_theme, self.sample_html)
        result = applier.apply_all()

        # CSS変数がエメラルドグリーンに置換されているか
        self.assertIn("--brand-50: #f0fdf4;", result)
        self.assertIn("--brand-600: #16a34a;", result)

    def test_apply_custom_ratio(self):
        custom_theme = {
            "ratio": "4:3"
        }
        applier = ThemeApplier(custom_theme, self.sample_html)
        result = applier.apply_all()

        # @page と要素寸法が 4:3 用に更新されているか
        self.assertIn("size: 4in 3in;", result)
        self.assertIn("width: 1024px;", result)
        self.assertIn("height: 768px;", result)
        self.assertIn("4:3 スタンダード", result)

    def test_apply_fixed_elements(self):
        custom_theme = {
            "fixed_elements": {
                "company_name": "New Global Corp",
                "copyright": "© 2026 New Global Corp"
            }
        }
        applier = ThemeApplier(custom_theme, self.sample_html)
        result = applier.apply_all()

        self.assertIn("New Global Corp", result)
        self.assertIn("© 2026 New Global Corp", result)

    def test_apply_typography(self):
        custom_theme = {
            "typography": {
                "font_family_en": "Inter",
                "font_family_ja": "Zen Kaku Gothic New",
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter&family=Zen+Kaku+Gothic+New&display=swap"
            }
        }
        applier = ThemeApplier(custom_theme, self.sample_html)
        result = applier.apply_all()

        self.assertIn("family=Inter&family=Zen+Kaku+Gothic+New", result)
        self.assertIn('"Inter"', result)
        self.assertIn('"Zen Kaku Gothic New"', result)

if __name__ == '__main__':
    unittest.main()
