#! /bin/sh

BASEDIR=$(dirname "$0")
cd "$BASEDIR" && uvicorn slow_server:app --host 0.0.0.0 --port 5678