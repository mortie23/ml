#!/bin/sh
set -e
. /build/.venv/bin/activate

# https://fastapi.tiangolo.com/deployment/docker/#dockerfile
fastapi run /model/predict.py --port 8080