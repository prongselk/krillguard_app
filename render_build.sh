#!/bin/bash

# Exit script if any command fails
set -e  

echo "Starting Render build script..."

# Install Miniconda
echo "Downloading and installing Miniconda..."
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

# Initialize Conda
echo "Initializing Conda..."
export PATH="$HOME/miniconda/bin:$PATH"
source $HOME/miniconda/etc/profile.d/conda.sh || true 
conda init || true 

# Create and activate a new Conda environment
echo "Creating Conda environment..."
conda create -n myenv python=3.9 -y
conda activate myenv

# Install Basemap
echo "Installing Basemap..."
conda install -n myenv -c conda-forge basemap -y

# Install Gunicorn and Pip dependencies inside Conda environment
echo "Installing Python dependencies..."
conda run -n myenv pip install --upgrade pip
conda run -n myenv pip install -r requirements.txt
conda run -n myenv pip install gunicorn

echo "Build process complete"

