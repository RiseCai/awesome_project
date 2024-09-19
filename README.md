# awesome_project!

## 提交流程

本项目使用自定义的提交流程来确保提交信息的一致性和可追踪性。请按照以下步骤进行代码提交：

1. 确保您的更改已经准备好提交。
2. 运行 `git add .` 或 `git add <file>` 将更改添加到暂存区。
3. 使用 `git ch` 命令代替普通的 `git commit`。这将启动我们的自定义提交助手。
4. 按照提示选择相关的任务、状态，并输入简短的提交描述。
5. 提交助手将自动生成格式化的提交信息并完成提交。

注意：如果您需要使用常规的 git commit 命令，请使用 `git commit` 而不是 `git ch`。

### 安装提交助手

新团队成员需要执行以下步骤来设置提交助手：

1. 确保您的系统安装了 Python 2.7。
2. 克隆项目后，运行以下命令设置 Git 别名：
   ```
   git config --global alias.ch '!python2.7 "$(git rev-parse --show-toplevel)/script/commit_helper.py" && git commit -F "$(git rev-parse --show-toplevel)/commit_message_file"'
   ```

如果您在使用提交助手时遇到任何问题，请联系项目维护者。

## 代码风格和质量

我们遵循以下代码风格指南：

- C代码：基于Linux内核编码风格，但针对不同平台有特定调整
- CMake代码：KDE项目的CMake编码风格指南

## 开发环境设置

本项目支持多个平台（Linux, macOS, Windows, Android, RTOS）。请确保您的开发环境能够编译和测试所有目标平台的代码。

### 必要的工具

- GCC (用于 Linux)
- Clang (用于 macOS)
- MinGW-w64 (用于 Windows 交叉编译)
- Android NDK (用于 Android)
- 您的 RTOS 特定工具链

### 代码风格和质量检查

在提交代码之前，请运行以下命令：

./script/check_style.sh
./script/check_compile.sh

如果发现任何问题，请使用 `./script/format_code.sh` 来自动修复大多数格式问题。
