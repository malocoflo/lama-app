#!/bin/bash
set -a
source .env
set +a
curl -X POST http://127.0.0.1:8000/predict \
 --header "${ACCESS_TOKEN_HEADER_NAME}: ${ACCESS_TOKEN}" \
 --header 'Content-Type: application/json' \
 --data '{"question": "Czym jest LLM?"}' \
 --connect-timeout 600 \
 --max-time 600