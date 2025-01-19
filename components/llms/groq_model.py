from langchain_groq import ChatGroq
def call_llm(api_key):
    llm = ChatGroq(
    api_key=api_key
    )
    return llm