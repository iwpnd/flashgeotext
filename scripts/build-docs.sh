#!/usr/bin/env bash

mkdocs build
pydocmd simple flashgeotext.geotext++ > docs/geotext.md
pydocmd simple flashgeotext.lookup++ > docs/lookup.md
