#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import argparse
from datetime import datetime

# 定义文档类型和它们的目录
DOC_TYPES = {
    'req': 'requirements',
    'design': 'design',
    'task': 'tasks'
}

# 文档模板
TEMPLATES = {
    'req': """# {id}: {title}

## Description
{description}

## Related Designs
<!-- Add related design documents here -->

## Related Tasks
<!-- Add related task documents here -->
""",
    'design': """# {id}: {title}

## Description
{description}

## Related Requirements
<!-- Add related requirement documents here -->

## Related Tasks
<!-- Add related task documents here -->
""",
    'task': """# {id}: {title}

## Description
{description}

## Related Requirements
<!-- Add related requirement documents here -->

## Related Designs
<!-- Add related design documents here -->

## Status
- [x] To Do
- [ ] In Progress
- [ ] Done

## Progress
- {date}: Task created
"""
}

def create_document(doc_type, title, description):
    """创建新的文档"""
    if doc_type not in DOC_TYPES:
        print("Error: Unknown document type '{}'".format(doc_type))
        return

    # 确保目录存在
    dir_path = os.path.join('docs', DOC_TYPES[doc_type])
    try:
        os.makedirs(dir_path)
    except OSError:
        if not os.path.isdir(dir_path):
            raise

    # 生成文档ID
    existing_docs = [f for f in os.listdir(dir_path) if f.endswith('.md')]
    new_id = "{}{}".format(doc_type.upper(), str(len(existing_docs) + 1).zfill(3))

    # 创建文件名
    file_name = "{}_{}".format(new_id, title.lower().replace(' ', '_')) + '.md'
    file_path = os.path.join(dir_path, file_name)

    # 使用模板创建文档内容
    content = TEMPLATES[doc_type].format(
        id=new_id,
        title=title,
        description=description,
        date=datetime.now().strftime("%Y-%m-%d")
    )

    # 写入文件
    with open(file_path, 'w') as f:
        f.write(content)

    print("Created new {} document: {}".format(doc_type, file_path))

def update_progress(task_id, status, progress_note):
    """更新任务进度"""
    task_dir = os.path.join('docs', DOC_TYPES['task'])
    task_file = None

    for file in os.listdir(task_dir):
        if file.startswith(task_id):
            task_file = os.path.join(task_dir, file)
            break

    if not task_file:
        print("Error: Task {} not found".format(task_id))
        return

    with open(task_file, 'r') as f:
        content = f.read()

    # 更新状态
    content = content.replace("- [x] To Do", "- [ ] To Do")
    content = content.replace("- [x] In Progress", "- [ ] In Progress")
    content = content.replace("- [x] Done", "- [ ] Done")
    content = content.replace("- [ ] {}".format(status), "- [x] {}".format(status))

    # 添加进度记录
    progress_entry = "- {}: {}\n".format(datetime.now().strftime('%Y-%m-%d'), progress_note)
    content = content.replace("## Progress\n", "## Progress\n{}".format(progress_entry))

    with open(task_file, 'w') as f:
        f.write(content)

    print("Updated task {}".format(task_id))

def main():
    parser = argparse.ArgumentParser(description="Manage project documentation")
    subparsers = parser.add_subparsers(dest="command")

    # 创建文档的子命令
    create_parser = subparsers.add_parser("create", help="Create a new document")
    create_parser.add_argument("type", choices=DOC_TYPES.keys(), help="Type of document")
    create_parser.add_argument("title", help="Document title")
    create_parser.add_argument("description", help="Document description")

    # 更新任务进度的子命令
    update_parser = subparsers.add_parser("update", help="Update task progress")
    update_parser.add_argument("task_id", help="Task ID (e.g., TASK001)")
    update_parser.add_argument("status", choices=["To Do", "In Progress", "Done"], help="New status")
    update_parser.add_argument("note", help="Progress note")

    args = parser.parse_args()

    if args.command == "create":
        create_document(args.type, args.title, args.description)
    elif args.command == "update":
        update_progress(args.task_id, args.status, args.note)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()