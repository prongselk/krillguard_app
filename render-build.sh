#!/usr/bin/env bash

# Update package lists
apt-get update 

# Install system dependencies required for ipopt and cyipopt
apt-get install -y \
    pkg-config \
    coinor-libipopt-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv

# Set PKG_CONFIG_PATH so pip can find ipopt
export PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig

# Upgrade pip and setuptools
pip install --upgrade pip setuptools

# Install cyipopt separately to ensure it finds ipopt
pip install --no-cache-dir --use-pep517 cyipopt

# Install all other Python dependencies
pip install --no-cache-dir -r requirements.txt
