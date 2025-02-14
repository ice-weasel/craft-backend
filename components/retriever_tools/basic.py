def call_retriever(llm,db):
    return db.as_retriever()