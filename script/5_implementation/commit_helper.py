#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
from datetime import datetime

def get_features():
    """获取所有未完成的功能列表"""
    print("Debug: Entering get_features function")
    features = []
    features_dir = os.path.join('docs', 'docs', 'features')
    print("Debug: Features directory:", features_dir)
    if os.path.exists(features_dir):
        print("Debug: Features directory exists")
        for file in os.listdir(features_dir):
            print("Debug: Found file:", file)
            if file.endswith('.md'):
                feature_id = file.split('_')[0]
                with open(os.path.join(features_dir, file), 'r') as f:
                    title = f.readline().strip('# \n')
                    content = f.read()
                    if "Status: Done" not in content:
                        status = "To Do" if "Status: To Do" in content else "In Progress"
                        features.append((feature_id, title, status))
                        print(f"Debug: Added feature: {feature_id}, {title}, {status}")
    else:
        print("Debug: Features directory does not exist")
    return sorted(features, key=lambda x: x[0])

def display_features(features):
    """显示功能列表"""
    print("Current features:")
    for i, (feature_id, title, status) in enumerate(features, 1):
        print(f"{i}. [{feature_id}] {title} - Status: {status}")
    print("\nOptions:")
    print("- Enter a number (e.g., '1', '2', '3') to select a feature")
    print("- Enter 'n' to create a new feature")
    print("- Enter 's' to skip the helper and enter a commit message directly")

def select_feature(features):
    """让用户选择一个功能"""
    while True:
        choice = input("Your choice (number, 'n', or 's'): ").lower()
        if choice == 'n' or choice == 's':
            return choice
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(features):
                return features[choice_num - 1][0]
        except ValueError:
            pass
        print(f"Invalid choice. Please enter a number between 1 and {len(features)}, 'n', or 's'.")

def generate_new_feature_id(features):
    """生成新的唯一功能ID"""
    existing_ids = [feature[0] for feature in features]
    max_id = max([int(re.findall(r'\d+', feature_id)[0]) for feature_id in existing_ids if re.findall(r'\d+', feature_id)], default=0)
    new_id = max_id + 1
    return "FEATURE{:03d}".format(new_id)

def create_new_feature(features):
    feature_id = generate_new_feature_id(features)
    title = input("Enter feature title: ")
    description = input("Enter feature description: ")
    
    feature_file = os.path.join('docs', 'docs', 'features', "{0}_{1}.md".format(feature_id, title.replace(' ', '_')))
    with open(feature_file, 'w') as f:
        f.write("# {0}\n\n{1}\n\nStatus: To Do\n".format(title, description))
    
    print("New feature created: {0}".format(feature_file))
    return feature_id, title

def get_status():
    """让用户选择功能状态"""
    statuses = ["To Do", "In Progress", "Done"]
    print("Select the new status:")
    for i, status in enumerate(statuses, 1):
        print(f"{i}. {status}")
    while True:
        try:
            choice = input("Enter the number of the status (1, 2, or 3): ")
            choice_num = int(choice)
            if 1 <= choice_num <= len(statuses):
                return statuses[choice_num - 1]
        except ValueError:
            pass
        print(f"Invalid choice. Please enter a number between 1 and {len(statuses)}.")

def get_message():
    """获取提交信息"""
    return input("Enter the commit message (e.g., 'Implemented new feature'): ")

def get_project_root():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')

def update_feature_status(feature_id, new_status):
    features_dir = os.path.join('docs', 'docs', 'features')
    for file in os.listdir(features_dir):
        if file.startswith(feature_id) and file.endswith('.md'):
            file_path = os.path.join(features_dir, file)
            with open(file_path, 'r') as f:
                content = f.read()
            
            content = re.sub(r'Status: .*', f'Status: {new_status}', content)
            
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Updated status of feature {feature_id} to {new_status}")
            break

def main():
    print("Debug: Entering main function")
    print("Current working directory: {0}".format(os.getcwd()))
    
    if not sys.stdin.isatty():
        print("Running in non-interactive environment. Exiting.")
        sys.exit(0)
    
    features = get_features()
    print("Debug: Found {0} unfinished features".format(len(features)))
    
    if not features:
        print("No unfinished features found. Creating a new feature.")
        feature_id, title = create_new_feature(features)
        status = "To Do"
        message = title
    else:
        print("Debug: Displaying unfinished features")
        display_features(features)
        while True:
            choice = select_feature(features)

            if choice == 'n':
                feature_id, title = create_new_feature(features)
                status = "To Do"
                message = title
                break
            elif choice == 's':
                commit_message = input("Enter your commit message: ")
                with open(os.path.join(get_project_root(), 'commit_message_file'), 'w') as f:
                    f.write(commit_message)
                print("Commit message saved. Proceeding with git commit.")
                sys.exit(0)
            else:
                feature_id = choice
                status = get_status()
                message = get_message()
                break

    commit_message = f"[{feature_id}] {status}: {message}"

    print(f"\nGenerated commit message:\n{commit_message}")

    project_root = get_project_root()
    commit_message_file = os.path.join(project_root, 'commit_message_file')
    with open(commit_message_file, 'w') as f:
        f.write(commit_message)

    print(f"Commit message has been generated and saved to {commit_message_file}")
    print(f"Use 'git commit -F {commit_message_file}' to commit with this message.")

    update_feature_status(feature_id, status)

if __name__ == "__main__":
    main()

__all__ = ['get_features', 'create_new_feature', 'update_feature_status']