#!/bin/bash
source .venv/bin/activate
sudo systemctl restart nginx




uvicorn main:app

