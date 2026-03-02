import os
import sys
import json
import requests
from github import Github

# =========================
# CONFIGURATION
# =========================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

QWEN_MODEL = "qwen-max"
QWEN_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

MAX_DIFF_LENGTH = 15000


# =========================
# GET PR DIFF
# =========================

def get_pr_diff():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    pr = repo.get_pull(int(PR_NUMBER))

    changes = []
    for file in pr.get_files():
        if file.patch and file.filename.endswith(".py"):
            changes.append(
                f"File: {file.filename}\nPatch:\n{file.patch}\n---\n"
            )

    return "\n".join(changes), pr


# =========================
# CALL QWEN API
# =========================

def call_qwen_api(code_context):

    prompt = f"""
Anda adalah Senior Backend Security Reviewer.

Review kode berikut dan WAJIB mengembalikan output dalam format JSON valid saja.

FORMAT WAJIB:

{{
  "severity": "LOW | MEDIUM | HIGH | CRITICAL",
  "summary": "Ringkasan singkat review",
  "issues": [
    {{
      "type": "Bug | Security | CleanCode | Performance",
      "description": "Penjelasan masalah",
      "suggestion": "Saran perbaikan"
    }}
  ]
}}

RULE:
- Hardcoded secret = minimal HIGH
- Security vulnerability serius = CRITICAL
- Bug logic berat = HIGH
- Style issue saja = LOW
- Jangan output teks di luar JSON

Kode:
{code_context}
"""

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": QWEN_MODEL,
        "messages": [
            {"role": "system", "content": "You are a strict DevSecOps reviewer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    response = requests.post(QWEN_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return None, f"Error calling Qwen API: {response.status_code} - {response.text}"

    result = response.json()
    content = result["choices"][0]["message"]["content"]

    return content, None


# =========================
# POST COMMENT
# =========================

def post_comment(pr, body):
    try:
        pr.create_issue_comment(body)
        print("Review posted successfully.")
    except Exception as e:
        print(f"Failed to post comment: {e}")


# =========================
# MAIN
# =========================

def main():

    if not QWEN_API_KEY:
        print("QWEN_API_KEY not found.")
        sys.exit(1)

    print("Fetching PR diff...")
    diff_content, pr = get_pr_diff()

    if not diff_content:
        print("No Python changes detected.")
        sys.exit(0)

    if len(diff_content) > MAX_DIFF_LENGTH:
        diff_content = diff_content[:MAX_DIFF_LENGTH] + "\n...(truncated)"

    print("Calling Qwen API...")
    review_result, error = call_qwen_api(diff_content)

    if error:
        post_comment(pr, f"### 🤖 AI Code Review\n\n{error}")
        sys.exit(1)

    try:
        review_json = json.loads(review_result)
    except json.JSONDecodeError:
        post_comment(
            pr,
            f"### 🤖 AI Code Review\n\n⚠️ Model returned invalid JSON:\n\n```\n{review_result}\n```"
        )
        sys.exit(1)

    severity = review_json.get("severity", "LOW")
    summary = review_json.get("summary", "")
    issues = review_json.get("issues", [])

    # Build comment
    comment_body = f"""
### 🤖 AI Code Review (Qwen)

**Severity:** `{severity}`

**Summary:**  
{summary}

---

### Issues:
"""

    if issues:
        for issue in issues:
            comment_body += f"""
- **Type:** {issue.get("type")}
  - Description: {issue.get("description")}
  - Suggestion: {issue.get("suggestion")}
"""
    else:
        comment_body += "\nNo issues found.\n"

    post_comment(pr, comment_body)

    # =========================
    # QUALITY GATE LOGIC
    # =========================

    if severity in ["HIGH", "CRITICAL"]:
        print("High severity detected. Blocking merge.")
        sys.exit(1)

    print("No blocking issues detected.")
    sys.exit(0)


if __name__ == "__main__":
    main()