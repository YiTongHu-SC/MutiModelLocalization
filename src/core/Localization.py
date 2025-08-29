import json
from pathlib import Path
import argparse
from ..translators.BaseTranslator import LocalizationConfig
from ..translators.BaseTranslator import BaseTranslator


class TranslatorFactory:
    @staticmethod
    def create_translator(config: LocalizationConfig) -> BaseTranslator:
        model_type = config.get_config("model_type", "Doubao")

        translators = {
            "Doubao",
            "DeepSeek",
            "Kimi",
            "TongYi",
            "TongYiQwen",
        }

        if model_type not in translators:
            raise ValueError(f"Unsupported model type: {model_type}")

        if model_type == "Doubao":
            from ..translators.DoubaoTranslator import DoubaoTranslator

            return DoubaoTranslator(config)
        elif model_type == "DeepSeek":
            from ..translators.OpenAIBaseedTranslator import OpenAIBaseedTranslator

            return OpenAIBaseedTranslator(config)
        elif model_type == "Kimi":
            from ..translators.OpenAIBaseedTranslator import OpenAIBaseedTranslator

            return OpenAIBaseedTranslator(config)
        elif model_type == "TongYi":
            from ..translators.OpenAIBaseedTranslator import OpenAIBaseedTranslator

            return OpenAIBaseedTranslator(config)
        elif model_type == "TongYiQwen":
            from ..translators.TongYiQwenTranslator import TongYiQwenTranslator

            return TongYiQwenTranslator(config)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


class LocalizationProcessor:
    def __init__(self, config: LocalizationConfig):
        self.config = config
        self.translator = TranslatorFactory.create_translator(config)

    def _process_value(
        self, value: dict, target_lang: str, style: str, is_use_comment: bool
    ):
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
            cache_key = self.translator._generate_hash_key(
                content_key, target_lang, style
            )
            if cache_key in self.config.translation_cache:
                translated[content_key] = self.config.translation_cache[cache_key]
                continue
            translated_text = self.translator.translate_text(
                text=content["text"],
                target_lang=target_lang,
                style=style,
                comment=content["comment"] if is_use_comment else None,
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
            translated_data = self._process_value(
                source_data, lang, style, self.translator.IsUseComment
            )
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
