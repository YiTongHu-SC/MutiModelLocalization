import json
import pandas as pd
import os
import re

# 1. 读取源数据（中文）
with open("data/data.json", "r", encoding="utf-8") as f:
    source_data = json.load(f)

# 创建基础字典结构
combined = {
    key: {
        "Key": key,
        "Chinese (Simplified)(zh-Hans)": item["text"],  # 中文文本
        "Comment": item["comment"],  # 注释信息
    }
    for key, item in source_data.items()
}

# 2. 读取多语言文件
output_dir = "output"
lang_files = [f for f in os.listdir(output_dir) if f.endswith(".json")]

for filename in lang_files:
    # 使用正则表达式提取语言代码（如en/ko/ja）
    match = re.search(r"\((\w+)\)\.json$", filename)
    if not match:
        continue
    filename.split(".")
    lang_code = filename.split(".")[0]

    with open(os.path.join(output_dir, filename), "r", encoding="utf-8") as f:
        lang_data = json.load(f)

    # 合并语言数据
    for key, text in lang_data.items():
        if key in combined:
            combined[key][lang_code] = text

# 3. 转换为DataFrame
df = pd.DataFrame(combined.values())

# 4. 列排序调整（Key列在最前，其他按字母顺序）
columns = ["Key", "Comment", "Chinese (Simplified)(zh-Hans)"] + sorted(
    [c for c in df.columns if c not in ["Key", "zh", "comment"]]
)
df = df[columns]

# 5. 导出CSV（使用BOM头确保Excel正确显示）
out_file_path = "output/localization.csv"
df.to_csv(out_file_path, index=False, encoding="utf-8")

print(f"导出成功！生成文件：{out_file_path}")
