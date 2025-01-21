from PIL import Image
import base64
from io import BytesIO

def encode_image_to_base64(uploaded_file_path) -> str:
    """Convert image to base64 string"""
    with Image.open(uploaded_file_path) as image:
        buffered = BytesIO()
        image.save(buffered, format=image.format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str