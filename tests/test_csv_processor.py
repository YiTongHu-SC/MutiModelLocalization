import unittest
import os
import json
import csv
from src.core.csv_processor import CSVProcessor

class TestCSVProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = CSVProcessor()
        self.test_csv = "data/test.csv"
        self.output_dir = "output/csv_test"
        
    def test_detect_languages(self):
        headers = ["ID", "zh-CN", "Comment", "en", "ja", "ko", "zh-TW"]
        langs, id_idx, src_idx, comment_idx = self.processor.detect_languages(headers)
        
        self.assertEqual(id_idx, 0)
        self.assertEqual(src_idx, 1)
        self.assertEqual(comment_idx, 2)
        self.assertEqual(langs, ["en", "ja", "ko", "zh-TW"])
        
    def test_read_csv(self):
        headers, rows = self.processor.read_csv(self.test_csv)
        
        # 验证表头
        self.assertIn("ID", headers)
        self.assertIn("zh-CN", headers)
        self.assertIn("Comment", headers)
        
        # 验证数据行
        self.assertTrue(len(rows) > 0)
        first_row = rows[0]
        self.assertEqual(first_row[headers.index("ID")], "welcome")
        self.assertEqual(first_row[headers.index("zh-CN")], "欢迎使用本地化工具")
        
    def test_process_file(self):
        # 处理文件
        self.processor.process_file(self.test_csv, self.output_dir)
        
        # 验证输出文件
        for lang in ["en", "ja", "ko", "zh-TW"]:
            output_file = os.path.join(self.output_dir, f"{lang}.csv")
            self.assertTrue(os.path.exists(output_file))
            
            # 验证输出内容
            with open(output_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                rows = list(reader)
                
            # 验证表头和数据结构
            self.assertEqual(headers[0], "ID")
            self.assertIn(lang, headers)
            self.assertIn("Comment", headers)
            self.assertTrue(len(rows) > 0)  # 确保有数据行

if __name__ == '__main__':
    unittest.main()
