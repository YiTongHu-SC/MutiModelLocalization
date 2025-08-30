import csv
from typing import Dict, List, Tuple
import json
from pathlib import Path
import os
from ..translators.TongYiQwenTranslator import TongYiQwenTranslator
from ..core.Localization import LocalizationConfig


class CSVProcessor:
    """CSV文件处理器"""

    # 支持的语言代码列表
    SUPPORTED_LANGUAGES = {
        "zh-CN": "简体中文",
        "zh-TW": "繁体中文",
        "en": "英语",
        "ja": "日语",
        "ko": "韩语",
        "de": "德语",
        "fr": "法语",
        "es": "西班牙语",
        "it": "意大利语",
        "ru": "俄语",
    }

    def __init__(self, config_path: str = "configs/tongyi_qwen_config.yaml"):
        self.source_language = "zh-CN"  # 默认源语言
        self.target_languages = []
        self.data = {}

        # 初始化翻译器
        self.config = LocalizationConfig(config_path)
        self.translator = TongYiQwenTranslator(self.config)

    def detect_languages(self, headers: List[str]) -> Tuple[List[str], int, int, int]:
        """
        检测CSV文件中的语言列
        返回：(目标语言列表, ID列索引, 源语言列索引, 注释列索引)
        """
        target_langs = []
        id_index = -1
        source_index = -1
        comment_index = -1

        for idx, header in enumerate(headers):
            header = header.strip()
            if header.lower() == "id":
                id_index = idx
            elif header == self.source_language:
                source_index = idx
            elif header.lower() == "comment":
                comment_index = idx
            elif header in self.SUPPORTED_LANGUAGES:
                target_langs.append(header)

        return target_langs, id_index, source_index, comment_index

    def read_csv(self, file_path: str) -> Tuple[List[str], List[List[str]]]:
        """
        读取CSV文件并保留原始结构
        返回：(表头列表, 数据行列表)
        """
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)  # 读取表头

            # 检测语言列
            self.target_languages, id_idx, source_idx, comment_idx = (
                self.detect_languages(headers)
            )

            if id_idx == -1 or source_idx == -1:
                raise ValueError("CSV文件必须包含ID列和源语言列")

            # 保存所有行数据
            rows = []
            for row in reader:
                if not row or not row[id_idx].strip():  # 跳过空行或无ID的行
                    continue
                rows.append(row)

        return headers, rows

    def process_file(self, csv_path: str, output_dir: str) -> None:
        """
        处理CSV文件并生成包含所有语言的CSV文件
        """
        # 读取CSV文件
        headers, rows = self.read_csv(csv_path)

        # 获取语言列索引映射
        lang_indices = {
            header.strip(): idx
            for idx, header in enumerate(headers)
            if header.strip() in self.SUPPORTED_LANGUAGES
        }

        # 获取必要的列索引
        _, id_idx, source_idx, comment_idx = self.detect_languages(headers)

        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 使用源文件的名称
        source_filename = os.path.basename(csv_path)
        output_file = output_path / source_filename

        # 处理每一行，进行翻译
        translated_rows = []
        total_rows = len(rows)

        for idx, row in enumerate(rows, 1):
            if not row:  # 跳过空行
                continue

            # 获取源文本和注释
            source_text = row[source_idx].strip()
            comment = row[comment_idx].strip() if comment_idx != -1 else ""

            # 创建新行，初始化为原始行的副本
            new_row = row.copy()

            # 对每个目标语言进行翻译
            for lang, col_idx in lang_indices.items():
                if lang != self.source_language:  # 跳过源语言
                    try:
                        translated_text = self.translator.translate_text(
                            text=source_text,
                            target_lang=lang,
                            style="formal",
                            comment=comment,
                        )
                        new_row[col_idx] = translated_text
                    except Exception as e:
                        print(f"翻译失败 (ID: {row[id_idx]}, 语言: {lang}): {str(e)}")
                        new_row[col_idx] = ""  # 翻译失败时留空

            translated_rows.append(new_row)
            print(
                f"\r处理进度: {idx}/{total_rows} ({int(idx/total_rows*100)}%)",
                end="",
                flush=True,
            )

        print("\n")  # 换行

        # 写入翻译后的文件
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # 写入表头
            writer.writerow(headers)
            # 写入翻译后的数据行
            writer.writerows(translated_rows)

        print(f"处理完成！")
        print(f"检测到的目标语言：{', '.join(self.target_languages)}")
        print(f"处理的记录数：{len(translated_rows)}")
        print(f"输出文件：{output_file}")
