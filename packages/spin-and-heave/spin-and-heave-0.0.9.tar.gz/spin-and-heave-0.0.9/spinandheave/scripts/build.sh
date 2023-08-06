#!/bin/bash

set -euo pipefail

# Read variables from command line arguments
FILENAME=$1
RUNTIME=$2
SOURCE_PATH=$3
if [[ $2 == *"nodejs"* ]]; then
    BUILD_CMD="npm install --production"
else
    BUILD_CMD="pip install --progress-bar off -r requirements.txt -t ."
fi
ZIP_NAME="$RUNTIME.zip"

# Install dependencies, using a Docker image to correctly build native extensions
docker run --rm -t -v "$FILENAME:/src" -v "$SOURCE_PATH:/out" lambci/lambda:build-$RUNTIME sh -c "
    cp -r /src /build &&
    cd /build &&
    $BUILD_CMD &&
    chmod -R 755 . &&
    zip -r /out/$ZIP_NAME . &&
    chown \$(stat -c '%u:%g' /out) /out/$ZIP_NAME
"
