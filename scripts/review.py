import os
import requests
import json
from github import Github

# Konfigurasi
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")
QWEN_MODEL = "qwen-max"  # Bisa diganti qwen-plus, qwen-max

def get_pr_diff():
    """Mengambil detail file yang berubah di PR"""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    pr = repo.get_pull(int(PR_NUMBER))
    
    changes = []
    for file in pr.get_files():
        if file.patch: # Hanya ambil file yang ada perubahan teks
            changes.append(f"File: {file.filename}\nPatch:\n{file.patch}\n---\n")
    
    return "\n".join(changes), pr

# def call_qwen_api(code_context):
#     """Mengirim kode ke Qwen API"""
#     url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
#     prompt = f"""
#     Anda adalah Senior Code Reviewer yang ahli. 
#     Tugas Anda adalah me-review kode berikut dari sebuah Pull Request.
    
#     Fokus pada:
#     1. Bug potensial.
#     2. Keamanan (Security vulnerabilities).
#     3. Best practices & Clean Code.
#     4. Saran perbaikan spesifik.
    
#     Jika kode sudah bagus, katakan "LGTM (Looks Good To Me)".
#     Jika ada masalah, jelaskan secara rinci dan berikan contoh kode perbaikan.
    
#     Kode yang di-review:
#     {code_context}
#     """

#     headers = {
#         "Authorization": f"Bearer {QWEN_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     payload = {
#         "model": QWEN_MODEL,
#         "input": {
#             "messages": [
#                 {"role": "system", "content": "You are a helpful code review assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         }
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     if response.status_code == 200:
#         result = response.json()
#         return result['output']['text']
#     else:
#         return f"Error calling Qwen API: {response.status_code} - {response.text}"

def call_qwen_api(code_context):
    """Mengirim kode ke Qwen API (International Endpoint)"""
    
    # URL International + OpenAI Compatible Mode
    url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
    
    prompt = f"""
    Anda adalah Senior Code Reviewer yang ahli. 
    Tugas Anda adalah me-review kode berikut dari sebuah Pull Request.
    
    Fokus pada:
    1. Bug potensial.
    2. Keamanan (Security vulnerabilities).
    3. Best practices & Clean Code.
    4. Saran perbaikan spesifik.
    
    Jika kode sudah bagus, katakan "LGTM (Looks Good To Me)".
    Jika ada masalah, jelaskan secara rinci dan berikan contoh kode perbaikan.
    
    Kode yang di-review:
    {code_context}
    """

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format OpenAI-compatible (bukan native DashScope)
    payload = {
        "model": "qwen-max",  # atau qwen-plus, qwen-max
        "messages": [
            {"role": "system", "content": "You are a helpful code review assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        # Format response juga beda di compatible mode
        return result['choices'][0]['message']['content']
    else:
        return f"Error calling Qwen API: {response.status_code} - {response.text}"
    
    
def post_comment(pr, review_text):
    """Memposting hasil review ke GitHub PR"""
    try:
        pr.create_issue_comment(f"### 🤖 Qwen Code Review\n\n{review_text}")
        print("Review berhasil diposting!")
    except Exception as e:
        print(f"Gagal memposting komentar: {e}")

def main():
    if not QWEN_API_KEY:
        print("Error: QWEN_API_KEY tidak ditemukan.")
        return

    print("Mengambil diff PR...")
    diff_content, pr = get_pr_diff()
    
    if not diff_content:
        print("Tidak ada perubahan kode untuk di-review.")
        return

    # Batasi panjang karakter jika terlalu besar (untuk menghemat token) 
    if len(diff_content) > 15000:
        diff_content = diff_content[:15000] + "\n...(truncated due to length)"

    print("Mengirim ke Qwen API...")
    review_result = call_qwen_api(diff_content)
     
    print("Memposting komentar...")
    post_comment(pr, review_result)

if __name__ == "__main__":
    main()