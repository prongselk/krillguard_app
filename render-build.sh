#!/usr/bin/env bash

# Install system dependencies
apt-get update && apt-get install -y \
    pkg-config \
    libipopt-dev \
    build-essential \
    python3-dev

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
