import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFileDialog, QLineEdit)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent

from src.core.Localization import LocalizationProcessor, LocalizationConfig
from src.translators.TongYiQwenTranslator import TongYiQwenTranslator

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
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('本地化工具')
        self.setGeometry(300, 300, 500, 300)

        # 主Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 拖拽区域
        self.drop_area = DropArea()
        layout.addWidget(self.drop_area)

        # 输出目录选择
        output_layout = QVBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("选择输出目录...")
        self.output_path.setReadOnly(True)
        
        output_btn = QPushButton("选择输出目录")
        output_btn.clicked.connect(self.select_output_dir)
        
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # 开始按钮
        start_btn = QPushButton("开始本地化")
        start_btn.clicked.connect(self.start_localization)
        layout.addWidget(start_btn)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_path.setText(dir_path)

    def start_localization(self):
        if not self.drop_area.filepath:
            return
        
        if not self.output_path.text():
            return

        # 创建本地化实例并运行
        config = LocalizationConfig("configs/tongyi_qwen_config.yaml")
        processor = LocalizationProcessor(config)
        
        try:
            # 执行本地化处理
            processor.generate_localization(
                source_path=self.drop_area.filepath,
                target_langs=config.get_config("target_languages"),
                output_dir=self.output_path.text(),
                style=config.get_config("translation_style", "formal")
            )
            print("本地化完成！")
        except Exception as e:
            print(f"本地化过程出错: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = LocalizationGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
