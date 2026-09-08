import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="EDA Dashboard",layout="wide")

st.markdown(
    "<h1 style='font-size:2rem;'>Exploratory Data Analysis Interface</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<h2 style='font-size:1.25rem;'>Dataset Ingestion</h2>",
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.markdown(
        "<h2 style='font-size:1.5rem;'>Dataset Overview</h2>",
        unsafe_allow_html=True
    )
    st.markdown("**First 5 Rows:**")
    st.dataframe(df.head())

    st.markdown("**Dataset Shape:**")
    st.markdown(f"Rows: {df.shape[0]}")
    st.markdown(f"Columns: {df.shape[1]}")

    st.markdown("**Column Data Types:**")
    st.dataframe(
        pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str)
        })
    )

    st.markdown("**Missing Values per Column:**")
    missing_values = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing Percentage": (df.isnull().sum() / len(df) * 100).round(2)
    })

    st.dataframe(missing_values)

    st.markdown("**Basic Numerical Statistics:**")
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
        st.markdown("No numerical columns found.")

    st.sidebar.markdown(
        "<h2 style='font-size:1.25rem;'>Attribute Selection</h2>",
        unsafe_allow_html=True
    )

    selected_column = st.sidebar.selectbox(
        "Select an Attribute",
        df.columns
    )

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        column_type = "Numerical"
    else:
        column_type = "Categorical"

    st.markdown(f"**Selected Attribute:** {selected_column}")
    st.markdown(f"**Attribute Type:** {column_type}")
    st.markdown(
        "<h2 style='font-size:1.5rem;'>Visualization</h2>",
        unsafe_allow_html=True
    )

    if column_type == "Numerical":
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
    st.markdown("<p style='font-size:24px;'>Please upload a CSV File</p>", unsafe_allow_html=True)