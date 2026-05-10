from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Iterable

from PIL import Image, ImageChops


RESAMPLE = getattr(Image, "Resampling", Image).LANCZOS
DEFAULT_WORK_DIR = Path(__file__).resolve().parent / "overlay_work"
DEFAULT_INPUT_DIR = DEFAULT_WORK_DIR / "input"
DEFAULT_OUTPUT_DIR = DEFAULT_WORK_DIR / "output"
DEFAULT_OVERLAY_PATH = DEFAULT_WORK_DIR / "overlay.png"


def overlay_channel(base: int, top: int) -> int:
    base_f = base / 255.0
    top_f = top / 255.0
    if base_f <= 0.5:
        out = 2.0 * base_f * top_f
    else:
        out = 1.0 - 2.0 * (1.0 - base_f) * (1.0 - top_f)
    return max(0, min(255, round(out * 255.0)))


def blend_overlay(base_rgb: Image.Image, top_rgb: Image.Image) -> Image.Image:
    base_px = base_rgb.load()
    top_px = top_rgb.load()
    out = Image.new("RGB", base_rgb.size)
    out_px = out.load()

    width, height = base_rgb.size
    for y in range(height):
        for x in range(width):
            br, bg, bb = base_px[x, y]
            tr, tg, tb = top_px[x, y]
            out_px[x, y] = (
                overlay_channel(br, tr),
                overlay_channel(bg, tg),
                overlay_channel(bb, tb),
            )
    return out


def apply_overlay(base_path: Path, overlay_path: Path, output_path: Path) -> None:
    with Image.open(base_path) as base_img, Image.open(overlay_path) as overlay_img:
        base_rgba = base_img.convert("RGBA")
        overlay_rgba = overlay_img.convert("RGBA").resize(base_rgba.size, RESAMPLE)

        base_rgb = base_rgba.convert("RGB")
        overlay_rgb = overlay_rgba.convert("RGB")
        blended_rgb = blend_overlay(base_rgb, overlay_rgb)

        base_alpha = base_rgba.getchannel("A")
        overlay_alpha = overlay_rgba.getchannel("A")

        # Emulate a clipping mask by restricting the overlay's visibility
        # to the opaque pixels of the original DDS.
        clipped_alpha = ImageChops.multiply(base_alpha, overlay_alpha)
        mixed_rgb = Image.composite(blended_rgb, base_rgb, clipped_alpha)

        result = Image.merge(
            "RGBA",
            (
                mixed_rgb.getchannel("R"),
                mixed_rgb.getchannel("G"),
                mixed_rgb.getchannel("B"),
                base_alpha,
            ),
        )
        result.save(output_path)


def run_single_file(source: Path, overlay_path: Path, target: Path) -> tuple[bool, str]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--single-file",
        str(source),
        "--overlay",
        str(overlay_path),
        "--output-file",
        str(target),
    ]
    completed = subprocess.run(command, capture_output=True, text=True)
    output = (completed.stdout or completed.stderr or "").strip()
    return completed.returncode == 0, output


def expand_inputs(inputs: Iterable[str]) -> list[tuple[Path, Path | None]]:
    paths: list[tuple[Path, Path | None]] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            root = path.resolve()
            paths.extend((child, root) for child in sorted(path.rglob("*.dds")))
        else:
            paths.append((path, None))
    return paths


def build_output_path(
    source: Path,
    root: Path | None,
    output_dir: Path | None,
    suffix: str | None,
) -> Path:
    if output_dir is None:
        return source

    if root is not None:
        try:
            relative = source.resolve().relative_to(root)
        except ValueError:
            relative = Path(source.name)
    else:
        relative = Path(source.name)

    target = output_dir / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    name = target.stem if suffix is None else f"{target.stem}{suffix}"
    return target.with_name(f"{name}{target.suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply an overlay texture to DDS files using the base alpha as a clipping mask."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="DDS file(s) or directories containing DDS files. Defaults to tools/overlay_work/input",
    )
    parser.add_argument(
        "--overlay",
        default=str(DEFAULT_OVERLAY_PATH),
        help="Overlay image path. Defaults to tools/overlay_work/overlay.png",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory. Defaults to tools/overlay_work/output",
    )
    parser.add_argument(
        "--suffix",
        default=None,
        help="Optional suffix when --output-dir is used, for example _overlay",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the source DDS files instead of writing to --output-dir",
    )
    parser.add_argument("--single-file", help=argparse.SUPPRESS)
    parser.add_argument("--output-file", help=argparse.SUPPRESS)
    args = parser.parse_args()

    overlay_path = Path(args.overlay)
    if not overlay_path.is_file():
        raise SystemExit(f"Overlay not found: {overlay_path}")

    if args.single_file:
        source = Path(args.single_file)
        target = Path(args.output_file) if args.output_file else source
        apply_overlay(source, overlay_path, target)
        print(f"ok: {source} -> {target}")
        return 0

    raw_inputs = args.inputs or [str(DEFAULT_INPUT_DIR)]
    sources = [
        (path, root)
        for path, root in expand_inputs(raw_inputs)
        if path.suffix.lower() == ".dds"
    ]
    if not sources:
        raise SystemExit("No DDS files found.")

    output_dir = None if args.in_place else Path(args.output_dir)

    failures: list[tuple[Path, str]] = []

    for source, root in sources:
        if not source.is_file():
            print(f"skip: not found: {source}")
            continue
        target = build_output_path(source, root, output_dir, args.suffix)
        try:
            ok, detail = run_single_file(source, overlay_path, target)
            if ok:
                print(detail or f"ok: {source} -> {target}")
            else:
                message = detail or "child process failed"
                failures.append((source, message))
                print(f"error: {source} -> {message}")
        except Exception as exc:
            failures.append((source, str(exc)))
            print(f"error: {source} -> {exc}")

    if failures:
        print(f"done with errors: {len(failures)} file(s) skipped")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
