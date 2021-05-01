#! /bin/sh

BASEDIR=$(dirname "$0")
cd "$BASEDIR" && ncat -lvkp 5680 -e a.py