"""
Setup script for GemmaSOS - Crisis Response and Intervention System
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gemma-sos",
    version="1.0.0",
    author="GemmaSOS Team",
    author_email="support@gemmasos.org",
    description="On-device crisis response and intervention system using Google's Gemma model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gemmasos/crisis-intervention",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "gpu": [
            "torch>=2.0.0+cu118",
            "transformers>=4.35.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gemma-sos=main_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords=[
        "crisis intervention",
        "mental health",
        "suicide prevention",
        "on-device AI",
        "privacy",
        "gemma",
        "crisis support",
        "trauma-informed care"
    ],
    project_urls={
        "Bug Reports": "https://github.com/gemmasos/crisis-intervention/issues",
        "Source": "https://github.com/gemmasos/crisis-intervention",
        "Documentation": "https://github.com/gemmasos/crisis-intervention/wiki",
    },
)
