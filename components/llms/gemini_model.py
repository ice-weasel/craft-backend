from langchain_google_genai import ChatGoogleGenerativeAI
def call_llm():
    google_api_key=""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key={google_api_key})
    return llm