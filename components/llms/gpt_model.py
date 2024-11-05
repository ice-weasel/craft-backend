from langchain_community.chat_models import ChatOpenAI
def call_llm():
    llm = ChatOpenAI(model="gpt-3.5-turbo",api_key="openai_api_key")
    return llm