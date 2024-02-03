#!/bin/bash
source .venv/bin/activate
sudo systemctl restart nginx




uvicorn dashcam/src/fast-api:app

