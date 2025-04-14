"""
Description: AI assistant for RAG based on Ollama and PyQt, integrated into other PyQt applications.
Author: ZHC
Date: 2025-3-14
"""

import requests
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QFrame, QMainWindow, QSizePolicy)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.uic import loadUi
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from numpy.linalg import norm

# User & AI Avatar path
USER_AVATAR = "./component/llm/basis/User Avatar.png"
AI_AVATAR = "./component/llm/basis/AI Avart.png"

# Ollama API configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2:1.5b"
HEADERS = {"Content-Type": "application/json"}

# Initial system prompt
messages = [{
    "role": "system",
    "content": (
        "你是小锂，可以回答有关锂电卫士平台的知识。"
        "请将回答组织成流畅、连贯的段落，禁止分点回答，禁止使用任何 Markdown 或加粗符号（如**）。"
        "确保输出为正常的文本格式。"
    )
}]

class DocumentRetriever:
    def __init__(self, file_path="./component/llm/basis/documents.txt",
                 model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.file_path = file_path
        self.documents = self._read_documents()
        self.model = SentenceTransformer(model_name)
        self.document_embeddings = np.array(self.model.encode(self.documents)).astype('float32')
        self.document_embeddings /= norm(self.document_embeddings, axis=1, keepdims=True)
        self.index = faiss.IndexFlatIP(self.document_embeddings.shape[1])
        self.index.add(self.document_embeddings)

    def _read_documents(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return [doc.strip() for doc in content.split('\n\n') if doc.strip()]

    def retrieve(self, query, k=1):
        if not self.documents:
            return ""
        query_embedding = np.array(self.model.encode([query])).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        if distances[0][0] > 10:
            return ""
        return " ".join([self.documents[i] for i in indices[0]])

# Instantiate globally for efficiency
doc_retriever = DocumentRetriever()

def send_to_ollama_generic(input_text, input_role="user", temperature=0.2, retries=2):
    global messages
    safe_instruction = (
        "\n\n注意：如果提供的上下文信息不足以回答问题，"
        "你仍需要基于自身知识尽力给出合理解释或建议，不要返回空内容。"
    )
    input_text += safe_instruction

    messages.append({"role": input_role, "content": input_text})
    data = {
        "model": MODEL_NAME,
        "options": {"temperature": temperature},
        "stream": False,
        "messages": messages
    }

    for attempt in range(retries + 1):
        try:
            response = requests.post(OLLAMA_URL, json=data, headers=HEADERS, timeout=60)
            if response.status_code == 200:
                result = response.json()
                output = result.get("message", {}).get("content", "").strip()
                if output:
                    messages.append({"role": "system", "content": output})
                    output = output.replace('*', '').replace('Answer:', '').replace('\n\n', '')
                    if len(messages) > 50:
                        messages = messages[:1] + messages[-20:]
                    return output
                else:
                    if attempt < retries:
                        continue
                    else:
                        fallback_message = "抱歉，我暂时无法准确回答你的问题，请尝试重新描述问题或提供更多细节。"
                        messages.append({"role": "system", "content": fallback_message})
                        return fallback_message
            else:
                return f"Error: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                continue
            else:
                return f"请求失败: {e}"

class OllamaWorker(QThread):
    response_received = pyqtSignal(str)
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.doc_retriever = DocumentRetriever()

    def run(self):
        context = self.doc_retriever.retrieve(self.message, k=1)
        input_text = f"Question: {self.message}\nContext: {context}"
        response = send_to_ollama_generic(input_text, temperature=0.2)
        self.response_received.emit(response)

class llmLogic(QMainWindow):
    def __init__(self, parent=None):
        super(llmLogic, self).__init__(parent)
        self.doc_retriever = DocumentRetriever()
        loadUi("./component/llm/basis/mainwin.ui", self)
        self.setWindowTitle('AI助理')
        self.setWindowIcon(QIcon('./component/llm/basis/Software Icon.png'))
        self.setStyleSheet("background-color: white;")
        self.send.clicked.connect(self.send_message)
        self.send.setStyleSheet("""
                    QPushButton {
                        background-color: #5C85D6;
                        color: white;
                        padding: 8px;
                        border-radius: 10px;
                        font-weight: bold;
                    }
                """)
        self.chat_container.setSpacing(10)

    def send_message(self):
        user_text = self.text_input.toPlainText().strip()
        if user_text:
            self.add_message(user_text, "user")
            self.text_input.clear()
            self.worker = OllamaWorker(user_text)
            self.worker.response_received.connect(self.display_ai_response)
            self.worker.start()

    def display_ai_response(self, response):
        """Show AI Response"""
        # 保证窗口始终显示并获取焦点
        self.add_message(response, "ai")
        if self.isHidden():
            self.show()
        self.raise_()
        self.activateWindow()

    def add_message(self, text, sender):
        """Add message bubbles to the interface and
         adjust the alignment according to the sender"""
        message_label = QLabel(text)
        max_width = int(self.width() * 0.7)
        message_label.setFixedWidth(max_width)
        message_label.setWordWrap(False)
        message_label.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px;")
        font_metrics = message_label.fontMetrics()
        text_width = font_metrics.boundingRect(message_label.text()).width() + 18 * 5  # 加内边距
        bubble_width = min(text_width, max_width)
        message_label.setFixedWidth(bubble_width)
        message_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        message_label.setWordWrap(True)
        # message_label.adjustSize()
        if sender == "user":
            message_label.setStyleSheet(message_label.styleSheet() + "background-color: #A7C7E7;")
        else:
            message_label.setStyleSheet(message_label.styleSheet() + "background-color: #89D961;")
        # Avatar
        avatar_label = QLabel()
        avatar_label.setFixedSize(40, 40)
        avatar_label.setScaledContents(True)
        avatar_path = USER_AVATAR if sender == "user" else AI_AVATAR
        avatar_label.setPixmap(QPixmap(avatar_path))
        avatar_label.setStyleSheet("border-radius: 20px;")

        # Layout settings: adjust alignment order according to sender
        message_layout = QHBoxLayout()
        message_layout.setAlignment(Qt.AlignTop)
        if sender == "user":
            message_layout.addStretch()
            message_layout.addWidget(message_label)
            message_layout.addWidget(avatar_label)
        else:
            message_layout.addWidget(avatar_label)
            message_layout.addWidget(message_label)
            message_layout.addStretch()
        container = QFrame()
        container.setLayout(message_layout)
        container.setContentsMargins(5, 5, 5, 5)
        container.setMinimumHeight(message_label.sizeHint().height())
        self.chat_container.addWidget(container)
        # self.chat_container.addSpacing(5)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
