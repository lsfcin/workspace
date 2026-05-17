---
name: datasets-root
description: Overview of the Datasets/ directory — what datasets live here, their purpose, and download links
metadata:
  type: reference
---

# Datasets

Research datasets used across workspace projects. Each subdirectory contains one dataset with its own `CONTEXT.md`.

Datasets are **not versioned** (binary files excluded via `.gitignore`). Only `CONTEXT.md` files are tracked. To reproduce a local setup, download each dataset from the link in its `CONTEXT.md`.

## Contents

| Folder | Dataset | Paper |
|--------|---------|-------|
| `relativistic_raytracer/` | GPU benchmark renders — Unity vs Vulkan, 6 scenes, 3 metrics, 4 integrators | Cavalcanti & Figueiredo 2026 |
