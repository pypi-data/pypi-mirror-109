"""Python package template."""

import json

with open('package.json', 'r') as f:
  __version__ = json.load(f)['version']
