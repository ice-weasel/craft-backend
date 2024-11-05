from langchain.retrievers.self_query.base import SelfQueryRetriever
def call_retriever(db,llm):
    document_content_description = ""
    metadata_field_info=""
    retriever = SelfQueryRetriever.from_llm(
        llm,
        db,
        document_content_description,
        metadata_field_info,
    )
    return retriever