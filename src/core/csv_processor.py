import csv
from typing import Dict, List, Tuple
import json
from pathlib import Path


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
        "ru": "俄语"
    }
    
    def __init__(self):
        self.source_language = "zh-CN"  # 默认源语言
        self.target_languages = []
        self.data = {}
        
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
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # 读取表头
            
            # 检测语言列
            self.target_languages, id_idx, source_idx, comment_idx = self.detect_languages(headers)
            
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
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成输出文件
        output_file = output_path / "localization.csv"
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入表头（保持原始表头不变）
            writer.writerow(headers)
            # 写入数据行（保持所有列不变）
            writer.writerows(rows)
        
        print(f"处理完成！")
        print(f"检测到的目标语言：{', '.join(self.target_languages)}")
        print(f"处理的记录数：{len(rows)}")
        print(f"输出文件：{output_file}")
