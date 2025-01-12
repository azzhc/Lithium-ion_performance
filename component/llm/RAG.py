from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


def read_documents_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # 读取整个文件内容
        documents = content.split('\n\n')  # 按照空行分割文档
        documents = [doc.strip() for doc in documents]  # 去除多余空白
    return documents
def get_doc(query):
    # 使用预训练的Sentence-BERT模型进行向量化
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # documents = [
    #     "The capital of France is Paris.",
    #     "Python is a programming language.",
    #     "The Eiffel Tower is located in Paris."
    # ]

    file_path = 'documents.txt'  # 请替换为实际的文件路径
    documents = read_documents_from_txt(file_path)

    document_embeddings = model.encode(documents)


    # 转换为float32类型
    document_embeddings = np.array(document_embeddings).astype('float32')

    # 创建FAISS索引
    index = faiss.IndexFlatL2(document_embeddings.shape[1])
    index.add(document_embeddings)



    # 将查询转换为向量
    query_embedding = model.encode([query]).astype('float32')

    # 使用FAISS进行检索
    k = 1  # 获取最相关的2个文档
    D, I = index.search(query_embedding, k)

    # 打印检索到的文档
    retrieved_docs = [documents[i] for i in I[0]]
    context = " ".join(retrieved_docs)

    # print("Retrieved Documents:", retrieved_docs)
    return retrieved_docs

get_doc("HEMS组成")
