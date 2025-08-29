import argparse
import json
import os
import sys
from typing import Any, Dict

import pandas as pd
import yaml

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.Localization import *

"""
BunnyLocalization.py 是一个基于多语言本地化工具的脚本，主要功能包括：

配置文件加载：从 YAML 配置文件中读取配置信息。
Excel 转 JSON：将 Excel 文件中的数据转换为指定的 JSON 格式。
本地化处理：根据配置文件中的设置，生成多语言本地化文件。
命令行支持：通过命令行参数指定配置文件路径
"""


class Configuration:
    """
    配置文件类，用于加载和管理配置文件。
    """

    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化Configuration对象，加载配置文件。

        Args:
            config_path (str): 配置文件的路径，默认为"config.yaml"。
        """
        self.config = self._load_config(config_path)
        pass

    def _load_config(self, path: str) -> Dict[str, Any]:
        """
        加载YAML格式的配置文件。

        Args:
            path (str): 配置文件的路径。

        Returns:
            Dict[str, Any]: 解析后的配置字典。
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)


def excel_to_json(config: Configuration):
    """
    将Excel文件转换为JSON文件。

    Args:
        config (Configuration): 包含配置信息的Configuration对象。
    """
    # 读取Excel文件
    excel_file_path = config.config["excel_file_path"]
    if not excel_file_path:
        raise ValueError("Excel file path not found in the configuration file.")

    df = pd.read_excel(excel_file_path)

    # 转换为字典结构
    result = {}
    for _, row in df.iterrows():
        key = row[config.config["key_name"]]
        result[key] = {
            "text": str(row[config.config["value_name"]]),
            "comment": str(
                row.get(config.config["comment_name"], "")
            ),  # 假设可能有"comment"列，没有则留空
        }

    # 保存为JSON文件
    out_json_path = config.config["out_json_path"]
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"read excel file success, out json file: {out_json_path}")


def main():
    """
    主函数，解析命令行参数并执行本地化处理。
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Bunny Localization Based on Multi-language Localization Tool"
    )
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument(
        "--config_model", default="config.yaml", help="Config file path"
    )
    args = parser.parse_args()

    # 加载配置文件
    config = Configuration(args.config)
    if not config.config["skip_file_transfor"]:
        excel_to_json(config)

    # 加载本地化配置并执行本地化处理
    config_model = LocalizationConfig(args.config_model)
    processor = LocalizationProcessor(config_model)

    try:
        processor.generate_localization(
            source_path=config_model.get_config("source"),
            target_langs=config_model.get_config("target_languages"),
            output_dir=config_model.get_config("output"),
            style=config_model.get_config("translation_style", "formal"),
        )
    finally:
        # 保存缓存
        config_model.save_cache()


if __name__ == "__main__":
    main()
