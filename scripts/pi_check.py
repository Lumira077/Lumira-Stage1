"""Pi development preflight; no installs, service changes, or motor commands.

Run: python3 scripts/pi_check.py --verify
Evidence remains in ignored artifacts/. No automatic uploads.
"""
import argparse
import datetime
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(argv):
    try:
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                                errors="replace", timeout=30)
        output = result.stdout + result.stderr
        output = re.sub(r"(?im)^.*Serial Number:.*$", "Serial Number: [redacted]", output)
        return {"exit_code": result.returncode, "output": output.strip()}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"exit_code": -1, "output": str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Also run offline suites")
    args = parser.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out = ROOT / "artifacts" / "pi-check" / stamp
    out.mkdir(parents=True)
    model_path = Path("/proc/device-tree/model")
    model = model_path.read_text().rstrip("\0\n") if model_path.exists() else "unavailable"
    checks = {
        "os": ["cat", "/etc/os-release"],
        "packages": ["dpkg", "--audit"],
        "pcie": ["lspci", "-nn"],
        "hailo_identity": ["hailortcli", "fw-control", "identify"],
        "temperature": ["vcgencmd", "measure_temp"],
        "throttling": ["vcgencmd", "get_throttled"],
    }
    results = {name: run(cmd) for name, cmd in checks.items()}
    identity = results["hailo_identity"]
    gates = {
        "pi5": "Raspberry Pi 5" in model,
        "arm64": platform.machine() == "aarch64",
        "hailo_device": Path("/dev/hailo0").exists(),
        "hailo8l_communication": identity["exit_code"] == 0 and "HAILO8L" in identity["output"],
        "package_audit": results["packages"]["exit_code"] == 0 and not results["packages"]["output"],
        "no_throttle_flags": results["throttling"]["exit_code"] == 0 and results["throttling"]["output"] == "throttled=0x0",
    }
    report = {"utc": stamp, "model": model, "architecture": platform.machine(),
              "python": platform.python_version(), "commit": run(["git", "rev-parse", "HEAD"]),
              "worktree": run(["git", "status", "--porcelain"]), "checks": results,
              "gates": gates, "offline_exit_code": None,
              "ai_inference_tested": False, "motor_tested": False, "release_ready": False}
    if args.verify:
        report["offline_exit_code"] = subprocess.call(
            [sys.executable, str(ROOT / "scripts/verify_all.py"), "--output", str(out / "offline")], cwd=ROOT)
    report["preflight_passed"] = all(gates.values())
    (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for name, passed in gates.items():
        print(name, "PASS" if passed else "CHECK REQUIRED")
    print("Evidence:", out / "report.json")
    print("AI inference and physical robot operation remain unverified.")
    return 0 if report["preflight_passed"] and report["offline_exit_code"] in (None, 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
