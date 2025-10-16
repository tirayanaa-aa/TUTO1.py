import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Constants for Data and Columns ---
DATA_URL = 'https://raw.githubusercontent.com/tirayanaa-aa/TUTO1.py/refs/heads/main/arts_faculty_data.csv'
COL_SSC_GPA = 'S.S.C (GPA)'
COL_HSC_GPA = 'H.S.C (GPA)'
COL_GENDER = 'Gender'
# Use a standardized name after cleaning
COL_ACADEMIC_YEAR_CLEANED = 'Academic Year'
ACADEMIC_ORDER = ['1st Year', '2nd Year', '3rd Year', '4th Year']

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_data():
    """
    Loads the dataset and cleans up the academic year column name.
    """
    try:
        df = pd.read_csv(DATA_URL)
        
        # Identify and rename the problematic academic year column
        # It's often 'Bachelor \tAcademic Year in EU' or 'Bachelor Academic Year in EU'
        academic_col_match = [col for col in df.columns if 'Academic Year in EU' in col]
        
        if academic_col_match:
            df.rename(columns={academic_col_match[0]: COL_ACADEMIC_YEAR_CLEANED}, inplace=True)
            # Ensure the string values themselves are also clean (remove potential leading/trailing spaces/tabs)
            df[COL_ACADEMIC_YEAR_CLEANED] = df[COL_ACADEMIC_YEAR_CLEANED].str.strip()
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

st.title("🎓 Arts Faculty Data Dashboard: Interactive Plotly Visualizations")

if df.empty or not all(col in df.columns for col in [COL_SSC_GPA, COL_HSC_GPA, COL_GENDER, COL_ACADEMIC_YEAR_CLEANED]):
    st.error("Dashboard cannot run due to missing data or essential columns.")
    st.stop()

st.subheader("Data Preview")
st.dataframe(df.head())

st.divider()

# ==============================================================================
# 1. Row of Plots: Gender Distribution & GPA Scatter
# ==============================================================================
st.header("1. Gender Distribution and GPA Comparison")
col1, col2 = st.columns(2)

# --- A. Pie/Donut Chart (Gender Distribution) ---
with col1:
    st.subheader("Gender Distribution")
    
    # Data prep
    gender_counts = df[COL_GENDER].value_counts().reset_index()
    gender_counts.columns = [COL_GENDER, 'Count']
    
    fig_pie = px.pie(
        gender_counts, 
        values='Count', 
        names=COL_GENDER, 
        title='Distribution of Gender in Arts Faculty',
        hole=0.4 # Making it a donut chart
    )
    fig_pie.update_traces(textinfo='percent+label', textposition='outside')
    st.plotly_chart(fig_pie, use_container_width=True)

# --- B. Scatter Plot (GPA Comparison) ---
with col2:
    st.subheader("S.S.C GPA vs H.S.C GPA")
    
    fig_scatter = px.scatter(
        df,
        x=COL_SSC_GPA,
        y=COL_HSC_GPA,
        color=COL_GENDER, # Differentiate by Gender
        title='Comparison of S.S.C (GPA) and H.S.C (GPA)',
        opacity=0.6,
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ==============================================================================
# 2. Row of Plots: Academic Year Distribution & Grouped Bar Chart
# ==============================================================================
st.header("2. Academic Year Breakdown")
col3, col4 = st.columns(2)

# --- C. Donut Chart (Academic Year Distribution) ---
with col3:
    st.subheader("Distribution of Bachelor Academic Year")

    # Data prep
    academic_year_counts = df[COL_ACADEMIC_YEAR_CLEANED].value_counts().reset_index()
    academic_year_counts.columns = [COL_ACADEMIC_YEAR_CLEANED, 'Count']
    
    fig_donut_year = px.pie(
        academic_year_counts, 
        values='Count', 
        names=COL_ACADEMIC_YEAR_CLEANED, 
        title='Distribution of Bachelor Academic Year in Arts Faculty',
        hole=0.4,
        category_orders={COL_ACADEMIC_YEAR_CLEANED: ACADEMIC_ORDER}
    )
    fig_donut_year.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig_donut_year, use_container_width=True)


# --- D. Grouped Bar Chart (Academic Year by Gender) ---
with col4:
    st.subheader("Bachelor Academic Year by Gender")
    
    # Data prep
    grouped_data = df.groupby([COL_GENDER, COL_ACADEMIC_YEAR_CLEANED]).size().reset_index(name='Count')

    fig_grouped_bar = px.bar(
        grouped_data,
        x=COL_GENDER,
        y='Count',
        color=COL_ACADEMIC_YEAR_CLEANED,
        barmode='group', # Creates the grouped bars
        category_orders={COL_ACADEMIC_YEAR_CLEANED: ACADEMIC_ORDER},
        title='Distribution of Bachelor Academic Year by Gender',
        template="plotly_white"
    )
    fig_grouped_bar.update_xaxes(tickangle=0)
    st.plotly_chart(fig_grouped_bar, use_container_width=True)

st.divider()

# ==============================================================================
# 3. Row of Plots: Box Plot and Heatmap
# ==============================================================================
st.header("3. Performance Analysis (S.S.C GPA)")
col5, col6 = st.columns(2)

# --- E. Box Plot (S.S.C GPA by Academic Year) ---
with col5:
    st.subheader("S.S.C GPA Distribution by Academic Year")

    # Filter data (already done by ACADEMIC_ORDER, but good practice to filter)
    filtered_df_box = df[df[COL_ACADEMIC_YEAR_CLEANED].isin(ACADEMIC_ORDER)].copy()

    fig_box = px.box(
        filtered_df_box,
        x=COL_ACADEMIC_YEAR_CLEANED,
        y=COL_SSC_GPA,
        color=COL_ACADEMIC_YEAR_CLEANED,
        category_orders={COL_ACADEMIC_YEAR_CLEANED: ACADEMIC_ORDER},
        title='Distribution of S.S.C (GPA) by Bachelor Academic Year',
        template="plotly_white"
    )
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

# --- F. Heatmap (High Performers) ---
with col6:
    st.subheader("Students with GPA > 3.00 Heatmap")
    
    # Data prep for Heatmap
    performance_df = df[df[COL_SSC_GPA] > 3.00].copy()

    performance_pivot = performance_df.pivot_table(
        index=COL_GENDER,
        columns=COL_ACADEMIC_YEAR_CLEANED,
        aggfunc='size',
        fill_value=0
    )

    performance_pivot = performance_pivot.reindex(columns=ACADEMIC_ORDER, fill_value=0)

    # Plotly Graph Objects is best for direct pivot table/matrix heatmaps
    z_data = performance_pivot.values
    x_data = performance_pivot.columns.tolist()
    y_data = performance_pivot.index.tolist()

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_data,
        y=y_data,
        colorscale='Greens', 
        text=z_data,
        texttemplate="%{text}",
        hoverongaps=False
    ))

    fig_heatmap.update_layout(
        title='Number of Students with GPA > 3.00 by Gender and Academic Year',
        xaxis_title='Bachelor Academic Year in EU',
        yaxis_title='Gender'
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

st.caption("All charts are interactive: pan, zoom, and hover for details.")
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
