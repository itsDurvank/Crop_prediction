import streamlit as st
import numpy as np
import pandas as pd
import joblib
import random
from datetime import datetime
from db import CropDatabase
from PIL import Image
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()



db=CropDatabase()

# Theme settings
st.set_page_config(page_title="Crop Recommendation System", page_icon="🌾", layout="wide")

# Expanded theme options
themes = {
    "Dark": {
        "primaryColor": "#8fce00",
        "backgroundColor": "#0e1117",
        "secondaryBackgroundColor": "#1e2130",
        "textColor": "#fafafa",
        "font": "sans-serif",
        "icon": "🌙"
    },
    "Light": {
        "primaryColor": "#6eb52f",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#262730",
        "font": "sans-serif",
        "icon": "🌱"
    },
    "Earth Tones": {
        "primaryColor": "#8B5A2B",
        "backgroundColor": "#F5F5DC",
        "secondaryBackgroundColor": "#DEB887",
        "textColor": "#3E2723",
        "font": "serif",
        "icon": "🌾"
    },
    "Ocean Blue": {
        "primaryColor": "#1E88E5",
        "backgroundColor": "#E3F2FD",
        "secondaryBackgroundColor": "#BBDEFB",
        "textColor": "#0D47A1",
        "font": "sans-serif",
        "icon": "🌊"
    },
    "Forest Green": {
        "primaryColor": "#2E7D32",
        "backgroundColor": "#E8F5E9",
        "secondaryBackgroundColor": "#C8E6C9",
        "textColor": "#1B5E20",
        "font": "serif",
        "icon": "🌲"
    },
    "Desert Sand": {
        "primaryColor": "#FF8F00",
        "backgroundColor": "#FFF8E1",
        "secondaryBackgroundColor": "#FFECB3",
        "textColor": "#E65100",
        "font": "sans-serif",
        "icon": "🏜️"
    },
    "Berry Purple": {
        "primaryColor": "#8E24AA",
        "backgroundColor": "#F3E5F5",
        "secondaryBackgroundColor": "#E1BEE7",
        "textColor": "#4A148C",
        "font": "cursive",
        "icon": "🍇"
    },
    "Sunrise": {
        "primaryColor": "#FF7043",
        "backgroundColor": "#FFF3E0",
        "secondaryBackgroundColor": "#FFE0B2",
        "textColor": "#D84315",
        "font": "sans-serif",
        "icon": "🌅"
    },
    "Monochrome": {
        "primaryColor": "#424242",
        "backgroundColor": "#FAFAFA",
        "secondaryBackgroundColor": "#EEEEEE",
        "textColor": "#212121",
        "font": "monospace",
        "icon": "⚫"
    },
    "High Contrast": {
        "primaryColor": "#FFEB3B",
        "backgroundColor": "#000000",
        "secondaryBackgroundColor": "#212121",
        "textColor": "#FFFFFF",
        "font": "sans-serif",
        "icon": "👁️"
    }
}

# Sidebar for theme selection
with st.sidebar:
    st.title("Settings")
    selected_theme = st.selectbox("Choose Theme", list(themes.keys()))
    
    # Show theme preview
    theme = themes[selected_theme]
    st.markdown(f"### {theme['icon']} {selected_theme} Theme")
    
    # Preview boxes for the theme colors
    st.markdown("""
    <style>
    .color-box {
        display: inline-block;
        width: 20px;
        height: 20px;
        margin-right: 5px;
        border: 1px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

    # Season-based theme suggestion
   
    current_month = datetime.now().month
    seasonal_style = "background-color: black; color: white; padding: 0.7rem; border-radius: 0.5rem;"

    if 3 <= current_month <= 5:  # Spring
        st.markdown(f"<div style='{seasonal_style}'>🌷 Spring is here! Try the 'Forest Green' or 'Sunrise' theme!</div>", unsafe_allow_html=True)
    elif 6 <= current_month <= 8:  # Summer
        st.markdown(f"<div style='{seasonal_style}'>☀️ Summer vibes! The 'Ocean Blue' or 'Desert Sand' theme might feel refreshing!</div>", unsafe_allow_html=True)
    elif 9 <= current_month <= 11:  # Fall
        st.markdown(f"<div style='{seasonal_style}'>🍂 Fall colors! The 'Earth Tones' or 'Berry Purple' theme matches the season!</div>", unsafe_allow_html=True)
    else:  # Winter
        st.markdown(f"<div style='{seasonal_style}'>❄️ Winter mood! Try the 'Dark' or 'Monochrome' theme!</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    
    
    
    # Initialize Gemini API
 
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    # Load the model
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    # Streamlit app
    st.title("ChatBot 🤖")


    prompt = st.text_input("Enter your prompt:")

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                try:
                    response = model.generate_content(prompt)
                    st.success("Response generated!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt first!")


    # Apply the selected theme
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {theme["backgroundColor"]};
            color: {theme["textColor"]};
            font-family: {theme["font"]}, sans-serif;
        }}
        .stButton button {{
            background-color: {theme["primaryColor"]} !important;
            color: {"#ffffff" if "Dark" in selected_theme or "Contrast" in selected_theme else "#ffffff"} !important;
            font-family: {theme["font"]}, sans-serif;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 15px !important;
            transition: all 0.3s ease !important;
        }}
        .stButton button:hover {{
            opacity: 0.85 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        }}
        .css-1d391kg, .css-12w0qpk {{
            background-color: {theme["secondaryBackgroundColor"]};
            border-radius: 10px;
        }}
        h1, h2, h3 {{
            color: {theme["primaryColor"]};
            font-family: {theme["font"]}, sans-serif;
        }}
        .stAlert {{
            background-color: {theme["secondaryBackgroundColor"]}; 
            border-left-color: {theme["primaryColor"]} !important;
        }}
        .stTextInput, .stNumberInput {{
            border-radius: 8px;
        }}
        .stSlider div[data-baseweb="slider"] {{
            background-color: {theme["secondaryBackgroundColor"]};
        }}
        .stSlider [data-testid="stThumbValue"] {{
            background-color: {theme["primaryColor"]};
        }}
        
        </style>
    """, unsafe_allow_html=True)

# Load the trained model and scalers
try:
    model = joblib.load('models/crop_recommendation_model.pkl')
    minmax_scaler = joblib.load('models/minmax_scaler.pkl')
    standard_scaler = joblib.load('models/standard_scaler.pkl')
except:
    st.error("⚠️ Model files not found. This is a UI demo only. Prediction functionality will not work.")
    # Create dummy functions for demo purposes
    class DummyModel:
        def predict(self, X):
            return [random.randint(1, 22)]
    class DummyScaler:
        def transform(self, X):
            return X
    model = DummyModel()
    minmax_scaler = DummyScaler()
    standard_scaler = DummyScaler()

# Crop number to name mapping
crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

# App title and description with theme icon
st.title(f"🌾 Crop Recommendation System")
# st.markdown("This intelligent system analyzes soil and climate parameters to recommend the most suitable crop for optimal yield.")


# Create two columns for input parameters
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧪 Soil Parameters")
    with st.container():
        st.markdown("""
            <style>
            .parameter-container {
                background-color: rgba(0,0,0,0.05);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                 
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='textcolor: {theme["primaryColor"]}'>Nitrogen (N) content in soil</div>", unsafe_allow_html=True)
        N = st.number_input(" ", value=80, min_value=0, max_value=140, 
                           help="Nitrogen is essential for leaf growth and protein formation")
        st.markdown(f"<div style='textcolor: {theme["primaryColor"]}'>Phosphorus (P) content in soil</div>", unsafe_allow_html=True)
        P = st.number_input(" ", value=60, min_value=0, max_value=145,
                           help="Phosphorus helps in root development and flowering")
        st.markdown(f"<div style='textcolor: {theme["primaryColor"]}'>Potassium (K) content in soil</div>", unsafe_allow_html=True)
        K = st.number_input(" ", value=60, min_value=0, max_value=205,
                           help="Potassium is important for overall plant health and disease resistance")
        st.markdown(f"<div style='textcolor: {theme["primaryColor"]}'>Soil pH level</div>", unsafe_allow_html=True)
        ph = st.number_input(" ", value=6.5, min_value=0.0, max_value=14.0, step=0.1,
                            help="pH affects nutrient availability in soil. 7 is neutral, below 7 is acidic, above 7 is alkaline")

with col2:
    
    st.markdown("### ☁️ Climate Parameters")
    with st.container():
        st.markdown(f"<div style='padding: 12px'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='textcolor: {theme["primaryColor"]}'>Temperature (°C)</div>", unsafe_allow_html=True)
        temperature = st.number_input(" ", value=25.0, min_value=0.0, max_value=50.0, step=0.1,
                                     help="Average temperature in the region")
        st.markdown(f"<div style='textcolor: {theme["primaryColor"]}'>Humidity (%)</div>", unsafe_allow_html=True)
        humidity = st.slider(" ", 0.0, 100.0, 80.0, 
                            help="Average relative humidity in the air")
        st.markdown(f"<div style='textcolor: {theme["primaryColor"]}'>Annual Rainfall (mm)</div>", unsafe_allow_html=True)
        rainfall = st.number_input(" ", value=200.0, min_value=0.0, max_value=3000.0, step=10.0,
                                  help="Total rainfall in the region per year")
        




st.markdown(f"<div style='textcolor: {theme["primaryColor"]}; text-align: center; '>🤖 This intelligent system analyzes soil and climate parameters to recommend the most suitable crop for optimal yield.</div>", unsafe_allow_html=True)
# Add a divider
st.markdown("---")

def load_crop_image(crop_name):
    try:
        # Get the image filename from crop_info
        image_file = crop_info.get(crop_name, {}).get("image", "")
        if not image_file:
            return None
        
        # Construct the full path - adjust this to your actual path
        image_path = f"images/{image_file}"
        
        # Open and return the image
        return Image.open(image_path)
    except Exception as e:
        st.warning(f"Could not load image for {crop_name}: {str(e)}")
        return None

# Center the button and add animation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("🔍 Analyze and Recommend Crop", use_container_width=True)

#crop_info dictionary holds all the crops info
crop_info = {
    "Rice": {
        "description": "Rice thrives in warm, humid environments with abundant water.",
        "ideal_conditions": "Temperature: 20-35°C, pH: 5.5-6.5, High rainfall",
        "growth_period": "3-6 months depending on variety",
        "fun_fact": "Rice feeds more than half of the world's population daily.",
        "image": "Rice.jpg"
    },
    "Maize": {
        "description": "Maize requires moderate temperatures and well-drained soils.",
        "ideal_conditions": "Temperature: 18-32°C, pH: 5.8-7.0, Moderate rainfall",
        "growth_period": "70-210 days depending on variety",
        "fun_fact": "Corn (maize) is grown on every continent except Antarctica.",
        "image": "Maize.jpg"
    },
    "Cotton": {
        "description": "Cotton grows best in warm climates with moderate rainfall.",
        "ideal_conditions": "Temperature: 21-35°C, pH: 5.5-8.5, Moderate rainfall",
        "growth_period": "150-180 days",
        "fun_fact": "One cotton boll contains approximately 500,000 fibers.",
        "image": "Cotton.jpg"
    },
    "Apple": {
        "description": "Apples need cool temperatures and well-drained soil.",
        "ideal_conditions": "Temperature: 10-25°C, pH: 6.0-7.0, Moderate rainfall",
        "growth_period": "100-200 days to maturity after flowering",
        "fun_fact": "It takes about 36 apples to create one gallon of apple cider.",
        "image": "Apple.jpg"
    },
    "Jute": {
        "description": "Jute is a rain-fed crop that grows best in warm, humid climates.",
        "ideal_conditions": "Temperature: 24-37°C, pH: 6.0-7.5, High rainfall (1200-2500mm)",
        "growth_period": "120-150 days",
        "fun_fact": "Jute is often called the 'golden fiber' and is the second most important vegetable fiber after cotton.",
        "image": "Jute.jpg"
    },
    "Coconut": {
        "description": "Coconut palms thrive in tropical coastal regions with sandy soil.",
        "ideal_conditions": "Temperature: 27-35°C, pH: 5.5-7.0, Rainfall: 1500-2500mm",
        "growth_period": "12-15 months for first fruit, productive for 60-80 years",
        "fun_fact": "A coconut palm can produce up to 75 fruits per year and continue producing for up to 80 years.",
        "image": "Coconut.jpg"
    },
    "Papaya": {
        "description": "Papaya grows rapidly in tropical and subtropical regions.",
        "ideal_conditions": "Temperature: 22-30°C, pH: 6.0-7.0, Moderate rainfall with good drainage",
        "growth_period": "10-12 months from planting to first harvest",
        "fun_fact": "Papaya enzymes (papain) are used as meat tenderizers and in brewing beer.",
        "image": "Papaya.jpg"
    },
    "Orange": {
        "description": "Oranges require warm days and cool nights for optimal color and taste.",
        "ideal_conditions": "Temperature: 15-30°C, pH: 5.5-6.5, Moderate rainfall",
        "growth_period": "5-18 months from flowering to harvest",
        "fun_fact": "The flavor of oranges depends more on the ratio of sugar to acid than on the amount of sugar alone.",
        "image": "Orange.jpg"
    },
    "Muskmelon": {
        "description": "Muskmelons require hot, dry conditions with plenty of sunlight.",
        "ideal_conditions": "Temperature: 24-32°C, pH: 6.0-7.0, Low to moderate rainfall",
        "growth_period": "80-120 days from planting to harvest",
        "fun_fact": "Muskmelons are actually a type of berry botanically speaking.",
        "image": "Muskmelon.jpg"
    },
    "Watermelon": {
        "description": "Watermelons need long, hot growing seasons with plenty of space.",
        "ideal_conditions": "Temperature: 18-35°C, pH: 6.0-7.0, Moderate rainfall",
        "growth_period": "80-110 days from planting to harvest",
        "fun_fact": "Despite being 92% water, watermelon is rich in lycopene, an antioxidant that gives it its red color.",
        "image": "Watermelon.jpg"
    },
    "Grapes": {
        "description": "Grapes thrive in temperate climates with long, warm summers.",
        "ideal_conditions": "Temperature: 15-25°C, pH: 5.5-7.0, Low to moderate rainfall",
        "growth_period": "3 years to full production, harvest 150-180 days after flowering",
        "fun_fact": "There are over 10,000 varieties of wine grapes worldwide.",
        "image": "Grapes.jpg"
    },
    "Mango": {
        "description": "Mangoes require tropical conditions with a distinct dry season.",
        "ideal_conditions": "Temperature: 24-30°C, pH: 5.5-7.5, Moderate rainfall with dry period before flowering",
        "growth_period": "3-5 months from flowering to harvest, trees produce for 40+ years",
        "fun_fact": "Mango trees can grow to be 100 feet tall and live for over 300 years.",
        "image": "Mango.jpg"
    },
    "Banana": {
        "description": "Bananas thrive in humid tropical conditions with protection from wind.",
        "ideal_conditions": "Temperature: 27-30°C, pH: 5.5-7.0, High rainfall (1200-2200mm)",
        "growth_period": "9-12 months from planting to harvest",
        "fun_fact": "Bananas are berries, and the banana plant is actually a giant herb, not a tree.",
        "image": "Banana.jpg"
    },
    "Pomegranate": {
        "description": "Pomegranates need hot, dry summers and cool winters.",
        "ideal_conditions": "Temperature: 18-35°C, pH: 5.5-7.2, Low rainfall during fruiting",
        "growth_period": "5-7 months from flowering to harvest",
        "fun_fact": "A single pomegranate can contain up to 1,400 seeds, each surrounded by edible pulp.",
        "image": "Pomegranate.jpg"
    },
    "Lentil": {
        "description": "Lentils are cool-season crops that tolerate drought conditions.",
        "ideal_conditions": "Temperature: 18-30°C, pH: 6.0-8.0, Low to moderate rainfall",
        "growth_period": "80-110 days from planting to harvest",
        "fun_fact": "Lentils are one of the oldest cultivated crops, dating back to 8000 BCE.",
        "image": "Lentil.jpg"
    },
    "Blackgram": {
        "description": "Blackgram (urad dal) is a tropical legume that fixes nitrogen in soil.",
        "ideal_conditions": "Temperature: 25-35°C, pH: 6.5-7.5, Moderate rainfall",
        "growth_period": "90-120 days from planting to harvest",
        "fun_fact": "Blackgram is used to make the popular South Indian dish 'idli' and 'dosa'.",
        "image": "Blackgram.jpg" 
    },
    "Mungbean": {
        "description": "Mungbean is a warm-season legume that grows quickly in hot conditions.",
        "ideal_conditions": "Temperature: 28-30°C, pH: 6.2-7.2, Moderate rainfall",
        "growth_period": "60-90 days from planting to harvest",
        "fun_fact": "Mungbean sprouts can grow up to 10 times their original weight in just a few days.",
        "image": "Mungbean.jpg"
    },
    "Mothbeans": {
        "description": "Mothbeans are extremely drought-resistant legumes for arid regions.",
        "ideal_conditions": "Temperature: 25-35°C, pH: 6.5-7.5, Low rainfall (300-800mm)",
        "growth_period": "75-90 days from planting to harvest",
        "fun_fact": "Mothbeans can thrive in areas where most other crops would fail due to drought.",
        "image": "Mothbeans.jpg"
    },
    "Pigeonpeas": {
        "description": "Pigeonpeas are perennial legumes that can grow in poor soil conditions.",
        "ideal_conditions": "Temperature: 20-35°C, pH: 5.0-7.0, Moderate rainfall",
        "growth_period": "120-180 days for early varieties, up to 280 days for late varieties",
        "fun_fact": "Pigeonpea plants can fix up to 235 kg of nitrogen per hectare in the soil.",
        "image": "Pigeonpeas.jpg"
    },
    "Kidneybeans": {
        "description": "Kidneybeans prefer warm days and cool nights with consistent moisture.",
        "ideal_conditions": "Temperature: 18-25°C, pH: 6.0-7.5, Moderate, consistent rainfall",
        "growth_period": "85-115 days from planting to harvest",
        "fun_fact": "Kidney beans must be thoroughly cooked as they contain a toxin called phytohemagglutinin when raw.",
        "image": "Kidneybeans.jpg"
    },
    "Chickpea": {
        "description": "Chickpeas are cool-season legumes that can tolerate drought once established.",
        "ideal_conditions": "Temperature: 18-29°C, pH: 6.0-8.0, Low to moderate rainfall",
        "growth_period": "90-180 days depending on variety and climate",
        "fun_fact": "Chickpeas are one of the earliest cultivated legumes, dating back about 7,500 years.",
        "image": "Chickpea.jpg"
    },
    "Coffee": {
        "description": "Coffee thrives in tropical highlands with moderate temperatures.",
        "ideal_conditions": "Temperature: 15-24°C, pH: 6.0-6.5, Moderate rainfall (1500-2000mm)",
        "growth_period": "3-4 years to first harvest, then annually for 25+ years",
        "fun_fact": "It takes about 4,000 hand-picked coffee beans to make one pound of coffee.",
        "image": "Coffee.jpg"
    }
}

# Default information for crops not in the database
default_info = {
    "description": "This crop has specific soil and climate requirements for optimal growth.",
    "ideal_conditions": "Varies based on variety and region",
    "growth_period": "Varies based on variety and climate",
    "fun_fact": "Agriculture has been practiced by humans for over 10,000 years."
}

# Then in the predict button section, update the info retrieval and report generation:
if predict_button:
    # Show spinner while processing
    with st.spinner("📊 Analyzing soil and climate parameters..."):
        # Artificial delay for visual effect
        import time
        time.sleep(1.5)

        #called from db.py
        soil_data_id = db.add_data( N, P, K, ph, temperature, humidity, rainfall)
        
        # Prepare the input
        user_input = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        try:
            # Apply the scalers
            scaled_input = minmax_scaler.transform(user_input)
            scaled_input = standard_scaler.transform(scaled_input)

            # Predict
            prediction = model.predict(scaled_input)[0]
            
            
            # Show result
            crop_name = crop_dict.get(prediction, "Unknown Crop")

            db.add_prediction(soil_data_id, crop_name)
            
            # Get crop info - ensure we get the right info
            crop_specific_info = crop_info.get(crop_name, default_info)
            
            # Create result display with tabs
            st.markdown(f"## Result: {crop_name}")
            
            # Display tabs with information
            tab1, tab2, tab3 = st.tabs(["📝 Description", "🌡️ Growing Conditions", "ℹ️ Additional Info"])
            
            with tab1:
                st.markdown(f"### About {crop_name}")
                st.write(crop_specific_info["description"])
                st.success(f"✅ {crop_name} is the recommended crop for your specified soil and climate parameters.")
                
                # Add the image below the existing content
                crop_image = load_crop_image(crop_name)
                if crop_image:
                    crop_image = crop_image.resize((400, 300))  # (width, height) in pixels
                    st.image(crop_image)
                else:
                    st.warning(f"Image not available for {crop_name}")
            
            with tab2:
                st.markdown("### Ideal Growing Conditions")
                st.write(crop_specific_info["ideal_conditions"])
                
                # Compare user inputs with ideal conditions
                st.markdown("### Your Parameters")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Temperature", f"{temperature}°C")
                    st.metric("Humidity", f"{humidity}%")
                with col2:
                    st.metric("pH", f"{ph}")
                    st.metric("Rainfall", f"{rainfall} mm")
                with col3:
                    st.metric("Nitrogen", f"{N}")
                    st.metric("Phosphorus", f"{P}")
                    st.metric("Potassium", f"{K}")
            
            with tab3:
                st.markdown("### Growth Information")
                st.write(f"**Growth Period**: {crop_specific_info['growth_period']}")
                st.info(f"**Fun Fact**: {crop_specific_info['fun_fact']}")
                
                # Add a download button for a report - with explicit crop-specific info
                report_text = f"""# {crop_name} : Recommendation Report

## Recommended Crop 
- Recommended Crop🌾for this conditioning : {crop_name}            
                
## Soil Parameters
- Nitrogen (N): {N}
- Phosphorus (P): {P}
- Potassium (K): {K}
- pH: {ph}

## Climate Parameters
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Rainfall: {rainfall} mm

## Crop Information
{crop_specific_info['description']}

### Ideal Growing Conditions
{crop_specific_info['ideal_conditions']}

### Growth Period
{crop_specific_info['growth_period']}

### Fun Fact
{crop_specific_info['fun_fact']}

Report generated on {datetime.now().strftime('%Y-%m-%d')}
"""
                
                st.download_button(
                    label="📥 Download Crop Report",
                    data=report_text,
                    file_name=f"{crop_name.lower()}_recommendation_report.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
            st.info("This might be a UI demonstration mode. In a production environment, ensure all model files are correctly loaded.")




# Add a footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8em;">
    Crop Recommendation System | Powered by Machine Learning | Data-Driven Agriculture | Mini project for PRPCEM
</div>
""", unsafe_allow_html=True)
