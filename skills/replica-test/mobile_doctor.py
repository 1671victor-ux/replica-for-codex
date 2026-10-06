#!/usr/bin/env python3
"""Read-only Expo/React Native test-environment check."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            command, check=False, capture_output=True, text=True, timeout=8
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    output = (completed.stdout or completed.stderr).strip()
    return completed.returncode == 0, output


def package_info(root: Path) -> dict[str, object]:
    path = root / "package.json"
    if not path.is_file():
        return {"present": False, "expo": False, "react_native": False}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"present": True, "error": str(exc), "expo": False, "react_native": False}
    dependencies: dict[str, object] = {}
    for group in ("dependencies", "devDependencies"):
        value = data.get(group, {})
        if isinstance(value, dict):
            dependencies.update(value)
    return {
        "present": True,
        "expo": "expo" in dependencies,
        "react_native": "react-native" in dependencies,
        "expo_dev_client": "expo-dev-client" in dependencies,
    }


def ios_status() -> dict[str, object]:
    result: dict[str, object] = {
        "host_supported": platform.system() == "Darwin",
        "xcrun": bool(shutil.which("xcrun")),
        "booted_devices": [],
    }
    if result["host_supported"] and result["xcrun"]:
        ok, output = run(["xcrun", "simctl", "list", "devices", "booted", "-j"])
        if ok:
            try:
                payload = json.loads(output)
                devices = []
                for runtime_devices in payload.get("devices", {}).values():
                    devices.extend(
                        device.get("udid", "")
                        for device in runtime_devices
                        if device.get("state") == "Booted"
                    )
                result["booted_devices"] = [device for device in devices if device]
            except json.JSONDecodeError:
                result["error"] = "simctl returned invalid JSON"
        else:
            result["error"] = output
    result["ready"] = bool(result["host_supported"] and result["xcrun"] and result["booted_devices"])
    return result


def android_status() -> dict[str, object]:
    result: dict[str, object] = {"adb": bool(shutil.which("adb")), "devices": []}
    if result["adb"]:
        ok, output = run(["adb", "devices"])
        if ok:
            devices = []
            for line in output.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 2 and parts[1] == "device":
                    devices.append(parts[0])
            result["devices"] = devices
        else:
            result["error"] = output
    result["ready"] = bool(result["adb"] and result["devices"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--require", choices=("none", "ios", "android", "both"), default="none")
    parser.add_argument("--e2e", action="store_true", help="also require .maestro and the Maestro CLI")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    report = {
        "project": str(root),
        "package": package_info(root),
        "files": {
            "app_config": any((root / name).exists() for name in ("app.json", "app.config.js", "app.config.ts")),
            "eas_json": (root / "eas.json").is_file(),
            "maestro": (root / ".maestro").is_dir(),
        },
        "tools": {
            name: bool(shutil.which(name))
            for name in ("node", "npm", "npx", "maestro", "agent-device")
        },
        "ios": ios_status(),
        "android": android_status(),
    }

    required = [] if args.require == "none" else (["ios", "android"] if args.require == "both" else [args.require])
    failures = [name for name in required if not report[name]["ready"]]
    if required:
        if not report["package"].get("expo") or not report["package"].get("react_native"):
            failures.append("project:expo-react-native")
        if not report["files"]["app_config"]:
            failures.append("project:app-config")
        for command in ("node", "npx"):
            if not report["tools"][command]:
                failures.append(f"tool:{command}")
        if args.e2e:
            if not report["files"]["maestro"]:
                failures.append("project:.maestro")
            if not report["tools"]["maestro"]:
                failures.append("tool:maestro")
    report["required"] = required
    report["e2e"] = args.e2e
    report["failures"] = failures

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"project: {root}")
        print(f"expo: {report['package'].get('expo', False)}  react-native: {report['package'].get('react_native', False)}")
        print(f"maestro: {report['tools']['maestro']}  agent-device: {report['tools']['agent-device']}")
        print(f"ios ready: {report['ios']['ready']}  booted: {len(report['ios']['booted_devices'])}")
        print(f"android ready: {report['android']['ready']}  devices: {len(report['android']['devices'])}")
        if failures:
            print("missing required runtime: " + ", ".join(failures), file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
