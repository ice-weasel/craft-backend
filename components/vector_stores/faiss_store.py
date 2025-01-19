from langchain_community.vectorstores import FAISS
def call_vectorstore(embs,doc_splits):
    vector_store = FAISS.from_documents(
        documents=doc_splits,
        embedding_function=embs,
    )
    return vector_store