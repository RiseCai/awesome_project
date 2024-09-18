# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import subprocess

def get_tasks():
    """获取所有任务列表"""
    tasks = []
    tasks_dir = os.path.join('docs', 'docs', 'tasks')  # 修改这一行
    if os.path.exists(tasks_dir):
        for file in os.listdir(tasks_dir):
            if file.endswith('.md'):
                task_id = file.split('_')[0]
                with open(os.path.join(tasks_dir, file), 'r') as f:
                    title = f.readline().strip('# \n')
                tasks.append((task_id, title))
    return tasks

def select_task(tasks):
    """让用户选择一个任务"""
    print("Select a task:")
    for i, (task_id, title) in enumerate(tasks, 1):
        print("{}. [{}] {}".format(i, task_id, title))
    while True:
        try:
            choice = int(raw_input("Enter the number of the task: ")) - 1
            if 0 <= choice < len(tasks):
                return tasks[choice][0]
        except ValueError:
            pass
        print("Invalid choice. Please try again.")

def get_status():
    """让用户选择任务状态"""
    statuses = ["To Do", "In Progress", "Done"]
    print("Select the new status:")
    for i, status in enumerate(statuses, 1):
        print("{}. {}".format(i, status))
    while True:
        try:
            choice = int(raw_input("Enter the number of the status: ")) - 1
            if 0 <= choice < len(statuses):
                return statuses[choice]
        except ValueError:
            pass
        print("Invalid choice. Please try again.")

def get_message():
    """获取提交信息"""
    return raw_input("Enter the commit message: ")

def get_project_root():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip()

def main():
    print("Current working directory:", os.getcwd())
    
    # 检查是否在非交互式环境中运行
    if not sys.stdin.isatty():
        print("Running in non-interactive environment. Exiting.")
        sys.exit(0)
    
    tasks = get_tasks()
    if not tasks:
        print("No tasks found. Please create some tasks first.")
        sys.exit(1)

    task_id = select_task(tasks)
    status = get_status()
    message = get_message()

    commit_message = "[{}] {}: {}".format(task_id, status, message)

    print("\nGenerated commit message:\n{}".format(commit_message))

    # 将生成的提交消息写入文件
    project_root = get_project_root()
    commit_message_file = os.path.join(project_root, 'commit_message_file')
    with open(commit_message_file, 'w') as f:
        f.write(commit_message)

    print("Commit message has been generated. Proceed with git commit.")

if __name__ == "__main__":
    main()