# AutoValuate AI: Used Car Price Predictor

An end-to-end Machine Learning project that analyzes historical used car sales data and predicts resale prices based on key vehicle attributes.

## Overview

- **Data Exploration & Analysis (`eda.ipynb`)**: Exploratory Data Analysis, feature selection, and data cleaning on used car datasets.
- **Model Training**: Regression models predict valuation metrics using year, mileage, fuel type, transmission, and seller type.
- **Application (`app.py`)**: A Streamlit interface for entering vehicle specifications and receiving an estimated resale price.

## Tech Stack

- **Language**: Python 3
- **Data Analysis**: Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning**: Scikit-Learn
- **Model Storage**: Joblib
- **Application Framework**: Streamlit

## Setup & Execution

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR-USERNAME/AutoValuate-AI-Used-Car-Price-Predictor.git
   cd AutoValuate-AI-Used-Car-Price-Predictor
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run exploratory analysis:**

   Open `eda.ipynb` in Jupyter Notebook or VS Code to view the data exploration, visualizations, and model training workflow.

4. **Run the application:**

   ```bash
   streamlit run app.py
   ```

> **Model path note:** `app.py` currently loads the trained model from a local absolute path. Update that path to the location of `car_price_model.pkl` on your machine before running the app.

## Push to GitHub

After creating a repository named `AutoValuate-AI-Used-Car-Price-Predictor` on GitHub, run:

```bash
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AutoValuate-AI-Used-Car-Price-Predictor.git
git push -u origin main
```