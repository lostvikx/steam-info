#!/usr/bin/env bash

mkdir -p "$(pwd)/data/games"
mkdir -p "$(pwd)/data/deals"

source .venv/bin/activate
echo 'Visit http://localhost:8080/ to view the website.'

uv run app.py
