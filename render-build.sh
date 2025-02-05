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
    python3-dev

# Set PKG_CONFIG_PATH to help pip find ipopt
export PKG_CONFIG_PATH=/usr/lib/pkgconfig

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
