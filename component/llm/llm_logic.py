from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import messagebox
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader
from langchain_community import embeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, \
    QWidget, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

from component.llm import llm_ui, LLM

class LLMThread(QThread):

    task_done = pyqtSignal(str)  # 传递模型响应
    def __init__(self, input_text, llmtype, api):
        super(LLMThread, self).__init__()
        self.input_text = input_text
        self.llmtype = llmtype
        self.api = api

    def run(self):
        response = LLM.query_model(self.input_text, self.llmtype, self.api)
        self.task_done.emit(response)  # 发出信号，将结果返回给主线程


class llmLogic(QWidget, llm_ui.Ui_LLM):
    def __init__(self):
        super(llmLogic, self).__init__()
        self.setupUi(self)
        self.msg_send.clicked.connect(self.send_msg)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_text)
        self.is_blinking = False


    def send_msg(self):
        input_text = self.msg_text.text().strip()
        llmtype_ori = self.type.currentText()
        api = self.api_adress.text().strip()

        if llmtype_ori == '外部API':
            llmtype = 'outside'
        else:
            llmtype = 'local'

        if llmtype == 'outside' and not api:
            QMessageBox.critical(self, '错误', '请提供API地址')
            return

        if not input_text:
            return

        try:
            # 将用户输入显示在对话显示区域
            self.dialog.append(f"你: {input_text}")

            # 创建并启动子线程来处理任务
            self.llm_thread = LLMThread(input_text, llmtype, api)
            self.llm_thread.task_done.connect(self.handle_bot_response)
            self.llm_thread.start()

            # 清空输入框
            self.msg_text.clear()

            self.timer.start(800)  # 每500毫秒切换一次文字
            self.msg_text.setText("回应中，请勿点击发送按钮...")  # 设置初始文本为"回应中..."

        except Exception as e:
            # 捕获异常并显示错误消息
            QMessageBox.critical(self, '出错啦', str(e))

    def toggle_text(self):
        """切换文本的显示/隐藏，产生闪烁效果"""
        if self.is_blinking:
            self.msg_text.setText("回应中，请勿点击发送按钮...")
        else:
            self.msg_text.setText("")
        self.is_blinking = not self.is_blinking

    def handle_bot_response(self, response):
        self.timer.stop()
        self.msg_text.setText("")  # 清空输入框
        # 更新对话区域，显示 Ollama 的回应
        self.dialog.append(f"AI助手: {response}\n")

#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = llmLogic()
#     window.show()
#     sys.exit(app.exec_())
