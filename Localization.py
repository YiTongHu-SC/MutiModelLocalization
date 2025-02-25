import json
from pathlib import Path
from typing import Dict, Any
import hashlib
import yaml
import argparse
import time
from time import sleep
from volcenginesdkarkruntime import Ark
from openai import OpenAI


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

    def translate_text(
        self, text: str, target_lang: str, style: str, comment: str
    ) -> str:
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

    def translate_text(
        self, text: str, target_lang: str, style: str = "formal", comment: str = None
    ) -> str:
        super().translate_text(text, target_lang, style, comment)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.config.get_config("system_prompt")
                    + f" 翻译风格：{style}",
                },
                {
                    "role": "user",
                    "content": f"基于注释内容：{comment}，将以下文本直接翻译为{target_lang}: {text}",
                },
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
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
        except KeyError:
            print("Invalid API response format")
        except Exception as e:
            print(f"Translation failed: {str(e)}")

        self.last_request = time.time()
        return ""  # 失败时返回原文


class TongYiQwenTranslator(BaseTranslator):
    """
    Qwen-MT模型是基于通义千问模型优化的机器翻译大语言模型，
    擅长中英互译、中文与小语种互译、英文与小语种互译，
    小语种包括日、韩、法、西、德、葡（巴西）、泰、印尼、越、阿等26种。
    在多语言互译的基础上，提供术语干预、领域提示、记忆库等能力，提升模型在复杂应用场景下的翻译效果
    """

    def __init__(self, config: LocalizationConfig):
        super().__init__(config)
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def translate_text(self, text: str, target_lang: str, style: str = None) -> str:
        super().translate_text(text, target_lang, style)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": text,
                }
            ],
            "translation_options": {
                "source_lang": "Chinese",
                "target_lang": target_lang,
            },
        }

        try:
            completion = self.client.chat.completions.create(
                model=payload["model"],
                messages=payload["messages"],
                extra_body={"translation_options": payload["translation_options"]},
            )
            self.last_request = time.time()

            # 解析豆包API响应格式
            return completion.choices[0].message.content
        except KeyError:
            print("Invalid API response format")
        except Exception as e:
            print(f"Translation failed: {str(e)}")

        self.last_request = time.time()
        return ""  # 失败时返回原文


class OpenAIBaseedTranslator(BaseTranslator):
    """
    基于OpenAI SDK的大模型,支持DeepSeek、Kimi,等
    """

    def __init__(self, config: LocalizationConfig):
        super().__init__(config)
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def translate_text(self, text: str, target_lang: str, style: str = None) -> str:
        super().translate_text(text, target_lang, style)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.config.get_config("system_prompt"),
                },
                {
                    "role": "user",
                    "content": f"将以下文本直接翻译为{target_lang}: {text}",
                },
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            completion = self.client.chat.completions.create(
                model=payload["model"],
                messages=payload["messages"],
                max_tokens=payload["max_tokens"],
                temperature=payload["temperature"],
                stream=False,
            )
            self.last_request = time.time()

            # 解析豆包API响应格式
            return completion.choices[0].message.content
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

        translators = {
            "Doubao": DoubaoTranslator,
            "DeepSeek": OpenAIBaseedTranslator,
            "Kimi": OpenAIBaseedTranslator,
            "TongYi": OpenAIBaseedTranslator,
            "TongYiQwen": TongYiQwenTranslator,
        }

        if model_type not in translators:
            raise ValueError(f"Unsupported model type: {model_type}")

        return translators[model_type](config)


class LocalizationProcessor:
    def __init__(self, config: LocalizationConfig):
        self.config = config
        self.translator = TranslatorFactory.create_translator(config)

    def _process_value(self, value: dict, target_lang: str, style: str):
        # 遍历字典，输入数据结构示例：
        # {
        #   "welcome": {
        #     "Text": "欢迎使用基于AI大模型的本地化工具",
        #     "Comment": "工具欢迎语，用于测试"
        #   }
        # }
        #
        translated = {}
        for content_key in value.keys():
            content = value[content_key]
            cache_key = self.translator._generate_hash_key(content_key, target_lang, style)
            if cache_key in self.config.translation_cache:
                translated[content_key] = self.config.translation_cache[cache_key]
                continue
            translated_text = self.translator.translate_text(
                content["text"], target_lang, style, content["comment"]
            )
            if translated_text.strip():
                self.config.translation_cache[cache_key] = translated
            translated[content_key] = translated_text
        return translated

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
            target_langs=config.get_config("target_languages"),
            output_dir=args.output,
            style=config.get_config("translation_style", "formal"),
        )
    finally:
        config.save_cache()


if __name__ == "__main__":
    main()
