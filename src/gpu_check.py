"""Pre-flight GPU detection for Mawari node install."""
from __future__ import annotations
import os
import shutil
import subprocess
import sys


def detect() -> dict:
    info: dict = {"vendor": None, "model": None, "cuda": None, "rocm": None, "driver": None}

    # NVIDIA
    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
                text=True, timeout=10,
            )
            first = out.splitlines()[0]
            name, drv = (s.strip() for s in first.split(",", 1))
            info["vendor"] = "nvidia"
            info["model"] = name
            info["driver"] = drv
        except Exception as e:
            print(f"nvidia-smi failed: {e}", file=sys.stderr)

        if shutil.which("nvcc"):
            try:
                v = subprocess.check_output(["nvcc", "--version"], text=True, timeout=10)
                for line in v.splitlines():
                    if "release" in line:
                        info["cuda"] = line.split("release")[-1].strip().split(",")[0]
                        break
            except Exception as e:
                print(f"nvcc failed: {e}", file=sys.stderr)

    # AMD
    if shutil.which("rocm-smi"):
        try:
            out = subprocess.check_output(["rocm-smi", "--showproductname"], text=True, timeout=10)
            info["vendor"] = info["vendor"] or "amd"
            info["model"] = info["model"] or out.strip().splitlines()[-1] if out.strip() else "AMD GPU"
        except Exception as e:
            print(f"rocm-smi failed: {e}", file=sys.stderr)

    return info


def main() -> int:
    info = detect()
    print(f"vendor : {info['vendor']}")
    print(f"model  : {info['model']}")
    print(f"driver : {info['driver']}")
    print(f"cuda   : {info['cuda']}")
    print(f"rocm   : {info['rocm']}")
    if not info["vendor"]:
        print("\nNo GPU detected. Mawari will run in CPU mode (low rewards).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
