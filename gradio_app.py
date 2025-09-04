import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
import pandas as pd
import numpy as np
from PIL import Image
import io
import base64
from data_generator import data_gen
from visualizations import viz_gen

# Custom CSS for dark theme
custom_css = """
.gradio-container {
    background-color: #0e1117 !important;
    color: #ffffff !important;
}

.main-container {
    background-color: #0e1117 !important;
}

.sidebar {
    background-color: #262730 !important;
    border-right: 1px solid #404040 !important;
}

.control-panel {
    background-color: #262730 !important;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #404040;
    margin: 1rem 0;
}

.chart-container {
    background-color: #262730 !important;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #404040;
    margin: 1rem 0;
}

.header {
    background: linear-gradient(90deg, #00ff88, #4ecdc4);
    padding: 2rem;
    border-radius: 1rem;
    margin-bottom: 2rem;
    text-align: center;
    color: #000000;
}

.metric-card {
    background-color: #262730;
    padding: 1.5rem;
    border-radius: 0.5rem;
    border-left: 4px solid #00ff88;
    margin: 0.5rem 0;
    color: #ffffff;
}

/* Override Gradio default styles */
.gr-button {
    background-color: #00ff88 !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 0.5rem !important;
    padding: 0.5rem 1rem !important;
}

.gr-button:hover {
    background-color: #4ecdc4 !important;
}

.gr-dropdown {
    background-color: #262730 !important;
    color: #ffffff !important;
    border: 1px solid #404040 !important;
}

.gr-slider {
    background-color: #262730 !important;
}

.gr-text {
    color: #ffffff !important;
}

.gr-label {
    color: #ffffff !important;
}
"""

def create_header():
    """Create the header component"""
    return gr.HTML("""
    <div class="header">
        <h1>📊 Modern Data Visualization Dashboard</h1>
        <p style="font-size: 1.2rem; margin: 0;">15 Interactive Visualizations with Dark Theme</p>
        <p style="font-size: 1rem; margin: 0.5rem 0 0 0;">Built with Gradio & Plotly</p>
    </div>
    """)

def create_visualization(viz_type, refresh_data=False):
    """Create the selected visualization"""
    try:
        viz_function = viz_gen.get_all_visualizations()[viz_type]
        
        if viz_type == "Map":
            # For map visualization, we'll return a placeholder since Gradio doesn't handle Folium well
            return gr.HTML("""
            <div style="background-color: #262730; padding: 2rem; border-radius: 0.5rem; text-align: center;">
                <h3>🌍 Map Visualization</h3>
                <p>Map visualization is available in the Streamlit version.</p>
                <p>This shows geographic data points across global locations.</p>
            </div>
            """)
        else:
            fig = viz_function()
            return fig
            
    except Exception as e:
        return gr.HTML(f"""
        <div style="background-color: #ff6b6b; padding: 1rem; border-radius: 0.5rem; color: white;">
            <h3>Error</h3>
            <p>Error creating visualization: {str(e)}</p>
        </div>
        """)

def get_data_summary(viz_type):
    """Get data summary for the selected visualization"""
    try:
        if viz_type in ["Line Chart", "Area Chart"]:
            data = data_gen.generate_time_series_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Time Range:</strong> {data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}</p>
                <p><strong>Data Points:</strong> {len(data):,}</p>
                <p><strong>Value Range:</strong> {data['value'].min():.2f} - {data['value'].max():.2f}</p>
                <p><strong>Average Value:</strong> {data['value'].mean():.2f}</p>
            </div>
            """
        
        elif viz_type == "Bar Chart":
            data = data_gen.generate_categorical_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Categories:</strong> {len(data)}</p>
                <p><strong>Value Range:</strong> {data['value'].min():.2f} - {data['value'].max():.2f}</p>
                <p><strong>Top Category:</strong> {data.loc[data['value'].idxmax(), 'category']}</p>
                <p><strong>Average Value:</strong> {data['value'].mean():.2f}</p>
            </div>
            """
        
        elif viz_type == "Scatter Plot":
            data = data_gen.generate_scatter_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Data Points:</strong> {len(data):,}</p>
                <p><strong>Categories:</strong> {data['category'].nunique()}</p>
                <p><strong>Correlation:</strong> {data['x'].corr(data['y']):.3f}</p>
                <p><strong>Size Range:</strong> {data['size'].min():.1f} - {data['size'].max():.1f}</p>
            </div>
            """
        
        elif viz_type == "Pie Chart":
            data = data_gen.generate_pie_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Categories:</strong> {len(data)}</p>
                <p><strong>Total Value:</strong> {data['value'].sum()}</p>
                <p><strong>Largest Share:</strong> {data.loc[data['value'].idxmax(), 'category']} ({data.loc[data['value'].idxmax(), 'percentage']:.1f}%)</p>
            </div>
            """
        
        elif viz_type == "Heatmap":
            data = data_gen.generate_heatmap_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Matrix Size:</strong> {data.shape[0]}x{data.shape[1]}</p>
                <p><strong>Value Range:</strong> {data.values.min():.3f} - {data.values.max():.3f}</p>
                <p><strong>Average Correlation:</strong> {data.values.mean():.3f}</p>
            </div>
            """
        
        elif viz_type == "3D Scatter":
            data = data_gen.generate_3d_scatter_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Data Points:</strong> {len(data):,}</p>
                <p><strong>Color Categories:</strong> {data['color'].nunique()}</p>
                <p><strong>Size Range:</strong> {data['size'].min():.1f} - {data['size'].max():.1f}</p>
            </div>
            """
        
        elif viz_type == "Box Plot":
            data = data_gen.generate_boxplot_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Groups:</strong> {data['group'].nunique()}</p>
                <p><strong>Total Points:</strong> {len(data):,}</p>
                <p><strong>Value Range:</strong> {data['value'].min():.2f} - {data['value'].max():.2f}</p>
            </div>
            """
        
        elif viz_type == "Histogram":
            data = data_gen.generate_histogram_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Data Points:</strong> {len(data):,}</p>
                <p><strong>Value Range:</strong> {data['value'].min():.2f} - {data['value'].max():.2f}</p>
                <p><strong>Mean:</strong> {data['value'].mean():.2f}</p>
                <p><strong>Std Dev:</strong> {data['value'].std():.2f}</p>
            </div>
            """
        
        elif viz_type == "Violin Plot":
            data = data_gen.generate_violin_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Categories:</strong> {data['category'].nunique()}</p>
                <p><strong>Total Points:</strong> {len(data):,}</p>
                <p><strong>Value Range:</strong> {data['value'].min():.2f} - {data['value'].max():.2f}</p>
            </div>
            """
        
        elif viz_type == "Word Cloud":
            words = data_gen.generate_wordcloud_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Unique Words:</strong> {len(words)}</p>
                <p><strong>Max Frequency:</strong> {max(words.values())}</p>
                <p><strong>Min Frequency:</strong> {min(words.values())}</p>
            </div>
            """
        
        elif viz_type == "Map":
            data = data_gen.generate_map_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Locations:</strong> {len(data)}</p>
                <p><strong>Value Range:</strong> {data['value'].min()} - {data['value'].max()}</p>
                <p><strong>Top Location:</strong> {data.loc[data['value'].idxmax(), 'city']}</p>
            </div>
            """
        
        elif viz_type == "Gauge Chart":
            data = data_gen.generate_gauge_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Metrics:</strong> {len(data)}</p>
                <p><strong>Average Usage:</strong> {data['percentage'].mean():.1f}%</p>
                <p><strong>Highest Usage:</strong> {data.loc[data['percentage'].idxmax(), 'metric']}</p>
            </div>
            """
        
        elif viz_type == "Funnel Chart":
            data = data_gen.generate_funnel_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Stages:</strong> {len(data)}</p>
                <p><strong>Total Visitors:</strong> {data['value'].max():,}</p>
                <p><strong>Conversion Rate:</strong> {data['conversion_rate'].min():.1f}%</p>
            </div>
            """
        
        elif viz_type == "Radar Chart":
            data = data_gen.generate_radar_data()
            summary = f"""
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p><strong>Categories:</strong> {len(data)}</p>
                <p><strong>Products:</strong> 3</p>
                <p><strong>Score Range:</strong> 0-100</p>
            </div>
            """
        
        else:
            summary = """
            <div class="metric-card">
                <h4>📊 Data Summary</h4>
                <p>Data summary not available for this visualization.</p>
            </div>
            """
        
        return gr.HTML(summary)
        
    except Exception as e:
        return gr.HTML(f"""
        <div class="metric-card" style="border-left-color: #ff6b6b;">
            <h4>❌ Error</h4>
            <p>Error generating data summary: {str(e)}</p>
        </div>
        """)

def get_visualization_description(viz_type):
    """Get description for the selected visualization"""
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
    
    return gr.HTML(f"""
    <div class="metric-card">
        <h4>📋 Visualization Info</h4>
        <p><strong>Description:</strong> {descriptions.get(viz_type, 'Interactive data visualization.')}</p>
    </div>
    """)

def get_quick_stats():
    """Get quick statistics"""
    try:
        all_data = data_gen.get_all_data()
        time_series_data = all_data['time_series']
        total_points = len(time_series_data)
        avg_value = time_series_data['value'].mean()
        max_value = time_series_data['value'].max()
        
        return gr.HTML(f"""
        <div class="metric-card">
            <h4>📊 Quick Stats</h4>
            <p><strong>Total Data Points:</strong> {total_points:,}</p>
            <p><strong>Average Value:</strong> {avg_value:.2f}</p>
            <p><strong>Peak Value:</strong> {max_value:.2f}</p>
        </div>
        """)
    except Exception as e:
        return gr.HTML(f"""
        <div class="metric-card" style="border-left-color: #ff6b6b;">
            <h4>❌ Error</h4>
            <p>Error generating quick stats: {str(e)}</p>
        </div>
        """)

def main():
    """Main Gradio interface"""
    
    # Create the interface
    with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
        
        # Header
        create_header()
        
        with gr.Row():
            # Left column - Controls
            with gr.Column(scale=1):
                gr.HTML('<div class="control-panel">')
                gr.Markdown("## 🎛️ Dashboard Controls")
                
                # Visualization selector
                viz_options = list(viz_gen.get_all_visualizations().keys())
                viz_selector = gr.Dropdown(
                    choices=viz_options,
                    value=viz_options[0],
                    label="Choose Visualization:",
                    interactive=True
                )
                
                gr.Markdown("---")
                
                # Data controls
                gr.Markdown("### 📈 Data Controls")
                refresh_btn = gr.Button("🔄 Refresh Data", variant="primary")
                
                gr.Markdown("---")
                
                # Quick stats
                quick_stats = gr.HTML()
                gr.HTML('</div>')
            
            # Right column - Visualization and Info
            with gr.Column(scale=3):
                with gr.Row():
                    # Main visualization
                    with gr.Column(scale=2):
                        gr.Markdown("## 📊 Visualization")
                        viz_output = gr.Plot()
                    
                    # Info panel
                    with gr.Column(scale=1):
                        description_output = gr.HTML()
                        data_summary_output = gr.HTML()
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; color: #b0b0b0; padding: 1rem; margin-top: 2rem;">
            <p>Built with ❤️ using Gradio, Plotly, and modern data visualization techniques</p>
            <p>Dark theme optimized for professional data analysis</p>
        </div>
        """)
        
        # Event handlers
        def update_visualization(viz_type):
            return create_visualization(viz_type), get_visualization_description(viz_type), get_data_summary(viz_type)
        
        def refresh_all():
            return get_quick_stats()
        
        # Connect events
        viz_selector.change(
            fn=update_visualization,
            inputs=[viz_selector],
            outputs=[viz_output, description_output, data_summary_output]
        )
        
        refresh_btn.click(
            fn=refresh_all,
            outputs=[quick_stats]
        )
        
        # Initialize
        demo.load(
            fn=lambda: (create_visualization(viz_options[0]), get_visualization_description(viz_options[0]), get_data_summary(viz_options[0]), get_quick_stats()),
            outputs=[viz_output, description_output, data_summary_output, quick_stats]
        )
    
    return demo

if __name__ == "__main__":
    # Launch the app
    app = main()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 