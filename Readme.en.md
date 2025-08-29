<!-- markdownlint-disable MD041 -->
[中文](./Readme.md) | [English](./Readme.en.md)

# MultiModelLocalization
<!-- markdownlint-enable MD041 -->

A localization toolkit powered by Large Language Models (LLMs). It supports multi-language translation, caching, and flexible configuration.

## Changelog

### v-0.1.0

- Refactored project structure
- Added automated testing support
- Optimized package dependencies

### v-0.0.4

- Added support for TongYi Qwen model, an optimized TongYi model specialized for machine translation.

### v-0.0.3

- Added support for TongYi model.

### v-0.0.2

- Added support for Kimi model, with known limitation:
  - Kimi API requires RPM <= 3, so batching requests may be necessary.

### v-0.0.1

- Added Doubao model support
- Added DeepSeek model support

## ✨ Features

- Support multiple LLM APIs
- Localization for JSON files
- Translation result caching to avoid duplicate work
- Configurable translation style (formal/casual)
- Batch generation for multiple target languages
- API rate limiting

## 📦 Dependencies

Use `pipenv` to install dependencies

```bash
pipenv install
pipenv run pip install volcengine-python-sdk[ark]  # Volcano Engine ARK SDK (optional if you don't use Doubao model)
```

## Example Config

```yaml
model_type: Doubao
model: "youer-model-name"
base_url: "https://example/api" # API endpoint
api_key: "your-api-key-here" # Replace with a real API key
default_languages: # Target languages
  - en
  - ja
  - fr
cache_path: output/translations.cache # Translation cache file
translation_style: formal # Default translation style
rate_limit: 3
temperature: 0.1
max_tokens: 1024
```

Available model_type values

```yaml
model_type: Doubao # Doubao
model_type: DeepSeek
model_type: Kimi
model_type: TongYi # TongYi
model_type: TongYiQwen # TongYi Qwen machine translation model
```

## 🚀 Quick Start

```bash
# Use the main entry
python main.py \
  --source ./data/test_data/test.json \
  --output ./output \
  --config ./configs/doubao_config.yaml

# Or run the core module directly
python -m src.core.Localization \
  --source ./data/test_data/test.json \
  --output ./output \
  --config ./configs/doubao_config.yaml
```

## Language Codes

In localization, languages are identified by ISO codes: two-letter (ISO 639-1) or three-letter (ISO 639-2). Common examples:

| Language            | Code  | Notes                                   |
| ------------------- | ----- | --------------------------------------- |
| Chinese (Simplified)| zh-CN | zh for Chinese, CN for China            |
| English (US)        | en-US | en for English, US for United States    |
| English (UK)        | en-GB | en for English, GB for United Kingdom   |
| Spanish             | es    |                                         |
| Spanish (Mexico)    | es-MX | es for Spanish, MX for Mexico           |
| French              | fr    |                                         |
| French (Canada)     | fr-CA | fr for French, CA for Canada            |
| German              | de    |                                         |
| Japanese            | ja    |                                         |
| Korean              | ko    |                                         |
| Russian             | ru    |                                         |
| Arabic              | ar    |                                         |
| Portuguese          | pt    |                                         |
| Portuguese (Brazil) | pt-BR | pt for Portuguese, BR for Brazil        |
| Italian             | it    |                                         |
| Dutch               | nl    |                                         |
| Indonesian          | id    |                                         |
| Turkish             | tr    |                                         |

## Project Structure

```text
.
├── src/                     # Source code
│   ├── __init__.py         # Package initialization
│   ├── core/               # Core module
│   └── translators/        # Translators module
├── configs/                 # Configuration files
├── data/                    # Data directory
├── output/                  # Generated files directory
├── tests/                   # Test files directory
├── tools/                   # Tool scripts directory
├── main.py                 # Main entry file
├── Pipfile                 # Dependency management file
├── Readme.md               # Chinese documentation
└── Readme.en.md            # English documentation
```

## Contributing

PRs are welcome. Please follow:

- New models should inherit from BaseTranslator
- Configuration is managed via LocalizationConfig
- Keep cache mechanism compatible
- Add corresponding unit tests
