#!/bin/bash
# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

# Initialize Conda and install dependencies
conda init
conda create -n myenv python=3.9 -y
conda activate myenv
conda install -c conda-forge basemap -y

# Install Gunicorn inside Conda
conda install -n myenv -c conda-forge gunicorn -y


# Install pip dependencies
pip install -r requirements.txt
