#!/bin/bash
# Start Ollama and pull necessary model
if ! command -v ollama >/dev/null 2>&1; then
  echo "Please install Ollama: https://ollama.com/"
  exit 1
fi

if ! ollama list | grep -q llama3; then
  echo "Pulling Llama3 model via Ollama..."
  ollama pull llama3
fi
ollama serve