#!/usr/bin/env python3
"""
Launcher script for Modern Data Visualization Dashboard
Run either Streamlit or Gradio application
"""

import sys
import subprocess
import os
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    📊 Modern Data Visualization Dashboard                   ║
    ║                                                              ║
    ║    15 Interactive Visualizations with Dark Theme            ║
    ║                                                              ║
    ║    Built with Streamlit & Gradio                            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit', 'gradio', 'plotly', 'pandas', 'numpy',
        'matplotlib', 'seaborn', 'folium', 'wordcloud'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def run_streamlit():
    """Run Streamlit application"""
    print("🚀 Starting Streamlit application...")
    print("📊 Dashboard will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 60)
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Streamlit application stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

def run_gradio():
    """Run Gradio application"""
    print("🚀 Starting Gradio application...")
    print("📊 Dashboard will open in your browser at: http://localhost:7860")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 60)
    
    try:
        # Start Gradio
        subprocess.run([sys.executable, "gradio_app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Gradio application stopped.")
    except Exception as e:
        print(f"❌ Error running Gradio: {e}")

def run_both():
    """Run both applications"""
    print("🚀 Starting both applications...")
    print("📊 Streamlit: http://localhost:8501")
    print("📊 Gradio: http://localhost:7860")
    print("⏹️  Press Ctrl+C to stop both applications")
    print("-" * 60)
    
    try:
        # Start Streamlit in background
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        # Start Gradio
        gradio_process = subprocess.Popen([sys.executable, "gradio_app.py"])
        
        # Wait for either process to finish
        while True:
            if streamlit_process.poll() is not None:
                print("🛑 Streamlit application stopped.")
                gradio_process.terminate()
                break
            elif gradio_process.poll() is not None:
                print("🛑 Gradio application stopped.")
                streamlit_process.terminate()
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping both applications...")
        try:
            streamlit_process.terminate()
            gradio_process.terminate()
        except:
            pass
        print("✅ Both applications stopped.")
    except Exception as e:
        print(f"❌ Error running applications: {e}")

def show_help():
    """Show help information"""
    help_text = """
    📖 Usage:
        python run_apps.py [option]
    
    🎯 Options:
        streamlit    Run Streamlit application (http://localhost:8501)
        gradio       Run Gradio application (http://localhost:7860)
        both         Run both applications simultaneously
        help         Show this help message
    
    📋 Examples:
        python run_apps.py streamlit
        python run_apps.py gradio
        python run_apps.py both
    
    🔧 Prerequisites:
        - Python 3.7+
        - All dependencies installed (pip install -r requirements.txt)
    
    🌐 Features:
        - 15 different visualizations
        - Modern dark theme UI
        - Interactive controls
        - Demo data included
        - Responsive design
    """
    print(help_text)

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("❌ Please specify which application to run.")
        print("💡 Use 'python run_apps.py help' for usage information.")
        sys.exit(1)
    
    option = sys.argv[1].lower()
    
    if option == "streamlit":
        run_streamlit()
    elif option == "gradio":
        run_gradio()
    elif option == "both":
        run_both()
    elif option in ["help", "-h", "--help"]:
        show_help()
    else:
        print(f"❌ Unknown option: {option}")
        print("💡 Use 'python run_apps.py help' for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    main() 