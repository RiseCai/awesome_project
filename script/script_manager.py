#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import subprocess
import argparse
import json

# 定义 V 模型的阶段及其描述
V_MODEL_STAGES = {
    "1_requirements": {
        "description": "需求分析阶段，定义系统功能和约束",
        "scripts": {
            "doc_manager.py": {
                "description": "管理需求文档",
                "usage": "python doc_manager.py create feature <project_code> <branch_code> <title> <description>",
                "input": "项目代码、分支代码、特性标题和描述",
                "output": "新的特性文档文件"
            },
            "feature_cli.py": {
                "description": "特性管理命令行界面",
                "usage": "python feature_cli.py [list|add|update|show] [args]",
                "input": "命令和相关参数",
                "output": "特性列表、更新状态或特性详情"
            }
        }
    },
    "2_system_design": {
        "description": "系统设计阶段，定义系统整体架构",
        "scripts": {}
    },
    "3_architecture_design": {
        "description": "架构设计阶段，详细设计系统组件",
        "scripts": {}
    },
    "4_module_design": {
        "description": "模块设计阶段，设计具体模块实现",
        "scripts": {}
    },
    "5_implementation": {
        "description": "实现阶段，编写和管理代码",
        "scripts": {
            "commit_helper.py": {
                "description": "辅助生成规范的提交信息",
                "usage": "python commit_helper.py",
                "input": "用户交互输入",
                "output": "格式化的提交信息"
            },
            "backup_commit_helper.sh": {
                "description": "备份提交辅助脚本",
                "usage": "bash backup_commit_helper.sh",
                "input": "无",
                "output": "commit_helper.py 的备份文件"
            },
            "check_compile.sh": {
                "description": "检查代码是否能够正确编译",
                "usage": "bash check_compile.sh",
                "input": "项目源代码",
                "output": "编译状态报告"
            },
            "check_style.sh": {
                "description": "检查代码风格是否符合规范",
                "usage": "bash check_style.sh",
                "input": "项目源代码",
                "output": "代码风格检查报告"
            },
            "format_code.sh": {
                "description": "格式化代码以符合项目规范",
                "usage": "bash format_code.sh",
                "input": "项目源代码",
                "output": "格式化后的代码"
            },
            "manage_dependencies.sh": {
                "description": "管理项目依赖",
                "usage": "bash manage_dependencies.sh [install|update|list]",
                "input": "命令参数",
                "output": "依赖管理操作结果"
            }
        }
    },
    "6_unit_tests": {
        "description": "单元测试阶段，测试单个模块功能",
        "scripts": {}
    },
    "7_integration_tests": {
        "description": "集成测试阶段，测试模块间交互",
        "scripts": {}
    },
    "8_system_tests": {
        "description": "系统测试阶段，测试整个系统功能",
        "scripts": {}
    },
    "9_acceptance_tests": {
        "description": "验收测试阶段，确认系统满足需求",
        "scripts": {}
    }
}

def list_scripts(stage):
    """列出指定阶段的所有脚本及其描述"""
    stage_info = V_MODEL_STAGES.get(stage, {})
    scripts = stage_info.get("scripts", {})
    return scripts

def run_script(stage, script):
    """运行指定的脚本"""
    script_path = os.path.join(os.path.dirname(__file__), stage, script)
    if not os.path.exists(script_path):
        print("Script not found: {}".format(script_path))
        return
    
    print("Running script: {}".format(script_path))
    if script.endswith('.py'):
        subprocess.call([sys.executable, script_path])
    elif script.endswith('.sh'):
        subprocess.call(['bash', script_path])

def show_script_details(stage, script):
    """显示脚本的详细信息"""
    script_info = V_MODEL_STAGES.get(stage, {}).get("scripts", {}).get(script, {})
    if script_info:
        print("Script: {}".format(script))
        print("Description: {}".format(script_info.get("description", "N/A")))
        print("Usage: {}".format(script_info.get("usage", "N/A")))
        print("Input: {}".format(script_info.get("input", "N/A")))
        print("Output: {}".format(script_info.get("output", "N/A")))
    else:
        print("No detailed information available for this script.")

def main():
    parser = argparse.ArgumentParser(description="Script Manager for V-Model Development")
    parser.add_argument("stage", choices=list(V_MODEL_STAGES.keys()) + ["all"], help="Select the development stage or 'all' to list all scripts")
    parser.add_argument("--run", help="Specify the script to run")
    parser.add_argument("--info", help="Show detailed information about a specific script")
    
    args = parser.parse_args()

    if args.stage == "all":
        for stage in sorted(V_MODEL_STAGES.keys()):
            info = V_MODEL_STAGES[stage]
            print("\n{}: {}".format(stage, info["description"]))
            scripts = list_scripts(stage)
            for script, script_info in scripts.items():
                print("  - {}: {}".format(script, script_info["description"]))
    else:
        if args.info:
            show_script_details(args.stage, args.info)
        elif args.run:
            scripts = list_scripts(args.stage)
            if args.run in scripts:
                run_script(args.stage, args.run)
            else:
                print("Script '{}' not found in stage '{}'".format(args.run, args.stage))
        else:
            print("{}: {}".format(args.stage, V_MODEL_STAGES[args.stage]["description"]))
            scripts = list_scripts(args.stage)
            for script, script_info in scripts.items():
                print("  - {}: {}".format(script, script_info["description"]))

if __name__ == "__main__":
    main()
