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


def get_model(model_type: str, api_url: str = None):
    """
    根据model_type参数和api_url决定使用本地ollama或外部大模型。
    出现错误时不退出，而是返回None。
    """
    try:
        if model_type == "local":
            model = ChatOllama(model="qwen2:1.5b")
            print("使用本地ollama模型。")
        elif model_type == "outside":
            if not api_url:
                raise ValueError("当类型为outside时，必须提供有效的api地址。")
            model = ChatOllama(api_url=api_url, model="qwen2:1.5b")
            print("使用外部大模型，api地址为：", api_url)
        else:
            raise ValueError("未知的model_type参数，仅支持'本地'或'外部API'.")
        return model
    except Exception as e:
        show_error("模型初始化错误", f"初始化模型时出错：{e}")
        return None


def show_error(title: str, message: str):
    """
    弹出提示框显示错误信息
    """
    # 初始化tkinter根窗口并隐藏
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()


def query_model(user_input: str, model_type: str = "local", api_url: str = None) -> str:
    """
    封装全文档检索、提示生成和大模型调用的流程，
    出现错误时通过弹出提示框显示错误信息，且不会退出程序。

    参数:
        user_input: 用户输入的问题。
        model_type: 模型类型，'local'表示使用本地ollama，'outside'表示使用外部api。
        api_url: 当model_type为'outside'时，需要提供外部大模型的api地址。
    返回:
        模型的回答字符串。如果出现错误则返回空字符串或错误提示。
    """
    try:
        # 获取模型实例
        model_instance = get_model(model_type, api_url)
        if model_instance is None:
            raise RuntimeError("无法获取可用的模型实例，请检查本地ollama和外部api设置。")

        # 定义角色描述（系统信息，可根据需要自定义）
        role_description = SystemMessage(
            content="你是一个锂电池软件帮助助手，叫小锂，来自四川大学电气工程实验室。"
        )

        # 1. 读取文件并分词
        documents = TextLoader("component/llm/documents.txt").load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
        doc_splits = text_splitter.split_documents(documents)

        # 2. 嵌入并存储
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        vectorstore = DocArrayInMemorySearch.from_documents(doc_splits, embedding_model)
        retriever = vectorstore.as_retriever()

        # 3. 定义提示模板
        template = """
        系统信息：请你根据以下文本回答问题，同时记住你的角色是一个叫小锂的锂电池软件助手，来自四川大学电气工程实验室。
        文本: {context}
        问题: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        # 构建链路，将检索、提示和模型调用连接
        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | model_instance
                | StrOutputParser()
        )

        # 调用链路，并返回结果
        response = chain.invoke(user_input)
        return response

    except Exception as e:
        show_error("执行错误", f"处理请求时出错，请检查本地Ollama运行情况或API地址：{e}")
        return ""  # 或返回一个错误提示字符串


# 示例调用
# if __name__ == "__main__":
#     # 修改以下参数，根据需要选择使用本地或外部模型
#     model_type = "local"  # 或 "outside"
#     api_url = "http://external-model-api-address"  # 若model_type为"outside"时使用
#     question = "锂电池的主要优点有哪些？"
#
#     answer = query_model(question, model_type, api_url)
#     if answer:
#         print("回答：", answer)
#     else:
#         print("未能获得有效回答。")
