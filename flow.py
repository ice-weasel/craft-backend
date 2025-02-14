import json
from templates.selfrag_workflow import customise_workflow
def create_flow(filepath):
    print('hello')
    with open(filepath, 'r') as f:
        config = json.load(f)
    print('config')
    code_lines = []
    
    # Load and append contents for each component specified in the configuration
    if "llm" in config:
        print(config["llm"]["llm_name"])
        #print(config["llm"][0])
        llm_config = config["llm"]["llm_name"].lower()
        
        #print( config["llm"])
        llm_file = f'./components/llms/{llm_config}.py'
        #key="api_key ={config['llm']}"
        with open(llm_file, 'r') as file:
            #code_lines.extend([key])
            code_lines.extend([line for line in file])
    print('checkpoint2')
    if "doc_type" in config:
        doc_config = config["doc_type"].lower()
        print(config["doc_type"])
        print("doc_config - ",doc_config)
        doc_file = f'./components/doc_type/{doc_config}.py'
        with open(doc_file, 'r') as file:
            code_lines.extend([line for line in file])
    print('checkpoint21')
    if "embeddings" in config:
        emb_config = config["embeddings"].lower()
        emb_file = f'./components/embeddings/{emb_config}.py'
        with open(emb_file, 'r') as file:
            code_lines.extend([line for line in file])
    print('checkpoint22')
    if "retriever_tools" in config:
        ret_config = config["retriever_tools"].lower()
        print('ret _config : ',ret_config)
        ret_file = f'./components/retriever_tools/{ret_config}.py'
        with open(ret_file, 'r') as file:
            code_lines.extend([line for line in file])
    print('checkpoint23')
    if "web_search_tools" in config:
        web_config = config["web_search_tools"]
        web_file = f'./components/web_search_tools/{web_config}.py'
        with open(web_file, 'r') as file:
            code_lines.extend([line for line in file])
    print('checkpoint24')
    if "vector_stores" in config:
        vector_config = config["vector_stores"]
        vector_file = f'./components/vector_stores/{vector_config}.py'
        with open(vector_file, 'r') as file:
            code_lines.extend([line for line in file])

#templates
    print('checkpoint3')
    if "template" in config:
        print('template')
        if config["template"]=="self_rag":
            template="self_rag"
            print('self rag')
            with open(f'./templates/{template}.py', 'r') as file:
                for line in file:
                    if "api_key" in line:
                        print(config["llm"]["config"]["apiKey"])
                        line = line.replace("api_key", config["llm"]["config"]["apiKey"])
                    code_lines.append(line)
            code_lines=customise_workflow(code_lines,config)
        elif config["template"]=="img-search":
            template="img_search"
        else:
            template="custom"

        print('reading done')
    # Write the collected lines to the output file
    output_file = './output_files/rag_system.py'
    with open(output_file, 'w') as f:
        f.write('\n'.join(code_lines))
    print('writing done')
    print(f"RAG code has been generated in {output_file}")