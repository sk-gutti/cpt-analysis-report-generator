#!/usr/bin/env python3
"""
macOS Setup Script for CPT Analysis Report Generator
Creates a virtual environment and installs dependencies safely
"""

import subprocess
import sys
import os

def create_virtual_environment():
    """Create a virtual environment"""
    print("🔧 Creating virtual environment...")
    try:
        subprocess.check_call(["python3", "-m", "venv", "venv"])
        print("✅ Virtual environment created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def install_requirements():
    """Install required packages in virtual environment"""
    print("📦 Installing required packages...")
    try:
        # Use the virtual environment's pip
        pip_path = "./venv/bin/pip"
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_streamlit_app():
    """Run the Streamlit application using virtual environment"""
    print("🚀 Starting CPT Analysis Report Generator...")
    try:
        # Use the virtual environment's python
        python_path = "./venv/bin/python"
        subprocess.run([python_path, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup and run function for macOS"""
    print("=" * 60)
    print("🍎 CPT Analysis Report Generator - macOS Setup & Run")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        print("Please run this script from the project directory")
        return
    
    # Check if virtual environment already exists
    if not os.path.exists("venv"):
        if not create_virtual_environment():
            print("❌ Failed to create virtual environment.")
            return
    else:
        print("✅ Virtual environment already exists!")
    
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