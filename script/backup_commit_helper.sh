#!/bin/bash

# 设置备份目录
BACKUP_DIR="$HOME/commit_helper_backup"

# 创建备份目录（如果不存在）
mkdir -p "$BACKUP_DIR"

# 备份 commit_helper.py
cp "$(git rev-parse --show-toplevel)/script/commit_helper.py" "$BACKUP_DIR/commit_helper_$(date +%Y%m%d_%H%M%S).py"

# 备份任务文件
cp -r "$(git rev-parse --show-toplevel)/docs/docs/tasks" "$BACKUP_DIR/tasks_$(date +%Y%m%d_%H%M%S)"

echo "Backup completed. Files saved in $BACKUP_DIR"
