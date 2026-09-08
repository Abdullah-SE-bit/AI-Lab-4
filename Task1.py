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

st.sidebar.header("Dataset Ingestion")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    # Read dataset
    df = pd.read_csv(uploaded_file)
        
    # 3. Dataset Overview
    
    st.subheader("Dataset Overview")

    #set subheader for dataset overview
    st.write("**First 5 Rows:**")

    #display the first 5 rows of the dataset
    st.dataframe(df.head())

    #display the shape of the dataset
    st.write("**Dataset Shape:**")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    st.write("**Column Data Types:**")
    
    #display the data types of each column in the dataset
    st.dataframe(
        pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str)
        })
    )

    # Missing value summary
    st.write("**Missing Values per Column:**")

    #display the count and percentage of missing values for each column in the dataset
    missing_values = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing Percentage": (df.isnull().sum() / len(df) * 100).round(2)
    })

    st.dataframe(missing_values)

    
    # Basic statistics for numerical columns
    st.write("**Basic Numerical Statistics:**")

    #display the basic statistics
    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numerical_columns) > 0:
        statistics = pd.DataFrame({
            "Mean": df[numerical_columns].mean(),
            "Median": df[numerical_columns].median(),
            "Min": df[numerical_columns].min(),
            "Max": df[numerical_columns].max()
        })

        st.dataframe(statistics)
    else:
        st.write("No numerical columns found.")

    
    # 4. Attribute Selection
    
    #set header for attribute selection in the sidebar
    st.sidebar.header("Attribute Selection")

    #create a selectbox in the sidebar to choose an attribute for visualization
    selected_column = st.sidebar.selectbox(
        "Select an Attribute",
        df.columns
    )

    # Detect column type
    if pd.api.types.is_numeric_dtype(df[selected_column]):
        column_type = "Numerical"
    else:
        column_type = "Categorical"

    st.write("**Selected Attribute:**", selected_column)
    st.write("**Attribute Type:**", column_type)


    
    # 5. Visualization Rendering
    
    st.subheader("Visualization")

    if column_type == "Numerical":
        # Histogram with seaborn
        
        fig, ax = plt.subplots()

        sns.histplot(
            df[selected_column].dropna(),
            bins=20,
            kde=True,
            ax=ax
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of " + selected_column)

        st.pyplot(fig)

    else:
        # Bar chart for categorical

        value_counts = df[selected_column].value_counts()

        fig, ax = plt.subplots()

        sns.barplot(
            x=value_counts.index,
            y=value_counts.values,
            ax=ax
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        ax.set_title("Frequency of " + selected_column)

        plt.xticks(rotation=45)

        st.pyplot(fig)    

else:
    st.info("Please upload a CSV file to start EDA.")