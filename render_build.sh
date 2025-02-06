#!/bin/bash
set -e  # Exit on error

echo "Initializing Conda..."
source $HOME/miniconda/etc/profile.d/conda.sh || true 
conda init || true 

echo "Creating Conda environment..."
conda create -n myenv python=3.9 -y
conda activate myenv

echo "Installing dependencies with Conda..."
conda install -n myenv -c conda-forge \
    pandas numpy matplotlib basemap openpyxl -y

echo "Installing remaining dependencies with pip..."
pip install dash flask plotly gunicorn

echo "Build process complete"
