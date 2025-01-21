from langchain_groq import ChatGroq
def call_llm(api_key):
    llm = ChatGroq(
    model="llama-3.2-11b-vision-preview",
    api_key=api_key
    )
    return llm