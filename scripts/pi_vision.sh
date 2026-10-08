#!/usr/bin/env bash
# Camera 0 + installed Raspberry Pi Hailo YOLOv6 demo.
# No installs, motor commands, automatic startup, or video recording.
set -euo pipefail
mode="${1:-headless}"
case "$mode" in
  headless) preview=(--nopreview); duration=30000 ;;
  preview) preview=(); duration=0 ;;
  *) echo "Usage: bash scripts/pi_vision.sh [headless|preview]" >&2; exit 2 ;;
esac
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
config=/usr/share/rpi-camera-assets/hailo_yolov6_inference.json
for program in python3 rpicam-hello hailortcli timeout; do
  command -v "$program" >/dev/null || { echo "Missing command: $program"; exit 2; }
done
if [[ ! -r "$config" ]]; then
  echo "Missing installed YOLOv6 config: $config"
  echo "Inspect: dpkg -L rpicam-apps-hailo-postprocess"
  exit 2
fi
python3 "$root/scripts/pi_check.py"
out="$root/artifacts/vision/$(date -u +%Y%m%dT%H%M%S)-$$"
mkdir -p "$out"
git -C "$root" rev-parse HEAD > "$out/source-commit.txt"
cp -- "$config" "$out/post-process.json"
echo "Starting real camera/NPU demo. Focus affects recognition quality."
echo "Log: $out/vision.log"
# A hard timeout also bounds failures to stop during the headless smoke test.
limit=50
if [[ "$mode" == preview ]]; then limit=0; fi
set +e
timeout --signal=TERM --kill-after=5 "$limit" rpicam-hello --camera 0 \
  --timeout "$duration" "${preview[@]}" --verbose 2 \
  --post-process-file "$config" 2>&1 | tee "$out/vision.log"
status=${PIPESTATUS[0]}
set -e
printf '%s\n' "$status" > "$out/exit-code.txt"
echo "Process exit code: $status"
echo "Review log for model load, frame processing and detections; exit 0 alone is not acceptance."
echo "This demo does not control motors or run robot dialogue."
exit "$status"
