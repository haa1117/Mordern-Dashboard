import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
from PIL import Image
import io
import base64
from data_generator import data_gen
from visualizations import viz_gen

# Page configuration
st.set_page_config(
    page_title="Modern Data Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0e1117;
    }
    
    .stSidebar {
        background-color: #262730;
        color: #ffffff;
    }
    
    .stSelectbox, .stSlider, .stButton {
        background-color: #262730;
        color: #ffffff;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    .metric-container {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #404040;
        margin: 0.5rem 0;
    }
    
    .chart-container {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #404040;
        margin: 1rem 0;
    }
    
    .header-container {
        background: linear-gradient(90deg, #00ff88, #4ecdc4);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00ff88;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>📊 Modern Data Visualization Dashboard</h1>
        <p style="font-size: 1.2rem; margin: 0;">15 Interactive Visualizations with Dark Theme</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Dashboard Controls")
        
        # Visualization selector
        viz_options = list(viz_gen.get_all_visualizations().keys())
        selected_viz = st.selectbox(
            "Choose Visualization:",
            viz_options,
            index=0
        )
        
        st.markdown("---")
        
        # Data controls
        st.markdown("### 📈 Data Controls")
        refresh_data = st.button("🔄 Refresh Data", type="primary")
        
        if refresh_data:
            st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        all_data = data_gen.get_all_data()
        
        # Calculate some quick metrics
        time_series_data = all_data['time_series']
        total_points = len(time_series_data)
        avg_value = time_series_data['value'].mean()
        max_value = time_series_data['value'].max()
        
        st.metric("Total Data Points", f"{total_points:,}")
        st.metric("Average Value", f"{avg_value:.2f}")
        st.metric("Peak Value", f"{max_value:.2f}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## {selected_viz}")
        
        # Create the selected visualization
        viz_function = viz_gen.get_all_visualizations()[selected_viz]
        
        try:
            if selected_viz == "Map":
                # Handle map visualization separately
                map_viz = viz_function()
                folium_static(map_viz, width=800, height=400)
            else:
                # Handle other visualizations
                fig = viz_function()
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
                
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            st.info("Please try refreshing the data or selecting a different visualization.")
    
    with col2:
        st.markdown("## 📋 Visualization Info")
        
        # Description for each visualization
        descriptions = {
            "Line Chart": "Time series analysis showing trends over time with seasonal patterns and noise.",
            "Bar Chart": "Categorical comparison across different industry sectors with performance metrics.",
            "Scatter Plot": "Correlation analysis between variables with categorical grouping and size encoding.",
            "Pie Chart": "Distribution analysis showing market share across different device types.",
            "Heatmap": "Correlation matrix visualization for multiple variables with color-coded intensity.",
            "3D Scatter": "Multi-dimensional data exploration in three-dimensional space.",
            "Area Chart": "Cumulative financial performance showing revenue, costs, and profit trends.",
            "Box Plot": "Statistical distribution analysis with quartiles and outliers by group.",
            "Histogram": "Frequency distribution showing the spread and shape of data values.",
            "Violin Plot": "Density distribution visualization combining box plot and kernel density estimation.",
            "Word Cloud": "Text analysis showing frequency and importance of key terms.",
            "Map": "Geographic visualization of data points across global locations.",
            "Gauge Chart": "Progress indicators for system metrics and performance monitoring.",
            "Funnel Chart": "Conversion analysis showing the flow through different stages.",
            "Radar Chart": "Multi-dimensional comparison of different products across various attributes."
        }
        
        st.markdown(f"**Description:** {descriptions.get(selected_viz, 'Interactive data visualization.')}")
        
        # Data summary
        st.markdown("### 📊 Data Summary")
        try:
            if selected_viz in ["Line Chart", "Area Chart"]:
                data = data_gen.generate_time_series_data()
                st.write(f"**Time Range:** {data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}")
                st.write(f"**Data Points:** {len(data):,}")
                st.write(f"**Value Range:** {data['value'].min():.2f} - {data['value'].max():.2f}")
            
            elif selected_viz == "Bar Chart":
                data = data_gen.generate_categorical_data()
                st.write(f"**Categories:** {len(data)}")
                st.write(f"**Value Range:** {data['value'].min():.2f} - {data['value'].max():.2f}")
                st.write(f"**Top Category:** {data.loc[data['value'].idxmax(), 'category']}")
            
            elif selected_viz == "Scatter Plot":
                data = data_gen.generate_scatter_data()
                st.write(f"**Data Points:** {len(data):,}")
                st.write(f"**Categories:** {data['category'].nunique()}")
                st.write(f"**Correlation:** {data['x'].corr(data['y']):.3f}")
            
            elif selected_viz == "Pie Chart":
                data = data_gen.generate_pie_data()
                st.write(f"**Categories:** {len(data)}")
                st.write(f"**Total Value:** {data['value'].sum()}")
                st.write(f"**Largest Share:** {data.loc[data['value'].idxmax(), 'category']} ({data.loc[data['value'].idxmax(), 'percentage']:.1f}%)")
            
            elif selected_viz == "Heatmap":
                data = data_gen.generate_heatmap_data()
                st.write(f"**Matrix Size:** {data.shape[0]}x{data.shape[1]}")
                st.write(f"**Value Range:** {data.values.min():.3f} - {data.values.max():.3f}")
                st.write(f"**Average Correlation:** {data.values.mean():.3f}")
            
            elif selected_viz == "3D Scatter":
                data = data_gen.generate_3d_scatter_data()
                st.write(f"**Data Points:** {len(data):,}")
                st.write(f"**Color Categories:** {data['color'].nunique()}")
                st.write(f"**Size Range:** {data['size'].min():.1f} - {data['size'].max():.1f}")
            
            elif selected_viz == "Box Plot":
                data = data_gen.generate_boxplot_data()
                st.write(f"**Groups:** {data['group'].nunique()}")
                st.write(f"**Total Points:** {len(data):,}")
                st.write(f"**Value Range:** {data['value'].min():.2f} - {data['value'].max():.2f}")
            
            elif selected_viz == "Histogram":
                data = data_gen.generate_histogram_data()
                st.write(f"**Data Points:** {len(data):,}")
                st.write(f"**Value Range:** {data['value'].min():.2f} - {data['value'].max():.2f}")
                st.write(f"**Mean:** {data['value'].mean():.2f}")
                st.write(f"**Std Dev:** {data['value'].std():.2f}")
            
            elif selected_viz == "Violin Plot":
                data = data_gen.generate_violin_data()
                st.write(f"**Categories:** {data['category'].nunique()}")
                st.write(f"**Total Points:** {len(data):,}")
                st.write(f"**Value Range:** {data['value'].min():.2f} - {data['value'].max():.2f}")
            
            elif selected_viz == "Word Cloud":
                words = data_gen.generate_wordcloud_data()
                st.write(f"**Unique Words:** {len(words)}")
                st.write(f"**Max Frequency:** {max(words.values())}")
                st.write(f"**Min Frequency:** {min(words.values())}")
            
            elif selected_viz == "Map":
                data = data_gen.generate_map_data()
                st.write(f"**Locations:** {len(data)}")
                st.write(f"**Value Range:** {data['value'].min()} - {data['value'].max()}")
                st.write(f"**Top Location:** {data.loc[data['value'].idxmax(), 'city']}")
            
            elif selected_viz == "Gauge Chart":
                data = data_gen.generate_gauge_data()
                st.write(f"**Metrics:** {len(data)}")
                st.write(f"**Average Usage:** {data['percentage'].mean():.1f}%")
                st.write(f"**Highest Usage:** {data.loc[data['percentage'].idxmax(), 'metric']}")
            
            elif selected_viz == "Funnel Chart":
                data = data_gen.generate_funnel_data()
                st.write(f"**Stages:** {len(data)}")
                st.write(f"**Total Visitors:** {data['value'].max():,}")
                st.write(f"**Conversion Rate:** {data['conversion_rate'].min():.1f}%")
            
            elif selected_viz == "Radar Chart":
                data = data_gen.generate_radar_data()
                st.write(f"**Categories:** {len(data)}")
                st.write(f"**Products:** 3")
                st.write(f"**Score Range:** 0-100")
                
        except Exception as e:
            st.write("Data summary not available for this visualization.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #b0b0b0; padding: 1rem;">
        <p>Built with ❤️ using Streamlit, Plotly, and modern data visualization techniques</p>
        <p>Dark theme optimized for professional data analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 