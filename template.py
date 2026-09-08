# lab_eda_gui.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration

st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface")


# 2. Sidebar: Dataset Ingestion

#set header for sidebar

#create a file uploader in the sidebar for CSV files

if uploaded_file is not None:
    # Read dataset
        
    # 3. Dataset Overview
    
    #set subheader for dataset overview
    st.write("**First 5 Rows:**")
    #display the first 5 rows of the dataset

    #display the shape of the dataset
    st.write("**Column Data Types:**")
    #display the data types of each column in the dataset

    # Missing value summary
    st.write("**Missing Values per Column:**")
   #display the count and percentage of missing values for each column in the dataset
    

    # Basic statistics for numerical columns
    st.write("**Basic Numerical Statistics:**")
    #display the basic statistics

    
    # 4. Attribute Selection
    
    #set header for attribute selection in the sidebar
    #create a selectbox in the sidebar to choose an attribute for visualization
    

    # Detect column type
    

    
    # 5. Visualization Rendering
    
    st.subheader("Visualization")

    if column_type == "Numerical":
        # Histogram with seaborn
        
        pass
    else:
        # Bar chart for categorical
        pass    

else:
    st.info("Please upload a CSV file to start EDA.")
