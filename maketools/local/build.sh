#!/usr/bin/env bash
#
# $1 the name to use for the image locally
# $2 the tag to use for the image locally
# $3 docker image
# $4 make marker file


marker_file=$4
if [ "$1" == "-c" ]; then
marker_file=$2
fi

touch "${marker_file}"
