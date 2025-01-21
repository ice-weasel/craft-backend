import streamlit as st
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from templates.img_search import process_workflow

UPLOAD_DIR = "temp_files"
IMAGE_STORE = "image_store"

# Create necessary directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGE_STORE, exist_ok=True)

st.title("Hosted Workflow")



# Mode selection
mode = st.radio(
    "Select Operation Mode",
    ["Describe Image", "Search Similar Images"]
)

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Query input (only show for search mode)
query = None
if mode == "Search Similar Images":
    query = st.text_input("Enter your search query:", placeholder="Describe what you're looking for...")

if st.button("Process Image"):

    if not uploaded_file:
        st.error("Please upload an image first.")
    elif mode == "Search Similar Images" and not query:
        st.error("Please enter a search query.")
    else:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name_with_timestamp = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(UPLOAD_DIR, file_name_with_timestamp)
        
        try:
            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Optionally save to image store for future searches
            if st.checkbox("Save image to database for future searches"):
                store_path = os.path.join(IMAGE_STORE, uploaded_file.name)
                with open(store_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            # Process the image
            with st.spinner("Processing image..."):
                result = process_workflow(
                    query=query if query else "",
                    image_path=file_path,
                    mode="search" if mode == "Search Similar Images" else "describe",
                    
                )
            
            # Display results
            if mode == "Describe Image":
                st.success("Image Description Generated!")
                st.write("Description:")
                st.write(result['description'])
                
            else:  # Search mode
                st.success("Search Completed!")
                if result['similar_images']:
                    st.write("Similar Images Found:")
                    cols = st.columns(min(len(result['similar_images']), 3))
                    for idx, (image_path, col) in enumerate(zip(result['similar_images'], cols)):
                        with col:
                            st.image(image_path, caption=f"Match {idx + 1}")
                else:
                    st.info("No similar images found in the database.")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
        finally:
            # Cleanup temporary file
            try:
                os.remove(file_path)
            except:
                pass

# Add database management options in sidebar
