from typing import Dict, Any
import pandas as pd
import yaml
import argparse
import json
from Localization import *


class Configuration:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        pass

    def _load_config(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)


def excel_to_json(config: Configuration):
    # 读取Excel文件
    excel_file_path = config.config["excel_file_path"]
    if not excel_file_path:
        raise ValueError("Excel file path not found in the configuration file.")

    df = pd.read_excel(excel_file_path)

    # 保存为json文件
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
    parser = argparse.ArgumentParser(
        description="Bunny Localization Based on Multi-language Localization Tool"
    )
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument(
        "--config_model", default="config.yaml", help="Config file path"
    )
    args = parser.parse_args()
    config = Configuration(args.config)
    if not config.config["skip_file_transfor"]:
        excel_to_json(config)

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
        config_model.save_cache()


if __name__ == "__main__":
    main()
