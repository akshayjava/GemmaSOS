#!/usr/bin/env python3
"""
GemmaSOS Demo Launcher
Simple launcher for the crisis intervention demo
"""

import sys
import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_demo_dependencies():
    """Check if required dependencies are installed for demo"""
    required_packages = [
        "gradio",
        "torch",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages for demo: {', '.join(missing_packages)}")
        logger.info("Please install dependencies with: pip install gradio torch numpy")
        return False
    
    return True

def main():
    """Main demo launcher function"""
    logger.info("Starting GemmaSOS Demo...")
    
    # Check dependencies
    if not check_demo_dependencies():
        sys.exit(1)
    
    # Check if demo app exists
    if not os.path.exists("demo_app.py"):
        logger.error("demo_app.py not found. Please run from the correct directory.")
        sys.exit(1)
    
    try:
        # Import and run the demo application
        from demo_app import main as run_demo
        run_demo()
        
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Error running demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
