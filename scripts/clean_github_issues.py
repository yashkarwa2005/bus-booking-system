"""Script to clean and update GitHub Issues on bus-booking-system
Applies color-coded priority and status distribution across Kanban columns.
"""
import urllib.request
import urllib.parse
import json
import subprocess
import time
import re
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_token():
    env_token = os.environ.get("GITHUB_TOKEN", "")
    if env_token:
        return env_token
    try:
        proc = subprocess.Popen(
            "git credential fill",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        out, _ = proc.communicate(input="protocol=https\nhost=github.com\n")
        for line in out.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""


OWNER = "yashkarwa2005"
REPO = "bus-booking-system"
TOKEN = get_token()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Agile-PBL-Cleaner",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}


def api_request(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=HEADERS,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return {"error": e.code, "message": err_msg}


def create_or_update_label(name, color, description):
    res = api_request("labels", method="POST", data={
        "name": name,
        "color": color,
        "description": description
    })
    if "error" in res and res["error"] == 422:
        safe_name = urllib.parse.quote(name)
        api_request(f"labels/{safe_name}", method="PATCH", data={
            "color": color,
            "description": description
        })
    print(f"[*] Configured label: {name} (#{color})")


def main():
    if not TOKEN:
        print("[!] No GitHub token found.")
        return

    print("=== Step 1: Configuring Clean Color-Coded Labels ===")
    labels = [
        ("priority: high", "d73a4a", "High Priority - Must Have"),
        ("priority: medium", "fbca04", "Medium Priority - Should Have"),
        ("priority: low", "0e8a16", "Low Priority - Could Have"),
        ("status: backlog", "cfd3d7", "Backlog item"),
        ("status: todo", "1d76db", "Ready to start"),
        ("status: in-progress", "d93f0b", "Currently in development"),
        ("status: review-testing", "a2eeef", "Under testing and review"),
        ("status: done", "0e8a16", "Completed and verified"),
    ]
    for name, color, desc in labels:
        create_or_update_label(name, color, desc)

    print("\n=== Step 2: Fetching Existing Issues ===")
    issues = api_request("issues?state=all&per_page=50")
    if not isinstance(issues, list):
        print("[-] Error fetching issues:", issues)
        return

    print(f"Found {len(issues)} issues to review.")

    for issue in issues:
        num = issue["number"]
        old_title = issue["title"]
        clean_title = re.sub(r"^\[US-\d+\]\s*", "", old_title).strip()
        print(f"[*] Issue #{num}: {clean_title} (State: {issue['state']})")


if __name__ == "__main__":
    main()
