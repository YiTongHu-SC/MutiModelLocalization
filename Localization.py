import json
from pathlib import Path
from typing import Dict, Any
import hashlib
import yaml
import argparse
import time
from time import sleep
from volcenginesdkarkruntime import Ark


class LocalizationConfig:
    """本地化配置管理类，负责加载配置和翻译缓存"""

    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化本地化配置

        参数:
        config_path (str): 配置文件路径，默认为config.yaml
        """
        self.config = self._load_config(config_path)
        self.cache_file = Path(self.config.get("cache_path", "translations.cache"))
        self.translation_cache = self._load_cache()

    def get_config(self, key: str, defaultValue: Any = None):
        return self.config.get(key, defaultValue)

    def _load_config(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _load_cache(self) -> Dict[str, str]:
        if self.cache_file.exists():
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.translation_cache, f, ensure_ascii=False)


class BaseTranslator:
    def __init__(self, config: LocalizationConfig):
        self.config = config
        self.base_url = config.get_config("base_url")
        self.api_key = config.get_config("api_key")
        self.model = config.get_config("model")
        self.rate_limit = config.get_config("rate_limit", 3)  # 限制API请求频率
        self.temperature = config.get_config("temperature", 0.1)
        self.max_tokens = config.get_config("max_tokens", 1024)
        self.default_style = config.get_config(
            "translation_style", "formal"
        )  # 默认风格
        self.last_request = 0
        pass

    def _generate_hash_key(self, text: str, target_lang: str, style: str) -> str:
        return hashlib.md5(f"{text}_{target_lang}_{style}".encode()).hexdigest()

    def translate_text(self, text: str, target_lang: str, style: str) -> str:
        # 限流控制
        elapsed = time.time() - self.last_request
        if elapsed < 1 / self.rate_limit:
            sleep(1 / self.rate_limit - elapsed)
        pass


class DoubaoTranslator(BaseTranslator):
    """
    豆包大模型
    """

    def __init__(self, config: LocalizationConfig):
        super().__init__(config)
        self.client = Ark(base_url=self.base_url, api_key=self.api_key)

    def translate_text(self, text: str, target_lang: str, style: str = None) -> str:
        super().translate_text(text, target_lang, style)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": f"你是一名专业游戏本地化翻译员，仅将以下文本直接翻译为{target_lang}，输出无额外内容，限定游戏场景，只输出一个候选: {text}",
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "translation_config": {
                "formal_level": style or self.default_style,
                "domain": "software",
            },
        }

        try:
            completion = self.client.chat.completions.create(
                model=payload["model"],
                messages=payload["messages"],
                # 开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
                extra_headers={"x-is-encrypted": "true"},
                max_tokens=payload["max_tokens"],
                temperature=payload["temperature"],
            )
            self.last_request = time.time()

            # 解析豆包API响应格式
            return completion.choices[0].message.content
        except requests.exceptions.HTTPError as e:
            print(f"API Error: {e.response.status_code} - {e.response.text}")
        except KeyError:
            print("Invalid API response format")
        except Exception as e:
            print(f"Translation failed: {str(e)}")

        self.last_request = time.time()
        return ""  # 失败时返回原文


class TranslatorFactory:
    @staticmethod
    def create_translator(config: LocalizationConfig) -> BaseTranslator:
        model_type = config.get_config("model_type", "Doubao")

        translators = {"Doubao": DoubaoTranslator}

        if model_type not in translators:
            raise ValueError(f"Unsupported model type: {model_type}")

        return translators[model_type](config)


class LocalizationProcessor:
    def __init__(self, config: LocalizationConfig):
        self.config = config
        self.translator = TranslatorFactory.create_translator(config)

    def _process_value(self, value, target_lang: str, style: str):
        if isinstance(value, dict):
            return {
                k: self._process_value(v, target_lang, style) for k, v in value.items()
            }
        elif isinstance(value, list):
            return [self._process_value(item, target_lang, style) for item in value]
        elif isinstance(value, str):
            cache_key = self.translator._generate_hash_key(value, target_lang, style)
            if cache_key in self.config.translation_cache:
                return self.config.translation_cache[cache_key]

            translated = self.translator.translate_text(value, target_lang, style)
            if not translated:
                self.config.translation_cache[cache_key] = translated
            return translated
        return value

    def generate_localization(
        self, source_path: str, target_langs: list, output_dir: str, style: str = None
    ):
        with open(source_path, "r", encoding="utf-8") as f:
            source_data = json.load(f)

        for lang in target_langs:
            translated_data = self._process_value(source_data, lang, style)
            output_path = Path(output_dir) / f"{lang}.json"

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(translated_data, f, ensure_ascii=False, indent=2)

            print(f"Generated localization for {lang} at {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Multi-language Localization Tool")
    parser.add_argument(
        "-s", "--source", required=True, help="Source localization file"
    )
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    parser.add_argument("--config", default="config.yaml", help="Config file path")

    args = parser.parse_args()

    config = LocalizationConfig(args.config)
    processor = LocalizationProcessor(config)

    try:
        processor.generate_localization(
            source_path=args.source,
            target_langs=config.get_config("default_languages"),
            output_dir=args.output,
            style=config.get_config("translation_style", "formal"),
        )
    finally:
        config.save_cache()


if __name__ == "__main__":
    main()
