import json
import importlib
def create_flow(filepath):
    print('hello')
    with open(filepath,'r') as f:
        config = json.load(f)
    code_lines=[]
    if "llm" in config:
        llm_config = config["llm"]
        llm_file=f'llms/{llm_config}.py'
        with open(llm_file, 'r') as file:
            file_contents= [line.strip() for line in file]
        file.close()
        code_lines.append(file_contents)   
    if "doc_type" in config:
        doc_config=config["doc_type"]
        doc_file=f'doc_type/{doc_config}.py'
        with open(doc_file, 'r') as file:
            file_contents= [line.strip() for line in file]
        file.close()
        code_lines.append(file_contents)   
    if "embeddings" in config:
        emb_config=config["embeddings"]  
        emb_file=f'embeddings/{emb_config}.py'
        with open(emb_file, 'r') as file:
            file_contents= [line.strip() for line in file]
        file.close()
        code_lines.append(file_contents)   
    if "retriever_tools" in config:
        ret_config=config['retriever_tools']
        ret_file=f'retriever_tools'/{ret_config}.py
        with open(ret_file, 'r') as file:
            file_contents= [line.strip() for line in file]
        file.close()
        code_lines.append(file_contents) 
    if "web_search_tools" in config:
        web_config=config['web_search_tools']
        web_file=f'web_search_tools'/{web_config}.py
        with open(web_file, 'r') as file:
            file_contents= [line.strip() for line in file]
        file.close()
        code_lines.append(file_contents) 
    if "vector_stores" in config:
        vector_config=config['vector_stores']
        vector_file=f'vector_stores'/{vector_config}.py
        with open(vector_file, 'r') as file:
            file_contents= [line.strip() for line in file]
        file.close()
        code_lines.append(file_contents)  
    with open('self_rag.py', 'r') as file:
        file_contents= [line.strip() for line in file]
    code_lines.append(file_contents)
    file.close()
    
    output_file='./output_files/rag_system.py'
    with open(output_file, 'w') as f:
        f.write('\n'.join(code_lines))

    print(f"RAG code has been generated in {output_file}")

    

