import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from output_files.rag_system import process_workflow

UPLOAD_DIR = "temp_files"
st.title("Hosted Workflow")

question = st.text_input("Search query:", placeholder="")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Run Workflow"):
    if not question:
        st.error("Please enter a question before running the workflow.")
    elif not uploaded_file:
        st.error("Please upload a PDF file before running the workflow.")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name_with_timestamp = f"{timestamp}_{uploaded_file.name}"

        # Construct the full file path
        file_path = os.path.join(UPLOAD_DIR, file_name_with_timestamp)

        # Save the uploaded file
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success(f"File uploaded and saved as: {file_name_with_timestamp}")
        except Exception as e:
            st.error(f"Error saving the file: {e}")
            st.stop()

        # Call the main logic with the uploaded file path
        try:
            st.info("Processing the workflow...")
            result = process_workflow(question, file_path)
            st.success("Workflow Completed!")
            st.write("Generated Answer:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")