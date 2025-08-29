import time
from .BaseTranslator import LocalizationConfig
from .BaseTranslator import BaseTranslator
from openai import OpenAI


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
        self.IsUseComment = False

    def translate_text(
        self, text: str, target_lang: str, style: str = None, comment: str = None
    ) -> str:
        super().translate_text(text, target_lang, style, comment)
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
