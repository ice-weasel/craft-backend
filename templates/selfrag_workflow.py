import os
def customise_workflow(code_lines,config):
    file_path = './selfrag_final.py'
    if os.path.exists(file_path):
        print("File exists")
    flow=config["flowPaths"]
    print("inside custmise wokrflow")
    code_lines.extend(["    workflow.add_edge(START, 'retrieve')"])
    code_lines.extend(["    workflow.add_node('retrieve', retrieve)"])
    code_lines.extend(["    workflow.add_node('generate', generate)"])
    if "grade-documents" in config["flowPaths"] :
        print("inside custmise wokrflow 2")
        code_lines.extend(["    workflow.add_node('grade_documents', grade_documents)"])
        code_lines.extend(["    workflow.add_node('transform_query', transform_query)"])
        code_lines.extend(["    workflow.add_edge('retrieve', 'grade_documents')"])
        code_lines.extend(["    workflow.add_conditional_edges('grade_documents', decide_to_generate,{ 'transform_query': 'transform_query','generate': 'generate',}, )"])
        code_lines.extend(["    workflow.add_edge('transform_query', 'retrieve')"])
        if "hallucination-checker" not in config["flowPaths"]:
            code_lines.extend(["    workflow.add_edge('generate', END)"])
            code_lines.extend(["    app = workflow.compile()"])
            code_lines.extend(["    inputs = {'question': question}"])
            code_lines.extend(["    for output in app.stream(inputs):"])
            code_lines.extend(["        for key, value in output.items():"])
            code_lines.extend(["            print(f'{key}')"])
            code_lines.extend(["    return value['generation']"])
            return code_lines
    if "hallucination-checker" in config["flowPaths"]:
        print("inside custmise wokrflow 3")
        if "grade-documents" not in config["flowPaths"] :
            code_lines.extend(["    workflow.add_edge('retrieve','generate')"])
            code_lines.extend(["    workflow.add_node('transform_query', transform_query)"])
        print('here')
        code_lines.extend(["    workflow.add_conditional_edges('generate',grade_generation_v_documents_and_question,{'not supported': 'generate','useful': END,'not useful': 'transform_query',}, )"])
        print('here2')
        code_lines.extend(["    app = workflow.compile()"])
        print('here3')
        code_lines.extend(["    inputs = {'question': question}"])
        code_lines.extend(["    for output in app.stream(inputs):"])
        code_lines.extend(["        for key, value in output.items():"])
        code_lines.extend(["            print(f'{key}')"])
        code_lines.extend(["    return value['generation']"])
        
        print('returning')
        return code_lines
    if "grade-documents"not in config["flowPaths"] and "hallucination-checker" not in config["flowPaths"]:
        print("inside custmise wokrflow 4")
        code_lines.extend(["    workflow.add_edge('retrieve','generate')"])
        code_lines.extend(["    workflow.add_edge('generate', END)"])
        code_lines.extend(["    app = workflow.compile()"])
        code_lines.extend(["    inputs = {'question': question}"])
        code_lines.extend(["    for output in app.stream(inputs):"])
        code_lines.extend(["        for key, value in output.items():"])
        code_lines.extend(["            print(f'{key}')"])
        code_lines.extend(["    return value['generation']"])
        return code_lines