#!/usr/bin/env bash
#
# $1 local name for the image
# $2 local tag for the image
index=3
if [ "$1" == "-c" ]; then
index=2
fi

/usr/bin/env bash -c "${@:${index}}"
