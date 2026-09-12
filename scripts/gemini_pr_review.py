#!/usr/bin/env python3
"""
AINativeSlide Gemini PR Reviewer (Python 3, Pure Standard Library)

GitHub Actions環境で実行され、PRの差分・メタデータ・AGENTS.mdの規約・verify_slide.pyの結果を
Gemini APIに送信し、高精度なコードレビューと要約を生成してGitHub PRにコメントします。
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

def run_command(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        return res.stdout.strip()
    except Exception as e:
        return f"Command error: {e}"

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[SKIP] GEMINI_API_KEY is not set in secrets. Skipping Gemini PR review.")
        sys.exit(0)

    pr_number = os.environ.get("PR_NUMBER")
    base_ref = os.environ.get("BASE_REF", "main")
    head_ref = os.environ.get("HEAD_REF", "HEAD")

    # 1. PRの差分を取得
    diff_output = run_command(f"git diff origin/{base_ref}...HEAD")
    if not diff_output:
        print("[INFO] No git diff detected. Skipping review.")
        sys.exit(0)

    # 差分が長すぎる場合は切り詰め（トークン上限・ノイズ防止）
    if len(diff_output) > 50000:
        diff_output = diff_output[:50000] + "\n\n...[Diff truncated due to size limit]..."

    # 2. AGENTS.md のルール読み込み
    agents_md_content = ""
    agents_path = Path("AGENTS.md")
    if agents_path.exists():
        try:
            agents_md_content = agents_path.read_text(encoding="utf-8")
        except Exception:
            pass

    # 3. verify_slide.py の実行結果チェック (HTMLファイルに変更がある場合)
    changed_files = run_command(f"git diff --name-only origin/{base_ref}...HEAD").splitlines()
    html_files = [f for f in changed_files if f.endswith(".html")]
    verification_results = []

    for html_file in html_files:
        if Path(html_file).exists():
            v_res = run_command(f"python3 scripts/verify_slide.py {html_file}")
            verification_results.append(f"### Verification for `{html_file}`:\n```\n{v_res}\n```")

    verification_context = "\n\n".join(verification_results) if verification_results else "No HTML slide changes detected."

    # 4. プロンプトの組み立て
    system_instruction = (
        "You are an expert code reviewer and quality auditor for the AINativeSlide project.\n"
        "Your role is to analyze the Pull Request diff, evaluate compliance with project architectural rules (AGENTS.md), "
        "and provide an actionable, constructive, and well-structured code review in Japanese.\n\n"
        "### Crucial Checkpoints for AINativeSlide:\n"
        "1. Maintain 1:1 relationship between `.slide` and `.slide-meta-box`.\n"
        "2. Strict aspect ratio preservation (16:9, 4:3, A4 landscape, A4 portrait).\n"
        "3. Zero-margin print CSS (@page { margin: 0; }) must not be broken.\n"
        "4. No in-slide HTML download buttons (only edit toggle, copy comments, presentation, and print).\n"
        "5. Automated verification script (`scripts/verify_slide.py`) pass status."
    )

    prompt = f"""以下のPull Requestの変更差分と検証結果をレビューし、Markdown形式でレビューレポートを出力してください。

## 1. プロジェクト規約 (AGENTS.md)
```markdown
{agents_md_content[:3000]}
```

## 2. スライド自動検証ツールの実行結果
{verification_context}

## 3. PR 変更差分 (Git Diff)
```diff
{diff_output}
```

---

### 出力フォーマット:
## 🤖 Gemini Code Assist PR Review

### 📝 変更概要サマリー
(変更内容の要約を2〜3行で簡潔に)

### 🎯 規約適合性チェック (AGENTS.md 基準)
- [ ] スライド枠とメタ情報ボックスの 1:1 整合性
- [ ] アスペクト比・余白ゼロ印刷CSSの保持
- [ ] 外部JSライブラリや不要ボタンの混入防止

### 🔍 コードレビュー & 改善提案
(潜在的なリスク、レイアウト崩れの危険、改善できる点があれば箇条書きで具体的に指摘。問題がなければ「特段の懸念点はありません。綺麗に実装されています。」と記載)

### 💡 総合判定
(LGTM / 要修正 / 確認推奨 のいずれかを理由とともに提示)
"""

    # 5. Gemini API 呼び出し (v1beta API: gemini-2.5-flash または gemini-1.5-flash)
    # 複数モデルにフォールバックできるように設定
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]

    review_text = None
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "systemInstruction": {
                "role": "system",
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        review_text = parts[0].get("text", "")
                        print(f"[SUCCESS] Review generated successfully using {model_name}.")
                        break
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"[WARN] Failed with {model_name}: HTTP {e.code} - {err_body[:200]}")
        except Exception as e:
            print(f"[WARN] Error with {model_name}: {e}")

    if not review_text:
        print("[ERROR] Failed to generate review from all candidate Gemini models.")
        sys.exit(1)

    # 6. 結果をファイルに保存 (GitHub ActionsのワークフローステップでPRに投稿)
    output_path = Path("pr_review_comment.md")
    output_path.write_text(review_text, encoding="utf-8")
    print(f"[INFO] Review saved to {output_path}")

if __name__ == "__main__":
    main()
