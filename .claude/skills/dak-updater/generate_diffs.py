#!/usr/bin/env python3
"""
DAK GitHub Updater - Diff Generator

Compares an updates spreadsheet against existing DAK Excel files in a repo
and produces structured diffs for each update.

Usage: python generate_diffs.py --repo-dir /path/to/repo --updates /path/to/updates.xlsx --mapping mapping.json --output diffs.json
"""

import argparse
import glob
import json
import os
import sys

import pandas as pd


def load_dak_files(repo_dir):
    """Load all Excel files from the repo into a dict of DataFrames."""
    excel_files = glob.glob(os.path.join(repo_dir, "**/*.xlsx"), recursive=True)
    dak_data = {}
    for filepath in excel_files:
        rel_path = os.path.relpath(filepath, repo_dir)
        try:
            sheets = pd.read_excel(filepath, sheet_name=None, dtype=str)
            dak_data[rel_path] = sheets
        except Exception as e:
            print(f"Warning: Could not read {rel_path}: {e}", file=sys.stderr)
    return dak_data


def load_updates(updates_path):
    """Load the updates spreadsheet."""
    sheets = pd.read_excel(updates_path, sheet_name=None, dtype=str)
    return sheets


def find_matching_row(dak_sheet_df, id_column, id_value):
    """Find a row in a DAK sheet by an identifier column and value."""
    if id_column not in dak_sheet_df.columns:
        return None, None
    matches = dak_sheet_df[dak_sheet_df[id_column].astype(str).str.strip() == str(id_value).strip()]
    if len(matches) == 0:
        return None, None
    idx = matches.index[0]
    return idx, matches.iloc[0]


def compute_diff(old_row, new_values, columns_to_compare):
    """Compute column-level diff between old row and new values."""
    diff = {}
    for col in columns_to_compare:
        old_val = str(old_row.get(col, "")) if old_row is not None else ""
        new_val = str(new_values.get(col, ""))
        old_val = "" if old_val == "nan" else old_val
        new_val = "" if new_val == "nan" else new_val
        if old_val != new_val:
            diff[col] = {"old": old_val, "new": new_val}
    return diff


def generate_diffs(dak_data, updates_sheets, mapping):
    """
    Generate diffs for each update row.

    mapping is a dict with:
      - file_column: column in updates that identifies the target DAK file
      - sheet_column: column in updates that identifies the target sheet
      - id_column: column used to match rows (e.g., "Activity ID")
      - change_type_column: column indicating add/modify/delete (optional)
      - rationale_column: column with change rationale (optional)
      - updates_sheet: which sheet in the updates workbook to process
      - value_columns: list of columns containing the new values (optional, defaults to all)
    """
    updates_sheet_name = mapping.get("updates_sheet", list(updates_sheets.keys())[0])
    updates_df = updates_sheets[updates_sheet_name]

    file_col = mapping.get("file_column")
    sheet_col = mapping.get("sheet_column")
    id_col = mapping.get("id_column")
    change_type_col = mapping.get("change_type_column")
    rationale_col = mapping.get("rationale_column")
    value_cols = mapping.get("value_columns")

    diffs = []
    for idx, row in updates_df.iterrows():
        update = {
            "update_row": idx,
            "file": str(row.get(file_col, "unknown")) if file_col else "unknown",
            "sheet": str(row.get(sheet_col, "unknown")) if sheet_col else "unknown",
            "change_type": str(row.get(change_type_col, "modify")).lower() if change_type_col else "modify",
            "row_identifier": f"{id_col}: {row.get(id_col, 'N/A')}" if id_col else f"Row {idx}",
            "rationale": str(row.get(rationale_col, "")) if rationale_col else "",
            "summary": "",
            "diff": {},
            "matched": False,
            "match_warnings": [],
        }

        # Clean up nan values
        for key in ["file", "sheet", "change_type", "rationale"]:
            if update[key] == "nan":
                update[key] = ""

        # Try to find the target file
        target_file = None
        for dak_file in dak_data:
            if file_col and update["file"]:
                # Try exact match, then substring match
                if update["file"] in dak_file or dak_file in update["file"]:
                    target_file = dak_file
                    break
                # Try matching just the filename
                if os.path.basename(dak_file).replace(".xlsx", "").lower() in update["file"].lower():
                    target_file = dak_file
                    break

        if target_file is None and len(dak_data) == 1:
            target_file = list(dak_data.keys())[0]
            update["match_warnings"].append(f"Auto-matched to only DAK file: {target_file}")

        if target_file is None:
            update["match_warnings"].append(f"Could not match file: {update['file']}")
            update["summary"] = f"Unmatched update for file '{update['file']}'"
            diffs.append(update)
            continue

        update["file"] = target_file

        # Find the target sheet
        target_sheets = dak_data[target_file]
        target_sheet_name = None
        for sname in target_sheets:
            if sheet_col and update["sheet"]:
                if update["sheet"].lower() in sname.lower() or sname.lower() in update["sheet"].lower():
                    target_sheet_name = sname
                    break

        if target_sheet_name is None and len(target_sheets) == 1:
            target_sheet_name = list(target_sheets.keys())[0]

        if target_sheet_name is None:
            update["match_warnings"].append(f"Could not match sheet: {update['sheet']}")
            update["summary"] = f"Unmatched update for sheet '{update['sheet']}' in {target_file}"
            diffs.append(update)
            continue

        update["sheet"] = target_sheet_name
        dak_df = target_sheets[target_sheet_name]

        # Determine columns to compare
        if value_cols:
            cols_to_compare = [c for c in value_cols if c in updates_df.columns]
        else:
            # Use all columns that exist in both the updates and the DAK sheet
            cols_to_compare = [c for c in updates_df.columns if c in dak_df.columns]
            # Exclude mapping/meta columns
            exclude = [file_col, sheet_col, change_type_col, rationale_col]
            cols_to_compare = [c for c in cols_to_compare if c not in exclude]

        # Find matching row in DAK
        if id_col and id_col in updates_df.columns:
            id_value = row.get(id_col)
            match_idx, old_row = find_matching_row(dak_df, id_col, id_value)

            if update["change_type"] == "add":
                # For adds, old_row is None
                new_values = {col: row.get(col, "") for col in cols_to_compare}
                update["diff"] = {col: {"old": "—", "new": str(v) if str(v) != "nan" else ""} for col, v in new_values.items() if str(v) != "nan" and str(v) != ""}
                update["matched"] = True
                update["summary"] = f"Add new row to {target_sheet_name} ({update['row_identifier']})"
            elif old_row is not None:
                new_values = {col: row.get(col, "") for col in cols_to_compare}
                update["diff"] = compute_diff(old_row, new_values, cols_to_compare)
                update["matched"] = True
                if update["change_type"] == "delete":
                    update["summary"] = f"Delete row from {target_sheet_name} ({update['row_identifier']})"
                else:
                    changed_cols = list(update["diff"].keys())
                    update["summary"] = f"Modify {', '.join(changed_cols[:3])}{'...' if len(changed_cols) > 3 else ''} in {target_sheet_name} ({update['row_identifier']})"
            else:
                update["match_warnings"].append(f"No matching row found for {update['row_identifier']}")
                update["summary"] = f"Unmatched row: {update['row_identifier']} in {target_sheet_name}"
        else:
            update["match_warnings"].append("No ID column specified — cannot match individual rows")
            update["summary"] = f"Update to {target_sheet_name} (row matching not configured)"

        diffs.append(update)

    return diffs


def main():
    parser = argparse.ArgumentParser(description="Generate diffs between updates and DAK files")
    parser.add_argument("--repo-dir", required=True, help="Path to cloned DAK repository")
    parser.add_argument("--updates", required=True, help="Path to updates Excel file")
    parser.add_argument("--mapping", required=True, help="Path to column mapping JSON")
    parser.add_argument("--output", default="diffs.json", help="Output path for diffs JSON")
    args = parser.parse_args()

    with open(args.mapping) as f:
        mapping = json.load(f)

    print("Loading DAK files...")
    dak_data = load_dak_files(args.repo_dir)
    print(f"Loaded {len(dak_data)} DAK files")

    print("Loading updates spreadsheet...")
    updates = load_updates(args.updates)
    print(f"Updates has {len(updates)} sheets")

    print("Generating diffs...")
    diffs = generate_diffs(dak_data, updates, mapping)

    with open(args.output, "w") as f:
        json.dump(diffs, f, indent=2, default=str)

    matched = sum(1 for d in diffs if d["matched"])
    unmatched = len(diffs) - matched
    print(f"\nGenerated {len(diffs)} diffs ({matched} matched, {unmatched} unmatched)")
    print(f"Saved to {args.output}")

    if unmatched > 0:
        print("\nUnmatched updates:")
        for d in diffs:
            if not d["matched"]:
                print(f"  - Row {d['update_row']}: {'; '.join(d['match_warnings'])}")


if __name__ == "__main__":
    main()
