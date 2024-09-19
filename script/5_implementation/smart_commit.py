#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import os
import re
import tempfile
from datetime import datetime

def get_current_branch():
    result = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8')
    return result.strip()

def get_feature_id():
    # 首先尝试从分支名称获取 feature ID
    branch = get_current_branch()
    match = re.search(r'(MAIN|SUB\d+)-([A-Z]+)-F(\d{7})', branch)
    if match:
        return match.group(0)
    
    # 如果分支名称中没有 feature ID，则尝试从最近创建的 feature 文件中获取
    features_dir = os.path.join('docs', 'docs', 'features')
    if os.path.exists(features_dir):
        feature_files = sorted(
            [f for f in os.listdir(features_dir) if f.startswith('MAIN-DEV-F') and f.endswith('.md')],
            reverse=True
        )
        if feature_files:
            return feature_files[0].split('_')[0]
    
    # 如果无法自动获取 feature ID，则提示用户输入
    try:
        return raw_input("Enter feature ID (e.g., MAIN-DEV-F2300001): ")
    except NameError:
        return input("Enter feature ID (e.g., MAIN-DEV-F2300001): ")

def get_changed_files():
    result = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8')
    return result.strip().split('\n')

def categorize_changes(changes):
    categories = {
        'Added': [],
        'Modified': [],
        'Deleted': [],
        'Renamed': [],
        'Untracked': []
    }
    for change in changes:
        if change:
            status, filename = change.split(' ', 1)
            if status == 'A':
                categories['Added'].append(filename)
            elif status == 'M':
                categories['Modified'].append(filename)
            elif status == 'D':
                categories['Deleted'].append(filename)
            elif status == 'R':
                categories['Renamed'].append(filename)
            elif status == '??':
                categories['Untracked'].append(filename)
    return categories

def get_file_type(filename):
    _, ext = os.path.splitext(filename)
    if ext in ['.py', '.pyc']:
        return 'Python'
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        return 'JavaScript/TypeScript'
    elif ext in ['.html', '.htm']:
        return 'HTML'
    elif ext in ['.css', '.scss', '.sass']:
        return 'CSS'
    elif ext in ['.md', '.markdown']:
        return 'Markdown'
    elif ext in ['.json', '.yaml', '.yml']:
        return 'Configuration'
    else:
        return 'Other'

def generate_commit_message(feature_id, changes):
    categories = categorize_changes(changes)
    
    message = "[{0}] Update related to V-model script management\n\n".format(feature_id)
    
    # Add a summary of changes
    for category, files in categories.items():
        if files:
            message += "- {0} {1} file(s)\n".format(category, len(files))
    
    message += "\nDetailed changes:\n"
    for category, files in categories.items():
        for file in files:
            file_type = get_file_type(file)
            message += "- {0} [{1}]: {2}\n".format(category, file_type, file)
    
    return message

def edit_message(message):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        temp.write(message)
        temp_filename = temp.name
    
    editor = os.environ.get('EDITOR', 'vim')
    subprocess.call([editor, temp_filename])
    
    with open(temp_filename, 'r') as temp:
        edited_message = temp.read()
    
    os.unlink(temp_filename)
    return edited_message

def select_files_to_commit(changes):
    print("Select files to commit:")
    for i, change in enumerate(changes):
        print("{0}. {1}".format(i + 1, change))
    
    try:
        selected = raw_input("Enter the numbers of files to commit (comma-separated) or 'all': ")
    except NameError:
        selected = input("Enter the numbers of files to commit (comma-separated) or 'all': ")
    if selected.lower() == 'all':
        return changes
    else:
        selected_indices = [int(x.strip()) - 1 for x in selected.split(',')]
        return [changes[i] for i in selected_indices if 0 <= i < len(changes)]

def create_commit(message, selected_files):
    for file in selected_files:
        subprocess.call(['git', 'add', file.split(' ', 1)[1]])
    subprocess.call(['git', 'commit', '-m', message])
    print("Commit created successfully.")

def main():
    feature_id = get_feature_id()
    changes = get_changed_files()
    
    if not changes:
        print("No changes to commit.")
        return
    
    selected_files = select_files_to_commit(changes)
    if not selected_files:
        print("No files selected for commit.")
        return
    
    initial_message = generate_commit_message(feature_id, selected_files)
    print("Initial commit message:")
    print(initial_message)
    print("\nYou can now edit the commit message. Save and close the editor when done.")
    
    final_message = edit_message(initial_message)
    
    print("\nFinal commit message:")
    print(final_message)
    
    try:
        confirm = raw_input("Do you want to proceed with this commit? (y/n): ")
    except NameError:
        confirm = input("Do you want to proceed with this commit? (y/n): ")
    if confirm.lower() == 'y':
        create_commit(final_message, selected_files)
    else:
        print("Commit cancelled.")

if __name__ == "__main__":
    main()
