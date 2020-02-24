#!/usr/bin/env bash

python -m mkdocs build
cp ./docs/index.md ./readme.md
