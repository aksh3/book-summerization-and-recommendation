#!/bin/bash
set -e
echo "Copying .env.example to .env ..."
if [ ! -f .env ]; then
  cp .env .env
fi
echo "Installing python deps ..."
pip install -U pip
pip install -r requirements.txt
echo "Setup complete."