#! /bin/sh

BASEDIR=$(dirname "$0")
cd "$BASEDIR" && ncat -lvkp 5683 -e a.out

# a.out is same as vuln in the static folder