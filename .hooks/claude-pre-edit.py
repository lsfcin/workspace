#!/usr/bin/env python3
# Claude-specific pre-edit shim — delegate to neutral implementation

import os, sys

os.execv(sys.executable, [sys.executable, "/mnt/workspace/.hooks/pre-edit.py"] + sys.argv[1:])
