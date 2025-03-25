from BaseTranslator import LocalizationConfig
from BaseTranslator import BaseTranslator
from volcenginesdkarkruntime import Ark
import time


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
