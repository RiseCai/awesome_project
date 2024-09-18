#!/bin/bash

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 定义依赖
DEPENDENCIES=(
    "imgui,https://github.com/ocornut/imgui.git"
    "SDL2,https://github.com/libsdl-org/SDL.git"
)

# 在脚本开头添加这个函数
is_git_repository() {
    git rev-parse --is-inside-work-tree >/dev/null 2>&1
}

# 查找项目根目录（包含.git文件夹的最近父目录）
find_project_root() {
    local current_dir="$PWD"
    while [[ "$current_dir" != "/" ]]; do
        if [[ -d "$current_dir/.git" ]]; then
            echo "$current_dir"
            return 0
        fi
        current_dir="$(dirname "$current_dir")"
    done
    return 1
}

# 切换到项目根目录
switch_to_project_root() {
    local root_dir=$(find_project_root)
    if [[ -n "$root_dir" ]]; then
        cd "$root_dir"
        echo -e "${GREEN}Switched to project root: $root_dir${NC}"
    else
        echo -e "${RED}Error: Could not find the root of the git repository.${NC}"
        exit 1
    fi
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 初始化依赖
init_dependencies() {
    echo -e "${YELLOW}Initializing dependencies...${NC}"
    mkdir -p external
    cd external || exit
    local init_success=true
    for dep in "${DEPENDENCIES[@]}"; do
        IFS=',' read -r name url <<< "$dep"
        if [ ! -d "$name" ]; then
            echo -e "${GREEN}Cloning $name...${NC}"
            if git submodule add "$url" "$name"; then
                echo -e "${GREEN}Successfully cloned $name${NC}"
            else
                echo -e "${RED}Failed to clone $name${NC}"
                init_success=false
            fi
        else
            echo -e "${YELLOW}$name already exists. Skipping...${NC}"
        fi
    done
    cd ..
    if $init_success; then
        if git submodule update --init --recursive; then
            echo -e "${GREEN}Dependencies initialized successfully.${NC}"
        else
            echo -e "${RED}Failed to update submodules.${NC}"
            init_success=false
        fi
    fi
    if ! $init_success; then
        echo -e "${RED}Some dependencies failed to initialize. Please check the errors above.${NC}"
    fi
}

# 更新依赖
update_dependencies() {
    echo -e "${YELLOW}Updating dependencies...${NC}"
    git submodule update --remote --merge
    echo -e "${GREEN}Dependencies updated.${NC}"
}

# 检查依赖状态
check_dependencies() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
    git submodule status
}

# 清理依赖
clean_dependencies() {
    echo -e "${YELLOW}Cleaning dependencies...${NC}"
    read -p "Are you sure you want to remove all dependencies? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for dep in "${DEPENDENCIES[@]}"; do
            IFS=',' read -r name _ <<< "$dep"
            if [ -d "external/$name" ]; then
                echo -e "${RED}Removing $name...${NC}"
                git submodule deinit -f "external/$name"
                git rm -f "external/$name"
                rm -rf ".git/modules/external/$name"
            fi
        done
        echo -e "${GREEN}Dependencies cleaned.${NC}"
    else
        echo -e "${YELLOW}Clean operation cancelled.${NC}"
    fi
}

# 主菜单
main_menu() {
    # 检查是否安装了 git
    if ! command_exists git; then
        echo -e "${RED}Error: git is not installed. Please install git and try again.${NC}"
        exit 1
    fi

    # 切换到项目根目录
    switch_to_project_root

    # 检查是否在 Git 仓库中
    if ! is_git_repository; then
        echo -e "${RED}Error: Current directory is not a git repository. Please run this script from within your git project.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Dependency Management Script${NC}"
    echo "1) Initialize dependencies"
    echo "2) Update dependencies"
    echo "3) Check dependencies status"
    echo "4) Clean dependencies"
    echo "5) Exit"
    read -p "Enter your choice: " choice
    case $choice in
        1) init_dependencies ;;
        2) update_dependencies ;;
        3) check_dependencies ;;
        4) clean_dependencies ;;
        5) exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
}

# 检查是否安装了 git
if ! command_exists git; then
    echo -e "${RED}Error: git is not installed. Please install git and try again.${NC}"
    exit 1
fi

# 运行主菜单
while true; do
    main_menu
    echo
done