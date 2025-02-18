# MultiModelLocalization

基于大语言模型的本地化工具，支持多语言自动翻译和缓存管理

## 更新

### v-0.0.1

- 豆包模型支持
- DeepSeek模型支持

## ✨ 功能特性

- 支持豆包等大模型翻译接口
- JSON格式文件本地化处理
- 翻译结果缓存机制，避免重复翻译
- 可配置的翻译风格（正式/口语化）
- 多语言批量生成
- API请求频率控制

## 📦 安装依赖

``` text
PyYAML==6.0.1               # YAML配置解析
volcenginesdkarkruntime==1.0.11  # 火山引擎ARK运行时SDK,如果不需要豆包则可以不要
```

```bash
pip install pyyaml volcenginesdkarkruntime
```

## 参考配置文件

```yaml

model_type: Doubao
model: "youer-model-name"
base_url: "https://example/api"  # API端口
api_key: "your-api-key-here"  # 替换为真实API密钥
default_languages:  # 目标语言列表
  - en
  - ja
  - fr
cache_path: output/translations.cache  # 翻译缓存文件路径
translation_style: formal # 默认翻译风格
rate_limit: 3
temperature: 0.1
max_tokens: 1024

```

可选的 model_type

``` yaml
model_type: Doubao # 豆包
model_type: DeepSeek
```

## 🚀 快速使用

```bash
python Localization.py \
  --source ./data/test.json \
  --output ./localized_files \
  --config ./configs/doubao_config.yaml
```

## 项目结构

```
.
├── data/                 # 源语言文件
│   └── test.json         # 示例翻译源文件
├── configs/              # 配置文件目录
│   └── doubao_config.yaml # 豆包模型配置
├── output/               # 生成文件目录
│   ├── en.json          # 英文翻译结果
│   └── translations.cache # 翻译缓存
└── Localization.py       # 主程序
```

## 贡献

欢迎提交PR，请遵循以下规范：

- 新模型实现继承BaseTranslator
- 配置参数通过LocalizationConfig管理
- 保持缓存机制兼容性
- 添加对应的单元测试
