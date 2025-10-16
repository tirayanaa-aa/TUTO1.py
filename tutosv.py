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


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Data Loading and Preprocessing ---
# The URL remains the same as provided in your original snippets.
DATA_URL = 'https://raw.githubusercontent.com/tirayanaa-aa/TUTO1.py/refs/heads/main/arts_faculty_data.csv'

# Define the expected column names
COL_SSC_GPA = 'S.S.C (GPA)'
COL_HSC_GPA = 'H.S.C (GPA)'
COL_GENDER = 'Gender'
# Note: The 'Bachelor Academic Year in EU' column in the source data 
# often contains hidden spaces or tabs. We will clean it up for plotting.
COL_ACADEMIC_YEAR_RAW = 'Bachelor \tAcademic Year in EU' # Using the user's observed name

@st.cache_data
def load_data():
    """
    Loads the dataset from the URL and cleans up the academic year column name 
    to ensure smooth processing.
    """
    try:
        df = pd.read_csv(DATA_URL)
        
        # Standardize the academic year column name
        if COL_ACADEMIC_YEAR_RAW in df.columns:
            df.rename(columns={COL_ACADEMIC_YEAR_RAW: 'Academic Year'}, inplace=True)
        # Handle cases where the column name might have slight variations (e.g., just spaces)
        elif 'Bachelor Academic Year in EU' in df.columns:
             df.rename(columns={'Bachelor Academic Year in EU': 'Academic Year'}, inplace=True)
        else:
             st.error("The 'Bachelor Academic Year in EU' column was not found. Please check the CSV file structure.")
             return pd.DataFrame()
        
        return df
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        return pd.DataFrame()

df = load_data()

# --- Streamlit App Layout ---
st.set_page_config(
    page_title="Arts Faculty Data Dashboard (Plotly)",
    layout="wide"
)

st.title("Arts Faculty Data Dashboard: Academic Performance & Demographics")

if df.empty or not all(col in df.columns for col in [COL_SSC_GPA, COL_HSC_GPA, COL_GENDER, 'Academic Year']):
    st.warning("Data is missing or key columns are unavailable. Please ensure the CSV link is correct.")
    st.stop()

st.subheader("Raw Data Preview")
st.dataframe(df.head())
st.divider()


# --- ROW 1: Scatter Plot and Donut Chart ---
st.header("1. GPA Comparison and Academic Year Distribution")
col1, col2 = st.columns(2)

with col1:
    st.subheader("S.S.C GPA vs H.S.C GPA")
    
    # Plotly Scatter Plot (Conversion of first Matplotlib plot)
    fig_scatter = px.scatter(
        df,
        x=COL_SSC_GPA,
        y=COL_HSC_GPA,
        color=COL_GENDER, # Adding color for differentiation
        title='Comparison of S.S.C (GPA) and H.S.C (GPA)',
        opacity=0.6,
        template="plotly_white"
    )
    fig_scatter.update_layout(xaxis_title=COL_SSC_GPA, yaxis_title=COL_HSC_GPA)
    st.plotly_chart(fig_scatter, use_container_width=True)


with col2:
    st.subheader("Distribution of Bachelor Academic Year")

    # Data prep for Donut Chart
    academic_year_counts = df['Academic Year'].value_counts().reset_index()
    academic_year_counts.columns = ['Academic Year', 'Count']
    
    # Plotly Donut Chart (Conversion of second Matplotlib plot)
    fig_donut = px.pie(
        academic_year_counts, 
        values='Count', 
        names='Academic Year', 
        title='Distribution of Bachelor Academic Year in Arts Faculty',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Agsunset # Custom color sequence
    )
    fig_donut.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# --- ROW 2: Grouped Bar Chart and Box Plot ---
st.header("2. Gender Breakdown and GPA Distribution by Year")
col3, col4 = st.columns(2)

# Define the correct order for academic years for consistency in all plots
ACADEMIC_ORDER = ['1st Year', '2nd Year', '3rd Year', '4th Year']

with col3:
    st.subheader("Bachelor Academic Year by Gender")
    
    # Data prep for Grouped Bar Chart
    # Use pandas groupby to get the counts for Plotly
    grouped_data = df.groupby([COL_GENDER, 'Academic Year']).size().reset_index(name='Count')

    # Plotly Grouped Bar Chart (Conversion of third Matplotlib plot)
    fig_grouped_bar = px.bar(
        grouped_data,
        x=COL_GENDER,
        y='Count',
        color='Academic Year',
        barmode='group', # Important for grouped style
        category_orders={"Academic Year": ACADEMIC_ORDER},
        title='Distribution of Bachelor Academic Year by Gender',
        template="plotly_white"
    )
    fig_grouped_bar.update_xaxes(tickangle=0)
    st.plotly_chart(fig_grouped_bar, use_container_width=True)


with col4:
    st.subheader("S.S.C GPA Box Plot by Academic Year")

    # Filter data for the specified academic years 
    filtered_df_box = df[df['Academic Year'].isin(ACADEMIC_ORDER)].copy()

    # Plotly Box Plot (Conversion of fourth Matplotlib/Seaborn plot)
    fig_box = px.box(
        filtered_df_box,
        x='Academic Year',
        y=COL_SSC_GPA,
        color='Academic Year',
        category_orders={"Academic Year": ACADEMIC_ORDER},
        title='Distribution of S.S.C (GPA) by Bachelor Academic Year',
        template="plotly_white"
    )
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# --- ROW 3: Heatmap (Performance Analysis) ---
st.header("3. High-Performing Students (GPA > 3.00) Heatmap")

# Data prep for Heatmap
# Filter data for students with GPA > 3.00
performance_df = df[df[COL_SSC_GPA] > 3.00].copy()

# Create a pivot table to count students by Gender and Academic Year
performance_pivot = performance_df.pivot_table(
    index=COL_GENDER,
    columns='Academic Year',
    aggfunc='size',
    fill_value=0
)

# Reindex the columns to ensure the desired order
performance_pivot = performance_pivot.reindex(columns=ACADEMIC_ORDER, fill_value=0)

# Plotly Heatmap (Conversion of fifth Seaborn plot)
# Plotly Express does not have a native heatmap for this pivoted structure,
# so we use plotly.graph_objects.Heatmap
z_data = performance_pivot.values
x_data = performance_pivot.columns.tolist()
y_data = performance_pivot.index.tolist()

fig_heatmap = go.Figure(data=go.Heatmap(
    z=z_data,
    x=x_data,
    y=y_data,
    colorscale='Greens', # Use a green color scale similar to the original
    text=z_data,
    texttemplate="%{text}",
    hoverongaps=False
))

fig_heatmap.update_layout(
    title='Number of Students with GPA > 3.00 by Gender and Academic Year',
    xaxis_title='Bachelor Academic Year in EU',
    yaxis_title='Gender',
    xaxis_nticks=len(x_data)
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.caption("All charts are interactive. Hover over elements for detailed information.")
