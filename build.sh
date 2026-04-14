#!/bin/bash
# Install system dependencies for Pillow and PyMuPDF
apt-get update
apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    mupdf-tools

# Install Python packages
pip install -r requirements.txt
