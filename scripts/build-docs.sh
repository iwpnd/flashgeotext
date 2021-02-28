#!/usr/bin/env bash

poetry run mkdocs build
poetry run pydocmd simple flashgeotext.geotext++ > docs/geotext.md
poetry run pydocmd simple flashgeotext.lookup++ > docs/lookup.md
