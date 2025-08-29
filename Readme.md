<!-- markdownlint-disable MD041 -->
[中文](./Readme.md) | [English](./Readme.en.md)

# MultiModelLocalization
<!-- markdownlint-enable MD041 -->

基于大语言模型的本地化工具，支持多语言自动翻译和缓存管理

## ✨ 未来可能的特性

详见[future](future.md)

## 更新

### v-0.1.0

- 重构项目结构
- 新增自动化测试支持
- 优化包依赖

### v-0.0.4

- 新增通义 Qwen 模型支持，基于通义的优化模型，专门用于机翻

### v-0.0.3

- 新增通义模型支持

### v-0.0.2

- 新增 Kimi 模型支持,但仍然存在**问题**:
  - Kimi API 要求 RPM 不超过 3,所以可能需要打包批量请求

### v-0.0.1

- 豆包模型支持
- DeepSeek 模型支持

## ✨ 功能特性

- 支持多种大模型 API 调用
- JSON 格式文件本地化处理
- 翻译结果缓存机制，避免重复翻译
- 可配置的翻译风格（正式/口语化）
- 多语言批量生成
- API 请求频率控制

## 📦 安装依赖

使用 `pipenv` 安装依赖

```bash
pipenv install
pipenv run pip install volcengine-python-sdk[ark]  # 火山引擎ARK运行时SDK,如果不需要豆包模型则可以忽略
```

## 参考配置文件

```yaml
model_type: Doubao
model: "youer-model-name"
base_url: "https://example/api" # API端口
api_key: "your-api-key-here" # 替换为真实API密钥
default_languages: # 目标语言列表
  - en
  - ja
  - fr
cache_path: output/translations.cache # 翻译缓存文件路径
translation_style: formal # 默认翻译风格
rate_limit: 3
temperature: 0.1
max_tokens: 1024
```

可选的 model_type

```yaml
model_type: Doubao # 豆包
model_type: DeepSeek
model_type: Kimi
model_type: TongYi # 通义
model_type: TongYiQwen # 通义Qewn机翻大模型
```

## 🚀 快速使用

```bash
# 使用主入口文件
python main.py \
  --source ./data/test_data/test.json \
  --output ./output \
  --config ./configs/doubao_config.yaml

# 或者直接运行核心模块
python -m src.core.Localization \
  --source ./data/test_data/test.json \
  --output ./output \
  --config ./configs/doubao_config.yaml
```

## 多语言对照表

在多语言本地化中，不同语言通常使用 ISO 语言代码进行标识，这些代码可以是两位字母代码（ISO 639-1）或三位字母代码（ISO 639-2）。以下是一些常见语言的英文缩写：

| 语言               | 缩写  | 说明                             |
| ------------------ | ----- | -------------------------------- |
| 中文（简体）       | zh-CN | zh 表示中文，CN 表示中国。       |
| 中文（繁体）       | zh-TW | zh 表示中文，TW 表示台湾。       |
| 英语（美国）       | en-US | en 表示英语，US 表示美国。       |
| 英语（英国）       | en-GB | en 表示英语，GB 表示英国。       |
| 西班牙语           | es    | es 表示西班牙语。                |
| 西班牙语（墨西哥） | es-MX | es 表示西班牙语，MX 表示墨西哥。 |
| 法语               | fr    | fr 表示法语。                    |
| 法语（加拿大）     | fr-CA | fr 表示法语，CA 表示加拿大。     |
| 德语               | de    | de 表示德语。                    |
| 日语               | ja    | ja 表示日语。                    |
| 韩语               | ko    | ko 表示韩语。                    |
| 俄语               | ru    | ru 表示俄语。                    |
| 阿拉伯语           | ar    | ar 表示阿拉伯语。                |
| 葡萄牙语           | pt    | pt 表示葡萄牙语。                |
| 葡萄牙语（巴西）   | pt-BR | pt 表示葡萄牙语，BR 表示巴西。   |
| 意大利语           | it    | it 表示意大利语。                |
| 荷兰语             | nl    | nl 表示荷兰语。                  |
| 印度尼西亚语       | id    | id 表示印度尼西亚语。            |
| 土耳其语           | tr    | tr 表示土耳其语。                |

## 项目结构

```text
.
├── src/                     # 源代码目录
│   ├── __init__.py         # 包初始化文件
│   ├── core/               # 核心模块
│   └── translators/        # 翻译器模块
├── configs/                 # 配置文件目录
├── data/                    # 数据目录
├── output/                  # 生成文件目录
├── tests/                   # 测试文件目录
├── tools/                   # 工具脚本目录
├── main.py                  # 主入口文件
├── Pipfile                  # 依赖管理文件
├── Readme.md               # 中文说明文档
└── Readme.en.md             # 英文说明文档

```

## 贡献

欢迎提交 PR，请遵循以下规范：

- 新模型实现继承 BaseTranslator
- 配置参数通过 LocalizationConfig 管理
- 保持缓存机制兼容性
- 添加对应的单元测试
