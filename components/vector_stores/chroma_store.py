from langchain_chroma import Chroma
def call_vectorstore(embs,doc_splits):
    vector_store = Chroma.from_documents(
    documents=doc_splits,
    embedding=embs,
    )
    return vector_store