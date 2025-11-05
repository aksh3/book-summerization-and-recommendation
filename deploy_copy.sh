#!/bin/bash
set -e

BASE_DIR="bookman"
mkdir -p $BASE_DIR

cp -r app $BASE_DIR/
cp -r migrations $BASE_DIR/
cp -r tests $BASE_DIR/
cp -r scripts $BASE_DIR/
cp Dockerfile $BASE_DIR/
cp docker-compose.yml $BASE_DIR/
cp requirements.txt $BASE_DIR/
cp .env.example $BASE_DIR/
cp README.md $BASE_DIR/
cp .gitignore $BASE_DIR/
echo "Project files copied to ./$BASE_DIR/"