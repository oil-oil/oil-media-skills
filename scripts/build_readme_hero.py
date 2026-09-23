from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "assets" / "readme" / "source" / "hero-layout.svg"
SUBJECT = ROOT / "vendor" / "oil-visual" / "assets" / "readme" / "hero-character.png"
OUTPUT = ROOT / "assets" / "readme" / "hero.svg"
MARKER = "__OIL_VISUAL_CHARACTER_PNG_DATA__"


def main() -> None:
    layout = LAYOUT.read_text(encoding="utf-8")
    if layout.count(MARKER) != 1:
        raise SystemExit(f"expected exactly one image marker in {LAYOUT}")

    png = SUBJECT.read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"oil-visual image is not a PNG: {SUBJECT}")

    image_data = "data:image/png;base64," + base64.b64encode(png).decode("ascii")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(layout.replace(MARKER, image_data), encoding="utf-8")
    print(f"Built {OUTPUT} ({OUTPUT.stat().st_size:,} bytes) from {SUBJECT}")


if __name__ == "__main__":
    main()
