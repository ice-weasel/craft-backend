from langchain_openai import OpenAIEmbeddings
def embs():
     model_name=""
     open_ai_api_key=""
     model={model_name}
     embeddings= OpenAIEmbeddings(
          model=model_name,
          api_key={open_ai_api_key}
     )
     return embeddings