#!/usr/bin/env python3
import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "corpus/metadata/map_sh2_tracks.csv"
KDT_TOOL = ROOT / "tools/kdt-tool/kdt-tool.py"
OUT_DIR = ROOT / "corpus/game"

def main():
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {Path(sys.argv[0]).name} '<path - sound>'")

    trigger_dir = Path(sys.argv[1]).expanduser().resolve() / "TriggerData"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with CSV.open(newline="", encoding="utf-8-sig") as f:
        tracks = [row for row in csv.DictReader(f) if row["use"].strip().lower() == "yes"]

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for row in tracks:
            bgm_id = row["bgm_id"].strip()
            matches = list(trigger_dir.glob(f"* - BGM {int(bgm_id)}.TD"))
            if len(matches) != 1:
                raise SystemExit(f"Expected one .TD for BGM {bgm_id}, found {len(matches)}")

            data = matches[0].read_bytes()
            start = data.find(b"KDT1")
            if start < 0 or start + 8 > len(data):
                raise SystemExit(f"KDT1 not found in {matches[0].name}")
            size = int.from_bytes(data[start + 4:start + 8], "little")
            if size < 0x10 or start + size > len(data):
                raise SystemExit(f"Invalid KDT1 size in {matches[0].name}")

            kdt = tmp / f"{bgm_id}.kdt"
            kdt.write_bytes(data[start:start + size])
            subprocess.run([sys.executable, str(KDT_TOOL), "-c", str(kdt)], check=True)

            title = re.sub(r"[^\w.-]+", "_", row["title"].strip()).strip("._") or "untitled"
            out = OUT_DIR / f"SH2_{bgm_id}_{title}.mid"
            out.write_bytes(kdt.with_suffix(".midi").read_bytes())
            print(out.relative_to(ROOT))

if __name__ == "__main__":
    main()