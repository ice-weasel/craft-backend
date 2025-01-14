import json

def create_flow(filepath):
    print('hello')
    with open(filepath, 'r') as f:
        config = json.load(f)
    print('config')
    code_lines = []
    
    # Load and append contents for each component specified in the configuration
    if "llm" in config:
        llm_config = config["llm"]
        llm_file = f'./components/llms/{llm_config}.py'
        with open(llm_file, 'r') as file:
            code_lines.extend([line for line in file])

    if "doc_type" in config:
        doc_config = config["doc_type"]
        doc_file = f'./components/doc_type/{doc_config}.py'
        with open(doc_file, 'r') as file:
            code_lines.extend([line for line in file])

    if "embeddings" in config:
        emb_config = config["embeddings"]
        emb_file = f'./components/embeddings/{emb_config}.py'
        with open(emb_file, 'r') as file:
            code_lines.extend([line for line in file])

    if "retriever_tools" in config:
        ret_config = config["retriever_tools"]
        ret_file = f'./components/retriever_tools/{ret_config}.py'
        with open(ret_file, 'r') as file:
            code_lines.extend([line for line in file])

    if "web_search_tools" in config:
        web_config = config["web_search_tools"]
        web_file = f'./components/web_search_tools/{web_config}.py'
        with open(web_file, 'r') as file:
            code_lines.extend([line for line in file])

    if "vector_stores" in config:
        vector_config = config["vector_stores"]
        vector_file = f'./components/vector_stores/{vector_config}.py'
        with open(vector_file, 'r') as file:
            code_lines.extend([line for line in file])

    # Append the contents of the main self_rag.py file
    with open('./templates/self_rag.py', 'r') as file:
        code_lines.extend([line for line in file])
    print('reading done')
    # Write the collected lines to the output file
    output_file = './output_files/rag_system.txt'
    with open(output_file, 'w') as f:
        f.write('\n'.join(code_lines))
    print('writing done')
    print(f"RAG code has been generated in {output_file}")