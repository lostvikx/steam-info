#!/usr/bin/env bash

mkdir -p data/games
source .venv/bin/activate
uv run app.py
# firefox --private-window "http://localhost:8080/"
