#!/usr/bin/env bash

source .venv/bin/activate
uv run app.py
# firefox --private-window "http://localhost:8080/"
