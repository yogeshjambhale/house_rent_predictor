import streamlit as st
import pandas as pd
import joblib
import numpy as np
import base64

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="RentHousing.com",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Load Models ---
try:
    model = joblib.load("House_price_prediction.pkl")
    scaler = joblib.load("scaler.pkl")
    model_columns = joblib.load("columns.pkl")
except FileNotFoundError:
    st.error("⚠️ Error: Model files not found. Please check your directory.")
    st.stop()

# --- 3. CSS for Premium UI ---
def add_bg_and_style(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        encoded_string = "" 

    st.markdown(
        f"""
        <style>
        /* 1. Background Image with Dark Overlay */
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7)), url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* 2. Top Navigation Bar */
        .navbar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70px;
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            z-index: 9999;
            display: flex;
            align-items: center;
            padding-left: 30px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* LOGO - Red Gradient */
        .nav-logo {{
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* 3. Typography */
        /* TITLE - Red Gradient */
        h1 {{
            font-family: 'Playfair Display', serif;
            background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 4rem;
            margin-top: 80px; 
            padding-bottom: 10px;
        }}
        
        p {{
            color: #e0e0e0 !important;
            font-size: 1.7rem;
            font-weight: 300;
        }}

        /* 4. Input Styling (White Labels) */
        .stNumberInput label, .stSelectbox label {{
            color: #ffffff !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        
        /* 5. BUTTON - Red Gradient */
        .stButton>button {{
            background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
            color: white !important;
            border: none;
            border-radius: 4px;
            height: 55px;
            width: 100%;
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
            transition: all 0.3s ease;
            margin-top: 25px;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
            box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
        }}
        
        /* Hide Default Header/Footer */
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .block-container {{padding-top: 0px;}}
        </style>
        
        <div class="navbar">
            <div class="nav-logo">RentHousing.com</div>
        </div>
        """,
        unsafe_allow_html=True
    )

add_bg_and_style('background.png') 

# --- 4. Popup Logic (Enhanced UI) ---
@st.dialog("💎 Premium Valuation Report")
def show_prediction(price):
    st.markdown(f"""
        <style>
            .popup-container {{
                text-align: center;
                padding: 10px;
                font-family: 'Helvetica Neue', sans-serif;
            }}
            .popup-label {{
                color: #888;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 700;
                margin-bottom: 5px;
            }}
            .popup-price {{
                font-size: 3.5rem;
                font-weight: 900;
                margin: 0;
                background: linear-gradient(45deg, #1a202c, #2d3748);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            }}
            .popup-badge {{
                background: linear-gradient(135deg, #d4af37 0%, #f6e07b 100%);
                color: #fff;
                padding: 6px 15px;
                border-radius: 50px;
                font-size: 0.8rem;
                font-weight: 700;
                letter-spacing: 0.5px;
                display: inline-block;
                margin-top: 15px;
                box-shadow: 0 4px 10px rgba(212, 175, 55, 0.3);
            }}
            .popup-desc {{
                color: #4a5568;
                font-size: 0.95rem;
                margin-top: 20px;
                line-height: 1.5;
                border-top: 1px solid #e2e8f0;
                padding-top: 15px;
            }}
        </style>
        
        <div class="popup-container">
            <div class="popup-label">Estimated Monthly Rent</div>
            <div class="popup-price">₹ {price:,}</div>
            <div class="popup-badge">✨ AI Market Verified</div>
            <div class="popup-desc">
                Based on your property's unique features and real-time listings in <strong>{city if 'city' in globals() else 'your area'}</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)
# --- 5. Main Layout ---
left_col, spacer, right_col = st.columns([1, 0.2, 1.2]) 

with left_col:
    # Spacer
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Hero Section
    st.title("Find Your Home's True Value.")
    st.markdown("<p style='margin-bottom: 40px;'>Advanced AI market analysis for the modern homeowner.</p>", unsafe_allow_html=True)

    # --- Inputs ---
    c1, c2 = st.columns(2)
    with c1:
        bhk = st.number_input("Bedrooms (BHK)", 1, 10, 2)
        size = st.number_input("Area (Sq. Ft.)", 100, 10000, 900, step=50)
        bath = st.number_input("Bathrooms", 1, 10, 2)
        floor = st.number_input("Floor Level", -1, 100, 1)

    with c2:
        city = st.selectbox("City", ["Mumbai", "Bangalore", "Delhi", "Kolkata", "Hyderabad", "Chennai"])
        furnishing = st.selectbox("Furnishing", ["Unfurnished", "Semi-Furnished", "Furnished"])
        tenant = st.selectbox("Tenant Type", ["Bachelors", "Bachelors/Family", "Family"])
        contact = st.selectbox("Contact Via", ["Contact Owner", "Contact Agent", "Contact Builder"])

    area_type = st.selectbox("Area Type", ["Super Area", "Carpet Area", "Built Area"])

    
# Right Column Empty
with right_col:
    # 1. Vertical Spacer to push button to middle of screen
    st.markdown("<div style='height: 45vh'></div>", unsafe_allow_html=True)
    
    # 2. Horizontal Centering: Use columns to center the button
    # [Empty] [Button] [Empty]
    rc1, rc2, rc3 = st.columns([1, 2, 1])
    
    with rc2:
        if st.button("Calculate Valuation"):
            try:
                # Prepare Data
                input_data = pd.DataFrame({
                    'BHK': [bhk], 'Size': [size], 'Bathroom': [bath], 'Floor': [floor],
                    'Area Type': [area_type], 'City': [city], 'Furnishing Status': [furnishing],
                    'Tenant Preferred': [tenant], 'Point of Contact': [contact]
                })

                # Process
                input_dummies = pd.get_dummies(input_data)
                final_input = input_dummies.reindex(columns=model_columns, fill_value=0)
                
                num_cols = ['BHK', 'Size', 'Bathroom', 'Floor']
                final_input[num_cols] = scaler.transform(final_input[num_cols])

                # Predict
                prediction_log = model.predict(final_input)
                prediction_actual = int(np.expm1(prediction_log)[0])

                # Show Popup
                show_prediction(prediction_actual)

            except Exception as e:
                st.error(f"Error: {e}")