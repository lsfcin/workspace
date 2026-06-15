# Dataset: Relativistic Raytracer Benchmark
> GPU benchmark renders and timing CSV — Unity vs Vulkan, 6 scenes, 4 integrators

**Download:** https://zenodo.org/records/20240662

## Setup

```
Datasets/relativistic_raytracer/
  Benchmark.csv          ← timing + metadata for all runs
  unity/
    unity_s1/ … unity_s6/   ← Unity render images (session batches, not scene-ordered)
  vulkan/
    vulkan_s1/ … vulkan_s6/ ← Vulkan render images (vulkan_s5 large, may need separate download)
```

Place the unzipped contents directly under `Datasets/relativistic_raytracer/` so the paths above match.

## Key facts

- **17,308 PNG images** total (9,636 Unity + 7,672 Vulkan when complete)
- **Timing CSV:** `Benchmark.csv` — columns: Timestamp, Application_Type, Resolution, Metric, Integrator, Scene_ID, Camera_Name, Step_Size, Step_Name, Gravity_Value, Gravity_Name, Spin_Speed, Spin_Name, Average_FPS, Frame_Count, Duration_Seconds, Image_Path
- **Image_Path** in CSV uses Windows-relative paths (`./Benchmarks\filename.png`); actual files are under `unity/unity_sX/` or `vulkan/vulkan_sX/`. Use filename-only lookup, not the full path.
- **Session folders** (`unity_s1`, etc.) are batch-export groups, not scene-ordered — images from multiple scenes appear in each session folder.
- **Step sizes:** SmallStep h=1, MediumStep h=52, BigStep h=260 (simulation internal units)
- **Spin names:** NaturalSpinSpeed, StrongSpinSpeed, UnaturalSpinSpeed, FunnySpinSpeed
- **Gravity names:** NormalG, StrongG, MuchStrongerG; Scene 6 uses Grav_1.989e31/32/33/34

## Analysis scripts

See `Academy/papers/relativistic_raytracer/scripts/`:
- `image_metrics.py` — computes PSNR/SSIM/L∞/MAE between image pairs
- `image_summarize.py` — aggregates raw outputs into summary CSVs

Run from `Datasets/relativistic_raytracer/`:
```bash
pip install pillow scikit-image numpy pandas
python ../../Academy/papers/relativistic_raytracer/scripts/image_metrics.py platform   --csv Benchmark.csv --base .
python ../../Academy/papers/relativistic_raytracer/scripts/image_metrics.py integrator --csv Benchmark.csv --base .
python ../../Academy/papers/relativistic_raytracer/scripts/image_summarize.py platform
python ../../Academy/papers/relativistic_raytracer/scripts/image_summarize.py integrator
```
