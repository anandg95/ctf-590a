#! /bin/sh

BASEDIR=$(dirname "$0")
cd "$BASEDIR" && ncat -lvkp 5679 -e a.out