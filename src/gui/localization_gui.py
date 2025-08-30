import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QCheckBox,
    QTextEdit,
    QScrollArea,
    QGroupBox,
    QListWidget,
    QAbstractItemView,
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent
import yaml
import os

from src.core.Localization import LocalizationProcessor, LocalizationConfig


class DropArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.label = QLabel("拖拽文件到这里")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setMinimumHeight(100)
        self.setStyleSheet("border: 2px dashed #999;")
        self.filepath = ""

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = event.mimeData().urls()
        if files:
            self.filepath = files[0].toLocalFile()
            self.label.setText(f"已选择文件: {os.path.basename(self.filepath)}")


class LocalizationGUI(QMainWindow):
    MODEL_TYPES = {
        "通义千问": "TongYiQwen",
        "通义": "TongYi",
        "豆包": "Doubao",
        "DeepSeek": "DeepSeek",
        "Kimi": "Kimi",
    }

    LANGUAGES = {
        "简体中文": "zh-CN",
        "繁体中文": "zh-TW",
        "英语": "en",
        "日语": "ja",
        "韩语": "ko",
        "德语": "de",
        "法语": "fr",
        "西班牙语": "es",
        "意大利语": "it",
        "俄语": "ru",
    }

    # 反向映射，用于从配置中恢复UI状态
    REVERSE_MODEL_TYPES = {v: k for k, v in MODEL_TYPES.items()}
    REVERSE_LANGUAGES = {v: k for k, v in LANGUAGES.items()}

    def __init__(self):
        super().__init__()
        self.config = {}
        self.ui_cache_path = os.path.join("default", "cache", "ui_settings.yaml")
        self.load_config()
        self.load_ui_cache()
        self.initUI()

    def load_config(self, model_type=None):
        if model_type is None:
            model_type = "TongYiQwen"  # 默认使用通义千问的配置

        # 根据模型类型确定配置文件名
        config_filename = ""
        match model_type:
            case "TongYiQwen":
                config_filename = "tongyi_qwen_config.yaml"
            case "TongYi":
                config_filename = "tongyi_config.yaml"
            case "Doubao":
                config_filename = "doubao_config.yaml"
            case "DeepSeek":
                config_filename = "deepseek_config.yaml"
            case "Kimi":
                config_filename = "kimi_config.yaml"

        config_path = os.path.join("default", "configs", config_filename)

        # 如果默认配置目录不存在，使用主配置目录
        if not os.path.exists(config_path):
            config_path = os.path.join("configs", config_filename)

        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        else:
            # 如果配置文件不存在，使用空配置
            self.config = {}

    def load_ui_cache(self):
        """加载用户界面缓存设置"""
        if os.path.exists(self.ui_cache_path):
            try:
                with open(self.ui_cache_path, "r", encoding="utf-8") as f:
                    cached_settings = yaml.safe_load(f)

                # 恢复缓存的设置
                if cached_settings:
                    # 恢复模型类型选择
                    if "model_type" in cached_settings:
                        model_type = cached_settings["model_type"]
                        if model_type in self.REVERSE_MODEL_TYPES:
                            self.config["model_type"] = model_type

                    # 恢复其他设置
                    self.config["model"] = cached_settings.get(
                        "model", self.config.get("model", "")
                    )
                    self.config["base_url"] = cached_settings.get(
                        "base_url", self.config.get("base_url", "")
                    )
                    self.config["api_key"] = cached_settings.get(
                        "api_key", self.config.get("api_key", "")
                    )
                    self.config["use_cache"] = cached_settings.get(
                        "use_cache", self.config.get("use_cache", True)
                    )
                    self.config["system_prompt"] = cached_settings.get(
                        "system_prompt", self.config.get("system_prompt", "")
                    )
                    self.config["target_languages"] = cached_settings.get(
                        "target_languages", self.config.get("target_languages", [])
                    )
                    self.config["output_dir"] = cached_settings.get("output_dir", "")
            except Exception as e:
                print(f"加载界面缓存失败: {str(e)}")

    def save_ui_cache(self):
        """保存用户界面设置到缓存"""
        try:
            # 创建要缓存的设置
            cache_settings = {
                "model_type": self.MODEL_TYPES[self.model_type.currentText()],
                "model": self.model_name.text(),
                "base_url": self.base_url.text(),
                "api_key": self.api_key.text(),
                "use_cache": self.use_cache.isChecked(),
                "system_prompt": self.system_prompt.toPlainText(),
                "target_languages": self.get_selected_languages(),
                "output_dir": self.output_path.text(),
            }

            # 保存到文件
            os.makedirs(os.path.dirname(self.ui_cache_path), exist_ok=True)
            with open(self.ui_cache_path, "w", encoding="utf-8") as f:
                yaml.dump(cache_settings, f, allow_unicode=True)
        except Exception as e:
            print(f"保存界面缓存失败: {str(e)}")

    def initUI(self):
        self.setWindowTitle("本地化工具")
        self.setGeometry(300, 300, 800, 600)

        # 创建主滚动区域
        scroll = QScrollArea()
        self.setCentralWidget(scroll)
        container = QWidget()
        main_layout = QVBoxLayout(container)

        # 确保目录存在
        os.makedirs(os.path.dirname(self.ui_cache_path), exist_ok=True)

        # 在初始化UI组件之前应用缓存的设置
        cached_model_type = self.config.get("model_type", "TongYiQwen")

        # 文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QVBoxLayout()

        # 拖拽区域
        self.drop_area = DropArea()
        file_layout.addWidget(self.drop_area)

        # 输出目录选择
        output_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("选择输出目录...")
        self.output_path.setReadOnly(True)
        output_btn = QPushButton("选择输出目录")
        output_btn.clicked.connect(self.select_output_dir)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(output_btn)
        file_layout.addLayout(output_layout)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # 模型配置区域
        model_group = QGroupBox("模型配置")
        model_layout = QVBoxLayout()

        # 模型选择
        model_type_layout = QHBoxLayout()
        model_type_layout.addWidget(QLabel("模型类型:"))
        self.model_type = QComboBox()
        self.model_type.addItems(self.MODEL_TYPES.keys())
        self.model_type.currentTextChanged.connect(self.on_model_changed)
        model_type_layout.addWidget(self.model_type)
        model_layout.addLayout(model_type_layout)

        # 模型名称
        model_name_layout = QHBoxLayout()
        model_name_layout.addWidget(QLabel("模型名称:"))
        self.model_name = QLineEdit()
        self.model_name.setText(self.config.get("model", ""))
        model_name_layout.addWidget(self.model_name)
        model_layout.addLayout(model_name_layout)

        # API配置
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API地址:"))
        self.base_url = QLineEdit()
        self.base_url.setText(self.config.get("base_url", ""))
        api_layout.addWidget(self.base_url)
        model_layout.addLayout(api_layout)

        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel("API Key:"))
        self.api_key = QLineEdit()
        self.api_key.setText(self.config.get("api_key", ""))
        api_key_layout.addWidget(self.api_key)
        model_layout.addLayout(api_key_layout)

        # 缓存设置
        cache_layout = QHBoxLayout()
        self.use_cache = QCheckBox("启用缓存")
        self.use_cache.setChecked(self.config.get("use_cache", True))
        cache_layout.addWidget(self.use_cache)
        model_layout.addLayout(cache_layout)

        # 系统提示词
        prompt_layout = QVBoxLayout()
        prompt_layout.addWidget(QLabel("自定义系统提示词:"))
        self.system_prompt = QTextEdit()
        self.system_prompt.setPlaceholderText("在这里输入额外的系统提示词...")
        self.system_prompt.setMaximumHeight(100)
        prompt_layout.addWidget(self.system_prompt)
        model_layout.addLayout(prompt_layout)

        model_group.setLayout(model_layout)
        main_layout.addWidget(model_group)

        # 目标语言选择
        lang_group = QGroupBox("目标语言")
        lang_layout = QVBoxLayout()
        self.lang_list = QListWidget()
        self.lang_list.setSelectionMode(QAbstractItemView.MultiSelection)
        for lang_name in self.LANGUAGES.keys():
            self.lang_list.addItem(lang_name)
        # 根据配置选中默认语言
        self.select_default_languages()
        lang_layout.addWidget(self.lang_list)
        lang_group.setLayout(lang_layout)
        main_layout.addWidget(lang_group)

        # 开始按钮
        start_btn = QPushButton("开始本地化")
        start_btn.clicked.connect(self.start_localization)
        main_layout.addWidget(start_btn)

        # 恢复保存的输出目录
        if self.config.get("output_dir"):
            self.output_path.setText(self.config["output_dir"])

        # 设置滚动区域
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

    def select_default_languages(self):
        default_langs = self.config.get("target_languages", [])
        for i in range(self.lang_list.count()):
            item = self.lang_list.item(i)
            lang_code = self.LANGUAGES[item.text()]
            if lang_code in default_langs:
                item.setSelected(True)

    def on_model_changed(self, model_name):
        # 获取选择的模型类型
        model_type = self.MODEL_TYPES[model_name]

        # 加载对应的配置
        self.load_config(model_type)

        # 更新界面上的配置值
        self.model_name.setText(self.config.get("model", ""))
        self.base_url.setText(self.config.get("base_url", ""))
        self.api_key.setText(self.config.get("api_key", ""))
        self.use_cache.setChecked(self.config.get("use_cache", True))
        self.system_prompt.setText(self.config.get("system_prompt", ""))

        # 更新选中的语言
        self.select_default_languages()

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_path.setText(dir_path)

    def get_selected_languages(self):
        selected_langs = []
        for item in self.lang_list.selectedItems():
            selected_langs.append(self.LANGUAGES[item.text()])
        return selected_langs

    def create_config(self):
        # 创建配置字典
        config = {
            "model_type": self.MODEL_TYPES[self.model_type.currentText()],
            "model": self.model_name.text(),
            "base_url": self.base_url.text(),
            "api_key": self.api_key.text(),
            "use_cache": self.use_cache.isChecked(),
            "cache_path": os.path.join("default", "cache", "localization.cache"),
            "translation_style": "formal",
            "target_languages": self.get_selected_languages(),
        }

        # 处理系统提示词
        base_prompt = self.config.get("system_prompt", "")
        custom_prompt = self.system_prompt.toPlainText()
        if custom_prompt:
            config["system_prompt"] = f"{base_prompt}\n{custom_prompt}"
        else:
            config["system_prompt"] = base_prompt

        return config

    def start_localization(self):
        if not self.api_key.text():
            print("需要API密钥！")
            return

        if not self.drop_area.filepath:
            print("请先选择源文件！")
            return

        if not self.output_path.text():
            print("请选择输出目录！")
            return

        if not self.get_selected_languages():
            print("请至少选择一个目标语言！")
            return

        # 创建临时配置文件
        temp_config = self.create_config()
        temp_config_path = "configs/temp_config.yaml"

        try:
            # 保存临时配置
            with open(temp_config_path, "w", encoding="utf-8") as f:
                yaml.dump(temp_config, f, allow_unicode=True)

            # 创建本地化实例并运行
            config = LocalizationConfig(temp_config_path)
            processor = LocalizationProcessor(config)

            # 执行本地化处理
            processor.generate_localization(
                source_path=self.drop_area.filepath,
                target_langs=self.get_selected_languages(),
                output_dir=self.output_path.text(),
                style="formal",
            )
            print("本地化完成！")

        except Exception as e:
            print(f"本地化过程出错: {str(e)}")
        finally:
            config.save_cache()
            print("缓存已保存。")
            # 清理临时配置文件
            if os.path.exists(temp_config_path):
                os.remove(temp_config_path)

    def closeEvent(self, event):
        """窗口关闭时保存界面设置"""
        self.save_ui_cache()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = LocalizationGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
