#!/usr/bin/env python3
"""
GemmaSOS Launcher Script
Simple launcher for the crisis intervention system
"""

import sys
import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "torch",
        "transformers", 
        "gradio",
        "PIL",
        "cv2",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "PIL":
                import PIL
            elif package == "cv2":
                import cv2
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.info("Please install dependencies with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function"""
    logger.info("Starting GemmaSOS Crisis Intervention System...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if main app exists
    if not os.path.exists("main_app.py"):
        logger.error("main_app.py not found. Please run from the correct directory.")
        sys.exit(1)
    
    try:
        # Import and run the main application
        from main_app import main as run_app
        run_app()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
