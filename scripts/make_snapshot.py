#!/usr/bin/env python3

import os
import datetime
import subprocess

# --- Configuration ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
date = datetime.datetime.now().strftime("%Y%m%d-%H%M")
output_file = os.path.join(project_root, "snapshots", f"ElysiumProject3.0-ConsolidatedContent-{date}.txt")

# --- Helper Function ---
def is_text_file(filepath):
    try:
        with open(filepath, 'rt') as check_file:  # try opening file in text mode
            check_file.read(512)  # read a small chunk
        return True
    except UnicodeDecodeError:
        return False

# --- Main Script ---

try:
    # 1. Read README.md and VERSION.md
    readme_path = os.path.join(project_root, "README.md")
    version_path = os.path.join(project_root, "VERSION.md")

    if os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        os.makedirs(os.path.dirname(output_file), exist_ok=True) #create directory if it doesn't exist
        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write("# --- File: README.md ---\n")
            out_f.write(readme_content)

    if os.path.isfile(version_path):
        with open(version_path, "r", encoding="utf-8") as f:
            version_content = f.read()
        with open(output_file, "a", encoding="utf-8") as out_f:
            out_f.write("# --- File: VERSION.md ---\n")
            out_f.write(version_content)

    # 2. Get tree output
    tree_output = subprocess.run(["tree", os.path.join(script_dir, "..")], capture_output=True, text=True, check=True).stdout
    with open(output_file, "a", encoding="utf-8") as out_f:
        out_f.write("# --- Directory Tree (../scripts) ---\n")
        out_f.write(tree_output)

    # 3. Recurse and append file contents
    for root, _, files in os.walk(project_root):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                relative_path = os.path.relpath(file_path, project_root)
                # Add this condition to skip files containing "ConsolidatedContent"
                if "ConsolidatedContent" in file:
                    continue
                if is_text_file(file_path):
                    with open(output_file, "a", encoding="utf-8") as out_f:
                        out_f.write(f"# --- File: {relative_path} ---\n")
                    with open(file_path, "r", encoding="utf-8") as in_f:
                        file_content = in_f.read()
                    with open(output_file, "a", encoding="utf-8") as out_f:
                        out_f.write(file_content)
                else:
                    with open(output_file, "a", encoding="utf-8") as out_f:
                        out_f.write(f"# --- File: {relative_path} (Binary file, skipped) ---\n")

    print(f"Content generated and saved to: {output_file}")

except Exception as e:
    print(f"Error during script execution: {e}")