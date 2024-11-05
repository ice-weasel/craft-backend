from langchain_tavily import TavilySearchAPIWrapper

def call_websearch():
    tavily_api_key=""
    return TavilySearchAPIWrapper(api_key={tavily_api_key})