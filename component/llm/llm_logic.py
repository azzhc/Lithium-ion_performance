from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget

from component.llm import llm_ui, LLM


class llmLogic(QWidget, llm_ui.Ui_LLM):
    def __init__(self):
        super(llmLogic, self).__init__()
        self.setupUi(self)
        self.msg_send.clicked.connect(self.send_msg)

    def send_msg(self):
        # user_input = self.input_field.text().strip()
        input = self.msg_text.text()
        if not input:
            pass
        # 将用户输入显示在对话显示区域
        self.dialog.append(f"你: {input}")
        # 模拟 Ollama 的响应（可以替换为实际的对话逻辑）
        bot_response = LLM.rag_and_send(input)
        self.dialog.append(f"Ollama: {bot_response}\n")
        # 清空输入框
        self.msg_text.clear()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = llmLogic()
#     window.show()
#     sys.exit(app.exec_())
