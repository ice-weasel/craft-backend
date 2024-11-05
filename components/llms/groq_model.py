from langchain_groq import ChatGroq
def call_llm(groq_api_key):
    llm = ChatGroq(
    api_key={groq_api_key} 
    )
    return llm