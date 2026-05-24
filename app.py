import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Soft Swirl Sales Predictor",
    page_icon="🍦",
    layout="wide"
)

# Custom CSS for branding
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF69B4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🍦 Soft Swirl Islamabad</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ice Cream Sales Predictor</p>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("📊 Prediction Parameters")

# Input parameters
temperature = st.sidebar.slider("Temperature (°C)", 15, 45, 30, help="Average daily temperature")
humidity = st.sidebar.slider("Humidity (%)", 20, 90, 50, help="Average daily humidity")
day_of_week = st.sidebar.selectbox("Day of Week", 
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
is_weekend = day_of_week in ["Saturday", "Sunday"]
is_holiday = st.sidebar.checkbox("Public Holiday", help="Is it a public holiday?")
month = st.sidebar.selectbox("Month", 
    ["January", "February", "March", "April", "May", "June", 
     "July", "August", "September", "October", "November", "December"])

# Simple prediction model (you can replace this with a trained ML model)
def predict_sales(temp, humid, is_weekend, is_holiday, month):
    # Base sales
    base_sales = 100
    
    # Temperature effect (higher temp = more sales)
    temp_factor = (temp - 20) * 8
    
    # Humidity effect (lower humidity = more sales)
    humidity_factor = (70 - humid) * 2
    
    # Weekend boost
    weekend_boost = 150 if is_weekend else 0
    
    # Holiday boost
    holiday_boost = 200 if is_holiday else 0
    
    # Summer months boost
    summer_months = ["May", "June", "July", "August"]
    season_boost = 100 if month in summer_months else 0
    
    # Calculate predicted sales
    predicted = base_sales + temp_factor + humidity_factor + weekend_boost + holiday_boost + season_boost
    
    # Add some randomness
    predicted = max(50, predicted + np.random.normal(0, 20))
    
    return round(predicted)

# Predict button
if st.sidebar.button("🔮 Predict Sales", type="primary"):
    predicted_sales = predict_sales(temperature, humidity, is_weekend, is_holiday, month)
    
    # Display prediction
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Predicted Sales", f"{predicted_sales} units", 
                 delta=f"{predicted_sales - 200} vs avg")
    
    with col2:
        revenue = predicted_sales * 250  # Assuming 250 PKR per unit
        st.metric("Expected Revenue", f"PKR {revenue:,}", 
                 delta_color="normal")
    
    with col3:
        profit_margin = 0.4
        profit = revenue * profit_margin
        st.metric("Estimated Profit", f"PKR {profit:,.0f}", 
                 delta_color="normal")
    
    # Visualization
    st.markdown("---")
    st.subheader("📈 Sales Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature vs Sales chart
        temp_range = np.arange(15, 46, 1)
        sales_by_temp = [predict_sales(t, humidity, is_weekend, is_holiday, month) for t in temp_range]
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=temp_range, 
            y=sales_by_temp,
            mode='lines+markers',
            name='Predicted Sales',
            line=dict(color='#FF69B4', width=3),
            marker=dict(size=6)
        ))
        fig1.add_vline(x=temperature, line_dash="dash", line_color="red", 
                      annotation_text="Current Temp")
        fig1.update_layout(
            title="Sales vs Temperature",
            xaxis_title="Temperature (°C)",
            yaxis_title="Sales (units)",
            hovermode='x'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Weekly sales pattern
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekly_sales = []
        for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
            is_wknd = day in ["Saturday", "Sunday"]
            sales = predict_sales(temperature, humidity, is_wknd, False, month)
            weekly_sales.append(sales)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=days,
            y=weekly_sales,
            marker_color=['#667eea' if i < 5 else '#FF69B4' for i in range(7)],
            text=weekly_sales,
            textposition='outside'
        ))
        fig2.update_layout(
            title="Weekly Sales Pattern",
            xaxis_title="Day of Week",
            yaxis_title="Sales (units)"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
    recommendations = []
    
    if temperature > 35:
        recommendations.append("🔥 High temperature alert! Stock up on inventory.")
    if is_weekend:
        recommendations.append("📅 Weekend boost expected. Consider extra staff.")
    if is_holiday:
        recommendations.append("🎉 Holiday sales! Prepare for high demand.")
    if predicted_sales > 300:
        recommendations.append("📈 High sales predicted. Ensure adequate supply chain.")
    if humidity > 70:
        recommendations.append("💧 High humidity may reduce sales. Plan promotions.")
    
    if recommendations:
        for rec in recommendations:
            st.info(rec)
    else:
        st.success("✅ Normal sales conditions expected.")

else:
    # Show sample data when prediction hasn't been made
    st.info("👈 Set your parameters in the sidebar and click 'Predict Sales' to see results!")
    
    # Sample historical data visualization
    st.subheader("📊 Sample Historical Data")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', end='2024-05-24', freq='D')
    sample_temps = np.random.randint(20, 40, size=len(dates))
    sample_sales = [predict_sales(t, 50, False, False, "April") for t in sample_temps]
    
    df = pd.DataFrame({
        'Date': dates,
        'Temperature': sample_temps,
        'Sales': sample_sales
    })
    
    fig = px.line(df, x='Date', y='Sales', 
                  title='Historical Sales Trend (Sample Data)',
                  labels={'Sales': 'Units Sold'})
    fig.update_traces(line_color='#FF69B4')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🍦 Soft Swirl Islamabad - Your Premium Ice Cream Destination</p>
        <p style='font-size: 0.9rem;'>Predictions are estimates based on historical patterns and weather conditions.</p>
    </div>
""", unsafe_allow_html=True)
