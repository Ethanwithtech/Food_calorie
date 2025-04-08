# Food Calorie Estimator

## Project Overview
An AI-driven application that allows users to upload food images and get estimated calorie information. The application uses computer vision AI to recognize food and retrieves nutritional information from multiple sources.

## Features
- **Food Recognition**: Upload food pictures and let AI identify food items
- **Calorie Estimation**: Get accurate calorie information for recognized foods
- **Detailed Nutrition Information**: View comprehensive nutrition details including macronutrients
- **Multi-source Data**: Get nutrition data from USDA, Nutritionix, and built-in database
- **Visualization**: Interactive charts showing macronutrient distribution
- **Search History**: Track your previous food searches
- **Modern UI**: Beautiful, responsive interface designed for intuitive use
- **Offline Mode**: Continue using the app even when API services are unavailable
- **Multilingual Support**: Supports English and Chinese interfaces, easily switch with the language button
- **Multiple Food Detection**: Can identify multiple foods in an image and provide calorie information for each
- **Personalized Fitness Recommendations**: Provide personalized fitness recommendations based on user's height, weight, age, and activity level
- **Dietary Advice**: Offer customized diet plans based on user's BMI and health goals
- **Portion Suggestions**: Provide healthy portion suggestions for identified foods
- **Meal Balance Analysis**: Analyze whether the user's meal is balanced and provide improvement suggestions
- **Comprehensive User Profiles**: Support user profiles for more accurate health and nutrition recommendations

## Target Users
- Health-conscious individuals tracking their food intake
- Fitness enthusiasts monitoring their diet
- Nutritionists and dietary consultants
- Anyone curious about food calorie content
- People seeking customized dietary guidance for weight loss or muscle gain
- International users who need multilingual support

## Technical Implementation
This project is built using the following technologies:
- **Streamlit**: Creating interactive web interfaces
- **HKBU GenAI Platform**: Using gpt-4-o-mini model for AI-driven food recognition
- **Python**: Backend programming language
- **Pandas**: Data processing and transformation
- **Plotly**: Creating interactive visualizations
- **USDA Food Database API**: Nutrition data
- **Nutritionix API**: Supplementary nutrition information
- **BMI/Health Calculators**: Calculating personalized health metrics and recommendations
- **NLP Processing**: Enhancing food recognition and multilingual capabilities

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/food-calorie-estimator.git
cd food-calorie-estimator
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python run_app.py
```
The application will automatically start and open in your default web browser at `http://localhost:8501`.

## Project Structure
```
food-calorie-estimator/
├── app/
│   ├── app.py              # Main application file
│   ├── utils/
│   │   ├── api_client.py   # API client for AI and nutrition services
│   │   └── image_utils.py  # Image processing utilities
│   └── data/
│       └── food_calories.py # Built-in database of food calories
├── uploads/                # Directory for uploaded images
├── run_app.py              # Application startup script
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Usage Guide
1. Start the application using `python run_app.py`
2. Upload a food image using the file uploader
3. Click the "Analyze Food Calories" button
4. View the recognized food and calorie information
5. Click "Show Nutrition Details" to explore detailed nutrition information
6. Your search history is saved in the sidebar for easy reference
7. Set up your profile in the sidebar for personalized fitness and diet recommendations
8. Use the language switch button at the top to toggle between English and Chinese interfaces

## First-time Use Considerations
- **User Profile Setup**: For first-time use, it's recommended to fill in your basic information (height, weight, age, gender, and activity level) in the sidebar first to get more accurate fitness and diet recommendations.
- **Streamlit Email Prompt**: When starting Streamlit for the first time, you may be asked to provide an email address to receive updates and feedback. This is a standard Streamlit feature and can be safely skipped (leave blank and press Enter).
- **API Connections**: The application will automatically attempt to use the HKBU GenAI Platform for food recognition. If connection issues occur, it will switch to built-in database mode.
- **API Settings**: If needed, you can update your API keys in the "API Settings" section of the sidebar.
- **Language Settings**: The default language is English, which can be changed to Chinese using the language switch button at the top.

## Error Handling
The application includes robust error handling:
- If image upload fails: Clear error messages are provided
- If food recognition fails: Possible causes and suggested actions are provided
- If nutrition data retrieval fails: Falls back to alternative data sources

## Performance Notes
- Image recognition takes 2-5 seconds depending on network conditions
- For best results, use clear, well-lit food images
- The application works best for common foods and standard dishes
- Complex mixed foods may require manual confirmation of recognition results

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- HKBU GenAI Platform for providing AI vision capabilities
- USDA for comprehensive food composition database
- Nutritionix for supplementary nutrition data
- The Streamlit team for an excellent framework
- All contributors and testers for valuable feedback 