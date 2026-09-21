import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Load our trained model
model = joblib.load("models/car_price_model.pkl")
# 2. App Title and Header
st.set_page_config(page_title="Car Value Predictor", page_icon="🚗", layout="centered")
st.title("🚗 Used Car Price Predictor")
st.write("Enter the vehicle specifications below to estimate its current market valuation.")

st.markdown("---")

# 3. Create Inputs for the User
col1, col2 = st.columns(2)

with col1:
    year = st.slider("Year of Manufacture", 2000, 2026, 2015)
    kms_driven = st.number_input("Total Kilometers Driven", min_value=0, max_value=500000, value=30000, step=1000)
    owner = st.selectbox("Number of Previous Owners", [0, 1, 3])

with col2:
    present_price = st.number_input("Original Showroom Price (in Lakhs)", min_value=0.0, max_value=50.0, value=6.0, step=0.5)
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission Type", ["Manual", "Automatic"])

# Calculate Age based on current year 2026
age = 2026 - year

st.markdown("---")

# 4. Process Inputs to Match Model Structure
if st.button("Calculate Estimated Value", use_container_width=True):
    # Map the dropdown values to the 0 and 1 dummy variables your model expects
    fuel_diesel = 1 if fuel_type == "Diesel" else 0
    fuel_petrol = 1 if fuel_type == "Petrol" else 0
    seller_individual = 1 if seller_type == "Individual" else 0
    transmission_manual = 1 if transmission == "Manual" else 0
    
    # Create a matching input array for the model
    # Order must match exactly: Year, Present_Price, Kms_Driven, Owner, Age, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual
    input_data = np.array([[year, present_price, kms_driven, owner, age, fuel_diesel, fuel_petrol, seller_individual, transmission_manual]])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    
    # Deal with edge cases where model predicts a negative number
    if prediction < 0:
        prediction = 0.0
        
    # Display the result beautifully
    st.balloons()
    st.success(f"### Estimated Market Value: ₹ {prediction:.2f} Lakhs")