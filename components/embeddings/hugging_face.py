from langchain_huggingface import HuggingFaceEmbeddings
def embs():
    model_name="BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings =  HuggingFaceEmbeddings(
        model_name=model_name,
       
    )
    return embeddings