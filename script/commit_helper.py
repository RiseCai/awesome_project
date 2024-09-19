#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
from datetime import datetime

print("Debug: Script started")
print("Python version:", sys.version)
print("Current working directory:", os.getcwd())

def get_tasks():
    """获取所有未完成的任务列表"""
    print("Debug: Entering get_tasks function")
    tasks = []
    tasks_dir = os.path.join('docs', 'docs', 'tasks')
    print("Debug: Tasks directory:", tasks_dir)
    if os.path.exists(tasks_dir):
        print("Debug: Tasks directory exists")
        for file in os.listdir(tasks_dir):
            print("Debug: Found file:", file)
            if file.endswith('.md'):
                task_id = file.split('_')[0]
                with open(os.path.join(tasks_dir, file), 'r') as f:
                    title = f.readline().strip('# \n')
                    # 读取文件内容来确定状态
                    content = f.read()
                    if "Status: Done" not in content:
                        status = "To Do" if "Status: To Do" in content else "In Progress"
                        tasks.append((task_id, title, status))
                        print(f"Debug: Added task: {task_id}, {title}, {status}")
    else:
        print("Debug: Tasks directory does not exist")
    return sorted(tasks, key=lambda x: x[0])

def display_tasks(tasks):
    """显示任务列表"""
    print("Current tasks:")
    for i, (task_id, title, status) in enumerate(tasks, 1):
        print(f"{i}. [{task_id}] {title} - Status: {status}")
    print("\nOptions:")
    print("- Enter a number (e.g., '1', '2', '3') to select a task")
    print("- Enter 'n' to create a new task")
    print("- Enter 's' to skip the helper and enter a commit message directly")

def select_task(tasks):
    """让用户选择一个任务"""
    while True:
        choice = input("Your choice (number, 'n', or 's'): ").lower()
        if choice == 'n' or choice == 's':
            return choice
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(tasks):
                return tasks[choice_num - 1][0]
        except ValueError:
            pass
        print(f"Invalid choice. Please enter a number between 1 and {len(tasks)}, 'n', or 's'.")

def generate_new_task_id(tasks):
    """生成新的唯一任务ID"""
    existing_ids = [task[0] for task in tasks]
    max_id = max([int(re.findall(r'\d+', task_id)[0]) for task_id in existing_ids if re.findall(r'\d+', task_id)], default=0)
    new_id = max_id + 1
    return "TASK{:03d}".format(new_id)

def create_new_task(tasks):
    task_id = generate_new_task_id(tasks)
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    
    task_file = os.path.join('docs', 'docs', 'tasks', "{0}_{1}.md".format(task_id, title.replace(' ', '_')))
    with open(task_file, 'w') as f:
        f.write("# {0}\n\n{1}\n\nStatus: To Do\n".format(title, description))
    
    print("New task created: {0}".format(task_file))
    return task_id, title

def get_status():
    """让用户选择任务状态"""
    statuses = ["To Do", "In Progress", "Done"]
    print("Select the new status:")
    for i, status in enumerate(statuses, 1):
        print("{}. {}".format(i, status))
    while True:
        try:
            choice = int(input("Enter the number of the status: ")) - 1
            if 0 <= choice < len(statuses):
                return statuses[choice]
        except ValueError:
            pass
        print("Invalid choice. Please try again.")

def get_message():
    """获取提交信息"""
    return input("Enter the commit message (e.g., 'Implemented new feature'): ")

def get_project_root():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')

def update_task_status(task_id, new_status):
    tasks_dir = os.path.join('docs', 'docs', 'tasks')
    for file in os.listdir(tasks_dir):
        if file.startswith(task_id) and file.endswith('.md'):
            file_path = os.path.join(tasks_dir, file)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # 更新状态
            content = re.sub(r'Status: .*', f'Status: {new_status}', content)
            
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Updated status of task {task_id} to {new_status}")
            break

def main():
    print("Debug: Entering main function")
    print("Current working directory: {0}".format(os.getcwd()))
    
    if not sys.stdin.isatty():
        print("Running in non-interactive environment. Exiting.")
        sys.exit(0)
    
    tasks = get_tasks()
    print("Debug: Found {0} unfinished tasks".format(len(tasks)))
    
    if not tasks:
        print("No unfinished tasks found. Creating a new task.")
        task_id, title = create_new_task(tasks)
        status = "To Do"
        message = title
    else:
        print("Debug: Displaying unfinished tasks")
        display_tasks(tasks)
        while True:
            choice = select_task(tasks)

            if choice == 'n':
                task_id, title = create_new_task(tasks)
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
                task_id = choice
                status = get_status()
                message = get_message()
                break

    commit_message = f"[{task_id}] {status}: {message}"

    print(f"\nGenerated commit message:\n{commit_message}")

    project_root = get_project_root()
    commit_message_file = os.path.join(project_root, 'commit_message_file')
    with open(commit_message_file, 'w') as f:
        f.write(commit_message)

    print(f"Commit message has been generated and saved to {commit_message_file}")
    print(f"Use 'git commit -F {commit_message_file}' to commit with this message.")

    # 更新任务状态
    update_task_status(task_id, status)

if __name__ == "__main__":
    main()