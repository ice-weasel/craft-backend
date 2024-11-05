from langchain.retrievers.multi_query import MultiQueryRetriever
def call_retriever(llm,db):
    retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(), llm=llm
    )
    return retriever_from_llm