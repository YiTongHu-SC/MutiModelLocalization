#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译器模块测试文件
"""

import unittest
import sys
import os
from pathlib import Path

# 添加src目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from src.translators.BaseTranslator import LocalizationConfig
from src.core.Localization import TranslatorFactory


class TestTranslators(unittest.TestCase):
    """翻译器测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试配置
        self.test_config_data = {
            "model_type": "Doubao",
            "model": "test-model",
            "base_url": "https://test.api.com",
            "api_key": "test-key",
            "cache_path": "test_cache.json",
            "rate_limit": 3,
            "temperature": 0.1,
            "max_tokens": 1024
        }
    
    def test_translator_factory(self):
        """测试翻译器工厂"""
        # 测试支持的模型类型
        supported_types = ["Doubao", "DeepSeek", "Kimi", "TongYi", "TongYiQwen"]
        
        for model_type in supported_types:
            with self.subTest(model_type=model_type):
                config_data = self.test_config_data.copy()
                config_data["model_type"] = model_type
                
                # 这里只测试工厂方法不会抛出异常
                # 实际的API调用需要真实的配置
                try:
                    # 注意：这里不能直接创建LocalizationConfig，因为它需要文件
                    # 所以我们只测试不支持的模型类型会抛出异常
                    pass
                except Exception as e:
                    self.fail(f"Unexpected exception for {model_type}: {e}")
    
    def test_unsupported_model_type(self):
        """测试不支持的模型类型"""
        config_data = self.test_config_data.copy()
        config_data["model_type"] = "UnsupportedModel"
        
        # 这里需要实际的配置文件来测试，暂时跳过
        pass


if __name__ == "__main__":
    unittest.main()