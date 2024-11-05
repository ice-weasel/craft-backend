from langchain_community.document_loaders import UnstructuredPowerPointLoader
def call_doctype():
    file_name=""
    loader = UnstructuredPowerPointLoader(
    file_name
    ) 
    return loader.load()