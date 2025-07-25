#!/usr/bin/env python3
"""
Setup and Run Script for CPT Analysis Report Generator
This script will install all required dependencies and run the Streamlit app
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call(["python3", "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_streamlit_app():
    """Run the Streamlit application"""
    print("🚀 Starting CPT Analysis Report Generator...")
    try:
        subprocess.run(["python3", "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup and run function"""
    print("=" * 60)
    print("🏥 CPT Analysis Report Generator - Setup & Run")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        print("Please run this script from the project directory")
        return
    
    # Install dependencies
    if not install_requirements():
        print("❌ Failed to install dependencies. Please check the error messages above.")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete! Starting the application...")
    print("📝 The app will open in your browser automatically")
    print("🔗 If it doesn't open, go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 60)
    
    # Run the application
    run_streamlit_app()

if __name__ == "__main__":
    main() 