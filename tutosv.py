import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Scientific Visualization", divider="gray")

# Set up the page configuration
st.set_page_config(
    page_title="Arts Faculty Data Dashboard",
    layout="wide"
)

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_data():
    """Loads the dataset from the URL."""
    url = 'https://raw.githubusercontent.com/tirayanaa-aa/TUTO1.py/refs/heads/main/arts_faculty_data.csv'
    try:
        df = pd.read_csv(url)
        # Assuming the DataFrame name 'arts_df' in the original code snippet 
        # meant the loaded DataFrame, we'll use 'df' for consistency.
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() # Return empty DataFrame on failure

df = load_data()

# Check if data was loaded successfully and has the 'Gender' column
if 'Gender' in df.columns:
    # Calculate gender counts
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
else:
    st.warning("Data not loaded or 'Gender' column not found.")
    st.stop() # Stop the app if data is not ready

# --- Streamlit App Layout ---
st.title("Gender Distribution in Arts Faculty")

# Display the head of the DataFrame
st.subheader("Raw Data Head")
st.dataframe(df.head())

st.divider()

# Create columns for side-by-side plots
col1, col2 = st.columns(2)

# --- 1. Plotly Pie Chart (Conversion of the first Matplotlib plot) ---
with col1:
    st.subheader("Gender Distribution (Pie Chart)")
    
    # Create Plotly Pie Chart
    # 'names' is used for labels, 'values' is used for sizes/counts
    fig_pie = px.pie(
        gender_counts, 
        values='Count', 
        names='Gender', 
        title='Distribution of Gender in Arts Faculty',
        hole=0.3 # Optional: makes it a donut chart
    )
    
    # Optional: Customize text information and position
    fig_pie.update_traces(textinfo='percent+label', textposition='inside')

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 2. Plotly Bar Chart (Conversion of the second Matplotlib plot) ---
with col2:
    st.subheader("Gender Distribution (Bar Chart)")

    # Create Plotly Bar Chart
    fig_bar = px.bar(
        gender_counts, 
        x='Gender', 
        y='Count', 
        title='Distribution of Gender in Arts Faculty',
        labels={'Gender': 'Gender', 'Count': 'Count'},
        color='Gender' # Optional: colors bars by Gender
    )
    
    # Optional: Customize layout for better appearance
    fig_bar.update_layout(xaxis={'categoryorder':'total descending'}) 
    fig_bar.update_xaxes(tickangle=0) # Ensures x-axis labels are not rotated

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig_bar, use_container_width=True)
