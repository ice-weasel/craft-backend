from langchain_community.chat_models import ChatOpenAI
def call_llm(api_key):
    llm = ChatOpenAI(model="gpt-3.5-turbo",api_key=api_key)
    return llm