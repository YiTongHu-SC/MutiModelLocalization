import time

from openai import OpenAI

from .BaseTranslator import BaseTranslator, LocalizationConfig


class OpenAIBaseedTranslator(BaseTranslator):
    """
    基于OpenAI SDK的大模型,支持DeepSeek、Kimi,等
    """

    def __init__(self, config: LocalizationConfig):
        super().__init__(config)
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def translate_text(
        self, text: str, target_lang: str, style: str = None, comment: str = None
    ) -> str:
        super().translate_text(text, target_lang, style, comment)
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
