# Food Calorie Estimator

## Project Overview
An AI-powered application that allows users to upload images of food and get estimated calorie information. The app identifies food items using computer vision AI and retrieves nutritional information from multiple sources.

## Features
- **Food Recognition**: Upload food images and let AI identify the food items
- **Calorie Estimation**: Get accurate calorie information for identified foods
- **Detailed Nutrition Information**: View comprehensive nutritional details including macronutrients
- **Multi-source Data**: Access nutrition data from USDA, Nutritionix, and a built-in database
- **Visualization**: Interactive charts showing macronutrient distribution
- **Search History**: Keep track of your previous food searches
- **Modern UI**: Beautiful, responsive interface with intuitive design
- **Offline Mode**: Continue using the app even when API services are unavailable

## Target Users
- Health-conscious individuals tracking their food intake
- Fitness enthusiasts monitoring their diet
- Nutritionists and dietitians
- Anyone curious about the calorie content of food

## Technical Implementation
This project is built using:
- **Streamlit**: For creating the interactive web interface
- **HKBU GenAI Platform**: For AI-powered food recognition using gpt-4-o-mini model
- **Python**: Backend programming language
- **Pandas**: For data processing and transformation
- **Plotly**: For creating interactive visualizations
- **USDA Food Database API**: For nutrition data
- **Nutritionix API**: For supplemental nutrition information

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
│   │   └── image_utils.py  # Utilities for image processing
│   └── data/
│       └── food_calories.py # Built-in database of food calories
├── uploads/                # Directory for uploaded images
├── run_app.py              # Application starter script
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Usage Guide
1. Start the application using `python run_app.py`
2. Upload a food image using the file uploader
3. Click the "Analyze Food Calories" button
4. View the identified food and calorie information
5. Explore detailed nutrition information by clicking "Show Nutrition Details"
6. Your search history is saved in the sidebar for easy reference

## First-time Use Considerations
- **Streamlit Email Prompt**: When starting Streamlit for the first time, you may be asked for an email address to receive updates and feedback. This is a standard Streamlit feature and can be safely skipped (leave blank and press Enter).
- **API Connections**: The app will automatically attempt to use the HKBU GenAI Platform for food recognition. If connection issues occur, it will switch to the built-in database mode.
- **API Settings**: You can update your API key in the sidebar's "API Settings" section if needed.

## Error Handling
The application includes robust error handling:
- If image upload fails: Provides clear error messages
- If food recognition fails: Offers potential reasons and suggested actions
- If nutrition data retrieval fails: Falls back to alternative data sources

## Performance Notes
- Image recognition takes 2-5 seconds depending on network conditions
- For optimal results, use clear, well-lit food images
- The app works best with common food items and standard dishes

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- HKBU GenAI Platform for providing the AI vision capabilities
- USDA for their comprehensive food composition database
- Nutritionix for supplementary nutrition data
- The Streamlit team for their excellent framework 