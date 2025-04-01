from langchain_groq import ChatGroq
def call_llm(api_key):
    llm = ChatGroq(
     model="llama3-8b-8192",
    api_key=api_key
    )
    return llm