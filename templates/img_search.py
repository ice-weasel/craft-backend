from langchain_core.messages import HumanMessage
import base64, httpx
from langchain_groq import ChatGroq
import getpass
import os
from typing import TypedDict, List, Dict
from langgraph.graph import Graph
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from dataclasses import dataclass
from langchain_core.runnables import RunnableConfig

class WorkflowState(TypedDict):
    query: str
    image_paths: List[str]
    embeddings: Dict[str, np.ndarray]
    results: List[str]

@dataclass
class ImageSearchConfig:
    model_name: str = "openai/clip-vit-base-patch32"
    similarity_threshold: float = 0.7
    max_results: int = 5

# Initialize CLIP model and processor
def init_clip():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

# Node functions
def process_query(state: WorkflowState, config: RunnableConfig) -> WorkflowState:
    """Process the text query and prepare it for embedding"""
    # Here you might clean or validate the query
    return state

def generate_embeddings(state: WorkflowState, config: RunnableConfig) -> WorkflowState:
    """Generate embeddings for both query and images"""
    model, processor = init_clip()
    
    # Process query
    inputs = processor(text=[state["query"]], return_tensors="pt", padding=True)
    query_features = model.get_text_features(**inputs)
    query_embedding = query_features.detach().numpy()
    
    # Process images
    image_embeddings = {}
    for image_path in state["image_paths"]:
        try:
            image = Image.open(image_path)
            inputs = processor(images=image, return_tensors="pt", padding=True)
            image_features = model.get_image_features(**inputs)
            image_embeddings[image_path] = image_features.detach().numpy()
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
    
    state["embeddings"] = image_embeddings
    state["query_embedding"] = query_embedding
    return state

def calculate_similarities(state: WorkflowState, config: RunnableConfig) -> WorkflowState:
    """Calculate similarity scores between query and images"""
    query_embedding = state["query_embedding"]
    search_config = ImageSearchConfig()
    
    similarities = {}
    for path, embedding in state["embeddings"].items():
        similarity = np.dot(query_embedding, embedding.T) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
        )
        similarities[path] = float(similarity)
    
    # Filter and sort results
    filtered_results = [
        path for path, score in similarities.items() 
        if score >= search_config.similarity_threshold
    ]
    sorted_results = sorted(
        filtered_results,
        key=lambda x: similarities[x],
        reverse=True
    )[:search_config.max_results]
    
    state["results"] = sorted_results
    return state

# Build the graph
def build_image_search_workflow() -> Graph:
    workflow = Graph()
    
    # Define the nodes
    workflow.add_node("process_query", process_query)
    workflow.add_node("generate_embeddings", generate_embeddings)
    workflow.add_node("calculate_similarities", calculate_similarities)
    
    # Define the edges
    workflow.add_edge("process_query", "generate_embeddings")
    workflow.add_edge("generate_embeddings", "calculate_similarities")
    
    # Set the entry point
    workflow.set_entry_point("process_query")
    
    # Compile the graph
    return workflow.compile()

# Example usage
def run_image_search(query: str, image_paths: List[str]) -> List[str]:
    """Run the image search workflow"""
    workflow = build_image_search_workflow()
    
    # Initialize state
    initial_state = WorkflowState(
        query=query,
        image_paths=image_paths,
        embeddings={},
        results=[]
    )
    
    # Run the workflow
    final_state = workflow.invoke(initial_state)
    return final_state["results"]