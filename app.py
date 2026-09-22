import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Page Configuration
st.set_page_config(
    page_title="AutoValuate AI | Car Price Predictor",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS: Tech Luxe Palette & Modern SaaS UI
st.markdown("""
<style>
    /* Tech Luxe Background */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }

    /* Primary Accent Styling (Electric Teal / Mint Green) */
    div.stButton > button:first-child {
        background-color: #00F5D4 !important;
        color: #121212 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:first-child:hover {
        background-color: #00D2B5 !important;
        box-shadow: 0 4px 15px rgba(0, 245, 212, 0.3) !important;
        transform: translateY(-1px);
    }

    /* Soft Container Cards (Dark Slate) */
    .card-container {
        background-color: #1E1E1E;
        border: 1px solid #2D2D2D;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Metric Cards */
    .metric-card {
        background-color: #1E1E1E;
        border: 1px solid #2D2D2D;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .metric-title {
        color: #A0AEC0;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: #00F5D4;
        font-size: 32px;
        font-weight: 700;
        margin-top: 5px;
    }

    .metric-sub {
        color: #A0AEC0;
        font-size: 13px;
        margin-top: 5px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #181818;
        border-right: 1px solid #2D2D2D;
    }
    
    /* Input Labels */
    label {
        color: #A0AEC0 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Model Loading with Cache
@st.cache_resource
def load_model():
    return joblib.load("models/car_price_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error("Model file not found. Ensure `models/car_price_model.pkl` exists in your repository.")
    st.stop()

# 4. Balanced Sidebar Navigation
with st.sidebar:
    st.title("🚘 AutoValuate AI")
    st.caption("AI-Powered Resale Valuation Engine")
    
    st.markdown("---")
    st.subheader("📌 How it works")
    st.markdown("""
    1. Enter the vehicle's manufacturing year and usage history.
    2. Input original showroom price and fuel configuration.
    3. Click **Calculate Market Valuation** to generate an instant ML valuation.
    """)
    
    st.markdown("---")
    st.caption("Powered by Scikit-Learn & Streamlit")

# 5. Header Area (Clear Visual Hierarchy)
st.title("AutoValuate AI: Used Car Price Predictor")
st.markdown("<p style='color: #A0AEC0; font-size: 16px;'>Input vehicle specifications below to evaluate current market valuation and depreciation analysis.</p>", unsafe_allow_html=True)
st.markdown("---")

# 6. Inputs Area wrapped inside a Unified Soft Container Card
st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.subheader("📋 Vehicle Profile")

col1, col2, col3 = st.columns(3)

with col1:
    year = st.slider("Manufacturing Year", 2000, 2026, 2018)
    present_price = st.number_input("Showroom Price (Lakhs ₹)", min_value=0.5, max_value=100.0, value=7.5, step=0.5)

with col2:
    kms_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=35000, step=2500)
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])

with col3:
    owner = st.selectbox("Previous Owners", [0, 1, 2, 3])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

st.markdown('</div>', unsafe_allow_html=True)

age = 2026 - year

# 7. Action Button & Results Display
if st.button("🚀 Calculate Market Valuation", use_container_width=True):
    # Map feature encoding
    fuel_diesel = 1 if fuel_type == "Diesel" else 0
    fuel_petrol = 1 if fuel_type == "Petrol" else 0
    seller_individual = 1 if seller_type == "Individual" else 0
    transmission_manual = 1 if transmission == "Manual" else 0

    input_data = np.array([[year, present_price, kms_driven, owner, age, fuel_diesel, fuel_petrol, seller_individual, transmission_manual]])
    
    # Model Prediction
    prediction = model.predict(input_data)[0]
    if prediction < 0:
        prediction = 0.0

    depreciation_pct = ((present_price - prediction) / present_price) * 100 if present_price > 0 else 0

    st.balloons()
    st.markdown("---")
    st.subheader("📊 Valuation Summary")

    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Estimated Market Price</div>
            <div class="metric-value">₹ {prediction:.2f} L</div>
            <div class="metric-sub">Resale Market Valuation</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Original Showroom Value</div>
            <div class="metric-value" style="color: #FFFFFF;">₹ {present_price:.2f} L</div>
            <div class="metric-sub">Base Reference Price</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Depreciation</div>
            <div class="metric-value" style="color: #FF5353;">{depreciation_pct:.1f}%</div>
            <div class="metric-sub">Over {age} Years</div>
        </div>
        """, unsafe_allow_html=True)