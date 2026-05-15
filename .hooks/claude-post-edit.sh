#!/usr/bin/env bash
# Claude-specific post-edit shim — delegate to neutral implementation

exec /mnt/workspace/.hooks/post-edit.sh "$@"
