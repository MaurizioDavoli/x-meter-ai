#!/bin/bash
set -e

exec uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 1 --forwarded-allow-ips '*'