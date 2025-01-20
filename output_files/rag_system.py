api_key ={config['llm']}
from langchain_groq import ChatGroq

def call_llm(api_key):

    llm = ChatGroq(

    api_key=api_key

    )

    return llm
from langchain_community.document_loaders import PyPDFLoader

def call_doctype(uploaded_file_path):

    file_name=uploaded_file_path

    loader = PyPDFLoader(

        file_name

    )

    return loader.load()
from langchain_huggingface import HuggingFaceEmbeddings

def embs():

    model_name="BAAI/bge-small-en-v1.5"

    model_kwargs = {'device': 'cpu'}

    encode_kwargs = {'normalize_embeddings': False}

    embeddings =  HuggingFaceEmbeddings(

        model_name=model_name,

        model_kwargs=model_kwargs,

        encode_kwargs=encode_kwargs

    )

    return embeddings
def call_retriever(db):

    return db.as_retriever()
from langchain_chroma import Chroma

def call_vectorstore(embs,doc_splits):

    vector_store = Chroma.from_documents(

    documents=doc_splits,

    embedding_function=embs,

    )

    return vector_store