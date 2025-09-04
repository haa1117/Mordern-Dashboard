import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import folium
import altair as alt
import streamlit as st
from data_generator import data_gen

# Dark theme colors
DARK_COLORS = {
    'background': '#0e1117',
    'surface': '#262730',
    'primary': '#00ff88',
    'secondary': '#ff6b6b',
    'accent': '#4ecdc4',
    'text': '#ffffff',
    'text_secondary': '#b0b0b0',
    'border': '#404040'
}

PLOTLY_COLORS = ['#00ff88', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff']

class VisualizationGenerator:
    def __init__(self):
        self.data_gen = data_gen
        self.setup_plotly_theme()
        self.setup_matplotlib_theme()
    
    def setup_plotly_theme(self):
        """Setup Plotly dark theme"""
        # We'll apply the theme to individual figures instead of globally
        pass
    
    def apply_dark_theme(self, fig):
        """Apply dark theme to a Plotly figure"""
        fig.update_layout(
            paper_bgcolor=DARK_COLORS['background'],
            plot_bgcolor=DARK_COLORS['background'],
            font=dict(color=DARK_COLORS['text']),
            xaxis=dict(
                gridcolor=DARK_COLORS['border'],
                linecolor=DARK_COLORS['border']
            ),
            yaxis=dict(
                gridcolor=DARK_COLORS['border'],
                linecolor=DARK_COLORS['border']
            )
        )
        return fig
    
    def setup_matplotlib_theme(self):
        """Setup Matplotlib dark theme"""
        plt.style.use('dark_background')
        sns.set_theme(style="darkgrid")
    
    def create_line_chart(self):
        """1. Line Chart - Time series data trends"""
        data = self.data_gen.generate_time_series_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['value'],
            mode='lines+markers',
            name='Value',
            line=dict(color=DARK_COLORS['primary'], width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Time Series Trend Analysis',
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            showlegend=True,
            height=400
        )
        
        # Apply dark theme
        fig = self.apply_dark_theme(fig)
        
        return fig
    
    def create_bar_chart(self):
        """2. Bar Chart - Categorical data comparison"""
        data = self.data_gen.generate_categorical_data()
        
        fig = go.Figure(data=[
            go.Bar(
                x=data['category'],
                y=data['value'],
                marker_color=PLOTLY_COLORS[:len(data)],
                text=data['value'].round(1),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Category Performance Comparison',
            xaxis_title='Category',
            yaxis_title='Value',
            height=400
        )
        
        # Apply dark theme
        fig = self.apply_dark_theme(fig)
        
        return fig
    
    def create_scatter_plot(self):
        """3. Scatter Plot - Correlation analysis"""
        data = self.data_gen.generate_scatter_data()
        
        fig = px.scatter(
            data, x='x', y='y', 
            color='category',
            size='size',
            title='Correlation Analysis',
            color_discrete_sequence=PLOTLY_COLORS
        )
        
        fig.update_layout(
            xaxis_title='X Variable',
            yaxis_title='Y Variable',
            height=400
        )
        
        return fig
    
    def create_pie_chart(self):
        """4. Pie Chart - Distribution visualization"""
        data = self.data_gen.generate_pie_data()
        
        fig = go.Figure(data=[go.Pie(
            labels=data['category'],
            values=data['value'],
            hole=0.3,
            marker_colors=PLOTLY_COLORS[:len(data)]
        )])
        
        fig.update_layout(
            title='Distribution Analysis',
            height=400
        )
        
        return fig
    
    def create_heatmap(self):
        """5. Heatmap - Matrix data representation"""
        data = self.data_gen.generate_heatmap_data()
        
        fig = go.Figure(data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale='Viridis',
            showscale=True
        ))
        
        fig.update_layout(
            title='Correlation Matrix Heatmap',
            height=400
        )
        
        return fig
    
    def create_3d_scatter(self):
        """6. 3D Scatter Plot - Multi-dimensional data"""
        data = self.data_gen.generate_3d_scatter_data()
        
        fig = go.Figure(data=[go.Scatter3d(
            x=data['x'],
            y=data['y'],
            z=data['z'],
            mode='markers',
            marker=dict(
                size=data['size'],
                color=data['color'],
                opacity=0.8
            )
        )])
        
        fig.update_layout(
            title='3D Scatter Plot',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            ),
            height=500
        )
        
        return fig
    
    def create_area_chart(self):
        """7. Area Chart - Cumulative data trends"""
        data = self.data_gen.generate_area_data()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['date'], y=data['revenue'],
            fill='tonexty', name='Revenue',
            line=dict(color=DARK_COLORS['primary'])
        ))
        
        fig.add_trace(go.Scatter(
            x=data['date'], y=data['costs'],
            fill='tonexty', name='Costs',
            line=dict(color=DARK_COLORS['secondary'])
        ))
        
        fig.add_trace(go.Scatter(
            x=data['date'], y=data['profit'],
            fill='tonexty', name='Profit',
            line=dict(color=DARK_COLORS['accent'])
        ))
        
        fig.update_layout(
            title='Financial Performance Over Time',
            xaxis_title='Date',
            yaxis_title='Amount ($)',
            height=400
        )
        
        return fig
    
    def create_box_plot(self):
        """8. Box Plot - Statistical distribution"""
        data = self.data_gen.generate_boxplot_data()
        
        fig = px.box(
            data, x='group', y='value',
            title='Statistical Distribution by Group',
            color_discrete_sequence=PLOTLY_COLORS
        )
        
        fig.update_layout(
            xaxis_title='Group',
            yaxis_title='Value',
            height=400
        )
        
        return fig
    
    def create_histogram(self):
        """9. Histogram - Frequency distribution"""
        data = self.data_gen.generate_histogram_data()
        
        fig = go.Figure(data=[go.Histogram(
            x=data['value'],
            nbinsx=30,
            marker_color=DARK_COLORS['primary'],
            opacity=0.8
        )])
        
        fig.update_layout(
            title='Frequency Distribution',
            xaxis_title='Value',
            yaxis_title='Frequency',
            height=400
        )
        
        return fig
    
    def create_violin_plot(self):
        """10. Violin Plot - Density distribution"""
        data = self.data_gen.generate_violin_data()
        
        fig = px.violin(
            data, x='category', y='value',
            title='Density Distribution by Category',
            color_discrete_sequence=PLOTLY_COLORS
        )
        
        fig.update_layout(
            xaxis_title='Category',
            yaxis_title='Value',
            height=400
        )
        
        return fig
    
    def create_wordcloud(self):
        """11. Word Cloud - Text data visualization"""
        words = self.data_gen.generate_wordcloud_data()
        
        wordcloud = WordCloud(
            width=800, height=400,
            background_color=DARK_COLORS['background'],
            colormap='viridis',
            max_words=50
        ).generate_from_frequencies(words)
        
        # Convert to PIL Image and then to base64
        import io
        import base64
        
        img_buffer = io.BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Convert to plotly figure
        fig = go.Figure()
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_str}",
                x=0, y=1, xref="paper", yref="paper",
                sizex=1, sizey=1,
                sizing="stretch"
            )
        )
        
        fig.update_layout(
            title='Word Cloud Analysis',
            height=400,
            showlegend=False
        )
        
        # Apply dark theme
        fig = self.apply_dark_theme(fig)
        
        return fig
    
    def create_map_visualization(self):
        """12. Map Visualization - Geographic data"""
        data = self.data_gen.generate_map_data()
        
        # Create a map centered on the world
        m = folium.Map(
            location=[20, 0],
            zoom_start=2,
            tiles='CartoDB dark_matter'
        )
        
        # Add markers for each city
        for idx, row in data.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=row['value']/10,
                popup=f"{row['city']}: {row['value']}",
                color=DARK_COLORS['primary'],
                fill=True,
                fillColor=DARK_COLORS['accent']
            ).add_to(m)
        
        return m
    
    def create_gauge_chart(self):
        """13. Gauge Chart - Progress indicators"""
        data = self.data_gen.generate_gauge_data()
        
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]],
            subplot_titles=data['metric'].tolist()
        )
        
        for i, (metric, value, max_val) in enumerate(zip(data['metric'], data['value'], data['max_value'])):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': metric},
                delta={'reference': max_val * 0.8},
                gauge={
                    'axis': {'range': [None, max_val]},
                    'bar': {'color': PLOTLY_COLORS[i]},
                    'steps': [
                        {'range': [0, max_val * 0.6], 'color': "lightgray"},
                        {'range': [max_val * 0.6, max_val * 0.8], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_val * 0.9
                    }
                }
            ), row=row, col=col)
        
        fig.update_layout(height=500, title_text="System Metrics Dashboard")
        return fig
    
    def create_funnel_chart(self):
        """14. Funnel Chart - Process flow"""
        data = self.data_gen.generate_funnel_data()
        
        fig = go.Figure(go.Funnel(
            y=data['stage'],
            x=data['value'],
            textinfo="value+percent initial"
        ))
        
        fig.update_layout(
            title='Conversion Funnel Analysis',
            height=400
        )
        
        return fig
    
    def create_radar_chart(self):
        """15. Radar Chart - Multi-dimensional comparison"""
        data = self.data_gen.generate_radar_data()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=data['Product A'],
            theta=data['category'],
            fill='toself',
            name='Product A',
            line_color=DARK_COLORS['primary']
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=data['Product B'],
            theta=data['category'],
            fill='toself',
            name='Product B',
            line_color=DARK_COLORS['secondary']
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=data['Product C'],
            theta=data['category'],
            fill='toself',
            name='Product C',
            line_color=DARK_COLORS['accent']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title='Product Comparison Radar Chart',
            height=400
        )
        
        return fig
    
    def get_all_visualizations(self):
        """Get all visualization functions"""
        return {
            'Line Chart': self.create_line_chart,
            'Bar Chart': self.create_bar_chart,
            'Scatter Plot': self.create_scatter_plot,
            'Pie Chart': self.create_pie_chart,
            'Heatmap': self.create_heatmap,
            '3D Scatter': self.create_3d_scatter,
            'Area Chart': self.create_area_chart,
            'Box Plot': self.create_box_plot,
            'Histogram': self.create_histogram,
            'Violin Plot': self.create_violin_plot,
            'Word Cloud': self.create_wordcloud,
            'Map': self.create_map_visualization,
            'Gauge Chart': self.create_gauge_chart,
            'Funnel Chart': self.create_funnel_chart,
            'Radar Chart': self.create_radar_chart
        }

# Global instance
viz_gen = VisualizationGenerator() 