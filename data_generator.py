import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from wordcloud import WordCloud
import json

class DataGenerator:
    def __init__(self):
        self.setup_random_seed()
        
    def setup_random_seed(self, seed=42):
        """Set random seed for reproducible data"""
        np.random.seed(seed)
        random.seed(seed)
    
    def generate_time_series_data(self, days=365):
        """Generate time series data for line charts"""
        dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
        base_trend = np.linspace(100, 150, days)
        seasonal = 20 * np.sin(2 * np.pi * np.arange(days) / 365)
        noise = np.random.normal(0, 5, days)
        
        data = pd.DataFrame({
            'date': dates,
            'value': base_trend + seasonal + noise,
            'volume': np.random.poisson(1000, days) + 500
        })
        return data
    
    def generate_categorical_data(self):
        """Generate categorical data for bar charts"""
        categories = ['Technology', 'Healthcare', 'Finance', 'Education', 'Retail', 'Manufacturing', 'Transportation']
        values = np.random.normal(100, 30, len(categories))
        
        data = pd.DataFrame({
            'category': categories,
            'value': np.abs(values),
            'growth': np.random.normal(5, 2, len(categories))
        })
        return data
    
    def generate_scatter_data(self, n_points=500):
        """Generate scatter plot data with correlation"""
        x = np.random.normal(0, 1, n_points)
        y = 0.7 * x + np.random.normal(0, 0.3, n_points)
        categories = np.random.choice(['A', 'B', 'C'], n_points)
        
        data = pd.DataFrame({
            'x': x,
            'y': y,
            'category': categories,
            'size': np.random.uniform(10, 100, n_points)
        })
        return data
    
    def generate_pie_data(self):
        """Generate data for pie charts"""
        categories = ['Desktop', 'Mobile', 'Tablet', 'Other']
        values = [45, 35, 15, 5]
        
        data = pd.DataFrame({
            'category': categories,
            'value': values,
            'percentage': [v/sum(values)*100 for v in values]
        })
        return data
    
    def generate_heatmap_data(self):
        """Generate correlation matrix data for heatmaps"""
        np.random.seed(42)
        n_vars = 8
        variables = [f'Var_{i+1}' for i in range(n_vars)]
        
        # Generate correlation matrix
        corr_matrix = np.random.uniform(-1, 1, (n_vars, n_vars))
        corr_matrix = (corr_matrix + corr_matrix.T) / 2  # Make symmetric
        np.fill_diagonal(corr_matrix, 1)  # Diagonal = 1
        
        data = pd.DataFrame(corr_matrix, columns=variables, index=variables)
        return data
    
    def generate_3d_scatter_data(self, n_points=200):
        """Generate 3D scatter plot data"""
        x = np.random.normal(0, 1, n_points)
        y = np.random.normal(0, 1, n_points)
        z = 0.5 * x + 0.3 * y + np.random.normal(0, 0.5, n_points)
        colors = np.random.choice(['red', 'blue', 'green'], n_points)
        
        data = pd.DataFrame({
            'x': x,
            'y': y,
            'z': z,
            'color': colors,
            'size': np.random.uniform(5, 20, n_points)
        })
        return data
    
    def generate_area_data(self, days=90):
        """Generate area chart data"""
        dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
        
        data = pd.DataFrame({
            'date': dates,
            'revenue': np.cumsum(np.random.normal(1000, 200, days)),
            'costs': np.cumsum(np.random.normal(600, 150, days)),
            'profit': np.cumsum(np.random.normal(400, 100, days))
        })
        return data
    
    def generate_boxplot_data(self):
        """Generate data for box plots"""
        groups = ['Group A', 'Group B', 'Group C', 'Group D']
        data_list = []
        
        for group in groups:
            n_samples = np.random.randint(50, 150)
            values = np.random.normal(np.random.uniform(50, 150), np.random.uniform(10, 30), n_samples)
            data_list.extend([{'group': group, 'value': val} for val in values])
        
        return pd.DataFrame(data_list)
    
    def generate_histogram_data(self, n_samples=1000):
        """Generate histogram data"""
        # Mix of normal distributions
        data1 = np.random.normal(50, 10, n_samples // 2)
        data2 = np.random.normal(80, 15, n_samples // 2)
        data = np.concatenate([data1, data2])
        
        return pd.DataFrame({'value': data})
    
    def generate_violin_data(self):
        """Generate violin plot data"""
        categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
        data_list = []
        
        for i, category in enumerate(categories):
            n_samples = np.random.randint(100, 300)
            mean = 50 + i * 20
            std = 10 + i * 5
            values = np.random.normal(mean, std, n_samples)
            data_list.extend([{'category': category, 'value': val} for val in values])
        
        return pd.DataFrame(data_list)
    
    def generate_wordcloud_data(self):
        """Generate text data for word clouds"""
        words = {
            'Data': 100, 'Analytics': 85, 'Visualization': 80, 'Machine Learning': 75,
            'Python': 90, 'Dashboard': 70, 'Insights': 65, 'Business': 60,
            'Technology': 55, 'Innovation': 50, 'Strategy': 45, 'Growth': 40,
            'Performance': 35, 'Optimization': 30, 'Efficiency': 25, 'Quality': 20
        }
        return words
    
    def generate_map_data(self):
        """Generate geographic data for maps"""
        cities = [
            {'city': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'value': 100},
            {'city': 'London', 'lat': 51.5074, 'lon': -0.1278, 'value': 85},
            {'city': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503, 'value': 90},
            {'city': 'Paris', 'lat': 48.8566, 'lon': 2.3522, 'value': 75},
            {'city': 'Sydney', 'lat': -33.8688, 'lon': 151.2093, 'value': 60},
            {'city': 'Berlin', 'lat': 52.5200, 'lon': 13.4050, 'value': 70},
            {'city': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'value': 80},
            {'city': 'São Paulo', 'lat': -23.5505, 'lon': -46.6333, 'value': 65}
        ]
        return pd.DataFrame(cities)
    
    def generate_gauge_data(self):
        """Generate data for gauge charts"""
        metrics = ['CPU Usage', 'Memory Usage', 'Disk Usage', 'Network Usage']
        values = [75, 60, 85, 45]
        max_values = [100, 100, 100, 100]
        
        data = pd.DataFrame({
            'metric': metrics,
            'value': values,
            'max_value': max_values,
            'percentage': [v/m*100 for v, m in zip(values, max_values)]
        })
        return data
    
    def generate_funnel_data(self):
        """Generate funnel chart data"""
        stages = ['Website Visits', 'Product Views', 'Add to Cart', 'Checkout', 'Purchase']
        values = [10000, 8000, 6000, 4000, 2500]
        
        data = pd.DataFrame({
            'stage': stages,
            'value': values,
            'conversion_rate': [100, 80, 60, 40, 25]
        })
        return data
    
    def generate_radar_data(self):
        """Generate radar chart data"""
        categories = ['Speed', 'Reliability', 'Usability', 'Features', 'Support', 'Price']
        product_a = [90, 85, 80, 75, 70, 65]
        product_b = [70, 90, 85, 80, 75, 90]
        product_c = [80, 75, 90, 85, 80, 75]
        
        data = pd.DataFrame({
            'category': categories,
            'Product A': product_a,
            'Product B': product_b,
            'Product C': product_c
        })
        return data
    
    def get_all_data(self):
        """Get all generated datasets"""
        return {
            'time_series': self.generate_time_series_data(),
            'categorical': self.generate_categorical_data(),
            'scatter': self.generate_scatter_data(),
            'pie': self.generate_pie_data(),
            'heatmap': self.generate_heatmap_data(),
            '3d_scatter': self.generate_3d_scatter_data(),
            'area': self.generate_area_data(),
            'boxplot': self.generate_boxplot_data(),
            'histogram': self.generate_histogram_data(),
            'violin': self.generate_violin_data(),
            'wordcloud': self.generate_wordcloud_data(),
            'map': self.generate_map_data(),
            'gauge': self.generate_gauge_data(),
            'funnel': self.generate_funnel_data(),
            'radar': self.generate_radar_data()
        }

# Global instance
data_gen = DataGenerator() 