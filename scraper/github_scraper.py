import requests
import os
import json

GITHUB_TOKEN = "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"  # optional for rate limit

headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def fetch_github_metadata(owner, repo):
    base = f"https://api.github.com/repos/{owner}/{repo}"
    all_commits = []

    for page in range(1, 4):  # Pages 1–3
        url = f"{base}/commits?per_page=100&page={page}"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            continue
        page_commits = r.json()
        if not page_commits:
            break
        all_commits.extend(page_commits)

    contributors = requests.get(f"{base}/contributors", headers=headers).json()

    return {
        "repo": f"{owner}/{repo}",
        "commits": all_commits,
        "contributors": contributors
    }

if __name__ == "__main__":
    os.makedirs("data/raw/github", exist_ok=True)
    repos = [
    ("facebook", "react"),
    ("vercel", "next.js"),
    ("microsoft", "vscode"),
    ("pallets", "flask"),
    ("numpy", "numpy"),
    ("vuejs", "vue"),
    ("torvalds", "linux")]
    for owner, repo in repos:
        data = fetch_github_metadata(owner, repo)
        with open(f"data/raw/github/{repo}.json", "w") as f:
            json.dump(data, f, indent=2)
