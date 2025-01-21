from langchain_community.document_loaders import PyPDFLoader
def call_doctype(uploaded_file_path):
    file_name=uploaded_file_path
    loader = PyPDFLoader(
        file_name
    )
    return loader.load()