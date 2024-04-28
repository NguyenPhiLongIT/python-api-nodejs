apt-get update && apt-get install ffmpeg libsm6 libxext6 python3-pip python3.10-venv python3-flask  -y
pip install -r python/requirements.txt

python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements.txt