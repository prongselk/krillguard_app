#!/bin/bash
set -e  # Exit on error

echo "Initializing Conda..."
export PATH="/usr/share/miniconda/bin:$PATH"  # Use system-installed Conda
source /usr/share/miniconda/etc/profile.d/conda.sh  # Initialize Conda
conda init bash  # Ensure Conda is properly initialized

echo "Creating Conda environment..."
conda create -n myenv python=3.9 -y

# Activate the Conda environment
echo "Activating Conda environment..."
source /usr/share/miniconda/etc/profile.d/conda.sh
conda activate myenv

echo "Installing Conda dependencies..."
conda install -n myenv -c conda-forge pandas numpy matplotlib basemap openpyxl -y

echo "Installing remaining dependencies with pip..."
pip install dash flask plotly gunicorn

echo "Build process complete"
