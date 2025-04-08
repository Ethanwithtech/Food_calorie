"""
Image Processing Utilities
Used for processing uploaded image files
"""

import os
import uuid
from pathlib import Path
from datetime import datetime
from PIL import Image
import io

def save_uploaded_image(uploaded_file, save_dir="temp_images"):
    """
    Save the uploaded image file
    
    Parameters:
        uploaded_file: Streamlit uploaded file object
        save_dir (str): Save directory
        
    Returns:
        str: Path to the saved image file
    """
    # Ensure save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(save_dir, unique_filename)
    
    # Read the uploaded file
    img_bytes = uploaded_file.getvalue()
    
    # Use PIL to open the image to validate it's a valid image file
    try:
        with Image.open(io.BytesIO(img_bytes)) as img:
            # Save the image
            img.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None

def is_valid_image(file):
    """
    Validate if the file is a valid image (JPG or PNG)
    
    Parameters:
        file: Streamlit uploaded file object
        
    Returns:
        bool: Returns True if the file is a valid JPG or PNG image
    """
    if file is None:
        return False
        
    # Check file extension
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in ['.jpg', '.jpeg', '.png']:
        return False
    
    # Try to open the file with PIL to confirm it's a valid image
    try:
        with Image.open(io.BytesIO(file.getvalue())):
            return True
    except:
        return False 