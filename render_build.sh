#!/bin/bash
set -e  # Exit script if any command fails

echo "Initializing Conda..."
export PATH="$HOME/miniconda/bin:$PATH"
source $HOME/miniconda/etc/profile.d/conda.sh || true
conda init bash

echo "Creating Conda environment..."
conda create -n myenv python=3.9 -y

# Reinitialize Conda environment
echo "Reinitializing Conda..."
source $HOME/miniconda/etc/profile.d/conda.sh
conda activate myenv

echo "Installing Conda dependencies..."
conda install -n myenv -c conda-forge pandas numpy matplotlib basemap openpyxl -y

echo "Installing remaining dependencies with pip..."
pip install dash flask plotly gunicorn

echo "Build process complete"
