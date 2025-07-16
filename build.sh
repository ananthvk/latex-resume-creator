#!/bin/sh
set -e
docker run -it \
  --env-file .env \
  -v $(pwd)/output:/output \
  -v $(pwd)/src/resume_creator:/app/src/resume_creator \
  resume