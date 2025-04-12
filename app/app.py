"""
Food Calorie Estimator Application
Uses HKBU GenAI Platform for food recognition and calorie estimation
"""

import streamlit as st
import os
import time
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import custom modules
from utils.api_client import GenAIClient
from utils.image_utils import save_uploaded_image, is_valid_image
from data.food_calories import get_food_calories

# 多语言支持 - 定义字典
TRANSLATIONS = {
    "en": {
        "page_title": "Food Calorie Estimator",
        "app_title": "🍔 Food Calorie Estimator",
        "intro_text": "Upload food images to quickly identify and estimate calories using AI technology. Supports JPG and PNG formats, with data from built-in database and online nutrition sources.",
        "first_use_title": "📝 First-time Use Note",
        "first_use_text": "When starting Streamlit for the first time, you may be asked for an email address to receive updates and feedback. This is a normal Streamlit feature. You can leave it blank and press Enter to skip, which won't affect the application's functionality.",
        "upload_label": "Upload Food Image",
        "analyze_button": "Analyze Food Calories",
        "please_upload": "Please upload a food image first",
        "saving_image": "Saving image...",
        "identifying_food": "AI is identifying the food, please wait...",
        "getting_nutrition": "Getting nutrition information...",
        "recognition_results": "Recognition Results",
        "food_label": "Food",
        "calories_label": "Calories",
        "calories_unit": "calories",
        "portion_label": "Suggested Portion",
        "data_source_label": "Data Source",
        "show_nutrition": "Show Nutrition Details",
        "hide_nutrition": "Hide Nutrition Details",
        "detailed_nutrition": "Detailed Nutrition Information",
        "no_nutrition_data": "No detailed nutrition information available",
        "no_calorie_info": "Food '{}' identified, but no calorie information found.",
        "error_identify": "Could not identify food in the image. Please try uploading a different image.",
        "error_processing": "Error processing image: {}",
        "api_unavailable": "API may be temporarily unavailable. Using demo mode with simulated data.",
        "error_saving": "Image saving failed. Please try again.",
        "error_invalid_image": "Please upload a valid JPG or PNG image file.",
        "how_to_use": "How to Use",
        "usage_steps": "1. Upload a clear food image on the left\n2. Click \"Analyze Food Calories\" button\n3. Wait for AI to identify the food and get calorie information\n4. View identification results and detailed nutrition information\n\nSupports JPG and PNG images. The app will try to get the most accurate calorie information from multiple data sources.",
        "search_history": "Search History",
        "no_history": "No history yet",
        "clear_history": "Clear History",
        "about": "About",
        "about_text": "The Food Calorie Estimator is a tool that uses AI technology to identify food and estimate calories.",
        "data_sources": "Data Sources:",
        "technology": "Technology:",
        "api_settings": "API Settings",
        "show_hide_api": "Show/Hide API Settings",
        "api_key": "API Key",
        "update_api_key": "Update API Key",
        "api_updated": "API key updated and saved!",
        "api_save_info": "API key will be saved to a local file and loaded automatically the next time you start the application.",
        "footer_text": "Food Calorie Estimator - Developed using HKBU GenAI Platform<br>© 2025 Food Calorie Estimator | Data Sources: USDA Food Composition Database, Nutritionix API",
        "language": "Language/语言",
        "switch_to_zh": "切换到中文",
        "food_number": "Food {}",
        "total_calories": "Total Calories",
        "combined_foods": "Combined Foods",
        "chart_title": "Chart",
        "portion_suggestion": "Suggested Portion",
        "portion_advice": "Healthy Portion Advice",
        "portion_explanation": "Balanced meal recommendations based on your food:",
        "tab_upload": "Upload Image",
        "tab_camera": "Use Camera",
        "camera_label": "Take a photo of your food",
        "camera_help": "Click on the camera to take a photo",
        "capture_button": "Capture and Analyze",
        "single_food_advice": "Nutritional Advice",
        "diet_advice": "Diet Recommendations",
        "open_camera": "Open Camera",
        "close_camera": "Close Camera",
        "camera_ready": "Camera is ready, take a photo of your food",
        "profile_setup": "Personal Profile",
        "profile_description": "Enter your details for personalized recommendations",
        "height_label": "Height (cm)",
        "weight_label": "Weight (kg)",
        "age_label": "Age",
        "gender_label": "Gender",
        "activity_label": "Activity Level",
        "save_profile": "Save Profile",
        "profile_saved": "Profile saved! Your recommendations will be personalized.",
        "activity_sedentary": "Sedentary (little or no exercise)",
        "activity_light": "Light (1-3 days/week)",
        "activity_moderate": "Moderate (3-5 days/week)",
        "activity_active": "Active (6-7 days/week)",
        "activity_very": "Very Active (physical job or 2x training)",
        "gender_male": "Male",
        "gender_female": "Female",
        "male": "Male",
        "female": "Female",
        "fitness_recommendations": "Fitness Recommendations",
        "diet_recommendations": "Diet Recommendations",
        "weekly_diet_plan": "Weekly Diet Plan",
        "weekly_workout_plan": "Weekly Workout Plan",
        "calorie_goal": "Calorie Goal",
        "weight_loss": "Weight Loss",
        "weight_gain": "Weight Gain",
        "weight_maintain": "Weight Maintenance",
        "fitness_plan": "Fitness Plan",
        "strength_training": "Strength Training",
        "cardio_training": "Cardio Training",
        "personal_recommendation": "Personal Recommendation",
        "daily_deficit": "Daily Deficit",
        "daily_surplus": "Daily Surplus",
        "protein_recommendation": "Protein Recommendation",
        "carbs_recommendation": "Carbs Recommendation",
        "fat_recommendation": "Fat Recommendation",
        "daily_target": "Daily Target",
        "meal_timing": "Meal Timing",
        "current_meal_calories": "This meal provides",
        "remaining_calories": "Remaining for today",
        "of_daily_needs": "of your daily needs",
        "workout_suggestion": "Workout Suggestion",
        "not_enough_data": "Please set up your profile for personalized recommendations",
        "breakfast": "Breakfast",
        "lunch": "Lunch",
        "dinner": "Dinner",
        "snacks": "Snacks",
        "day_plan": "Day Plan",
        "generate_plan": "Generate Personalized Plan",
        "plan_generated": "Your personalized plan has been generated!",
        "daily_macros": "Daily Macronutrients",
        "protein": "Protein",
        "carbs": "Carbohydrates",
        "fat": "Fat",
        "total": "Total",
        "workout_type": "Workout Type",
        "intensity": "Intensity",
        "duration": "Duration",
        "low": "Low",
        "moderate": "Moderate",
        "high": "High",
        "strength": "Strength",
        "cardio": "Cardio",
        "rest": "Rest/Recovery"
    },
    "zh": {
        "page_title": "食物热量估算器",
        "app_title": "🍔 食物热量估算器",
        "intro_text": "上传食物图片，利用AI技术快速识别食物并估算热量。支持JPG和PNG格式的图片，数据来源包括内置数据库和在线营养数据。",
        "first_use_title": "📝 首次使用提示",
        "first_use_text": "首次启动Streamlit时，可能会要求输入电子邮件地址用于接收更新和反馈。这是Streamlit的正常功能，您可以直接留空并按回车跳过，不会影响应用使用。",
        "upload_label": "上传食物图片",
        "analyze_button": "分析食物热量",
        "please_upload": "请先上传一张食物图片",
        "saving_image": "保存图像中...",
        "identifying_food": "AI正在识别食物中，请稍等...",
        "getting_nutrition": "正在获取营养信息...",
        "recognition_results": "识别结果",
        "food_label": "食物",
        "calories_label": "热量",
        "calories_unit": "卡路里",
        "portion_label": "建议份量",
        "data_source_label": "数据来源",
        "show_nutrition": "显示详细营养信息",
        "hide_nutrition": "隐藏详细营养信息",
        "detailed_nutrition": "详细营养成分",
        "no_nutrition_data": "没有详细的营养信息",
        "no_calorie_info": "已识别出食物 '{}'，但无法获取热量信息。",
        "error_identify": "无法识别图像中的食物，请尝试上传不同的图像。",
        "error_processing": "处理图像时出错: {}",
        "api_unavailable": "API可能暂时不可用，将使用模拟数据进行演示。",
        "error_saving": "图像保存失败，请重试。",
        "error_invalid_image": "请上传有效的JPG或PNG图像文件。",
        "how_to_use": "使用说明",
        "usage_steps": "1. 在左侧上传一张清晰的食物图片\n2. 点击\"分析食物热量\"按钮\n3. 等待AI识别食物并获取热量信息\n4. 查看识别结果和详细的营养成分\n\n支持JPG和PNG格式的图片，会尝试从多个数据源获取最准确的热量信息。",
        "search_history": "搜索历史",
        "no_history": "暂无历史记录",
        "clear_history": "清空历史记录",
        "about": "关于",
        "about_text": "食物热量估算器是一个使用AI技术识别食物并估算热量的工具。",
        "data_sources": "数据来源:",
        "technology": "技术实现:",
        "api_settings": "API设置",
        "show_hide_api": "显示/隐藏API设置",
        "api_key": "API密钥",
        "update_api_key": "更新API密钥",
        "api_updated": "API密钥已更新并保存!",
        "api_save_info": "API密钥将保存到本地文件，下次启动应用时将自动加载。",
        "footer_text": "食物热量估算器 - 使用HKBU GenAI平台开发<br>© 2025 食物热量估算器 | 数据来源: USDA食品成分数据库、Nutritionix API",
        "language": "Language/语言",
        "switch_to_en": "Switch to English",
        "food_number": "食物 {}",
        "total_calories": "总热量",
        "combined_foods": "组合食物",
        "chart_title": "图表",
        "portion_suggestion": "建议份量",
        "portion_advice": "健康份量建议",
        "portion_explanation": "基于您的食物的均衡饮食建议：",
        "tab_upload": "上传图片",
        "tab_camera": "使用摄像头",
        "camera_label": "拍摄您的食物照片",
        "camera_help": "点击摄像头拍照",
        "capture_button": "拍照并分析",
        "single_food_advice": "营养建议",
        "diet_advice": "饮食推荐",
        "open_camera": "打开摄像头",
        "close_camera": "关闭摄像头",
        "camera_ready": "摄像头已准备就绪，请拍摄您的食物",
        "profile_setup": "个人资料",
        "profile_description": "输入您的详细信息以获取个性化建议",
        "height_label": "身高 (厘米)",
        "weight_label": "体重 (公斤)",
        "age_label": "年龄",
        "gender_label": "性别",
        "activity_label": "活动水平",
        "save_profile": "保存资料",
        "profile_saved": "资料已保存！您将获得个性化建议。",
        "activity_sedentary": "久坐 (几乎不运动)",
        "activity_light": "轻度活动 (每周1-3天)",
        "activity_moderate": "中度活动 (每周3-5天)",
        "activity_active": "活跃 (每周6-7天)",
        "activity_very": "非常活跃 (体力工作或高强度训练)",
        "gender_male": "男性",
        "gender_female": "女性",
        "male": "男性",
        "female": "女性",
        "fitness_recommendations": "健身建议",
        "diet_recommendations": "饮食建议",
        "weekly_diet_plan": "一周饮食计划",
        "weekly_workout_plan": "一周锻炼计划",
        "calorie_goal": "卡路里目标",
        "weight_loss": "减重",
        "weight_gain": "增重",
        "weight_maintain": "保持体重",
        "fitness_plan": "健身计划",
        "strength_training": "力量训练",
        "cardio_training": "有氧训练",
        "personal_recommendation": "个人建议",
        "daily_deficit": "每日赤字",
        "daily_surplus": "每日盈余",
        "protein_recommendation": "蛋白质建议",
        "carbs_recommendation": "碳水化合物建议",
        "fat_recommendation": "脂肪建议",
        "daily_target": "每日目标",
        "meal_timing": "餐食时间",
        "current_meal_calories": "这餐提供",
        "remaining_calories": "今天剩余",
        "of_daily_needs": "满足每日需求的",
        "workout_suggestion": "锻炼建议",
        "not_enough_data": "请设置您的个人资料以获得个性化建议",
        "breakfast": "早餐",
        "lunch": "午餐",
        "dinner": "晚餐",
        "snacks": "零食",
        "day_plan": "每日计划",
        "generate_plan": "生成个性化计划",
        "plan_generated": "您的个性化计划已生成！",
        "daily_macros": "每日宏量营养素",
        "protein": "蛋白质",
        "carbs": "碳水化合物",
        "fat": "脂肪",
        "total": "总计",
        "workout_type": "锻炼类型",
        "intensity": "强度",
        "duration": "时长",
        "low": "低",
        "moderate": "中",
        "high": "高",
        "strength": "力量",
        "cardio": "有氧",
        "rest": "休息/恢复"
    }
}

# Set page configuration
st.set_page_config(
    page_title="Food Calorie Estimator",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        color: #FF5722;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #FF7043;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .result-container {
        background-color: #FFF3E0;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #FF9800;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .food-name {
        font-size: 2rem;
        color: #E65100;
        margin-bottom: 0.8rem;
        font-weight: 700;
    }
    
    .calories {
        font-size: 1.6rem;
        color: #FF5722;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }
    
    .portion {
        font-size: 1.3rem;
        color: #795548;
        font-style: italic;
        margin-bottom: 0.5rem;
    }
    
    .nutrient-title {
        font-size: 1.4rem;
        color: #E65100;
        margin: 1rem 0 0.5rem 0;
        font-weight: 500;
    }
    
    .source-info {
        font-size: 0.9rem;
        color: #8D6E63;
        margin-top: 1rem;
        text-align: right;
        font-style: italic;
    }
    
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-top: 5px solid #FF9800;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        color: #8D6E63;
        font-size: 0.9rem;
        border-top: 1px solid #E0E0E0;
    }
    
    .stButton>button {
        background-color: #FF9800;
        color: white;
        font-weight: 500;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        border: none;
        transition: background-color 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background-color: #F57C00;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* 语言切换按钮样式 */
    [data-testid="stButton"] button[kind="secondary"] {
        background-color: #FF9800;
        color: white;
        font-weight: 500;
        border-radius: 50px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    [data-testid="stButton"] button[kind="secondary"]:hover {
        background-color: #F57C00;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    div[data-testid="stFileUploader"] {
        padding: 2rem;
        border: 2px dashed #FFCC80;
        border-radius: 15px;
        background-color: #FFF8E1;
    }
    
    div[data-testid="stSidebar"] {
        background-color: #FFF8E1;
        border-right: 1px solid #FFE0B2;
    }
    
    .history-item {
        padding: 15px;
        margin-bottom: 15px;
        background-color: #FFF3E0;
        border-radius: 10px;
        border-left: 3px solid #FF9800;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .history-food {
        font-weight: 600;
        color: #E65100;
    }
    
    .history-calories {
        color: #FF5722;
    }
    
    .history-time {
        font-size: 0.8rem;
        color: #8D6E63;
        font-style: italic;
    }
    
    .note-box {
        background-color: #FFE0B2;
        border-left: 4px solid #E65100;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .note-title {
        font-weight: 700;
        color: #E65100;
        margin-bottom: 5px;
        font-size: 1.1rem;
    }
    
    .note-box p {
        color: #5D4037;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Style for tables */
    div[data-testid="stTable"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Style for dataframes */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'api_key' not in st.session_state:
        # 尝试从本地文件读取API key，如果没有则使用默认值
        try:
            api_key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'api_key.txt')
            if os.path.exists(api_key_file):
                with open(api_key_file, 'r') as f:
                    st.session_state.api_key = f.read().strip()
            else:
                st.session_state.api_key = "333cac1b-8367-480e-b2e7-8fa06024dd14"  # 新的默认API key
        except Exception:
            st.session_state.api_key = "333cac1b-8367-480e-b2e7-8fa06024dd14"  # 如果出现任何问题，使用默认值
    if 'image_path' not in st.session_state:
        st.session_state.image_path = None
    if 'food_names' not in st.session_state:
        st.session_state.food_names = None
    if 'calories_info_list' not in st.session_state:
        st.session_state.calories_info_list = None
    if 'data_sources' not in st.session_state:
        st.session_state.data_sources = None
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'show_nutrition_details' not in st.session_state:
        st.session_state.show_nutrition_details = False
    if 'streamlit_note_shown' not in st.session_state:
        st.session_state.streamlit_note_shown = False
    if 'api_settings_expanded' not in st.session_state:
        st.session_state.api_settings_expanded = False
    if 'language' not in st.session_state:
        st.session_state.language = "en"  # Default language is English
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False  # 默认不启用调试模式
    if 'camera_on' not in st.session_state:
        st.session_state.camera_on = False  # 默认摄像头关闭
    # 添加用户身体信息相关的session state
    if 'user_height' not in st.session_state:
        st.session_state.user_height = None
    if 'user_weight' not in st.session_state:
        st.session_state.user_weight = None
    if 'user_age' not in st.session_state:
        st.session_state.user_age = None
    if 'user_gender' not in st.session_state:
        st.session_state.user_gender = None
    if 'user_activity' not in st.session_state:
        st.session_state.user_activity = None
    if 'profile_setup' not in st.session_state:
        st.session_state.profile_setup = False

def toggle_language():
    """Toggle between English and Chinese"""
    if st.session_state.language == "en":
        st.session_state.language = "zh"
    else:
        st.session_state.language = "en"
    # Force page refresh
    st.rerun()

def get_text(key, default=None):
    """Get text based on current language"""
    if default is None:
        return TRANSLATIONS[st.session_state.language].get(key, key)
    else:
        return TRANSLATIONS[st.session_state.language].get(key, default)

def display_header():
    """Display application title and introduction"""
    # Add language selector in a more direct way
    lang_col1, lang_col2, lang_col3 = st.columns([1, 6, 3])
    with lang_col3:
        lang_button_text = get_text('switch_to_zh' if st.session_state.language == 'en' else 'switch_to_en')
        st.button(
            lang_button_text, 
            key="language_toggle_button", 
            on_click=toggle_language,
            use_container_width=True,
            type="primary"
        )
    
    st.markdown(f'<div class="main-header">{get_text("app_title")}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            {get_text("intro_text")}
        </div>
        """, unsafe_allow_html=True)
        
        # Display first-use note
        if not st.session_state.get("streamlit_note_shown", False):
            st.markdown(f"""
            <div class="note-box">
                <div class="note-title">{get_text("first_use_title")}</div>
                <p>{get_text("first_use_text")}</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.streamlit_note_shown = True

def update_api_key():
    """Update API key and save to file"""
    # 更新会话状态中的API key
    st.session_state.api_key = st.session_state.new_api_key
    
    # 保存API key到文件，以便下次启动时使用
    try:
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        api_key_file = os.path.join(config_dir, 'api_key.txt')
        with open(api_key_file, 'w') as f:
            f.write(st.session_state.api_key)
        
        st.success(get_text("api_updated"))
    except Exception as e:
        error_msg = str(e)
        st.error(f"无法保存API密钥: {error_msg}" if st.session_state.language == "zh" else f"Unable to save API key: {error_msg}")

def toggle_api_settings():
    """Toggle API settings display state"""
    st.session_state.api_settings_expanded = not st.session_state.api_settings_expanded

def toggle_debug_mode():
    """Toggle debug mode"""
    st.session_state.debug_mode = not st.session_state.debug_mode

def toggle_camera():
    """切换摄像头开关状态"""
    st.session_state.camera_on = not st.session_state.camera_on

def process_image(uploaded_file):
    """Process uploaded image and identify food"""
    st.session_state.food_names = None  # 使用复数形式表示可能有多个食物
    st.session_state.calories_info_list = None  # 存储多个食物的营养信息列表
    st.session_state.data_sources = None  # 存储多个食物的数据来源
    st.session_state.error_message = None
    st.session_state.show_nutrition_details = False  # 重置这个变量，确保每次处理新图片时都折叠营养信息
    
    if uploaded_file is not None:
        if is_valid_image(uploaded_file):
            with st.spinner(get_text("saving_image")):
                image_path = save_uploaded_image(uploaded_file)
            
            if image_path:
                # 处理图片并识别食物
                process_image_path(image_path, uploaded_file.name)
            else:
                st.session_state.error_message = get_text("error_saving")
                st.error(st.session_state.error_message)
        else:
            st.session_state.error_message = get_text("error_invalid_image")
            st.error(st.session_state.error_message)

def process_image_path(image_path, file_name=None):
    """处理图片路径并识别食物"""
    st.session_state.image_path = image_path
    
    # 显示上传的图片
    if file_name:
        st.image(Image.open(image_path), caption=f"{file_name}", use_column_width=True)
    else:
        st.image(Image.open(image_path), caption="Captured photo", use_column_width=True)
    
    with st.spinner(get_text("identifying_food")):
        try:
            # 显示调试信息
            if st.session_state.debug_mode:
                st.write(f"图片已保存至: {image_path}")
            
            # 创建GenAI客户端
            client = GenAIClient(st.session_state.api_key)
            if st.session_state.debug_mode:
                st.write("API客户端已创建，开始识别食物...")
            
            # 识别食物
            food_names = client.identify_food_in_image(image_path)
            
            # 处理多个食物的情况
            if isinstance(food_names, list):
                st.session_state.food_names = food_names
                if st.session_state.debug_mode:
                    st.write(f"识别到多种食物: {', '.join(food_names)}")
            else:
                st.session_state.food_names = [food_names]
                if st.session_state.debug_mode:
                    st.write(f"识别到食物: {food_names}")
            
            # 存储每种食物的营养信息和数据来源
            st.session_state.calories_info_list = []
            st.session_state.data_sources = []
            
            # 为每种食物获取营养信息
            for food_name in st.session_state.food_names:
                if st.session_state.debug_mode:
                    st.write(f"开始获取 '{food_name}' 的营养信息...")
                
                with st.spinner(get_text("getting_nutrition")):
                    # First try to get information from online sources
                    online_data, source = client.get_online_food_calories(food_name)
                    
                    if online_data:
                        st.session_state.calories_info_list.append(online_data)
                        st.session_state.data_sources.append(source)
                        if st.session_state.debug_mode:
                            st.write(f"从 {source} 获取到数据")
                    else:
                        # If online data is not available, use local database
                        if st.session_state.debug_mode:
                            st.write("在线数据获取失败，尝试使用本地数据库...")
                        local_data = get_food_calories(food_name)
                        if local_data:
                            st.session_state.calories_info_list.append(local_data)
                            st.session_state.data_sources.append("Built-in Database" if st.session_state.language == "en" else "内置数据库")
                            if st.session_state.debug_mode:
                                st.write("使用内置数据库的数据")
                        else:
                            # Use online service to generate estimated values
                            if st.session_state.debug_mode:
                                st.write("本地数据库中未找到，尝试生成估计值...")
                            estimated_data = client.fetch_nutrition_data_from_nutritionix(food_name)
                            if estimated_data:
                                st.session_state.calories_info_list.append(estimated_data)
                                st.session_state.data_sources.append("Estimated (Nutritionix API)" if st.session_state.language == "en" else "估计值 (Nutritionix API)")
                                if st.session_state.debug_mode:
                                    st.write("使用估计值")
                            
                    # Record history for each food
                    if st.session_state.calories_info_list and len(st.session_state.calories_info_list) > 0:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        calories = st.session_state.calories_info_list[-1].get("calories", 0)
                        source = st.session_state.data_sources[-1] if st.session_state.data_sources else "Unknown"
                        
                        st.session_state.history.append({
                            "food_name": food_name,
                            "calories": calories,
                            "timestamp": timestamp,
                            "source": source
                        })
                        
                        # Keep at most 10 history records
                        if len(st.session_state.history) > 10:
                            st.session_state.history = st.session_state.history[-10:]
                
        except Exception as e:
            st.session_state.error_message = get_text("error_processing").format(str(e))
            st.error(st.session_state.error_message)
            st.info(get_text("api_unavailable"))
            
            # 显示详细错误信息
            if st.session_state.debug_mode:
                st.write(f"详细错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc(), language="python")
            
            # Use default value for demo
            food_name = "hamburger"
            st.session_state.food_names = [food_name]
            if st.session_state.debug_mode:
                st.write(f"使用默认食物: {food_name}")
            
            # Use local data
            local_data = get_food_calories(food_name)
            if local_data:
                st.session_state.calories_info_list = [local_data]
                st.session_state.data_sources = ["Built-in Database (Demo Mode)" if st.session_state.language == "en" else "内置数据库 (演示模式)"]
                
                # 使用时间戳确保唯一ID
                import time
                st.session_state.food_names = [f"{food_name}_{int(time.time() * 1000)}"]

def toggle_nutrition_details():
    """Toggle nutrition details display"""
    st.session_state.show_nutrition_details = not st.session_state.show_nutrition_details

def display_nutrition_details(calories_info):
    """Display detailed nutrition information"""
    if calories_info and "details" in calories_info and calories_info["details"].get("nutrients"):
        nutrients = calories_info["details"]["nutrients"]
        
        # If it's USDA data, format will be different
        if isinstance(nutrients, list) and len(nutrients) > 0 and "name" in nutrients[0]:
            # Nutritionix format data
            df = pd.DataFrame([
                {"Nutrient": item["name"], "Value": item["value"], "Unit": item["unit"]}
                for item in nutrients
            ])
            st.dataframe(df, use_container_width=True)
            
        elif isinstance(nutrients, list) and len(nutrients) > 0 and "nutrientName" in nutrients[0]:
            # USDA format data
            df = pd.DataFrame([
                {"Nutrient": item.get("nutrientName", ""), "Value": item.get("value", 0), "Unit": item.get("unitName", "")}
                for item in nutrients if item.get("value") is not None
            ])
            st.dataframe(df, use_container_width=True)
        
        else:
            st.write(get_text("no_nutrition_data"))
    else:
        st.write(get_text("no_nutrition_data"))

def display_nutrient_chart(calories_info):
    """Display nutrition component chart"""
    if calories_info and "details" in calories_info and calories_info["details"].get("nutrients"):
        nutrients = calories_info["details"]["nutrients"]
        
        # Prepare data
        if isinstance(nutrients, list) and len(nutrients) > 0:
            if "name" in nutrients[0]:  # Nutritionix format
                # Translate nutrient names if Chinese
                protein_name = "Protein" if st.session_state.language == "en" else "蛋白质"
                fat_name = "Fat" if st.session_state.language == "en" else "脂肪"
                carbs_name = "Carbohydrates" if st.session_state.language == "en" else "碳水化合物"
                
                # Map English names to possible translations
                nutrient_map = {
                    "Protein": protein_name, 
                    "Fat": fat_name, 
                    "Carbohydrates": carbs_name
                }
                
                # Find relevant nutrients
                macro_nutrients = []
                for n in nutrients:
                    for eng_name, display_name in nutrient_map.items():
                        if n["name"].lower() == eng_name.lower():
                            n_copy = n.copy()
                            n_copy["display_name"] = display_name
                            macro_nutrients.append(n_copy)
                
                if macro_nutrients:
                    try:
                        # 准备图表数据
                        import pandas as pd
                        import plotly.express as px
                        
                        # 准备饼图数据
                        pie_data = pd.DataFrame({
                            "Nutrient": [n["display_name"] for n in macro_nutrients],
                            "Amount": [n["value"] for n in macro_nutrients]
                        })
                        
                        # 创建饼图
                        fig = px.pie(
                            pie_data,
                            values="Amount",
                            names="Nutrient",
                            color="Nutrient",
                            color_discrete_map={
                                protein_name: "#66BB6A",
                                fat_name: "#FFA726",
                                carbs_name: "#42A5F5"
                            },
                            hole=0.4
                        )
                        
                        title = "Macronutrient Distribution" if st.session_state.language == "en" else "宏量营养素分布"
                        fig.update_layout(
                            title=title,
                            height=400,
                            margin=dict(l=20, r=20, t=40, b=20),
                        )
                        
                        st.plotly_chart(fig, use_column_width=True, config={"staticPlot": False, "displayModeBar": False})
                        
                        # Display energy source percentages
                        title = "Energy Source Percentages" if st.session_state.language == "en" else "能量来源占比"
                        st.markdown(f'<div class="nutrient-title">{title}</div>', unsafe_allow_html=True)
                        
                        # Calculate energy contribution from each macronutrient
                        protein_value = next((n["value"] for n in macro_nutrients if "Protein" in n["name"]), 0)
                        fat_value = next((n["value"] for n in macro_nutrients if "Fat" in n["name"]), 0)
                        carb_value = next((n["value"] for n in macro_nutrients if "Carbohydrates" in n["name"]), 0)
                        
                        protein_cals = protein_value * 4
                        fat_cals = fat_value * 9
                        carb_cals = carb_value * 4
                        
                        total_cals = protein_cals + fat_cals + carb_cals
                        if total_cals > 0:
                            # Create horizontal bar chart
                            energy_data = pd.DataFrame({
                                "Nutrient": [n["display_name"] for n in macro_nutrients],
                                "Calories": [protein_cals, fat_cals, carb_cals],
                                "Percentage": [protein_cals/total_cals*100, fat_cals/total_cals*100, carb_cals/total_cals*100]
                            })
                            
                            fig = px.bar(
                                energy_data, 
                                y="Nutrient", 
                                x="Percentage", 
                                color="Nutrient",
                                color_discrete_map={
                                    protein_name: "#66BB6A",
                                    fat_name: "#FFA726",
                                    carbs_name: "#42A5F5"
                                },
                                text=[f"{x:.1f}%" for x in energy_data["Percentage"]]
                            )
                            
                            x_title = "Percentage of Total Calories" if st.session_state.language == "en" else "占总热量百分比"
                            fig.update_layout(
                                height=250,
                                margin=dict(l=20, r=20, t=20, b=20),
                                xaxis_title=x_title,
                                yaxis_title="",
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig, use_column_width=True, config={"staticPlot": False, "displayModeBar": False})
                    except Exception as e:
                        st.error(f"Error displaying chart: {str(e)}")
                        if st.session_state.debug_mode:
                            import traceback
                            st.code(traceback.format_exc(), language="python")

def display_multiple_results(food_names, calories_info_list, data_sources):
    """Display multiple food recognition and calorie estimation results"""
    st.markdown(f'<div class="sub-header">{get_text("recognition_results")}</div>', unsafe_allow_html=True)
    
    # 计算总卡路里
    total_calories = 0
    
    # 用于汇总营养成分的变量
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    
    # 显示每种食物的信息
    for i, (food_name, calories_info, data_source) in enumerate(zip(food_names, calories_info_list, data_sources)):
        if calories_info:
            total_calories += calories_info.get("calories", 0)
            
            # 提取该食物的营养成分
            if "details" in calories_info and calories_info["details"].get("nutrients"):
                nutrients = calories_info["details"]["nutrients"]
                if isinstance(nutrients, list) and len(nutrients) > 0:
                    # 处理不同格式的营养数据
                    if "name" in nutrients[0]:  # Nutritionix格式
                        for nutrient in nutrients:
                            name = nutrient["name"].lower()
                            if "protein" in name:
                                total_protein += nutrient.get("value", 0)
                            elif "fat" in name:
                                total_fat += nutrient.get("value", 0)
                            elif "carbohydrate" in name or "carbs" in name:
                                total_carbs += nutrient.get("value", 0)
                    elif "nutrientName" in nutrients[0]:  # USDA格式
                        for nutrient in nutrients:
                            name = nutrient.get("nutrientName", "").lower()
                            if "protein" in name:
                                total_protein += nutrient.get("value", 0)
                            elif "fat" in name and "total" in name:
                                total_fat += nutrient.get("value", 0)
                            elif "carbohydrate" in name:
                                total_carbs += nutrient.get("value", 0)
            
            if len(food_names) > 1:
                # 多种食物时显示序号
                food_number = i + 1
                food_number_text = get_text("food_number").format(food_number)
                st.markdown(f'<h3>{food_number_text}: {food_name}</h3>', unsafe_allow_html=True)
            
            # 获取这种食物的份量建议
            portion_suggestion = get_portion_suggestion(food_name)
            portion_text = portion_suggestion["en"] if st.session_state.language == "en" else portion_suggestion["zh"]
            
            st.markdown(f"""
            <div class="result-container">
                <div class="food-name">{get_text("food_label")}: {food_name}</div>
                <div class="calories">{get_text("calories_label")}: {calories_info["calories"]} {get_text("calories_unit")}</div>
                <div class="portion">{get_text("portion_label")}: {calories_info.get("portion", "Standard Portion")}</div>
                <div class="portion" style="color: #2E7D32; font-weight: bold;">{get_text("portion_suggestion")}: {portion_text}</div>
                <div class="source-info">{get_text("data_source_label")}: {data_source}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add button to show detailed nutrition information
            if "details" in calories_info and calories_info["details"].get("nutrients"):
                nutrition_btn_text = get_text("show_nutrition")
                # 使用食物名和索引创建稳定的key，而不是使用时间戳
                btn_key = f"nutrition_details_button_{food_name}_{i}"
                
                # 设置session state变量，但不直接在按钮事件中修改
                details_key = f"show_details_{food_name}_{i}"
                if details_key not in st.session_state:
                    st.session_state[details_key] = False
                
                # 使用按钮点击来触发状态改变
                if st.button(nutrition_btn_text, key=btn_key):
                    # 改变session_state变量，而不是按钮本身
                    st.session_state[details_key] = not st.session_state[details_key]
                
                # 根据session_state变量来显示或隐藏内容
                if st.session_state[details_key]:
                    # 展示营养成分详情
                    st.markdown(f'<div class="nutrient-title">{get_text("detailed_nutrition")}</div>', unsafe_allow_html=True)
                    
                    # Create two-column layout
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        display_nutrition_details(calories_info)
                    
                    with col2:
                        display_nutrient_chart(calories_info)
        else:
            st.warning(get_text("no_calorie_info").format(food_name))
    
    # 单个食物的情况下也显示饮食建议
    if len(food_names) == 1 and calories_info_list and calories_info_list[0]:
        # 单个食物的建议
        st.markdown(f'<h3 style="margin-top: 20px; color: #2E7D32;">{get_text("single_food_advice")}</h3>', unsafe_allow_html=True)
        
        # 获取特定食物的建议
        food_name = food_names[0]
        food_suggestions = {}
        
        # 根据食物类型提供特定建议
        food_name_lower = food_name.lower()
        if any(protein in food_name_lower for protein in ["chicken", "beef", "pork", "fish", "meat", "鸡", "牛", "猪", "肉", "鱼"]):
            food_suggestions["en"] = ["Pair this protein with whole grains and vegetables for a balanced meal.", 
                                     "Try to limit processed meats and opt for lean cuts when possible."]
            food_suggestions["zh"] = ["将这种蛋白质与全谷物和蔬菜搭配，形成均衡饮食。", 
                                     "尽量限制加工肉类，尽可能选择瘦肉。"]
        elif any(veg in food_name_lower for veg in ["vegetable", "veggie", "broccoli", "spinach", "carrot", "蔬菜", "西兰花", "菠菜", "胡萝卜"]):
            food_suggestions["en"] = ["Great choice! Vegetables are high in fiber, vitamins and minerals.", 
                                     "Try to include a variety of colorful vegetables in your diet."]
            food_suggestions["zh"] = ["很好的选择！蔬菜富含纤维、维生素和矿物质。", 
                                     "尝试在饮食中包含各种颜色的蔬菜。"]
        elif any(fruit in food_name_lower for fruit in ["fruit", "apple", "banana", "orange", "水果", "苹果", "香蕉", "橙子"]):
            food_suggestions["en"] = ["Fruits are a great source of vitamins and natural sugars.", 
                                     "Try to eat the whole fruit rather than just drinking fruit juice to get more fiber."]
            food_suggestions["zh"] = ["水果是维生素和天然糖分的良好来源。", 
                                     "尝试食用整个水果而不是仅喝果汁，以获取更多纤维。"]
        elif any(grain in food_name_lower for grain in ["rice", "bread", "pasta", "noodle", "米饭", "面包", "意面", "面条"]):
            food_suggestions["en"] = ["Choose whole grains when possible for more fiber and nutrients.", 
                                     "Balance your carbohydrates with protein and vegetables."]
            food_suggestions["zh"] = ["尽可能选择全谷物，获取更多纤维和营养。", 
                                     "将碳水化合物与蛋白质和蔬菜平衡搭配。"]
        elif any(ff in food_name_lower for ff in ["burger", "pizza", "fries", "hamburger", "汉堡", "披萨", "薯条"]):
            food_suggestions["en"] = ["Fast foods are typically high in calories, fat and sodium.", 
                                     "Try to limit these foods and balance with healthier options when possible."]
            food_suggestions["zh"] = ["快餐通常热量高、脂肪高、钠含量高。", 
                                     "尽量限制这些食物，尽可能与更健康的选择平衡。"]
        elif any(dessert in food_name_lower for dessert in ["ice cream", "cake", "cookie", "chocolate", "冰淇淋", "蛋糕", "饼干", "巧克力"]):
            food_suggestions["en"] = ["Sweets are high in sugar and should be enjoyed in moderation.", 
                                     "Consider fruit-based desserts for a healthier alternative."]
            food_suggestions["zh"] = ["甜食糖分高，应适量享用。", 
                                     "考虑以水果为基础的甜点作为更健康的替代品。"]
        else:
            # 通用建议
            food_suggestions = get_meal_balance_suggestion([food_name])
        
        # 显示建议
        suggestions = food_suggestions["en"] if st.session_state.language == "en" else food_suggestions["zh"]
        for suggestion in suggestions:
            st.markdown(f'<div style="padding: 10px; background-color: #F1F8E9; border-radius: 8px; margin: 8px 0; border-left: 4px solid #7CB342;"><p style="margin: 0; color: #33691E;">{suggestion}</p></div>', unsafe_allow_html=True)

    # 如果有多种食物，显示总卡路里和营养成分汇总
    if len(food_names) > 1 and total_calories > 0:
        # 添加翻译项
        total_nutrition = "Total Nutrition Information" if st.session_state.language == "en" else "总营养信息"
        protein_label = "Protein" if st.session_state.language == "en" else "蛋白质"
        fat_label = "Fat" if st.session_state.language == "en" else "脂肪"
        carbs_label = "Carbohydrates" if st.session_state.language == "en" else "碳水化合物"
        g_unit = "g" if st.session_state.language == "en" else "克"
        from_foods = "from Foods" if st.session_state.language == "en" else "来源食物"

        # 使用单独的markdown语句分别渲染各部分HTML，而不是一个大的HTML块
        st.markdown(f'<div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; margin-top: 20px; border: 2px solid #FFB74D;">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="text-align: center; color: #E65100;">{get_text("total_calories")}: {total_calories} {get_text("calories_unit")}</h2>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="margin-top: 15px; color: #FF7043;">{total_nutrition}</h3>', unsafe_allow_html=True)
        
        # 创建三列显示营养成分
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background-color: #E8F5E9; border-radius: 8px; margin: 0 5px; border: 1px solid #2E7D32;">
                <div style="font-weight: bold; color: #2E7D32; font-size: 1.2rem;">{protein_label}</div>
                <div style="font-size: 1.5rem; margin: 5px 0; color: #000000; font-weight: bold;">{round(total_protein, 1)} {g_unit}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background-color: #FFF3E0; border-radius: 8px; margin: 0 5px; border: 1px solid #EF6C00;">
                <div style="font-weight: bold; color: #EF6C00; font-size: 1.2rem;">{fat_label}</div>
                <div style="font-size: 1.5rem; margin: 5px 0; color: #000000; font-weight: bold;">{round(total_fat, 1)} {g_unit}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background-color: #E3F2FD; border-radius: 8px; margin: 0 5px; border: 1px solid #1565C0;">
                <div style="font-weight: bold; color: #1565C0; font-size: 1.2rem;">{carbs_label}</div>
                <div style="font-size: 1.5rem; margin: 5px 0; color: #000000; font-weight: bold;">{round(total_carbs, 1)} {g_unit}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f'<p style="font-style: italic; color: #795548; text-align: center; margin-top: 10px; font-size: 1.1rem;">{from_foods}: {", ".join(food_names)}</p>', unsafe_allow_html=True)
        
        # 添加健康饮食建议
        meal_suggestions = get_meal_balance_suggestion(food_names)
        suggestions = meal_suggestions["en"] if st.session_state.language == "en" else meal_suggestions["zh"]
        
        if suggestions:
            st.markdown(f'<h3 style="margin-top: 15px; color: #2E7D32;">{get_text("portion_advice")}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #455A64;">{get_text("portion_explanation")}</p>', unsafe_allow_html=True)
            
            for suggestion in suggestions:
                st.markdown(f'<div style="padding: 10px; background-color: #F1F8E9; border-radius: 8px; margin: 8px 0; border-left: 4px solid #7CB342;"><p style="margin: 0; color: #33691E;">{suggestion}</p></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 只有当存在显著的营养成分时才显示图表
        if total_protein > 0.1 or total_fat > 0.1 or total_carbs > 0.1:
            chart_title = "Macronutrient Distribution" if st.session_state.language == "en" else "宏量营养素分布"
            st.markdown(f"<h3 style='margin-top: 20px; color: #FF7043;'>{chart_title}</h3>", unsafe_allow_html=True)
            
            try:
                # 使用html表格替代图表
                st.markdown(f"""
                <div style="margin: 20px 0; border: 1px solid #E0E0E0; border-radius: 10px; overflow: hidden;">
                    <table style="width: 100%; border-collapse: collapse; text-align: center;">
                        <tr style="background-color: #F5F5F5;">
                            <th style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{get_text("food_label")}</th>
                            <th style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{g_unit}</th>
                            <th style="padding: 10px; border-bottom: 1px solid #E0E0E0;">%</th>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #E0E0E0; font-weight: bold; color: #2E7D32;">{protein_label}</td>
                            <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(total_protein, 1)}</td>
                            <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(100 * total_protein / (total_protein + total_fat + total_carbs), 1)}%</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #E0E0E0; font-weight: bold; color: #EF6C00;">{fat_label}</td>
                            <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(total_fat, 1)}</td>
                            <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(100 * total_fat / (total_protein + total_fat + total_carbs), 1)}%</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: bold; color: #1565C0;">{carbs_label}</td>
                            <td style="padding: 10px;">{round(total_carbs, 1)}</td>
                            <td style="padding: 10px;">{round(100 * total_carbs / (total_protein + total_fat + total_carbs), 1)}%</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                # 能量来源计算
                protein_cals = total_protein * 4
                fat_cals = total_fat * 9
                carb_cals = total_carbs * 4
                total_cals = protein_cals + fat_cals + carb_cals
                
                energy_title = "Energy Source Percentages" if st.session_state.language == "en" else "能量来源占比"
                st.markdown(f'<h3 style="margin-top: 20px; color: #FF7043;">{energy_title}</h3>', unsafe_allow_html=True)
                
                # 使用HTML表格显示能量分布
                if total_cals > 0:
                    st.markdown(f"""
                    <div style="margin: 20px 0; border: 1px solid #E0E0E0; border-radius: 10px; overflow: hidden;">
                        <table style="width: 100%; border-collapse: collapse; text-align: center;">
                            <tr style="background-color: #F5F5F5;">
                                <th style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{get_text("food_label")}</th>
                                <th style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{get_text("calories_unit")}</th>
                                <th style="padding: 10px; border-bottom: 1px solid #E0E0E0;">%</th>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #E0E0E0; font-weight: bold; color: #2E7D32;">{protein_label}</td>
                                <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(protein_cals, 1)}</td>
                                <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(100 * protein_cals / total_cals, 1)}%</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #E0E0E0; font-weight: bold; color: #EF6C00;">{fat_label}</td>
                                <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(fat_cals, 1)}</td>
                                <td style="padding: 10px; border-bottom: 1px solid #E0E0E0;">{round(100 * fat_cals / total_cals, 1)}%</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; font-weight: bold; color: #1565C0;">{carbs_label}</td>
                                <td style="padding: 10px;">{round(carb_cals, 1)}</td>
                                <td style="padding: 10px;">{round(100 * carb_cals / total_cals, 1)}%</td>
                            </tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error displaying nutrition data: {str(e)}")
                if st.session_state.debug_mode:
                    import traceback
                    st.code(traceback.format_exc(), language="python")
    
    # 添加个性化饮食和健身建议部分 - 只有当用户已经设置了个人资料时显示
    if st.session_state.profile_setup:
        # 准备用户数据
        user_profile = {
            "height": st.session_state.user_height,
            "weight": st.session_state.user_weight,
            "age": st.session_state.user_age,
            "gender": st.session_state.user_gender,
            "activity": st.session_state.user_activity,
            "bmi": calculate_bmi(st.session_state.user_height, st.session_state.user_weight)
        }
        
        daily_calories = calculate_daily_calories(
            st.session_state.user_height,
            st.session_state.user_weight,
            st.session_state.user_age,
            st.session_state.user_gender,
            st.session_state.user_activity
        )
        
        # 确定用户目标 (根据BMI简单判断)
        bmi = user_profile["bmi"]
        if bmi < 18.5:
            goal = "gain"  # 体重不足，需要增重
        elif bmi > 25:
            goal = "lose"  # 超重，需要减重
        else:
            goal = "maintain"  # 正常体重，保持即可
        
        # 显示个性化建议卡片
        st.markdown(f"""
        <div style="background-color: #EDE7F6; padding: 20px; border-radius: 10px; margin-top: 30px; border: 2px solid #7E57C2;">
            <h2 style="text-align: center; color: #512DA8;">{get_text('personal_recommendation')}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 创建选项卡为健身和饮食建议
        fitness_tab, diet_tab, weekly_diet_tab, weekly_workout_tab = st.tabs([
            get_text('fitness_recommendations'), 
            get_text('diet_recommendations'),
            get_text('weekly_diet_plan'),
            get_text('weekly_workout_plan')
        ])
        
        with fitness_tab:
            # 获取健身建议
            fitness_recs = get_fitness_recommendations(
                user_profile["gender"],
                user_profile["age"],
                user_profile["bmi"],
                user_profile["activity"]
            )
            
            strength_recs = fitness_recs["strength"]["en"] if st.session_state.language == "en" else fitness_recs["strength"]["zh"]
            cardio_recs = fitness_recs["cardio"]["en"] if st.session_state.language == "en" else fitness_recs["cardio"]["zh"]
            
            # 显示力量训练建议
            st.markdown(f"### 🏋️ {get_text('strength_training')}")
            for rec in strength_recs:
                st.markdown(f"""
                <div style="padding: 10px; background-color: #E8EAF6; border-radius: 8px; margin: 8px 0; border-left: 4px solid #3F51B5;">
                    <p style="margin: 0; color: #283593;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 显示有氧训练建议
            st.markdown(f"### 🏃 {get_text('cardio_training')}")
            for rec in cardio_recs:
                st.markdown(f"""
                <div style="padding: 10px; background-color: #E3F2FD; border-radius: 8px; margin: 8px 0; border-left: 4px solid #2196F3;">
                    <p style="margin: 0; color: #1565C0;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with diet_tab:
            # 确定用户目标 (根据BMI简单判断)
            if bmi < 18.5:
                goal = "gain"  # 体重不足，需要增重
            elif bmi > 25:
                goal = "lose"  # 超重，需要减重
            else:
                goal = "maintain"  # 正常体重，保持即可
                
            # 获取营养计划
            nutrition_plan = get_nutrition_plan(
                user_profile["gender"],
                user_profile["weight"], 
                user_profile["activity"],
                goal
            )
            
            # 显示每日宏量营养素目标
            st.markdown(f"### 🥗 {get_text('daily_macros')}")
            
            # 创建宏量营养素表格
            macro_data = {
                get_text("protein"): f"{nutrition_plan['protein']['amount']}g",
                get_text("carbs"): f"{nutrition_plan['carbs']['amount']}g",
                get_text("fat"): f"{nutrition_plan['fat']['amount']}g"
            }
            
            # 计算总卡路里
            total_calories = (nutrition_plan['protein']['amount'] * 4) + (nutrition_plan['carbs']['amount'] * 4) + (nutrition_plan['fat']['amount'] * 9)
            macro_data[get_text("total")] = f"{total_calories} {get_text('calories_unit')}"
            
            # 显示数据表格
            st.table(macro_data)
            
            # 显示宏量营养素饼图
            protein_cals = nutrition_plan['protein']['amount'] * 4
            carb_cals = nutrition_plan['carbs']['amount'] * 4
            fat_cals = nutrition_plan['fat']['amount'] * 9
            
            fig = go.Figure(data=[go.Pie(
                labels=[get_text("protein"), get_text("carbs"), get_text("fat")],
                values=[protein_cals, carb_cals, fat_cals],
                marker=dict(colors=['#3F51B5', '#4CAF50', '#FF9800']),
                hole=.4
            )])
            
            fig.update_layout(
                title=get_text("daily_macros"),
                legend=dict(orientation="h")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示宏量营养素建议
            st.markdown(f"### 🍽️ {get_text('diet_recommendations')}")
            
            # 蛋白质建议
            st.markdown(f"""
            <div style="padding: 10px; background-color: #E8EAF6; border-radius: 8px; margin: 8px 0; border-left: 4px solid #3F51B5;">
                <h4 style="margin-top: 0; font-size: 1rem; color: #283593;">{get_text('protein_recommendation')}</h4>
                <p style="margin: 0; color: #283593;">{nutrition_plan['protein']['advice']['en'] if st.session_state.language == 'en' else nutrition_plan['protein']['advice']['zh']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 碳水建议
            st.markdown(f"""
            <div style="padding: 10px; background-color: #E8F5E9; border-radius: 8px; margin: 8px 0; border-left: 4px solid #4CAF50;">
                <h4 style="margin-top: 0; font-size: 1rem; color: #2E7D32;">{get_text('carbs_recommendation')}</h4>
                <p style="margin: 0; color: #2E7D32;">{nutrition_plan['carbs']['advice']['en'] if st.session_state.language == 'en' else nutrition_plan['carbs']['advice']['zh']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 脂肪建议
            st.markdown(f"""
            <div style="padding: 10px; background-color: #FFF3E0; border-radius: 8px; margin: 8px 0; border-left: 4px solid #FF9800;">
                <h4 style="margin-top: 0; font-size: 1rem; color: #E65100;">{get_text('fat_recommendation')}</h4>
                <p style="margin: 0; color: #E65100;">{nutrition_plan['fat']['advice']['en'] if st.session_state.language == 'en' else nutrition_plan['fat']['advice']['zh']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 餐食时间建议
            st.markdown(f"### ⏰ {get_text('meal_timing')}")
            
            meal_timing = nutrition_plan['meal_timing']['en'] if st.session_state.language == 'en' else nutrition_plan['meal_timing']['zh']
            for timing in meal_timing:
                st.markdown(f"""
                <div style="padding: 10px; background-color: #F3E5F5; border-radius: 8px; margin: 8px 0; border-left: 4px solid #9C27B0;">
                    <p style="margin: 0; color: #6A1B9A;">{timing}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with weekly_diet_tab:
            # 生成一周饮食计划按钮
            if 'weekly_diet_plan' not in st.session_state:
                st.session_state.weekly_diet_plan = None
            
            if st.button(get_text('generate_plan'), key="generate_diet_plan"):
                # 确定用户目标
                if bmi < 18.5:
                    goal = "gain"  # 体重不足，需要增重
                elif bmi > 25:
                    goal = "lose"  # 超重，需要减重
                else:
                    goal = "maintain"  # 正常体重，保持即可
                
                # 计算每日卡路里需求
                daily_calories = calculate_daily_calories(
                    user_profile["height"],
                    user_profile["weight"],
                    user_profile["age"],
                    user_profile["gender"],
                    user_profile["activity"]
                )
                
                # 生成饮食计划
                st.session_state.weekly_diet_plan = generate_weekly_diet_plan(
                    user_profile["gender"],
                    user_profile["weight"],
                    user_profile["activity"],
                    goal,
                    daily_calories
                )
                
                st.success(get_text('plan_generated'))
                st.rerun()
            
            # 显示一周饮食计划
            if st.session_state.weekly_diet_plan:
                plan = st.session_state.weekly_diet_plan
                
                # 显示每日宏量营养素
                st.markdown(f"### 🥗 {get_text('daily_macros')}")
                
                macro_data = {
                    get_text("protein"): f"{plan['protein_g']}g",
                    get_text("carbs"): f"{plan['carbs_g']}g",
                    get_text("fat"): f"{plan['fat_g']}g",
                    get_text("total"): f"{plan['daily_calories']} {get_text('calories_unit')}"
                }
                
                st.table(macro_data)
                
                # 显示每天的计划
                for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                    day_plan = plan["days"][day]
                    day_name = day_plan["name"]["en"] if st.session_state.language == "en" else day_plan["name"]["zh"]
                    
                    with st.expander(f"📆 {day_name}"):
                        meals = day_plan["plan"]["meals"]
                        calories = day_plan["plan"]["calories"]
                        
                        st.markdown(f"""
                        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                            <h4 style="margin-top: 0; color: #2E7D32;">🍳 {get_text('breakfast')} - {calories['breakfast']} {get_text('calories_unit')}</h4>
                            <p style="margin: 0; font-size: 1.1rem; color: #1B5E20;">{meals['breakfast']['en'] if st.session_state.language == 'en' else meals['breakfast']['zh']}</p>
                        </div>
                        
                        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                            <h4 style="margin-top: 0; color: #1565C0;">🍲 {get_text('lunch')} - {calories['lunch']} {get_text('calories_unit')}</h4>
                            <p style="margin: 0; font-size: 1.1rem; color: #0D47A1;">{meals['lunch']['en'] if st.session_state.language == 'en' else meals['lunch']['zh']}</p>
                        </div>
                        
                        <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                            <h4 style="margin-top: 0; color: #E65100;">🍽️ {get_text('dinner')} - {calories['dinner']} {get_text('calories_unit')}</h4>
                            <p style="margin: 0; font-size: 1.1rem; color: #BF360C;">{meals['dinner']['en'] if st.session_state.language == 'en' else meals['dinner']['zh']}</p>
                        </div>
                        
                        <div style="background-color: #F3E5F5; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                            <h4 style="margin-top: 0; color: #6A1B9A;">🍌 {get_text('snacks')} - {calories['snacks']} {get_text('calories_unit')}</h4>
                            <p style="margin: 0; font-size: 1.1rem; color: #4A148C;">{meals['snacks']['en'] if st.session_state.language == 'en' else meals['snacks']['zh']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
        with weekly_workout_tab:
            # 生成一周锻炼计划按钮
            if 'weekly_workout_plan' not in st.session_state:
                st.session_state.weekly_workout_plan = None
            
            if st.button(get_text('generate_plan'), key="generate_workout_plan"):
                # 确定用户目标
                if bmi < 18.5:
                    goal = "gain"  # 体重不足，需要增重
                elif bmi > 25:
                    goal = "lose"  # 超重，需要减重
                else:
                    goal = "maintain"  # 正常体重，保持即可
                
                # 生成锻炼计划
                st.session_state.weekly_workout_plan = generate_weekly_workout_plan(
                    user_profile["gender"],
                    user_profile["age"],
                    user_profile["bmi"],
                    user_profile["activity"],
                    goal
                )
                
                st.success(get_text('plan_generated'))
                st.rerun()
            
            # 显示一周锻炼计划
            if st.session_state.weekly_workout_plan:
                plan = st.session_state.weekly_workout_plan
                
                # 显示计划概览
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(get_text('strength_training'), f"{plan['strength_days']} days")
                
                with col2:
                    st.metric(get_text('cardio_training'), f"{plan['cardio_days']} days")
                
                with col3:
                    st.metric(get_text('rest'), f"{plan['rest_days']} days")
                
                intensity_text = get_text('low') if plan['intensity'] == 'low' else (get_text('moderate') if plan['intensity'] == 'moderate' else get_text('high'))
                st.info(f"{get_text('intensity')}: {intensity_text}")
                
                # 显示每天的锻炼计划
                for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                    day_plan = plan["days"][day]
                    day_name = day_plan["name"]["en"] if st.session_state.language == "en" else day_plan["name"]["zh"]
                    workout = day_plan["workout"]
                    
                    # 设置不同类型的颜色
                    if workout["type"] == "strength":
                        bg_color = "#E8EAF6"
                        border_color = "#3F51B5"
                        text_color = "#283593"
                        icon = "🏋️"
                        type_text = get_text('strength')
                    elif workout["type"] == "cardio":
                        bg_color = "#E3F2FD"
                        border_color = "#2196F3"
                        text_color = "#1565C0"
                        icon = "🏃"
                        type_text = get_text('cardio')
                    else:  # rest
                        bg_color = "#ECEFF1"
                        border_color = "#607D8B"
                        text_color = "#37474F"
                        icon = "🧘"
                        type_text = get_text('rest')
                    
                    # 显示锻炼内容
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid {border_color};">
                        <h4 style="margin-top: 0; color: {text_color};">📆 {day_name} - {icon} {type_text}</h4>
                        <p style="margin: 0; font-size: 1.1rem; color: {text_color};">{workout['details']['en'] if st.session_state.language == 'en' else workout['details']['zh']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 显示一般性建议
                st.markdown(f"### 🔍 {get_text('fitness_recommendations')}")
                
                # 获取正确语言的建议
                lang = "en" if st.session_state.language == "en" else "zh"
                strength_advice = plan["general_advice"]["strength"][lang]
                cardio_advice = plan["general_advice"]["cardio"][lang]
                
                # 显示力量训练建议
                st.markdown(f"#### 🏋️ {get_text('strength_training')}")
                for advice in strength_advice:
                    st.markdown(f"""
                    <div style="padding: 10px; background-color: #E8EAF6; border-radius: 8px; margin: 8px 0; border-left: 4px solid #3F51B5;">
                        <p style="margin: 0; color: #283593;">{advice}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 显示有氧训练建议
                st.markdown(f"#### 🏃 {get_text('cardio_training')}")
                for advice in cardio_advice:
                    st.markdown(f"""
                    <div style="padding: 10px; background-color: #E3F2FD; border-radius: 8px; margin: 8px 0; border-left: 4px solid #2196F3;">
                        <p style="margin: 0; color: #1565C0;">{advice}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        # 如果用户没有设置个人资料，则显示提示
        st.warning(get_text("not_enough_data"))

def get_meal_specific_recommendations(meal_calories, food_names, daily_calories, user_profile):
    """获取针对特定餐食的建议"""
    # 根据餐食热量与每日目标的比例，确定这是哪一餐
    meal_ratio = meal_calories / daily_calories
    
    # 初始化建议列表
    recommendations = {
        "en": [],
        "zh": []
    }
    
    # 判断餐食类型
    if meal_ratio <= 0.15:
        # 可能是小吃或加餐
        recommendations["en"] = [
            "This appears to be a snack. Consider adding protein to feel fuller.",
            "Pair snacks with vegetables or fruits for added nutrients.",
            "Keep snacks between 100-300 calories for weight management."
        ]
        recommendations["zh"] = [
            "这似乎是一份小吃。考虑添加蛋白质以增加饱腹感。",
            "将小吃与蔬菜或水果搭配，增加营养。",
            "为了体重管理，保持小吃在100-300卡路里之间。"
        ]
    elif meal_ratio <= 0.30:
        # 可能是早餐
        recommendations["en"] = [
            "This appears to be a breakfast. Consider including protein for sustained energy.",
            "Adding fiber-rich foods will help you feel full until lunch.",
            "Stay hydrated by drinking water with breakfast."
        ]
        recommendations["zh"] = [
            "这似乎是一份早餐。考虑包含蛋白质以获得持续能量。",
            "添加富含纤维的食物将帮助您保持饱腹感直到午餐。",
            "早餐时喝水保持水分。"
        ]
    elif meal_ratio <= 0.45:
        # 可能是午餐
        recommendations["en"] = [
            "This appears to be a lunch. Balance with vegetables and lean protein.",
            "Consider adding a small amount of healthy fats for energy through the afternoon.",
            "Portion control at lunch can help prevent afternoon energy slumps."
        ]
        recommendations["zh"] = [
            "这似乎是一份午餐。建议搭配蔬菜和瘦肉蛋白。",
            "考虑添加少量健康脂肪，为下午提供能量。",
            "午餐的份量控制可以帮助防止下午能量不足。"
        ]
    else:
        # 可能是晚餐或大餐
        recommendations["en"] = [
            "This appears to be a larger meal. Consider reducing portion sizes if consumed late.",
            "Try to include at least 3 different food groups for balanced nutrition.",
            "Eat slowly and stop when you feel 80% full to prevent overeating."
        ]
        recommendations["zh"] = [
            "这似乎是一顿大餐。如果晚上食用，考虑减少份量。",
            "尝试包含至少3种不同的食物类别以获得均衡营养。",
            "慢慢进食，感觉八分饱就停止，以防止过度进食。"
        ]
    
    # 根据食物类型添加额外建议
    for food_name in food_names:
        food_lower = food_name.lower()
        if any(fast_food in food_lower for fast_food in ["burger", "pizza", "fries", "hamburger", "汉堡", "披萨", "薯条"]):
            recommendations["en"].append("Consider balancing fast food with a vegetable side dish next time.")
            recommendations["zh"].append("下次考虑用蔬菜配菜平衡快餐。")
            break
    
    return recommendations

def calculate_bmi(height, weight):
    """计算BMI"""
    if height and weight and height > 0:
        # 将身高转为米
        height_m = height / 100  
        return weight / (height_m * height_m)
    return 0

def calculate_daily_calories(height, weight, age, gender, activity):
    """计算每日卡路里需求"""
    if not all([height, weight, age, gender, activity]):
        return 2000  # 默认值
    
    # 转换活动系数
    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very": 1.9
    }
    
    activity_factor = activity_factors.get(activity, 1.2)
    
    # 基础代谢率计算 (BMR) - Harris-Benedict公式
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
    # 总热量需求
    return int(bmr * activity_factor)

def get_fitness_recommendations(gender, age, bmi, activity_level):
    """获取健身建议"""
    recommendations = {
        "strength": {
            "en": [],
            "zh": []
        },
        "cardio": {
            "en": [],
            "zh": []
        }
    }
    
    # 基于BMI的通用建议
    if bmi < 18.5:  # 体重过轻
        recommendations["strength"]["en"] = [
            "Focus on compound movements like squats, bench press, and rows",
            "Aim for 3-4 strength training sessions per week",
            "Progressive overload is key - gradually increase weights"
        ]
        recommendations["cardio"]["en"] = [
            "Limit intense cardio to 20-30 minutes, 2-3 times weekly",
            "Consider walking or light cycling for active recovery",
            "Prioritize strength training over cardio for weight gain"
        ]
        recommendations["strength"]["zh"] = [
            "专注于复合动作，如深蹲、卧推和划船",
            "每周进行3-4次力量训练",
            "渐进式负荷是关键 - 逐渐增加重量"
        ]
        recommendations["cardio"]["zh"] = [
            "将高强度有氧运动限制在每周2-3次，每次20-30分钟",
            "考虑步行或轻度骑行作为主动恢复",
            "为增重，优先考虑力量训练而非有氧运动"
        ]
    elif bmi > 25:  # 超重
        recommendations["strength"]["en"] = [
            "Incorporate full-body resistance training 2-3 times weekly",
            "Focus on higher repetitions (12-15) with moderate weights",
            "Include circuit training to maximize calorie burn"
        ]
        recommendations["cardio"]["en"] = [
            "Aim for 150-300 minutes of moderate cardio weekly",
            "Try interval training (HIIT) for efficient fat loss",
            "Include at least one longer (45+ min) steady-state session weekly"
        ]
        recommendations["strength"]["zh"] = [
            "每周进行2-3次全身阻力训练",
            "专注于中等重量下的高重复次数(12-15次)",
            "包括循环训练以最大化卡路里消耗"
        ]
        recommendations["cardio"]["zh"] = [
            "每周进行150-300分钟的中等强度有氧运动",
            "尝试间歇训练(HIIT)以高效减脂",
            "每周至少包括一次较长(45+分钟)的稳态有氧运动"
        ]
    else:  # 正常体重
        recommendations["strength"]["en"] = [
            "Balance between strength and hypertrophy (8-12 reps)",
            "Consider a split routine targeting different muscle groups",
            "Perform compound movements with proper form"
        ]
        recommendations["cardio"]["en"] = [
            "Mix cardio types (steady-state, intervals, recreational)",
            "Aim for 2-3 cardio sessions weekly, 20-40 minutes each",
            "Include active recovery like yoga or swimming"
        ]
        recommendations["strength"]["zh"] = [
            "平衡力量和肌肉增长训练(8-12次重复)",
            "考虑分化训练，针对不同肌肉群",
            "使用正确姿势进行复合动作"
        ]
        recommendations["cardio"]["zh"] = [
            "混合有氧类型(稳态、间歇、娱乐性)",
            "每周进行2-3次有氧训练，每次20-40分钟",
            "包括主动恢复活动，如瑜伽或游泳"
        ]
    
    # 根据年龄调整建议
    if age > 50:
        recommendations["strength"]["en"].append("Include balance and mobility exercises for joint health")
        recommendations["cardio"]["en"].append("Consider low-impact options like swimming or cycling")
        recommendations["strength"]["zh"].append("包括平衡和活动性练习以保护关节健康")
        recommendations["cardio"]["zh"].append("考虑低冲击选项，如游泳或骑车")
    elif age < 30:
        recommendations["strength"]["en"].append("Challenge yourself with varied workout styles and progressive overload")
        recommendations["cardio"]["en"].append("Try sports and outdoor activities for enjoyable cardio")
        recommendations["strength"]["zh"].append("通过各种训练风格和渐进负荷挑战自己")
        recommendations["cardio"]["zh"].append("尝试运动和户外活动，享受有氧运动乐趣")
    
    # 根据活动水平调整
    if activity_level in ["sedentary", "light"]:
        recommendations["strength"]["en"].append("Start with body weight exercises before adding external weights")
        recommendations["cardio"]["en"].append("Begin with walking and gradually increase intensity")
        recommendations["strength"]["zh"].append("在添加外部重量前，先从体重练习开始")
        recommendations["cardio"]["zh"].append("从步行开始，逐渐增加强度")
    elif activity_level in ["active", "very"]:
        recommendations["strength"]["en"].append("Consider periodization to avoid plateaus and overtraining")
        recommendations["cardio"]["en"].append("Focus on heart rate zones for optimal training effects")
        recommendations["strength"]["zh"].append("考虑周期化训练，避免平台期和过度训练")
        recommendations["cardio"]["zh"].append("关注心率区间以获得最佳训练效果")
    
    return recommendations

def get_nutrition_plan(gender, weight, activity, goal):
    """获取营养计划"""
    plan = {
        "protein": {
            "amount": 0,
            "advice": {
                "en": "",
                "zh": ""
            }
        },
        "carbs": {
            "amount": 0,
            "advice": {
                "en": "",
                "zh": ""
            }
        },
        "fat": {
            "amount": 0,
            "advice": {
                "en": "",
                "zh": ""
            }
        },
        "meal_timing": {
            "en": [],
            "zh": []
        }
    }
    
    # 蛋白质建议 (基于体重)
    if goal == "gain":
        # 增肌需要更多蛋白质
        protein_g_per_kg = 2.0 
        plan["protein"]["advice"]["en"] = "Higher protein intake supports muscle growth during caloric surplus"
        plan["protein"]["advice"]["zh"] = "高蛋白摄入支持热量盈余期间的肌肉生长"
    elif goal == "lose":
        # 减脂期间保留肌肉
        protein_g_per_kg = 2.2
        plan["protein"]["advice"]["en"] = "Higher protein preserves muscle mass during caloric deficit"
        plan["protein"]["advice"]["zh"] = "高蛋白在热量赤字期间保护肌肉量"
    else:
        # 维持体重
        protein_g_per_kg = 1.6
        plan["protein"]["advice"]["en"] = "Moderate protein supports muscle maintenance and recovery"
        plan["protein"]["advice"]["zh"] = "适量蛋白质支持肌肉维护和恢复"
    
    plan["protein"]["amount"] = int(weight * protein_g_per_kg)
    
    # 脂肪建议 (占总热量的百分比)
    if goal == "lose":
        fat_percentage = 0.25  # 减脂期间适度脂肪
        plan["fat"]["advice"]["en"] = "Moderate fat provides satiety and supports hormonal balance"
        plan["fat"]["advice"]["zh"] = "适量脂肪提供饱腹感并支持荷尔蒙平衡"
    elif goal == "gain":
        fat_percentage = 0.30  # 增肌期间略高脂肪
        plan["fat"]["advice"]["en"] = "Higher healthy fats support anabolic hormone production"
        plan["fat"]["advice"]["zh"] = "较高的健康脂肪支持合成代谢激素生成"
    else:
        fat_percentage = 0.30  # 维持期间正常脂肪
        plan["fat"]["advice"]["en"] = "Balanced fat intake supports overall health and energy levels"
        plan["fat"]["advice"]["zh"] = "平衡脂肪摄入支持整体健康和能量水平"
    
    # 基于活动水平估算总热量
    activity_multipliers = {
        "sedentary": 30,
        "light": 35,
        "moderate": 40,
        "active": 45,
        "very": 50
    }
    
    estimated_calories = weight * activity_multipliers.get(activity, 35)
    
    # 脂肪克数 (1克脂肪 = 9卡路里)
    plan["fat"]["amount"] = int((estimated_calories * fat_percentage) / 9)
    
    # 碳水化合物 (剩余热量)
    protein_calories = plan["protein"]["amount"] * 4
    fat_calories = plan["fat"]["amount"] * 9
    carb_calories = estimated_calories - protein_calories - fat_calories
    plan["carbs"]["amount"] = int(carb_calories / 4)
    
    # 碳水化合物建议
    if goal == "lose":
        plan["carbs"]["advice"]["en"] = "Focus on fiber-rich, low glycemic carbs to manage hunger"
        plan["carbs"]["advice"]["zh"] = "专注于富含纤维、低血糖指数的碳水化合物以管理饥饿感"
    elif goal == "gain":
        plan["carbs"]["advice"]["en"] = "Higher carbs fuel intense workouts and support muscle growth"
        plan["carbs"]["advice"]["zh"] = "较高的碳水化合物为高强度训练提供燃料并支持肌肉生长"
    else:
        plan["carbs"]["advice"]["en"] = "Balanced carbs provide steady energy throughout the day"
        plan["carbs"]["advice"]["zh"] = "平衡碳水化合物提供全天稳定能量"
    
    # 餐食时间建议
    plan["meal_timing"]["en"] = [
        "Eat breakfast within 1-2 hours of waking up",
        "Space meals 3-4 hours apart for optimal metabolism",
        "Consider a small protein-rich snack before bed for recovery"
    ]
    
    plan["meal_timing"]["zh"] = [
        "在起床后1-2小时内吃早餐",
        "餐与餐之间间隔3-4小时，优化代谢",
        "考虑睡前摄入富含蛋白质的小零食以促进恢复"
    ]
    
    # 根据目标调整餐食时间建议
    if goal == "lose":
        plan["meal_timing"]["en"].append("Front-load calories earlier in the day when possible")
        plan["meal_timing"]["zh"].append("尽可能在一天的早些时候摄入更多热量")
    elif goal == "gain":
        plan["meal_timing"]["en"].append("Include pre and post-workout nutrition to maximize muscle growth")
        plan["meal_timing"]["zh"].append("包括训练前后营养，最大化肌肉生长")
    
    return plan

def generate_weekly_diet_plan(gender, weight, activity, goal, daily_calories):
    """
    Generate a weekly diet plan based on user profile
    
    Parameters:
        gender: User's gender (male/female)
        weight: User's weight in kg
        activity: Activity level (sedentary/light/moderate/active/very)
        goal: Weight goal (lose/gain/maintain)
        daily_calories: Daily calorie target
        
    Returns:
        Dictionary with daily meal plans for a week
    """
    # 获取营养比例
    nutrition_plan = get_nutrition_plan(gender, weight, activity, goal)
    protein_g = nutrition_plan["protein"]["amount"]
    carbs_g = nutrition_plan["carbs"]["amount"]
    fat_g = nutrition_plan["fat"]["amount"]
    
    # 为不同目标设置不同类型的食物
    food_categories = {
        "protein_foods": {
            "en": ["Chicken breast", "Turkey", "Lean beef", "Salmon", "Tuna", "Eggs", "Greek yogurt", 
                   "Cottage cheese", "Tofu", "Lentils", "Chickpeas", "Protein shake"],
            "zh": ["鸡胸肉", "火鸡肉", "瘦牛肉", "三文鱼", "金枪鱼", "鸡蛋", "希腊酸奶", 
                   "农家奶酪", "豆腐", "小扁豆", "鹰嘴豆", "蛋白质奶昔"]
        },
        "carb_foods": {
            "en": ["Brown rice", "Quinoa", "Sweet potato", "Oatmeal", "Whole grain bread", 
                   "Whole wheat pasta", "Barley", "Black beans", "Fruits", "Vegetables"],
            "zh": ["糙米", "藜麦", "红薯", "燕麦片", "全麦面包", 
                   "全麦意面", "大麦", "黑豆", "水果", "蔬菜"]
        },
        "fat_foods": {
            "en": ["Avocado", "Olive oil", "Nuts", "Seeds", "Nut butters", "Fatty fish", "Eggs", "Cheese"],
            "zh": ["牛油果", "橄榄油", "坚果", "种子", "坚果酱", "脂肪鱼", "鸡蛋", "奶酪"]
        },
        "vegetables": {
            "en": ["Broccoli", "Spinach", "Kale", "Bell peppers", "Carrots", "Cauliflower", 
                   "Asparagus", "Brussels sprouts", "Zucchini", "Mushrooms"],
            "zh": ["西兰花", "菠菜", "羽衣甘蓝", "彩椒", "胡萝卜", "花椰菜", 
                   "芦笋", "孢子甘蓝", "西葫芦", "蘑菇"]
        },
        "fruits": {
            "en": ["Berries", "Apple", "Banana", "Orange", "Kiwi", "Pineapple", "Mango", "Grapefruit"],
            "zh": ["浆果", "苹果", "香蕉", "橙子", "猕猴桃", "菠萝", "芒果", "葡萄柚"]
        }
    }
    
    # 调整食物选择基于目标
    if goal == "lose":
        # 减重计划偏好低卡高蛋白和高纤维
        preferred_carbs = {
            "en": ["Vegetables", "Berries", "Green apple", "Oatmeal", "Sweet potato"],
            "zh": ["蔬菜", "浆果", "青苹果", "燕麦片", "红薯"]
        }
        preferred_fats = {
            "en": ["Avocado", "Olive oil", "Chia seeds", "Flaxseeds", "Almonds"],
            "zh": ["牛油果", "橄榄油", "奇亚籽", "亚麻籽", "杏仁"]
        }
    elif goal == "gain":
        # 增重计划偏好高卡路里、高营养密度
        preferred_carbs = {
            "en": ["Brown rice", "Quinoa", "Oatmeal", "Whole grain bread", "Pasta", "Potatoes", "Banana"],
            "zh": ["糙米", "藜麦", "燕麦片", "全麦面包", "意面", "土豆", "香蕉"]
        }
        preferred_fats = {
            "en": ["Nut butters", "Olive oil", "Avocado", "Whole eggs", "Full-fat dairy", "Mixed nuts"],
            "zh": ["坚果酱", "橄榄油", "牛油果", "全蛋", "全脂乳制品", "混合坚果"]
        }
    else:  # maintain
        # 维持体重计划注重均衡
        preferred_carbs = {
            "en": ["Brown rice", "Quinoa", "Sweet potato", "Fruits", "Oatmeal", "Whole grains"],
            "zh": ["糙米", "藜麦", "红薯", "水果", "燕麦片", "全谷物"]
        }
        preferred_fats = {
            "en": ["Avocado", "Olive oil", "Mixed nuts", "Seeds", "Fatty fish"],
            "zh": ["牛油果", "橄榄油", "混合坚果", "种子", "脂肪鱼"]
        }
    
    # 根据性别和活动水平调整食物量
    portion_modifier = 1.0
    if gender == "male" and activity in ["active", "very"]:
        portion_modifier = 1.3
    elif gender == "female" and activity in ["sedentary", "light"]:
        portion_modifier = 0.8
    
    # 每日卡路里分配到各餐
    meal_calories = {
        "breakfast": int(daily_calories * 0.25),  # 25% for breakfast
        "lunch": int(daily_calories * 0.35),      # 35% for lunch
        "dinner": int(daily_calories * 0.30),     # 30% for dinner
        "snacks": int(daily_calories * 0.10)      # 10% for snacks
    }
    
    # 生成一周的饮食计划
    import random
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day_names = {
        "monday": {"en": "Monday", "zh": "星期一"},
        "tuesday": {"en": "Tuesday", "zh": "星期二"},
        "wednesday": {"en": "Wednesday", "zh": "星期三"},
        "thursday": {"en": "Thursday", "zh": "星期四"},
        "friday": {"en": "Friday", "zh": "星期五"},
        "saturday": {"en": "Saturday", "zh": "星期六"},
        "sunday": {"en": "Sunday", "zh": "星期日"}
    }
    
    # 初始化饮食计划
    weekly_plan = {
        "daily_calories": daily_calories,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "days": {}
    }
    
    # 为每天生成饮食计划
    for day in days:
        lang = "en"  # 默认英文
        
        breakfast_protein = random.choice(food_categories["protein_foods"][lang])
        breakfast_carb = random.choice(preferred_carbs[lang])
        breakfast_fat = random.choice(preferred_fats[lang])
        
        lunch_protein = random.choice([p for p in food_categories["protein_foods"][lang] if p != breakfast_protein])
        lunch_carb = random.choice([c for c in preferred_carbs[lang] if c != breakfast_carb])
        lunch_veg = random.choice(food_categories["vegetables"][lang])
        
        dinner_protein = random.choice([p for p in food_categories["protein_foods"][lang] if p != lunch_protein])
        dinner_carb = random.choice([c for c in preferred_carbs[lang] if c != lunch_carb])
        dinner_veg = random.choice([v for v in food_categories["vegetables"][lang] if v != lunch_veg])
        dinner_fat = random.choice([f for f in preferred_fats[lang] if f != breakfast_fat])
        
        snack1 = random.choice(food_categories["fruits"][lang])
        snack2 = random.choice([p for p in food_categories["protein_foods"][lang] if p != dinner_protein and p != lunch_protein and p != breakfast_protein])
        
        # 构建每日计划
        daily_plan = {
            "meals": {
                "breakfast": {
                    "en": f"{breakfast_protein} with {breakfast_carb} and {breakfast_fat}",
                    "zh": f"{food_categories['protein_foods']['zh'][food_categories['protein_foods']['en'].index(breakfast_protein)]}配{preferred_carbs['zh'][preferred_carbs['en'].index(breakfast_carb)]}和{preferred_fats['zh'][preferred_fats['en'].index(breakfast_fat)]}"
                },
                "lunch": {
                    "en": f"{lunch_protein} with {lunch_carb} and {lunch_veg}",
                    "zh": f"{food_categories['protein_foods']['zh'][food_categories['protein_foods']['en'].index(lunch_protein)]}配{preferred_carbs['zh'][preferred_carbs['en'].index(lunch_carb)]}和{food_categories['vegetables']['zh'][food_categories['vegetables']['en'].index(lunch_veg)]}"
                },
                "dinner": {
                    "en": f"{dinner_protein} with {dinner_carb}, {dinner_veg} and {dinner_fat}",
                    "zh": f"{food_categories['protein_foods']['zh'][food_categories['protein_foods']['en'].index(dinner_protein)]}配{preferred_carbs['zh'][preferred_carbs['en'].index(dinner_carb)]}、{food_categories['vegetables']['zh'][food_categories['vegetables']['en'].index(dinner_veg)]}和{preferred_fats['zh'][preferred_fats['en'].index(dinner_fat)]}"
                },
                "snacks": {
                    "en": f"{snack1} and {snack2}",
                    "zh": f"{food_categories['fruits']['zh'][food_categories['fruits']['en'].index(snack1)]}和{food_categories['protein_foods']['zh'][food_categories['protein_foods']['en'].index(snack2)]}"
                }
            },
            "calories": meal_calories
        }
        
        weekly_plan["days"][day] = {
            "name": day_names[day],
            "plan": daily_plan
        }
    
    return weekly_plan

def generate_weekly_workout_plan(gender, age, bmi, activity_level, goal):
    """
    Generate a weekly workout plan based on user profile
    
    Parameters:
        gender: User's gender (male/female)
        age: User's age
        bmi: User's BMI
        activity_level: Activity level (sedentary/light/moderate/active/very)
        goal: Weight goal (lose/gain/maintain)
        
    Returns:
        Dictionary with daily workout plans for a week
    """
    # 先获取基础健身建议
    fitness_recs = get_fitness_recommendations(gender, age, bmi, activity_level)
    
    # 确定每周训练天数
    if activity_level in ["sedentary", "light"]:
        training_days = 3  # 初学者从每周3天开始
    elif activity_level == "moderate":
        training_days = 4  # 中级训练者每周4天
    else:  # 活跃或非常活跃
        training_days = 5  # 高级训练者每周5-6天
    
    # 根据目标调整训练类型分配
    if goal == "lose":
        # 减重注重有氧训练，但仍保持力量训练以保留肌肉
        cardio_days = training_days // 2 + (1 if training_days % 2 else 0)
        strength_days = training_days - cardio_days
    elif goal == "gain":
        # 增肌注重力量训练
        strength_days = training_days - 1  # 至少1天有氧
        cardio_days = 1
    else:  # maintain
        # 维持平衡训练
        strength_days = training_days // 2
        cardio_days = training_days - strength_days
    
    # 确保至少有1天力量和1天有氧
    strength_days = max(1, strength_days)
    cardio_days = max(1, cardio_days)
    
    # 调整确保总天数正确
    if strength_days + cardio_days > training_days:
        # 优先保持力量训练天数，减少有氧天数
        cardio_days = training_days - strength_days
    
    # 根据年龄和BMI调整训练强度
    intensity = "moderate"  # 默认强度
    
    if age > 60 or bmi > 30 or bmi < 18.5:
        intensity = "low"  # 高龄或BMI异常者使用低强度
    elif (age < 40 and bmi >= 18.5 and bmi <= 25) and activity_level in ["active", "very"]:
        intensity = "high"  # 年轻健康且已经活跃的人可以高强度
    
    # 训练类型
    cardio_types = {
        "low": {
            "en": ["Walking (30 min)", "Light cycling (20 min)", "Swimming (20 min)", "Elliptical (15 min)"],
            "zh": ["步行 (30分钟)", "轻度骑行 (20分钟)", "游泳 (20分钟)", "椭圆机 (15分钟)"]
        },
        "moderate": {
            "en": ["Jogging (25 min)", "Cycling (30 min)", "Swimming (30 min)", "HIIT (15 min)", "Rowing (20 min)"],
            "zh": ["慢跑 (25分钟)", "骑行 (30分钟)", "游泳 (30分钟)", "高强度间歇训练 (15分钟)", "划船 (20分钟)"]
        },
        "high": {
            "en": ["Running (30 min)", "HIIT (20 min)", "Cycling intervals (30 min)", "Swimming sprints (25 min)", "Boxing (30 min)"],
            "zh": ["跑步 (30分钟)", "高强度间歇训练 (20分钟)", "间歇骑行 (30分钟)", "游泳冲刺 (25分钟)", "拳击 (30分钟)"]
        }
    }
    
    strength_types = {
        "low": {
            "en": [
                "Full body - Light weights (20 min)", 
                "Body weight exercises (20 min)",
                "Light dumbbell workout (15 min)",
                "Resistance band workout (20 min)"
            ],
            "zh": [
                "全身 - 轻重量 (20分钟)", 
                "体重练习 (20分钟)",
                "轻哑铃锻炼 (15分钟)",
                "阻力带锻炼 (20分钟)"
            ]
        },
        "moderate": {
            "en": [
                "Upper body strength (30 min)", 
                "Lower body strength (30 min)",
                "Core workout (20 min)",
                "Full body strength (35 min)",
                "Push exercises (30 min)",
                "Pull exercises (30 min)"
            ],
            "zh": [
                "上肢力量 (30分钟)", 
                "下肢力量 (30分钟)",
                "核心锻炼 (20分钟)",
                "全身力量 (35分钟)",
                "推力训练 (30分钟)",
                "拉力训练 (30分钟)"
            ]
        },
        "high": {
            "en": [
                "Heavy upper body (40 min)", 
                "Heavy lower body (40 min)",
                "High-intensity circuit training (35 min)",
                "Power training (35 min)",
                "Olympic lifts (40 min)",
                "Full body with supersets (45 min)"
            ],
            "zh": [
                "重量上肢训练 (40分钟)", 
                "重量下肢训练 (40分钟)",
                "高强度循环训练 (35分钟)",
                "力量训练 (35分钟)",
                "奥林匹克举重 (40分钟)",
                "全身超级组训练 (45分钟)"
            ]
        }
    }
    
    # 休息放松训练
    recovery_types = {
        "en": ["Rest day", "Active recovery - Walking (20 min)", "Stretching (15 min)", "Yoga (20 min)", "Light mobility work (15 min)"],
        "zh": ["休息日", "主动恢复 - 步行 (20分钟)", "拉伸 (15分钟)", "瑜伽 (20分钟)", "轻度活动度锻炼 (15分钟)"]
    }
    
    # 生成每周计划
    import random
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day_names = {
        "monday": {"en": "Monday", "zh": "星期一"},
        "tuesday": {"en": "Tuesday", "zh": "星期二"},
        "wednesday": {"en": "Wednesday", "zh": "星期三"},
        "thursday": {"en": "Thursday", "zh": "星期四"},
        "friday": {"en": "Friday", "zh": "星期五"},
        "saturday": {"en": "Saturday", "zh": "星期六"},
        "sunday": {"en": "Sunday", "zh": "星期日"}
    }
    
    # 分配训练日
    all_days = days.copy()
    random.shuffle(all_days)
    
    strength_training_days = all_days[:strength_days]
    remaining_days = all_days[strength_days:]
    cardio_training_days = remaining_days[:cardio_days]
    rest_days = remaining_days[cardio_days:]
    
    # 创建周计划
    weekly_plan = {
        "training_days": training_days,
        "strength_days": strength_days,
        "cardio_days": cardio_days,
        "rest_days": len(rest_days),
        "intensity": intensity,
        "days": {}
    }
    
    # 填充每天的计划
    for day in days:
        workout = {}
        
        if day in strength_training_days:
            workout_type = "strength"
            workout_details = random.choice(strength_types[intensity]["en"])
            workout_details_zh = strength_types[intensity]["zh"][strength_types[intensity]["en"].index(workout_details)]
        elif day in cardio_training_days:
            workout_type = "cardio"
            workout_details = random.choice(cardio_types[intensity]["en"])
            workout_details_zh = cardio_types[intensity]["zh"][cardio_types[intensity]["en"].index(workout_details)]
        else:
            workout_type = "rest"
            workout_details = random.choice(recovery_types["en"])
            workout_details_zh = recovery_types["zh"][recovery_types["en"].index(workout_details)]
        
        workout = {
            "type": workout_type,
            "details": {
                "en": workout_details,
                "zh": workout_details_zh
            }
        }
        
        weekly_plan["days"][day] = {
            "name": day_names[day],
            "workout": workout
        }
    
    # 添加通用建议
    weekly_plan["general_advice"] = {
        "strength": fitness_recs["strength"],
        "cardio": fitness_recs["cardio"]
    }
    
    return weekly_plan

def get_portion_suggestion(food_name):
    """获取食物份量建议"""
    food_name_lower = food_name.lower()
    
    # 定义不同类型食物的份量建议
    portion_suggestions = {
        # 谷物类
        "grain": {
            "en": "1/2 to 1 cup cooked (size of your fist)",
            "zh": "半杯至1杯煮熟的量（拳头大小）"
        },
        # 蛋白质类
        "protein": {
            "en": "75-100g (size of your palm)",
            "zh": "75-100克（手掌大小）"
        },
        # 蔬菜类
        "vegetables": {
            "en": "1-2 cups (two handfuls)",
            "zh": "1-2杯（两手掌量）"
        },
        # 水果类
        "fruits": {
            "en": "1 medium piece or 1/2 cup (size of a tennis ball)",
            "zh": "1个中等大小或半杯（网球大小）"
        },
        # 快餐类
        "fast_food": {
            "en": "Half of typical restaurant portion, pair with vegetables",
            "zh": "餐厅典型份量的一半，搭配蔬菜"
        },
        # 零食类
        "snacks": {
            "en": "Small handful (30g) or 100-150 calories per serving",
            "zh": "小把（30克）或每份100-150卡路里"
        },
        # 其他
        "other": {
            "en": "Moderate portion (about the size of your fist)",
            "zh": "适量（约拳头大小）"
        }
    }
    
    # 根据食物名称判断类型
    if any(grain in food_name_lower for grain in ["rice", "bread", "pasta", "noodle", "cereals", "oats", "porridge", "米饭", "面包", "意面", "面条", "麦片", "燕麦", "粥"]):
        return portion_suggestions["grain"]
    
    elif any(protein in food_name_lower for protein in ["chicken", "beef", "pork", "fish", "meat", "egg", "tofu", "bean", "鸡", "牛", "猪", "肉", "鱼", "蛋", "豆腐", "豆"]):
        return portion_suggestions["protein"]
    
    elif any(veg in food_name_lower for veg in ["vegetable", "veggie", "broccoli", "spinach", "carrot", "lettuce", "salad", "蔬菜", "西兰花", "菠菜", "胡萝卜", "生菜", "沙拉"]):
        return portion_suggestions["vegetables"]
    
    elif any(fruit in food_name_lower for fruit in ["fruit", "apple", "banana", "orange", "strawberry", "grape", "水果", "苹果", "香蕉", "橙子", "草莓", "葡萄"]):
        return portion_suggestions["fruits"]
    
    elif any(ff in food_name_lower for ff in ["burger", "pizza", "fries", "hamburger", "fast food", "chips", "汉堡", "披萨", "薯条", "快餐", "炸薯片"]):
        return portion_suggestions["fast_food"]
        
    elif any(snack in food_name_lower for snack in ["cookie", "cake", "chocolate", "ice cream", "snack", "candy", "饼干", "蛋糕", "巧克力", "冰淇淋", "零食", "糖果"]):
        return portion_suggestions["snacks"]
        
    else:
        return portion_suggestions["other"]

def get_meal_balance_suggestion(food_names):
    """获取均衡饮食建议"""
    food_types = {
        "protein": False,
        "grain": False,
        "vegetable": False,
        "fruit": False
    }
    
    # 检查每种食物的类型
    for food_name in food_names:
        food_name_lower = food_name.lower()
        
        # 检查蛋白质
        if any(protein in food_name_lower for protein in ["chicken", "beef", "pork", "fish", "meat", "egg", "tofu", "bean", "鸡", "牛", "猪", "肉", "鱼", "蛋", "豆腐", "豆"]):
            food_types["protein"] = True
            
        # 检查谷物
        if any(grain in food_name_lower for grain in ["rice", "bread", "pasta", "noodle", "cereals", "oats", "porridge", "米饭", "面包", "意面", "面条", "麦片", "燕麦", "粥"]):
            food_types["grain"] = True
            
        # 检查蔬菜
        if any(veg in food_name_lower for veg in ["vegetable", "veggie", "broccoli", "spinach", "carrot", "lettuce", "salad", "蔬菜", "西兰花", "菠菜", "胡萝卜", "生菜", "沙拉"]):
            food_types["vegetable"] = True
            
        # 检查水果
        if any(fruit in food_name_lower for fruit in ["fruit", "apple", "banana", "orange", "strawberry", "grape", "水果", "苹果", "香蕉", "橙子", "草莓", "葡萄"]):
            food_types["fruit"] = True
    
    # 根据食物类型提供均衡饮食建议
    suggestions = {
        "en": [],
        "zh": []
    }
    
    # 检查蛋白质
    if not food_types["protein"]:
        suggestions["en"].append("Consider adding a protein source like chicken, fish, tofu, or beans.")
        suggestions["zh"].append("考虑添加蛋白质来源，如鸡肉、鱼肉、豆腐或豆类。")
    
    # 检查谷物
    if not food_types["grain"]:
        suggestions["en"].append("Add whole grains like brown rice, whole wheat bread, or oats for energy.")
        suggestions["zh"].append("添加全谷物，如糙米、全麦面包或燕麦，提供能量。")
    
    # 检查蔬菜
    if not food_types["vegetable"]:
        suggestions["en"].append("Include vegetables to add fiber, vitamins, and minerals to your meal.")
        suggestions["zh"].append("包含蔬菜，为餐食添加纤维、维生素和矿物质。")
    
    # 检查水果
    if not food_types["fruit"] and not food_types["vegetable"]:
        suggestions["en"].append("Add fruits or vegetables for essential vitamins and antioxidants.")
        suggestions["zh"].append("添加水果或蔬菜，摄入必需的维生素和抗氧化物。")
    
    # 如果食物结构相对均衡
    if sum(food_types.values()) >= 3:
        suggestions["en"].append("Your meal has good balance! Try to maintain this variety in your meals.")
        suggestions["zh"].append("您的餐食结构均衡！尝试在所有餐食中保持这种多样性。")
    
    # 如果只有一种类型的食物
    if sum(food_types.values()) <= 1:
        suggestions["en"].append("Try to include at least 3 food groups in your meals for better nutrition balance.")
        suggestions["zh"].append("尝试在餐食中包含至少3种食物类别，以获得更好的营养平衡。")
    
    return suggestions

def display_sidebar():
    """Display sidebar with app information and settings"""
    with st.sidebar:
        # 创建用户资料设置
        st.markdown(f"<h3 style='color: #FF9800;'>{get_text('profile_setup')}</h3>", unsafe_allow_html=True)
        st.write(get_text('profile_description'))
        
        # 收集用户信息
        user_height = st.number_input(get_text('height_label'), min_value=100, max_value=250, value=st.session_state.user_height if st.session_state.user_height else 170, step=1)
        user_weight = st.number_input(get_text('weight_label'), min_value=30, max_value=200, value=st.session_state.user_weight if st.session_state.user_weight else 70, step=1)
        user_age = st.number_input(get_text('age_label'), min_value=12, max_value=100, value=st.session_state.user_age if st.session_state.user_age else 30, step=1)
        
        # 性别选择
        gender_options = {
            "male": get_text('gender_male'),
            "female": get_text('gender_female')
        }
        user_gender = st.radio(get_text('gender_label'), options=list(gender_options.keys()), format_func=lambda x: gender_options[x], horizontal=True, index=0 if not st.session_state.user_gender or st.session_state.user_gender == "male" else 1)
        
        # 活动水平选择
        activity_options = {
            "sedentary": get_text('activity_sedentary'),
            "light": get_text('activity_light'),
            "moderate": get_text('activity_moderate'),
            "active": get_text('activity_active'),
            "very": get_text('activity_very')
        }
        user_activity = st.selectbox(get_text('activity_label'), options=list(activity_options.keys()), format_func=lambda x: activity_options[x], index=1 if not st.session_state.user_activity else list(activity_options.keys()).index(st.session_state.user_activity))
        
        # 保存按钮
        if st.button(get_text('save_profile'), use_container_width=True):
            st.session_state.user_height = user_height
            st.session_state.user_weight = user_weight
            st.session_state.user_age = user_age
            st.session_state.user_gender = user_gender
            st.session_state.user_activity = user_activity
            st.session_state.profile_setup = True
            st.success(get_text('profile_saved'))
        
        st.markdown("<hr>", unsafe_allow_html=True)

        # How to use section
        st.markdown(f"<h3 style='color: #FF9800;'>{get_text('how_to_use')}</h3>", unsafe_allow_html=True)
        st.markdown(get_text("usage_steps"))
        
        # Search history
        st.markdown(f"<h3 style='color: #FF9800;'>{get_text('search_history')}</h3>", unsafe_allow_html=True)
        
        if st.session_state.history:
            for item in reversed(st.session_state.history):
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-food">{item["food_name"]}</div>
                    <div class="history-calories">{item["calories"]} {get_text("calories_unit")}</div>
                    <div class="history-time">{item["timestamp"]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write(get_text("no_history"))
        
        if st.button(get_text("clear_history"), key="clear_history_button"):
            st.session_state.history = []
            st.rerun()
        
        # About section
        st.markdown(f"<h3 style='color: #FF9800;'>{get_text('about')}</h3>", unsafe_allow_html=True)
        st.write(get_text("about_text"))
        st.markdown(f"**{get_text('data_sources')}** USDA Food Database, Nutritionix API")
        st.markdown(f"**{get_text('technology')}** Python, Streamlit, HKBU GenAI Platform")
        
        # API settings section
        api_expander = st.expander(get_text("api_settings"), expanded=st.session_state.api_settings_expanded)
        with api_expander:
            st.text_input(get_text("api_key"), value=st.session_state.api_key, key="new_api_key")
            st.button(get_text("update_api_key"), key="update_api_key_button", on_click=update_api_key)
            st.info(get_text("api_save_info"))
        
        # 调试模式切换
        if st.checkbox("Debug Mode", value=st.session_state.debug_mode):
            toggle_debug_mode()
            st.rerun()  # 重新加载应用以应用调试模式

def main():
    """Main function to run the app"""
    init_session_state()
    display_header()
    display_sidebar()
    
    # 主界面部分
    tabs = st.tabs([get_text("tab_upload"), get_text("tab_camera")])
    
    with tabs[0]:  # 上传图片选项卡
        uploaded_file = st.file_uploader(get_text("upload_label"), type=["jpg", "jpeg", "png"])
        
        if st.button(get_text("analyze_button"), key="analyze_button", disabled=uploaded_file is None):
            if uploaded_file is not None:
                process_image(uploaded_file)
            else:
                st.warning(get_text("please_upload"))
    
    with tabs[1]:  # 摄像头选项卡
        camera_col1, camera_col2 = st.columns([3, 1])
        
        with camera_col1:
            st.markdown(f"### {get_text('camera_label')}")
            st.write(get_text('camera_help'))
        
        with camera_col2:
            if st.session_state.camera_on:
                if st.button(get_text('close_camera'), key="toggle_camera_button1"):
                    toggle_camera()
                    st.rerun()
            else:
                if st.button(get_text('open_camera'), key="toggle_camera_button2"):
                    toggle_camera()
                    st.rerun()
        
        if st.session_state.camera_on:
            st.info(get_text('camera_ready'))
            img_file = st.camera_input(label="", label_visibility="collapsed")
            
            if img_file is not None:
                if st.button(get_text('capture_button')):
                    process_image(img_file)
    
    # 显示结果
    if st.session_state.food_names and st.session_state.calories_info_list:
        display_multiple_results(st.session_state.food_names, st.session_state.calories_info_list, st.session_state.data_sources)
    elif st.session_state.error_message:
        st.error(st.session_state.error_message)
    
    # Display footer
    st.markdown(f"""
    <div class="footer">
        {get_text("footer_text")}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 