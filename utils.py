import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import base64
from PIL import Image
import io

# Dark theme color palette
DARK_THEME = {
    'background': '#0e1117',
    'surface': '#262730',
    'primary': '#00ff88',
    'secondary': '#ff6b6b',
    'accent': '#4ecdc4',
    'text': '#ffffff',
    'text_secondary': '#b0b0b0',
    'border': '#404040',
    'success': '#00ff88',
    'warning': '#ffca28',
    'error': '#ff6b6b',
    'info': '#4ecdc4'
}

PLOTLY_COLORS = [
    '#00ff88', '#ff6b6b', '#4ecdc4', '#45b7d1', 
    '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff',
    '#5f27cd', '#00d2d3', '#ff9f43', '#10ac84'
]

class ThemeManager:
    """Manage dark theme styling across applications"""
    
    @staticmethod
    def get_plotly_template():
        """Get Plotly dark theme template"""
        return {
            'layout': {
                'paper_bgcolor': DARK_THEME['background'],
                'plot_bgcolor': DARK_THEME['background'],
                'font': {'color': DARK_THEME['text']},
                'xaxis': {
                    'gridcolor': DARK_THEME['border'],
                    'linecolor': DARK_THEME['border'],
                    'tickfont': {'color': DARK_THEME['text']}
                },
                'yaxis': {
                    'gridcolor': DARK_THEME['border'],
                    'linecolor': DARK_THEME['border'],
                    'tickfont': {'color': DARK_THEME['text']}
                },
                'legend': {
                    'font': {'color': DARK_THEME['text']},
                    'bgcolor': DARK_THEME['surface']
                }
            }
        }
    
    @staticmethod
    def apply_dark_theme_to_figure(fig):
        """Apply dark theme to a Plotly figure"""
        fig.update_layout(
            paper_bgcolor=DARK_THEME['background'],
            plot_bgcolor=DARK_THEME['background'],
            font=dict(color=DARK_THEME['text']),
            xaxis=dict(
                gridcolor=DARK_THEME['border'],
                linecolor=DARK_THEME['border']
            ),
            yaxis=dict(
                gridcolor=DARK_THEME['border'],
                linecolor=DARK_THEME['border']
            )
        )
        return fig

class DataProcessor:
    """Utility functions for data processing"""
    
    @staticmethod
    def calculate_statistics(data, column):
        """Calculate basic statistics for a data column"""
        if isinstance(data, pd.DataFrame) and column in data.columns:
            return {
                'count': len(data),
                'mean': data[column].mean(),
                'median': data[column].median(),
                'std': data[column].std(),
                'min': data[column].min(),
                'max': data[column].max(),
                'q25': data[column].quantile(0.25),
                'q75': data[column].quantile(0.75)
            }
        return None
    
    @staticmethod
    def detect_outliers(data, column, method='iqr'):
        """Detect outliers in data using specified method"""
        if method == 'iqr':
            Q1 = data[column].quantile(0.25)
            Q3 = data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
            return outliers
        return pd.DataFrame()
    
    @staticmethod
    def normalize_data(data, column, method='minmax'):
        """Normalize data using specified method"""
        if method == 'minmax':
            return (data[column] - data[column].min()) / (data[column].max() - data[column].min())
        elif method == 'zscore':
            return (data[column] - data[column].mean()) / data[column].std()
        return data[column]

class ChartEnhancer:
    """Enhance charts with additional features"""
    
    @staticmethod
    def add_annotations(fig, annotations):
        """Add annotations to a Plotly figure"""
        for annotation in annotations:
            fig.add_annotation(
                x=annotation.get('x'),
                y=annotation.get('y'),
                text=annotation.get('text'),
                showarrow=annotation.get('showarrow', True),
                arrowhead=annotation.get('arrowhead', 2),
                arrowsize=annotation.get('arrowsize', 1),
                arrowwidth=annotation.get('arrowwidth', 2),
                arrowcolor=annotation.get('arrowcolor', DARK_THEME['primary'])
            )
        return fig
    
    @staticmethod
    def add_trend_line(fig, x, y, color=DARK_THEME['secondary']):
        """Add trend line to scatter plot"""
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=x,
            y=p(x),
            mode='lines',
            name='Trend Line',
            line=dict(color=color, width=2, dash='dash')
        ))
        return fig
    
    @staticmethod
    def add_confidence_interval(fig, x, y, confidence=0.95):
        """Add confidence interval to line plot"""
        # Simple confidence interval calculation
        mean_y = np.mean(y)
        std_y = np.std(y)
        z_score = 1.96  # 95% confidence interval
        
        upper_bound = mean_y + z_score * std_y
        lower_bound = mean_y - z_score * std_y
        
        fig.add_trace(go.Scatter(
            x=x,
            y=upper_bound,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            fillcolor=DARK_THEME['primary'],
            fill='tonexty'
        ))
        
        fig.add_trace(go.Scatter(
            x=x,
            y=lower_bound,
            mode='lines',
            line=dict(width=0),
            fillcolor=DARK_THEME['primary'],
            fill='tonexty',
            showlegend=False
        ))
        
        return fig

class ExportManager:
    """Handle chart and data export functionality"""
    
    @staticmethod
    def export_chart_as_image(fig, format='png', width=800, height=600):
        """Export Plotly chart as image"""
        try:
            img_bytes = fig.to_image(format=format, width=width, height=height)
            return img_bytes
        except Exception as e:
            print(f"Error exporting chart: {e}")
            return None
    
    @staticmethod
    def export_data_as_csv(data, filename='exported_data.csv'):
        """Export data as CSV"""
        try:
            if isinstance(data, pd.DataFrame):
                return data.to_csv(index=False)
            return None
        except Exception as e:
            print(f"Error exporting data: {e}")
            return None
    
    @staticmethod
    def export_data_as_json(data, filename='exported_data.json'):
        """Export data as JSON"""
        try:
            if isinstance(data, pd.DataFrame):
                return data.to_json(orient='records', indent=2)
            return None
        except Exception as e:
            print(f"Error exporting data: {e}")
            return None

class PerformanceMonitor:
    """Monitor and optimize performance"""
    
    @staticmethod
    def measure_execution_time(func):
        """Decorator to measure function execution time"""
        import time
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
            return result
        return wrapper
    
    @staticmethod
    def optimize_dataframe(df, columns=None):
        """Optimize DataFrame memory usage"""
        if columns is None:
            columns = df.columns
        
        for col in columns:
            if df[col].dtype == 'object':
                if df[col].nunique() / len(df) < 0.5:
                    df[col] = df[col].astype('category')
            elif df[col].dtype == 'int64':
                if df[col].min() >= 0:
                    if df[col].max() < 255:
                        df[col] = df[col].astype('uint8')
                    elif df[col].max() < 65535:
                        df[col] = df[col].astype('uint16')
                    else:
                        df[col] = df[col].astype('uint32')
                else:
                    if df[col].min() > -128 and df[col].max() < 127:
                        df[col] = df[col].astype('int8')
                    elif df[col].min() > -32768 and df[col].max() < 32767:
                        df[col] = df[col].astype('int16')
                    else:
                        df[col] = df[col].astype('int32')
            elif df[col].dtype == 'float64':
                df[col] = df[col].astype('float32')
        
        return df

# Global instances
theme_manager = ThemeManager()
data_processor = DataProcessor()
chart_enhancer = ChartEnhancer()
export_manager = ExportManager()
performance_monitor = PerformanceMonitor() 