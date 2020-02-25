#!/usr/bin/env bash

python -m mkdocs build
python -m pydocmd simple flashgeotext.geotext++ > docs/geotext.md
python -m pydocmd simple flashgeotext.lookup++ > docs/lookup.md
