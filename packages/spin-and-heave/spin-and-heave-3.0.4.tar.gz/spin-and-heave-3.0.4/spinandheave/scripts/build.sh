#!/bin/bash

set -euo pipefail

SRC=$1
RUNTIME=$2
CWD=$3
LAMBDA_NAME=$4
#if [[ $2 == *"nodejs"* ]]; then
#    BUILD_CMD="npm install --production"
#else
#    BUILD_CMD="pip install --progress-bar off -r requirements.txt -t ."
#fi
BUILD_CMD=$5
ZIP_NAME="$LAMBDA_NAME.zip"

docker run --rm -t -v "$SRC:/src" -v "$CWD:/out" lambci/lambda:build-$RUNTIME sh -c "
    cp -r /src /build &&
    cd /build &&
    $BUILD_CMD &&
    chmod -R 755 . &&
    zip -r /out/$ZIP_NAME . &&
    chown \$(stat -c '%u:%g' /out) /out/$ZIP_NAME
"
