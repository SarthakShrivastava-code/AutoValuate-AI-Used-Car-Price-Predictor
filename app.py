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

# 2. Custom CSS for Styling, Background, and Glassmorphism Cards
st.markdown("""
<style>
    /* Dark subtle background gradient */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #161b22 50%, #0d1117 100%);
    }

    /* Container Card Styling */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div {
        border-radius: 12px;
    }

    /* Metric Cards */
    .metric-card {
        background-color: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .metric-title {
        color: #8b949e;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        color: #2f81f7;
        font-size: 32px;
        font-weight: 700;
        margin-top: 5px;
    }

    .metric-sub {
        color: #3fb950;
        font-size: 14px;
        margin-top: 5px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# 3. Model Loading
@st.cache_resource
def load_model():
    return joblib.load("models/car_price_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error("Model file not found. Ensure `models/car_price_model.pkl` exists in your repository.")
    st.stop()

# 4. Sidebar Information Panel
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/car.png", width=80)
    st.title("AutoValuate AI")
    st.caption("AI-powered resale valuation engine")
    
    st.markdown("---")
    st.subheader("📌 How it works")
    st.markdown("""
    1. Enter the vehicle's manufacturing year and usage history.
    2. Input original showroom price and fuel configuration.
    3. Click **Calculate Valuation** to generate an instant ML market estimate.
    """)
    
    st.markdown("---")
    st.caption("Powered by Scikit-Learn & Streamlit")

# 5. App Header
st.title("🚘 AutoValuate AI: Used Car Price Predictor")
st.write("Input vehicle specifications below to evaluate current market valuation and depreciation analysis.")
st.markdown("---")

# 6. Inputs Section inside Structured Columns & Containers
with st.container():
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

age = 2026 - year

st.markdown("---")

# 7. Valuation Execution & Metric Cards Display
if st.button("🚀 Calculate Market Valuation", use_container_width=True, type="primary"):
    # Encoding dummy variables
    fuel_diesel = 1 if fuel_type == "Diesel" else 0
    fuel_petrol = 1 if fuel_type == "Petrol" else 0
    seller_individual = 1 if seller_type == "Individual" else 0
    transmission_manual = 1 if transmission == "Manual" else 0

    input_data = np.array([[year, present_price, kms_driven, owner, age, fuel_diesel, fuel_petrol, seller_individual, transmission_manual]])
    
    # Model Prediction
    prediction = model.predict(input_data)[0]
    if prediction < 0:
        prediction = 0.0

    # Calculate additional metrics
    depreciation_pct = ((present_price - prediction) / present_price) * 100 if present_price > 0 else 0

    st.balloons()
    
    # Custom Dashboard Metrics Display
    st.subheader("📊 Valuation Results")
    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Estimated Market Price</div>
            <div class="metric-value">₹ {prediction:.2f} L</div>
            <div class="metric-sub">Estimated Resale Value</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Original Showroom Value</div>
            <div class="metric-value" style="color: #e6edf3;">₹ {present_price:.2f} L</div>
            <div class="metric-sub" style="color: #8b949e;">Base Reference Price</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Depreciation</div>
            <div class="metric-value" style="color: #f85149;">{depreciation_pct:.1f}%</div>
            <div class="metric-sub" style="color: #8b949e;">Over {age} Years</div>
        </div>
        """, unsafe_allow_html=True)