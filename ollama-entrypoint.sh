#!/bin/sh
set -e

# Start Ollama in the background
ollama serve &

# Wait a few seconds to ensure the server is ready
sleep 3

# Pull the model
ollama pull tinyllama

# Wait for background process to finish (keeps container running)
wait
