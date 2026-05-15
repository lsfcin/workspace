#!/usr/bin/env bash
# Claude-specific pre-read shim — delegate to neutral implementation

exec /mnt/workspace/.hooks/pre-read.sh "$@"
