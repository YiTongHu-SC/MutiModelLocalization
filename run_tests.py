#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本 - 简化测试执行的脚本
"""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """运行所有测试"""
    project_root = Path(__file__).parent
    
    print("🚀 运行 MultiModelLocalization 测试套件...")
    print("-" * 50)
    
    # 运行pytest
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/test_translators.py", 
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=project_root)
        
        if result.returncode == 0:
            print("\n✅ 所有测试通过！")
        else:
            print(f"\n❌ 测试失败，退出代码：{result.returncode}")
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ 运行测试时发生错误：{e}")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
