"""
食物热量估算器启动脚本
"""

import os
import sys
import subprocess
import importlib.util

def check_module(module_name):
    """检查模块是否已安装"""
    return importlib.util.find_spec(module_name) is not None

def check_and_install_dependencies():
    """检查并安装所需的依赖项"""
    required_modules = [
        "streamlit", "pillow", "requests", "pandas", 
        "beautifulsoup4", "plotly", "uuid"
    ]
    
    missing_modules = []
    for module in required_modules:
        if not check_module(module):
            missing_modules.append(module)
    
    if missing_modules:
        print(f"正在安装缺少的依赖项: {', '.join(missing_modules)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_modules)
            print("依赖项安装完成。")
        except subprocess.CalledProcessError as e:
            print(f"安装依赖项时出错: {str(e)}")
            return False
    
    return True

def main():
    """启动Streamlit应用"""
    print("启动食物热量估算器应用...")
    
    # 检查和安装依赖项
    if not check_and_install_dependencies():
        print("无法安装所需的依赖项，应用程序可能无法正常运行。")
        user_input = input("是否仍要尝试启动应用? (y/n): ")
        if user_input.lower() != 'y':
            sys.exit(1)
    
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置应用路径
    app_path = os.path.join(script_dir, "app", "app.py")
    
    # 检查应用文件是否存在
    if not os.path.exists(app_path):
        print(f"错误: 找不到应用文件 {app_path}")
        sys.exit(1)
    
    # 确保temp_images目录存在
    temp_images_dir = os.path.join(script_dir, "temp_images")
    if not os.path.exists(temp_images_dir):
        os.makedirs(temp_images_dir)
        print(f"已创建临时图像目录: {temp_images_dir}")
    
    # 启动Streamlit应用
    try:
        print(f"正在启动应用，请稍等...")
        # 设置环境变量以显示完整日志
        env = os.environ.copy()
        env["PYTHONPATH"] = script_dir
        
        # 运行Streamlit应用
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], env=env, check=True)
    except Exception as e:
        print(f"启动应用时出错: {str(e)}")
        print("请确保已安装所有依赖项: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main() 