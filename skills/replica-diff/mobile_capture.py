#!/usr/bin/env python3
"""Capture a PNG from an iOS Simulator or Android device without a shell."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def booted_ios_devices() -> list[str]:
    completed = subprocess.run(
        ["xcrun", "simctl", "list", "devices", "booted", "-j"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    return [
        device["udid"]
        for runtime in payload.get("devices", {}).values()
        for device in runtime
        if device.get("state") == "Booted" and device.get("udid")
    ]


def connected_android_devices() -> list[str]:
    completed = subprocess.run(["adb", "devices"], check=True, capture_output=True, text=True)
    return [
        parts[0]
        for line in completed.stdout.splitlines()[1:]
        if len(parts := line.split()) >= 2 and parts[1] == "device"
    ]


def select_device(platform_name: str, requested: str | None) -> str:
    if requested:
        return requested
    devices = booted_ios_devices() if platform_name == "ios" else connected_android_devices()
    if len(devices) != 1:
        raise RuntimeError(
            f"expected exactly one running {platform_name} device, found {len(devices)}; pass --device"
        )
    return devices[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("platform", choices=("ios", "android"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--device", help="iOS simulator UDID or Android serial")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    output = args.output.resolve()
    if output.exists() and not args.force:
        print(f"refusing to overwrite {output}; pass --force", file=sys.stderr)
        return 2

    tool = "xcrun" if args.platform == "ios" else "adb"
    if not args.dry_run and not shutil.which(tool):
        print(f"required command not found: {tool}", file=sys.stderr)
        return 2

    try:
        device = args.device or ("booted" if args.dry_run and args.platform == "ios" else "DEVICE")
        if not args.dry_run:
            device = select_device(args.platform, args.device)
        if args.platform == "ios":
            command = ["xcrun", "simctl", "io", device, "screenshot", str(output)]
        else:
            command = ["adb"] + ([] if device == "DEVICE" else ["-s", device]) + ["exec-out", "screencap", "-p"]

        if args.dry_run:
            suffix = f" > {output}" if args.platform == "android" else ""
            print(" ".join(command) + suffix)
            return 0

        output.parent.mkdir(parents=True, exist_ok=True)
        if args.platform == "ios":
            subprocess.run(command, check=True)
        else:
            completed = subprocess.run(command, check=True, capture_output=True)
            output.write_bytes(completed.stdout)
    except (OSError, RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"capture failed: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
