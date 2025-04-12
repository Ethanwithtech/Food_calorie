"""
Food Calorie Estimator Startup Script
"""

import os
import sys
import subprocess
import importlib.util

def check_module(module_name):
    """Check if a module is installed"""
    return importlib.util.find_spec(module_name) is not None

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_modules = [
        "streamlit", "pillow", "requests", "pandas", 
        "beautifulsoup4", "plotly", "uuid"
    ]
    
    missing_modules = []
    for module in required_modules:
        if not check_module(module):
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Installing missing dependencies: {', '.join(missing_modules)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_modules)
            print("Dependencies installation completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {str(e)}")
            return False
    
    return True

def main():
    """Launch Streamlit application"""
    print("Starting Food Calorie Estimator application...")
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("Unable to install required dependencies, the application may not function properly.")
        user_input = input("Do you still want to try launching the application? (y/n): ")
        if user_input.lower() != 'y':
            sys.exit(1)
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set the application path
    app_path = os.path.join(script_dir, "app", "app.py")
    
    # Check if the application file exists
    if not os.path.exists(app_path):
        print(f"Error: Application file not found at {app_path}")
        sys.exit(1)
    
    # Ensure temp_images directory exists
    temp_images_dir = os.path.join(script_dir, "temp_images")
    if not os.path.exists(temp_images_dir):
        os.makedirs(temp_images_dir)
        print(f"Created temporary images directory: {temp_images_dir}")
    
    # 确保config目录存在
    config_dir = os.path.join(script_dir, "config")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"Created config directory: {config_dir}")
    
    # Start Streamlit application
    try:
        print(f"Launching the application, please wait...")
        # Set environment variables to display full logs
        env = os.environ.copy()
        env["PYTHONPATH"] = script_dir
        
        # Run the Streamlit application
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], env=env, check=True)
    except Exception as e:
        print(f"Error starting the application: {str(e)}")
        print("Please make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main() 