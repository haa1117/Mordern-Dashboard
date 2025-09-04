#!/usr/bin/env python3
"""
Demo script for Modern Data Visualization Dashboard
Showcases all 15 visualizations with explanations
"""

import sys
import time
from data_generator import data_gen
from visualizations import viz_gen
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def print_demo_header():
    """Print demo header"""
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🎯 Data Visualization Demo                               ║
    ║                                                              ║
    ║    15 Interactive Visualizations Showcase                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(header)

def demo_data_generation():
    """Demo data generation capabilities"""
    print("🔧 Data Generation Demo")
    print("=" * 50)
    
    # Generate all datasets
    all_data = data_gen.get_all_data()
    
    print(f"📊 Generated {len(all_data)} different datasets:")
    for name, data in all_data.items():
        if isinstance(data, dict):
            print(f"   • {name}: {len(data)} items")
        elif hasattr(data, 'shape'):
            print(f"   • {name}: {data.shape}")
        else:
            print(f"   • {name}: {len(data)} records")
    
    print("\n📈 Sample data from time series:")
    time_data = all_data['time_series']
    print(f"   Date range: {time_data['date'].min()} to {time_data['date'].max()}")
    print(f"   Value range: {time_data['value'].min():.2f} to {time_data['value'].max():.2f}")
    print(f"   Total records: {len(time_data):,}")
    
    print("\n✅ Data generation completed successfully!")
    print("-" * 50)

def demo_visualizations():
    """Demo all visualizations"""
    print("\n🎨 Visualization Demo")
    print("=" * 50)
    
    viz_functions = viz_gen.get_all_visualizations()
    
    for i, (name, func) in enumerate(viz_functions.items(), 1):
        print(f"\n{i:2d}. {name}")
        print("-" * 30)
        
        try:
            # Create visualization
            start_time = time.time()
            fig = func()
            end_time = time.time()
            
            print(f"   ✅ Created successfully in {end_time - start_time:.3f}s")
            
            # Get figure info
            if hasattr(fig, 'data'):
                print(f"   📊 Traces: {len(fig.data)}")
                print(f"   🎯 Type: {type(fig).__name__}")
            
            # Show figure info
            if hasattr(fig, 'layout') and fig.layout.title:
                print(f"   📝 Title: {fig.layout.title.text}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n✅ All {len(viz_functions)} visualizations processed!")
    print("-" * 50)

def demo_interactive_features():
    """Demo interactive features"""
    print("\n🎮 Interactive Features Demo")
    print("=" * 50)
    
    # Create a sample interactive visualization
    data = data_gen.generate_scatter_data()
    
    # Create interactive scatter plot
    fig = px.scatter(
        data, x='x', y='y', 
        color='category',
        size='size',
        title='Interactive Scatter Plot Demo',
        color_discrete_sequence=['#00ff88', '#ff6b6b', '#4ecdc4']
    )
    
    fig.update_layout(
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font=dict(color='#ffffff'),
        xaxis=dict(gridcolor='#404040'),
        yaxis=dict(gridcolor='#404040')
    )
    
    print("📊 Interactive Scatter Plot created with:")
    print("   • Color coding by category")
    print("   • Size encoding by value")
    print("   • Hover information")
    print("   • Zoom and pan capabilities")
    print("   • Dark theme styling")
    
    # Save the figure
    try:
        fig.write_html("demo_scatter_plot.html")
        print("   💾 Saved as 'demo_scatter_plot.html'")
    except Exception as e:
        print(f"   ❌ Could not save: {e}")
    
    print("\n✅ Interactive features demo completed!")
    print("-" * 50)

def demo_performance():
    """Demo performance metrics"""
    print("\n⚡ Performance Demo")
    print("=" * 50)
    
    # Test data generation performance
    print("📊 Data Generation Performance:")
    
    datasets = [
        ('Time Series (365 days)', lambda: data_gen.generate_time_series_data(365)),
        ('Scatter Data (500 points)', lambda: data_gen.generate_scatter_data(500)),
        ('3D Scatter (200 points)', lambda: data_gen.generate_3d_scatter_data(200)),
        ('Histogram (1000 samples)', lambda: data_gen.generate_histogram_data(1000)),
        ('Box Plot Data', lambda: data_gen.generate_boxplot_data()),
    ]
    
    for name, func in datasets:
        start_time = time.time()
        data = func()
        end_time = time.time()
        
        if hasattr(data, 'shape'):
            size_info = f"{data.shape}"
        else:
            size_info = f"{len(data)} records"
        
        print(f"   • {name}: {end_time - start_time:.4f}s ({size_info})")
    
    # Test visualization performance
    print("\n🎨 Visualization Performance:")
    
    viz_tests = [
        ('Line Chart', viz_gen.create_line_chart),
        ('Bar Chart', viz_gen.create_bar_chart),
        ('Scatter Plot', viz_gen.create_scatter_plot),
        ('Pie Chart', viz_gen.create_pie_chart),
        ('Heatmap', viz_gen.create_heatmap),
    ]
    
    for name, func in viz_tests:
        start_time = time.time()
        try:
            fig = func()
            end_time = time.time()
            print(f"   • {name}: {end_time - start_time:.4f}s")
        except Exception as e:
            print(f"   • {name}: Error - {e}")
    
    print("\n✅ Performance demo completed!")
    print("-" * 50)

def demo_data_analysis():
    """Demo data analysis capabilities"""
    print("\n📈 Data Analysis Demo")
    print("=" * 50)
    
    # Analyze time series data
    time_data = data_gen.generate_time_series_data()
    
    print("📊 Time Series Analysis:")
    print(f"   • Total records: {len(time_data):,}")
    print(f"   • Date range: {time_data['date'].min()} to {time_data['date'].max()}")
    print(f"   • Value statistics:")
    print(f"     - Mean: {time_data['value'].mean():.2f}")
    print(f"     - Median: {time_data['value'].median():.2f}")
    print(f"     - Std Dev: {time_data['value'].std():.2f}")
    print(f"     - Min: {time_data['value'].min():.2f}")
    print(f"     - Max: {time_data['value'].max():.2f}")
    
    # Analyze categorical data
    cat_data = data_gen.generate_categorical_data()
    
    print("\n📊 Categorical Analysis:")
    print(f"   • Categories: {len(cat_data)}")
    print(f"   • Top performer: {cat_data.loc[cat_data['value'].idxmax(), 'category']}")
    print(f"   • Average value: {cat_data['value'].mean():.2f}")
    print(f"   • Value range: {cat_data['value'].min():.2f} - {cat_data['value'].max():.2f}")
    
    # Analyze correlation
    scatter_data = data_gen.generate_scatter_data()
    correlation = scatter_data['x'].corr(scatter_data['y'])
    
    print(f"\n📊 Correlation Analysis:")
    print(f"   • X-Y correlation: {correlation:.3f}")
    print(f"   • Data points: {len(scatter_data):,}")
    print(f"   • Categories: {scatter_data['category'].nunique()}")
    
    print("\n✅ Data analysis demo completed!")
    print("-" * 50)

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📖 Usage Instructions")
    print("=" * 50)
    
    instructions = """
    🚀 To run the applications:
    
    1. Install dependencies:
       pip install -r requirements.txt
    
    2. Run Streamlit app:
       python run_apps.py streamlit
       # or
       streamlit run streamlit_app.py
    
    3. Run Gradio app:
       python run_apps.py gradio
       # or
       python gradio_app.py
    
    4. Run both simultaneously:
       python run_apps.py both
    
    🎯 Features available:
    • 15 different visualization types
    • Interactive controls and filters
    • Dark theme UI
    • Real-time data generation
    • Responsive design
    • Export capabilities
    
    📊 Visualization types:
    1. Line Chart - Time series trends
    2. Bar Chart - Categorical comparison
    3. Scatter Plot - Correlation analysis
    4. Pie Chart - Distribution visualization
    5. Heatmap - Matrix data representation
    6. 3D Scatter - Multi-dimensional data
    7. Area Chart - Cumulative trends
    8. Box Plot - Statistical distribution
    9. Histogram - Frequency distribution
    10. Violin Plot - Density distribution
    11. Word Cloud - Text visualization
    12. Map - Geographic data
    13. Gauge Chart - Progress indicators
    14. Funnel Chart - Process flow
    15. Radar Chart - Multi-dimensional comparison
    """
    
    print(instructions)

def main():
    """Main demo function"""
    print_demo_header()
    
    try:
        # Run all demos
        demo_data_generation()
        demo_visualizations()
        demo_interactive_features()
        demo_performance()
        demo_data_analysis()
        show_usage_instructions()
        
        print("\n🎉 Demo completed successfully!")
        print("🚀 Ready to run the full applications!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main() 