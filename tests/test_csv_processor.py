import unittest
import os
import json
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
        data = self.processor.read_csv(self.test_csv)
        
        # 验证数据结构
        self.assertIn("welcome", data)
        self.assertIn("text", data["welcome"])
        self.assertIn("comment", data["welcome"])
        
        # 验证内容
        self.assertEqual(data["welcome"]["text"], "欢迎使用本地化工具")
        self.assertEqual(data["welcome"]["comment"], "这是一个简单的欢迎语")
        
    def test_process_file(self):
        # 处理文件
        self.processor.process_file(self.test_csv, self.output_dir)
        
        # 验证输出文件
        output_file = os.path.join(self.output_dir, "zh-CN.json")
        self.assertTrue(os.path.exists(output_file))
        
        # 验证输出内容
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.assertIn("welcome", data)
        self.assertEqual(data["welcome"]["text"], "欢迎使用本地化工具")
        self.assertEqual(data["welcome"]["comment"], "这是一个简单的欢迎语")

if __name__ == '__main__':
    unittest.main()
