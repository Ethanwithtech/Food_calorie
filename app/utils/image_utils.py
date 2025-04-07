"""
图像处理工具
用于处理上传的图像文件
"""

import os
import uuid
from pathlib import Path
from datetime import datetime
from PIL import Image
import io

def save_uploaded_image(uploaded_file, save_dir="temp_images"):
    """
    保存上传的图像文件
    
    参数:
        uploaded_file: Streamlit上传的文件对象
        save_dir (str): 保存目录
        
    返回:
        str: 保存的图像文件路径
    """
    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)
    
    # 生成唯一文件名
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(save_dir, unique_filename)
    
    # 读取上传的文件
    img_bytes = uploaded_file.getvalue()
    
    # 使用PIL打开图像以验证它是有效的图像文件
    try:
        with Image.open(io.BytesIO(img_bytes)) as img:
            # 保存图像
            img.save(file_path)
        return file_path
    except Exception as e:
        print(f"保存图像时出错: {str(e)}")
        return None

def is_valid_image(file):
    """
    验证文件是否为有效的图像（JPG或PNG）
    
    参数:
        file: Streamlit上传的文件对象
        
    返回:
        bool: 如果文件是有效的JPG或PNG图像则返回True
    """
    if file is None:
        return False
        
    # 检查文件扩展名
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in ['.jpg', '.jpeg', '.png']:
        return False
    
    # 尝试使用PIL打开文件以确认它是一个有效的图像
    try:
        with Image.open(io.BytesIO(file.getvalue())):
            return True
    except:
        return False 