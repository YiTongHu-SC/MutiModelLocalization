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
    
    def read_csv(self, file_path: str) -> Dict:
        """
        读取CSV文件并转换为标准的本地化数据格式
        """
        result = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # 读取表头
            
            # 检测语言列
            self.target_languages, id_idx, source_idx, comment_idx = self.detect_languages(headers)
            
            if id_idx == -1 or source_idx == -1:
                raise ValueError("CSV文件必须包含ID列和源语言列")
                
            # 读取每一行数据
            for row in reader:
                if not row or not row[id_idx].strip():  # 跳过空行或无ID的行
                    continue
                    
                item_id = row[id_idx].strip()
                source_text = row[source_idx].strip() if source_idx < len(row) else ""
                comment = row[comment_idx].strip() if comment_idx != -1 and comment_idx < len(row) else ""
                
                result[item_id] = {
                    "text": source_text,
                    "comment": comment
                }
                
        return result
    
    def process_file(self, csv_path: str, output_dir: str) -> None:
        """
        处理CSV文件并生成JSON格式的本地化文件
        """
        # 读取CSV文件
        self.data = self.read_csv(csv_path)
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成源语言JSON文件
        source_file = output_path / f"{self.source_language}.json"
        with open(source_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
            
        print(f"已生成源语言文件：{source_file}")
        print(f"检测到的目标语言：{', '.join(self.target_languages)}")
        print(f"处理的记录数：{len(self.data)}")
        print(f"输出目录：{output_path}")
