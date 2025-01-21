from typing import List, TypedDict
from langgraph.graph import END, StateGraph, START
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from PIL import Image
import base64
from io import BytesIO
import os
import httpx

class ImageState(TypedDict):
    """
    Represents the state of our image processing graph.
    """
    query: str
    image_path: str
    mode: str  # 'describe' or 'search'
    description: str
    similar_images: List[str]

def encode_image_to_base64(image_path: str) -> str:
    """Convert image to base64 string"""
    with open(image_path, "rb") as image_file:  # Open the file in binary mode
        image_data = image_file.read()  # Read the binary content
    return base64.b64encode(image_data).decode("utf-8")

def init_llm(api_key: str):
    """Initialize Groq LLM"""
    return ChatGroq(
        api_key=api_key,
        model_name="llama-3.2-11b-vision-preview"  # Using text-only model as fallback
    )

def process_image(state: ImageState) -> ImageState:
    """Process the input image based on mode"""
    llm = init_llm("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")  # Replace with your API key
    
    # Convert image to base64
    base64_image = encode_image_to_base64(state['image_path'])
    
    if state['mode'] == 'describe':
        # Generate image description using text-only prompt
        messages = [
            HumanMessage(
                content=[
        {"type": "text", "text": "describe this image"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        },
    ],

            )
        ]
        
        response = llm.invoke(messages)
        state['description'] = response
        
    elif state['mode'] == 'search':
        # Use text comparison for search
        messages = [
            HumanMessage(
                content=f"Compare this image ({base64_image[:100]}...) with the following description: '{state['query']}'. Rate the similarity from 0 to 100 and explain why."
            )
        ]
        
        response = llm.invoke(messages)
        state['similarity_analysis'] = response
    
    return state

def search_similar_images(state: ImageState) -> ImageState:
    """Search for similar images based on text analysis"""
    if state['mode'] == 'search':
        similar_images = []
        
        image_directory = "./image_store"
        if os.path.exists(image_directory):
            llm = init_llm("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")
            
            for image_file in os.listdir(image_directory):
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(image_directory, image_file)
                    base64_image = encode_image_to_base64(image_path)
                    
                 
                    messages = [
                            HumanMessage(
                                content=[
                        {"type": "text", "text": "Given an image and a query, strictly respond with only a number from 0 to 100 representing how well they match."},
                         {"type": "text", "text": state['query']},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],

                            )
                        ]
                    response = llm.invoke(messages)
                    try:
                        similarity_score = float(response.content.strip())
                        if similarity_score > 70:
                            similar_images.append(image_path)
                    except ValueError:
                        continue
                    
                    if len(similar_images) >= 5:
                        break
        
        state['similar_images'] = similar_images
    
    return state

def decide_next_step(state: ImageState) -> str:
    """Decide next step based on mode"""
    if state['mode'] == 'describe':
        return END
    elif state['mode'] == 'search':
        return 'search_similar_images'

def process_workflow(query: str, image_path: str, mode: str) -> dict:
    """Main workflow processing function"""
    # Initialize workflow
    workflow = StateGraph(ImageState)
    
    # Add nodes
    workflow.add_node('process_image', process_image)
    workflow.add_node('search_similar_images', search_similar_images)
    
    # Add edges
    workflow.add_edge(START, 'process_image')
    workflow.add_conditional_edges(
        'process_image',
        decide_next_step,
        {
            'search_similar_images': 'search_similar_images',
            END: END
        }
    )
    workflow.add_edge('search_similar_images', END)
    
    # Compile and run
    app = workflow.compile()
    
    inputs = {
        'query': query,
        'image_path': image_path,
        'mode': mode,
        'description': '',
        'similar_images': []
    }
    
    result = app.invoke(inputs)
    return result