import requests
import json
from component.llm import RAG

# Ollama API 的 URL
url = "http://localhost:11434/api/chat"
model = "qwen2:1.5b"  # 替换为实际使用的模型
headers = {"Content-Type": "application/json"}

# 初始化对话上下文
messages = [
    {
        "role": "system",
        "content": "你是“四川大学电气实验室”的机器人，名叫小锂，可以回答用户的针对软件操作的问题并提供数据分析结果建议。请将回答组织成流畅、连贯的段落，禁止分点回答，禁止使用任何 Markdown 或加粗符号（如**）。确保输出为正常的文本格式。骤"
    }
]


def send_to_ollama(user_input):
    """
    将用户输入和当前上下文发送到 Ollama，并返回模型的响应。
    """
    global messages
    # 添加用户输入到消息上下文
    messages.append({"role": "user", "content": user_input})

    # 构造请求数据
    data = {
        "model": model,
        "options": {
            "temperature": 0  # 可调节生成结果的随机性
        },
        "stream": False,  # 不使用流式输出
        "messages": messages
    }

    try:
        # 发送请求
        response = requests.post(url, json=data, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            output = result.get("message", {}).get("content", "无内容")
            # 将模型响应添加到上下文
            messages.append({"role": "assistant", "content": output})
            output = output.replace('*', '')

            if len(messages) > 50:  # 限制上下文长度
                messages = messages[:1] + messages[-20:]  # 保留系统消息和最近 20 条记录

            return output
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"

def send_to_ollama_system(user_input):
    """
    将用户输入和当前上下文发送到 Ollama，并返回模型的响应。
    """
    global messages
    # 添加用户输入到消息上下文
    messages.append({"role": "system", "content": user_input})

    # 构造请求数据
    data = {
        "model": model,
        "options": {
            "temperature": 0  # 可调节生成结果的随机性
        },
        "stream": False,  # 不使用流式输出
        "messages": messages
    }

    try:
        # 发送请求
        response = requests.post(url, json=data, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            output = result.get("message", {}).get("content", "无内容")
            # 将模型响应添加到上下文
            messages.append({"role": "assistant", "content": output})
            output = output.replace('*', '')
            return output
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"

# def main():
#     print("开始与 Ollama 对话，输入 'exit' 退出程序。\n")
#
#     while True:
#         # choice = input("消息类型")
#         # 获取用户输入
#         user_input = input("你: ")
#         if user_input.lower() == "exit":
#             print("结束对话。再见！")
#             break
#
#         context = RAG.get_doc(user_input)
#         input_text = f"Question: {user_input}\nContext: {context}"
#         # if choice == "1":
#             # 获取 Ollama 的响应
#         response = send_to_ollama_system(input_text)
#         print(f"Ollama: {response}\n")
#         # else:
#         #     response = send_to_ollama(input_text)
#         #     print(f"Ollama: {response}\n")
#
# if __name__ == "__main__":
#     main()

def rag_and_send(user_input):
        context = RAG.get_doc(user_input)
        input_text = f"Question: {user_input}\nContext: {context}"
        response = send_to_ollama_system(input_text)

        return response