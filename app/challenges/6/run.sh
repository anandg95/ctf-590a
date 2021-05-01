#! /bin/sh

BASEDIR=$(dirname "$0")
cd "$BASEDIR" && uvicorn main:app --host 0.0.0.0 --port 5681