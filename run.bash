


sudo systemctl start supervisor
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn dashcam/src/fast-api:app


curl http://localhost:8000