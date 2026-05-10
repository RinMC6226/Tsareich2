Input files:
- Put target DDS files in tools/overlay_work/input

Overlay file:
- Replace tools/overlay_work/overlay.png with your material image

Output files:
- Processed DDS files are written to tools/overlay_work/output

Run:
- python tools\apply_overlay_to_dds.py

Overwrite originals instead:
- python tools\apply_overlay_to_dds.py gfx\leaders\RUS --overlay tools\overlay_work\overlay.png --in-place
