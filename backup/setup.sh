#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Set up chromedriver
python setup_chromedriver.py

# Start the application
streamlit run app.py
