from langchain_chroma import Chroma
def call_vectorstore(embs):
    vector_store = Chroma(
    embedding_function=embs,
    )
    return vector_store