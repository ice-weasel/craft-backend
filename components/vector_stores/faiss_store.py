from langchain_community.vectorstores import FAISS
def call_vectorstore(embs):
    vector_store = FAISS(
        embedding_function=embs,
    )
    return vector_store