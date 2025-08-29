#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MultiModelLocalization 安装脚本
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "Readme.md").read_text(encoding='utf-8')

# 读取requirements
requirements = [
    "PyYAML>=6.0.1",
    "volcenginesdkarkruntime>=1.0.11",
    "openai>=1.0.0",
    "pandas>=1.3.0",
    "openpyxl>=3.0.0"
]

setup(
    name="MultiModelLocalization",
    version="0.0.4",
    author="MultiModelLocalization Team",
    author_email="",
    description="基于大语言模型的本地化翻译工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/MultiModelLocalization",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "multimodel-localization=src.core.Localization:main",
        ],
    },
    include_package_data=True,
    package_data={
        "configs": ["*.yaml"],
        "data": ["**/*.json"],
    },
)