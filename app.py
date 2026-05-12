import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re

# 1. Page Config
st.set_page_config(page_title="📱 Mobile Phones EDA 2025", layout="wide", page_icon="📱")

# Helper function to clean numeric values dynamically
def clean_numeric(val):
    if pd.isna(val):
        return np.nan
    # Extract digits and decimal point
    matches = re.findall(r'\d+\.?\d*', str(val).replace(',', ''))
    if matches:
        return float(matches[0])
    return np.nan

@st.cache_data
def load_data():
    try:
        # Load the specified dataset
        df = pd.read_csv("Mobiles Dataset (2025).csv", encoding='latin-1')
    except FileNotFoundError:
        st.error("Dataset 'Mobiles Dataset (2025).csv' not found. Please ensure it is in the same directory.")
        st.stop()
        
    # Dynamically find column names
    company_col = next((c for c in df.columns if 'company' in c.lower() or 'brand' in c.lower()), None)
    ram_col = next((c for c in df.columns if 'ram' in c.lower()), None)
    battery_col = next((c for c in df.columns if 'battery' in c.lower()), None)
    price_cols = [c for c in df.columns if 'price' in c.lower()]
    price_col = price_cols[0] if price_cols else None
    
    # Pre-process numeric versions of features for KPIs & Plotting
    num_cols_map = {}
    if ram_col:
        df[ram_col + '_num'] = df[ram_col].apply(clean_numeric)
        num_cols_map['ram'] = ram_col + '_num'
    if battery_col:
        df[battery_col + '_num'] = df[battery_col].apply(clean_numeric)
        num_cols_map['battery'] = battery_col + '_num'
    if price_col:
        df[price_col + '_num'] = df[price_col].apply(clean_numeric)
        num_cols_map['price'] = price_col + '_num'
        
    return df, company_col, ram_col, battery_col, price_col, num_cols_map

df, company_col, ram_col, battery_col, price_col, num_cols_map = load_data()

# App Title
st.title("📱 Mobile Phones Exploratory Data Analysis 2025")
st.markdown("Explore trends in mobile phone specifications, prices, and hardware configurations.")

# 2. Sidebar Filters
st.sidebar.header("Filters")
selected_companies = []
if company_col:
    # Handle mixed types or NaNs
    companies = [str(c) for c in df[company_col].dropna().unique()]
    selected_companies = st.sidebar.multiselect("Filter by Company", sorted(companies), default=companies)

selected_rams = []
if ram_col:
    # Handle mixed types or NaNs
    rams = [str(r) for r in df[ram_col].dropna().unique()]
    selected_rams = st.sidebar.multiselect("Filter by RAM", sorted(rams), default=rams)

# Apply filters
filtered_df = df.copy()
if company_col and selected_companies:
    filtered_df = filtered_df[filtered_df[company_col].astype(str).isin(selected_companies)]
if ram_col and selected_rams:
    filtered_df = filtered_df[filtered_df[ram_col].astype(str).isin(selected_rams)]

# 3. KPI Metrics Row
st.markdown("### Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Phones Analyzed", len(filtered_df))
    
with col2:
    if 'price' in num_cols_map:
        avg_price = filtered_df[num_cols_map['price']].mean()
        st.metric(f"Avg Price ({price_col})", f"{avg_price:,.2f}")
    else:
        st.metric("Avg Price", "N/A")
        
with col3:
    if 'battery' in num_cols_map:
        avg_battery = filtered_df[num_cols_map['battery']].mean()
        st.metric("Avg Battery Capacity", f"{avg_battery:,.0f} mAh")
    else:
        st.metric("Avg Battery", "N/A")
        
with col4:
    if 'ram' in num_cols_map:
        avg_ram = filtered_df[num_cols_map['ram']].mean()
        st.metric("Avg RAM Size", f"{avg_ram:.1f} GB")
    else:
        st.metric("Avg RAM", "N/A")

st.markdown("---")

# 4. Tab Layout
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Price Analysis", "Hardware", "Correlations"])

# Original columns to show without the temporary numeric ones
display_cols = [c for c in df.columns if c not in num_cols_map.values()]

with tab1:
    st.subheader("Dataset Overview")
    search_query = st.text_input("🔍 Search within data (e.g., specific model name)")
    
    display_df = filtered_df[display_cols]
    if search_query:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        st.dataframe(display_df[mask], use_container_width=True)
    else:
        st.dataframe(display_df, use_container_width=True)

with tab2:
    st.subheader("Price Analysis by Brand")
    if company_col and 'price' in num_cols_map:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=filtered_df, x=company_col, y=num_cols_map['price'], ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.title(f"Price Distribution by {company_col}")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Required columns for Price Analysis not found.")

with tab3:
    st.subheader("Hardware Configurations: RAM vs Battery")
    if 'ram' in num_cols_map and 'battery' in num_cols_map:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=filtered_df, 
            x=num_cols_map['ram'], 
            y=num_cols_map['battery'], 
            hue=company_col if company_col else None,
            s=100, alpha=0.7, ax=ax
        )
        plt.title("Battery Capacity vs RAM")
        plt.xlabel("RAM (GB)")
        plt.ylabel("Battery Capacity (mAh)")
        # Move legend outside if there are many categories
        if company_col:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Required columns for Hardware analysis not found.")

with tab4:
    st.subheader("Feature Correlations")
    # Dynamically extract any numeric column including the ones we created
    # Also attempt to parse screen size and weight dynamically for better correlation
    weight_col = next((c for c in df.columns if 'weight' in c.lower()), None)
    screen_col = next((c for c in df.columns if 'screen' in c.lower()), None)
    
    # temporarily add them to correlation
    temp_df = filtered_df.copy()
    if weight_col:
        temp_df['Weight_num'] = temp_df[weight_col].apply(clean_numeric)
    if screen_col:
        temp_df['Screen_num'] = temp_df[screen_col].apply(clean_numeric)
        
    numeric_df = temp_df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) > 1:
        fig, ax = plt.subplots(figsize=(8, 6))
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        plt.title("Correlation Heatmap of Numeric Features")
        st.pyplot(fig)
    else:
        st.warning("Not enough numeric data to compute correlations.")
