from langchain_community.document_loaders import UnstructuredPowerPointLoader
def call_doctype(uploaded_file_path):
    file_name=uploaded_file_path
    loader = UnstructuredPowerPointLoader(
    file_name
    ) 
    return loader.load()