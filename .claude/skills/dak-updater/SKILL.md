---
name: dak-github-updater
description: "Process updates to WHO SMART Guidelines Digital Adaptation Kit (DAK) Excel files stored in a GitHub repository. Use this skill whenever the user wants to apply changes, updates, or revisions to a DAK repository — including uploading a spreadsheet of proposed changes, reviewing diffs against existing DAK Excel files, creating GitHub issues for each update, and assigning those issues to Copilot for automated pull requests. Also trigger when the user mentions 'DAK updates', 'L2 updates', 'decision table changes', 'indicator updates', 'data dictionary changes', or any reference to updating SMART Guidelines spreadsheets in a GitHub repo. Even if the user just says 'I have DAK updates' or 'process these changes against the repo', use this skill."
---

# DAK GitHub Updater

This skill processes a user-uploaded Excel spreadsheet containing proposed updates to a WHO SMART Guidelines Digital Adaptation Kit (DAK), compares each update against the existing DAK Excel files in a GitHub repository, generates a summary and diff for each change, and creates GitHub issues assigned to Copilot to implement the changes via pull requests.

## Prerequisites

- The user must have a GitHub repo containing the DAK Excel files
- The user must provide (or you must ask for):
  1. The **GitHub repository** URL or `owner/repo` identifier
  2. A **GitHub Personal Access Token** (PAT) with `repo` scope (for creating issues and assigning them)
  3. The **updates spreadsheet** (uploaded as an Excel file)

## Workflow

### Step 1: Gather Information

Ask the user for:

1. **The GitHub repository** — e.g. `myorg/smart-dak-hiv` or a full URL. Confirm the branch to target (default: `main`).
2. **A GitHub Personal Access Token** — needed to create issues. Remind the user this is used only in this session and not stored. The token needs `repo` scope.
3. **The updates Excel file** — the user should upload this. It contains the proposed changes to the DAK.

If the user has already provided some of these in their message, don't re-ask for them.

### Step 2: Understand the Updates Spreadsheet

Read the uploaded updates spreadsheet using pandas. Examine its structure:

```python
import pandas as pd

df = pd.read_excel('/mnt/user-data/uploads/<filename>', sheet_name=None)
# Print all sheet names and first few rows of each
for name, sheet in df.items():
    print(f"\n=== Sheet: {name} ===")
    print(sheet.head())
    print(f"Columns: {list(sheet.columns)}")
    print(f"Rows: {len(sheet)}")
```

The updates spreadsheet may have various formats. Common patterns include:

- A column identifying **which DAK file/sheet/section** the update applies to (e.g., "Sheet", "Tab", "Component", "File")
- A column identifying the **row or element** being changed (e.g., "Activity ID", "Element ID", "Row Number", "Data Element")
- Columns showing **old value** vs **new value**, or just the **new value** with context
- A column with **description/rationale** for the change
- A column with **change type** (Add, Modify, Delete)

If the structure is unclear, show the user the first few rows and ask them to clarify which columns map to what. Specifically ask:

- Which column identifies the target DAK file or sheet?
- Which column identifies the specific row/element to change?
- Which columns contain the actual changes?
- Is there a change-type column (add/modify/delete)?

### Step 3: Clone and Index the Repository

Clone the target repository and index the existing DAK Excel files:

```python
import subprocess
import os
import glob

# Clone the repo
repo_dir = '/home/claude/dak-repo'
subprocess.run(['git', 'clone', '--depth', '1', '-b', branch, repo_url, repo_dir], check=True)

# Find all Excel files
excel_files = glob.glob(os.path.join(repo_dir, '**/*.xlsx'), recursive=True)
print(f"Found {len(excel_files)} Excel files:")
for f in excel_files:
    print(f"  - {os.path.relpath(f, repo_dir)}")
```

Read each DAK Excel file and build an index of their sheets and content so you can match updates to the correct file and location:

```python
dak_index = {}
for filepath in excel_files:
    rel_path = os.path.relpath(filepath, repo_dir)
    wb_sheets = pd.read_excel(filepath, sheet_name=None)
    dak_index[rel_path] = {
        name: {
            'columns': list(sheet.columns),
            'row_count': len(sheet),
            'sample': sheet.head(3).to_dict()
        }
        for name, sheet in wb_sheets.items()
    }
```

### Step 4: Match Updates to DAK Files

For each update row in the updates spreadsheet, determine:

1. **Which DAK Excel file** it targets
2. **Which sheet** within that file
3. **Which row(s)** are affected
4. **What the change is** (add, modify, or delete)

Use fuzzy matching if the update references don't exactly match file/sheet names. Present any ambiguous matches to the user for confirmation.

### Step 5: Generate Diffs for Each Update

For each update, produce a clear diff showing:

- **File**: The relative path to the DAK Excel file
- **Sheet**: The sheet name
- **Location**: Row number(s) and column(s) affected
- **Change Type**: Add / Modify / Delete
- **Before**: Current values in the DAK (for modify/delete)
- **After**: New values from the updates spreadsheet (for add/modify)
- **Summary**: A human-readable 1-2 sentence description of the change

Format diffs as structured data so they can be included in GitHub issues:

```
### Change Summary
**File:** `path/to/dak-file.xlsx`
**Sheet:** Decision Logic
**Row:** 15 (Activity ID: HIV.B7.DT)
**Type:** Modify

| Column | Current Value | New Value |
|--------|--------------|-----------|
| Condition | Age > 18 | Age >= 15 |
| Action | Recommend test | Recommend test annually |

**Rationale:** Updated per WHO 2024 guidelines to lower testing age threshold.
```

### Step 6: Present Updates to User for Review

Before creating issues, present a summary of ALL updates to the user:

- Total number of updates found
- Breakdown by file, sheet, and change type
- Any updates that couldn't be matched to existing DAK content (flag these)
- Any potential conflicts or overlapping changes

Ask the user to confirm they want to proceed with creating GitHub issues, or if they want to adjust anything.

### Step 7: Create GitHub Issues

For each confirmed update, create a GitHub issue using the GitHub API:

```python
import requests
import json

def create_github_issue(owner, repo, token, title, body, labels=None, assignees=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": body,
        "labels": labels or ["dak-update"],
        "assignees": assignees or []
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
```

#### Issue Title Format
Use a clear, descriptive title:
```
[DAK Update] <Change Type> <Sheet>: <Brief Description>
```
Examples:
- `[DAK Update] Modify Decision Logic: Update HIV testing age threshold`
- `[DAK Update] Add Data Dictionary: New data element for PrEP eligibility`
- `[DAK Update] Delete Indicator: Remove deprecated viral load indicator`

#### Issue Body Format
Each issue body should contain:

1. **Summary** — 1-2 sentence human-readable description
2. **Change Details** — The full diff table (from Step 5)
3. **File and Location** — Exact file path, sheet name, row/column references
4. **Instructions for Implementation** — Clear, specific instructions that an automated agent (Copilot) can follow to make the change in the Excel file. Be explicit:
   - For **Modify**: "In file `X`, sheet `Y`, row `Z`, change column `A` from `old` to `new`"
   - For **Add**: "In file `X`, sheet `Y`, insert a new row after row `Z` with values: ..."
   - For **Delete**: "In file `X`, sheet `Y`, delete row `Z` (Activity ID: ...)"
5. **Rationale** — Why this change is being made (from the updates spreadsheet if available)
6. **Labels** — Apply `dak-update` label and any component-specific labels

#### Assigning to Copilot

To assign the issue to GitHub Copilot for automated implementation, add `copilot` to the assignees list when creating the issue. Note: Copilot workspace / Copilot coding agent must be enabled on the repository for this to work.

```python
create_github_issue(
    owner=owner,
    repo=repo,
    token=token,
    title=title,
    body=body,
    labels=["dak-update", component_label],
    assignees=["copilot"]
)
```

If assigning to Copilot fails (e.g., not enabled on the repo), fall back to creating the issue without assignment and let the user know they may need to enable Copilot or assign manually. Also try using `@copilot` mention in the issue body as a fallback.

### Step 8: Report Results

After all issues are created, present a summary:

- Total issues created (with links)
- Any issues that failed to create (with error details)
- Any updates that were skipped and why
- Next steps for the user (e.g., monitor Copilot PRs, review and merge)

## Error Handling

- **Network errors**: If the GitHub API is unreachable, save the issue bodies locally as markdown files so the user can create them manually.
- **Auth errors**: If the token is invalid or lacks permissions, explain what scopes are needed.
- **Matching failures**: If an update can't be matched to a DAK file, flag it clearly and ask the user.
- **Rate limiting**: If hitting GitHub API rate limits, add delays between issue creation.

## Important Notes

- Always preserve the exact structure and formatting of DAK Excel files — these follow WHO SMART Guidelines standards.
- DAK files commonly include sheets like: Health Interventions, Decision Logic, Indicators, Data Dictionary, Scheduling Logic, Functional Requirements, and others.
- Activity IDs and Element IDs are critical identifiers — always include them in diffs and issue descriptions.
- When in doubt about a match or change, ask the user rather than guessing.
- Process updates one at a time to ensure accuracy, but create issues efficiently.
