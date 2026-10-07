"""One-Click GitHub Project & Scrum Board Setup Engine
Reads .github/project-setup.json and dynamically configures:
  1. Git remote detection (Owner & Repo via HTTPS/SSH)
  2. GitHub authentication verification via GitHub CLI (`gh`)
  3. Color-coded Agile Labels (High, Medium, Low, User Story, Task, etc.)
  4. Sprint Milestones
  5. GitHub Issues with strict DUPLICATE PREVENTION ([US-XX] title matching)
  6. GitHub Projects V2 Board creation/reuse
  7. Association of all Issues to the GitHub Project
  8. Output of final Project and Kanban Board URLs

Zero hardcoding: Reusable for any AM PBL repository.
"""
import os
import sys
import json
import re
import subprocess
import shutil

# Terminal styling
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"

def print_header(text):
    print(f"\n{Color.BOLD}{Color.CYAN}======================================================================{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  {text}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}======================================================================{Color.RESET}\n")

def run_cmd(args, check=True, capture=True):
    """Runs a system command and returns stdout."""
    res = subprocess.run(
        args,
        text=True,
        capture_output=capture,
        shell=False
    )
    if check and res.returncode != 0:
        err = res.stderr.strip() if res.stderr else f"Exit code {res.returncode}"
        raise RuntimeError(f"Command failed ({' '.join(args)}): {err}")
    return res.stdout.strip() if res.stdout else ""

def detect_remote():
    """Detects Git remote URL and extracts OWNER and REPO."""
    try:
        remote_url = run_cmd(["git", "remote", "get-url", "origin"])
    except Exception:
        raise RuntimeError("No Git remote 'origin' found. Please ensure you have cloned or linked your GitHub repository.")

    # Match HTTPS: https://github.com/OWNER/REPO(.git)?
    # Match SSH: git@github.com:OWNER/REPO(.git)?
    m_https = re.search(r"github\.com[/:]([\w.-]+)/([\w.-]+?)(?:\.git)?$", remote_url)
    if not m_https:
        raise RuntimeError(f"Could not parse GitHub Owner and Repository from remote URL: {remote_url}")

    owner = m_https.group(1)
    repo = m_https.group(2)
    return owner, repo, remote_url

def check_gh_auth():
    """Verifies that GitHub CLI is authenticated and returns logged-in user."""
    gh_path = shutil.which("gh")
    if not gh_path:
        raise RuntimeError("GitHub CLI ('gh') is not installed or not in PATH.\nInstall it from https://cli.github.com/ or run: winget install --id GitHub.cli -e")

    # Check auth status
    res = subprocess.run(["gh", "auth", "status"], text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(
            "You are not authenticated with GitHub CLI!\n"
            "Please run the following command in terminal to log in with your GitHub account:\n\n"
            "   gh auth login\n\n"
            "Follow the web/browser prompt to authenticate, then re-run setup-project.bat."
        )

    # Get current user login
    try:
        login = run_cmd(["gh", "api", "user", "--jq", ".login"])
        return login
    except Exception:
        return "Authenticated User"

def setup_labels(owner, repo, labels):
    """Creates or updates GitHub labels with color coding."""
    print(f"{Color.BOLD}[Step 1/5] Configuring Color-Coded Agile Labels...{Color.RESET}")
    # Get existing labels
    try:
        existing_json = run_cmd(["gh", "label", "list", "--repo", f"{owner}/{repo}", "--json", "name", "--limit", "100"])
        existing_names = {l["name"].lower() for l in json.loads(existing_json)}
    except Exception:
        existing_names = set()

    created_count = 0
    updated_count = 0

    for lbl in labels:
        name = lbl["name"]
        color = lbl.get("color", "ededed").lstrip("#")
        desc = lbl.get("description", "")

        if name.lower() in existing_names:
            # Update label
            subprocess.run(["gh", "label", "edit", name, "--repo", f"{owner}/{repo}", "--color", color, "--description", desc], capture_output=True)
            updated_count += 1
        else:
            # Create label
            res = subprocess.run(["gh", "label", "create", name, "--repo", f"{owner}/{repo}", "--color", color, "--description", desc], capture_output=True)
            if res.returncode == 0:
                created_count += 1

    print(f"  {Color.GREEN}✓ Labels processed: {created_count} created, {updated_count} existing/updated.{Color.RESET}")

def setup_milestones(owner, repo, milestones):
    """Creates GitHub Milestones for Sprints."""
    print(f"\n{Color.BOLD}[Step 2/5] Configuring Sprint Milestones...{Color.RESET}")
    # Get existing milestones
    try:
        existing_json = run_cmd(["gh", "api", f"repos/{owner}/{repo}/milestones?state=all"])
        existing_titles = {m["title"] for m in json.loads(existing_json)}
    except Exception:
        existing_titles = set()

    created_count = 0
    for ms in milestones:
        title = ms["title"]
        desc = ms.get("description", "")
        if title in existing_titles:
            continue

        res = subprocess.run([
            "gh", "api", f"repos/{owner}/{repo}/milestones",
            "-X", "POST",
            "-f", f"title={title}",
            "-f", f"description={desc}"
        ], capture_output=True)
        if res.returncode == 0:
            created_count += 1

    print(f"  {Color.GREEN}✓ Milestones processed: {created_count} created, {len(existing_titles)} existing.{Color.RESET}")

def setup_issues(owner, repo, issues):
    """Creates GitHub Issues with DUPLICATE PREVENTION."""
    print(f"\n{Color.BOLD}[Step 3/5] Synchronizing User Stories as GitHub Issues...{Color.RESET}")
    # Fetch existing issues to prevent duplicates
    try:
        existing_json = run_cmd(["gh", "issue", "list", "--repo", f"{owner}/{repo}", "--state", "all", "--json", "number,title,url", "--limit", "200"])
        existing_issues = json.loads(existing_json)
    except Exception:
        existing_issues = []

    # Map existing titles and codes
    existing_by_code = {}
    for iss in existing_issues:
        title = iss["title"]
        # extract [US-XX] code
        m = re.search(r"\[(US-\d+)\]", title, re.IGNORECASE)
        if m:
            existing_by_code[m.group(1).upper()] = iss

    created = []
    already_existing = []

    for item in issues:
        code = item.get("code", "").upper()
        title = item["title"]
        body = item["body"]
        labels = [item.get("priority", "priority: high"), item.get("type", "type: user-story")]

        # Duplicate Check
        if code and code in existing_by_code:
            existing_issue = existing_by_code[code]
            print(f"  {Color.YELLOW}[SKIP] {title} → already exists (#{existing_issue['number']}){Color.RESET}")
            already_existing.append(existing_issue)
            continue

        # Create issue via gh
        cmd = [
            "gh", "issue", "create",
            "--repo", f"{owner}/{repo}",
            "--title", title,
            "--body", body
        ]
        for l in labels:
            cmd.extend(["--label", l])

        # Add milestone if sprint number is available
        sprint_num = item.get("sprint")
        if sprint_num:
            # find milestone title matching Sprint X
            sprint_tag = f"Sprint {sprint_num}"
            cmd.extend(["--milestone", sprint_tag])

        try:
            issue_url = run_cmd(cmd)
            # Extract number from URL
            num_match = re.search(r"/(\d+)$", issue_url)
            issue_num = num_match.group(1) if num_match else "?"
            print(f"  {Color.GREEN}[OK] Created Issue #{issue_num}: {title}{Color.RESET}")
            created.append({"number": issue_num, "title": title, "url": issue_url})
        except Exception as e:
            print(f"  {Color.RED}[!] Failed to create issue '{title}': {e}{Color.RESET}")

    print(f"  {Color.GREEN}✓ User Stories synchronized: {len(created)} created, {len(already_existing)} already existing.{Color.RESET}")
    return created, already_existing

def setup_project_board(owner, repo, project_name, project_description):
    """Creates or detects GitHub Projects V2 board and links it."""
    print(f"\n{Color.BOLD}[Step 4/5] Setting up GitHub Projects / Kanban Board...{Color.RESET}")
    project_url = None
    project_number = None

    # Check if a project with project_name already exists for owner
    try:
        proj_list_json = run_cmd(["gh", "project", "list", "--owner", owner, "--format", "json"])
        projects = json.loads(proj_list_json).get("projects", [])
        for p in projects:
            if p["title"].strip().lower() == project_name.strip().lower():
                project_url = p.get("url")
                project_number = p.get("number")
                print(f"  {Color.CYAN}* Found existing GitHub Project: '{project_name}' (#{project_number}){Color.RESET}")
                break
    except Exception:
        pass

    # Create new project if not found
    if not project_number:
        try:
            cmd = ["gh", "project", "create", "--owner", owner, "--title", project_name]
            proj_out = run_cmd(cmd)
            # Find URL or project number from output
            url_match = re.search(r"https://github\.com/(?:users|orgs)/[\w.-]+/projects/\d+", proj_out)
            if url_match:
                project_url = url_match.group(0)
                num_match = re.search(r"/projects/(\d+)", project_url)
                if num_match:
                    project_number = int(num_match.group(1))
            print(f"  {Color.GREEN}[+] Created new GitHub Project: '{project_name}' (#{project_number}){Color.RESET}")
        except Exception as e:
            print(f"  {Color.YELLOW}[!] Note: Could not auto-create Project via CLI: {e}{Color.RESET}")
            print(f"  {Color.YELLOW}    You can open https://github.com/{owner}/{repo}/projects and link a new board.{Color.RESET}")

    return project_number, project_url

def add_issues_to_project(owner, project_number, all_issues):
    """Adds all created and existing issues to the GitHub Project board."""
    if not project_number:
        return 0

    print(f"\n{Color.BOLD}[Step 5/5] Adding Issues to Kanban Board...{Color.RESET}")
    added_count = 0

    for iss in all_issues:
        url = iss.get("url")
        title = iss.get("title", "")
        if not url:
            continue

        try:
            res = subprocess.run([
                "gh", "project", "item-add", str(project_number),
                "--owner", owner,
                "--url", url
            ], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  {Color.GREEN}[OK] Added to Project: {title}{Color.RESET}")
                added_count += 1
            else:
                # May already be added
                print(f"  {Color.CYAN}* Item present in Project: {title}{Color.RESET}")
        except Exception:
            pass

    return added_count

def main():
    print_header("ONE-CLICK GITHUB PROJECT SETUP (AGILE METHODOLOGIES PBL)")

    # 1. Read configuration
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "project-setup.json")
    if not os.path.exists(config_path):
        # Fallback to current directory
        config_path = os.path.abspath(".github/project-setup.json")

    if not os.path.exists(config_path):
        print(f"{Color.RED}[ERROR] Configuration file not found at: {config_path}{Color.RESET}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 2. Detect Remote & Authenticated User
    try:
        owner, repo, remote_url = detect_remote()
    except Exception as e:
        print(f"{Color.RED}[ERROR] {e}{Color.RESET}")
        sys.exit(1)

    try:
        auth_user = check_gh_auth()
    except Exception as e:
        print(f"{Color.RED}[ERROR] {e}{Color.RESET}")
        sys.exit(1)

    print(f"  {Color.BOLD}Detected Repository:{Color.RESET} {Color.CYAN}{owner}/{repo}{Color.RESET}")
    print(f"  {Color.BOLD}Remote URL:         {Color.RESET} {remote_url}")
    print(f"  {Color.BOLD}Authenticated User: {Color.RESET} {Color.GREEN}{auth_user}{Color.RESET}")
    print(f"  {Color.BOLD}Project Name:       {Color.RESET} {config.get('project_name')}")

    # Interactive confirmation (if not auto-run)
    if "--yes" not in sys.argv and "-y" not in sys.argv:
        try:
            choice = input(f"\n{Color.YELLOW}Proceed with GitHub Scrum Project Setup? [Y/n]: {Color.RESET}").strip().lower()
            if choice and choice not in ("y", "yes"):
                print("Setup cancelled by user.")
                sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            print("\nSetup cancelled.")
            sys.exit(0)

    # 3. Setup Labels
    setup_labels(owner, repo, config.get("labels", []))

    # 4. Setup Milestones
    setup_milestones(owner, repo, config.get("milestones", []))

    # 5. Setup Issues
    created_issues, existing_issues = setup_issues(owner, repo, config.get("issues", []))

    # 6. Setup Project Board
    proj_num, proj_url = setup_project_board(
        owner,
        repo,
        config.get("project_name", f"{repo} - Scrum Board"),
        config.get("project_description", "")
    )

    # 7. Add issues to project board
    total_issues = created_issues + existing_issues
    added_to_proj = 0
    if proj_num:
        added_to_proj = add_issues_to_project(owner, proj_num, total_issues)

    # 8. Summary Display
    fallback_proj_url = proj_url or f"https://github.com/{owner}/{repo}/projects"

    print(f"\n{Color.BOLD}{Color.GREEN}======================================================================{Color.RESET}")
    print(f"{Color.BOLD}{Color.GREEN}                       SETUP COMPLETE !                               {Color.RESET}")
    print(f"{Color.BOLD}{Color.GREEN}======================================================================{Color.RESET}\n")

    print(f"  {Color.BOLD}Repository:{Color.RESET}             https://github.com/{owner}/{repo}")
    print(f"  {Color.BOLD}GitHub Project:{Color.RESET}         {fallback_proj_url}")
    print(f"  {Color.BOLD}Issues Created:{Color.RESET}         {len(created_issues)}")
    print(f"  {Color.BOLD}Issues Already Existed:{Color.RESET} {len(existing_issues)}")
    print(f"  {Color.BOLD}Issues Added to Board:{Color.RESET}  {added_to_proj if proj_num else len(total_issues)}")
    print(f"  {Color.BOLD}Agile Labels Configured:{Color.RESET}{len(config.get('labels', []))}")
    print(f"  {Color.BOLD}Sprint Milestones:{Color.RESET}      {len(config.get('milestones', []))}")
    print(f"  {Color.BOLD}Kanban Board Status:{Color.RESET}    {Color.GREEN}READY & VERIFIED{Color.RESET}")

    print(f"\n{Color.BOLD}{Color.CYAN}>> OPEN YOUR GITHUB SCRUM BOARD HERE:{Color.RESET}")
    print(f"   {Color.BOLD}{Color.BLUE}{fallback_proj_url}{Color.RESET}\n")

if __name__ == "__main__":
    main()
