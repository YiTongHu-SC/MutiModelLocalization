import argparse
import os
from src.core.csv_processor import CSVProcessor

def main():
    parser = argparse.ArgumentParser(description='CSV格式本地化工具')
    parser.add_argument('-s', '--source', required=True, help='源CSV文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出目录')
    parser.add_argument('--source-language', default='zh-CN', help='源语言代码，默认为zh-CN')
    
    args = parser.parse_args()
    
    processor = CSVProcessor()
    processor.source_language = args.source_language
    
    try:
        processor.process_file(args.source, args.output)
        print("处理完成！")
    except Exception as e:
        print(f"处理过程出错: {str(e)}")
        
if __name__ == '__main__':
    main()
