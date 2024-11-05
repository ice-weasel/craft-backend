from langchain_community.document_loaders import PyPDFLoader
def call_doctype():
    file_name="" #your file path here
    loader = PyPDFLoader(
        file_name
    )
    return loader.load()