#!/usr/bin/env python3
"""
Simple run script for CPT Analysis Report Generator
Use this after initial setup is complete
"""

import subprocess
import os

def main():
    """Run the Streamlit application"""
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found!")
        print("Please run 'python3 setup_mac.py' first to set up the environment.")
        return
    
    print("🚀 Starting CPT Analysis Report Generator...")
    print("🔗 Opening at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        # Use the virtual environment's python
        python_path = "./venv/bin/python"
        subprocess.run([python_path, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 