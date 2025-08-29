#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MultiModelLocalization 主入口文件
基于大语言模型的本地化翻译工具
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.core.Localization import main

if __name__ == "__main__":
    main()
