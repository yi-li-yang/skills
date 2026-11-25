"""Write colormaps.json: six of Fabio Crameri's Scientific colour maps and the custom lichen ramp, 256 stops each.

colormaps.json is hand-owned source like tokens.json: run this once when a map is added or changed, then commit
the result. The build reads colormaps.json and never needs cmcrameri.

    python dev/visual-preference/make_colormaps.py
"""
import json
from pathlib import Path

import cmcrameri.cm as cmc
import numpy as np
from colorspacious import cspace_convert

OUT = Path(__file__).resolve().parents[2] / "plugins" / "yili-skills" / "skills" / "visual-preference" / "colormaps.json"
CREDIT = ("Crameri, F. (2018). Scientific colour maps. Zenodo. doi:10.5281/zenodo.1243862. "
          "bamako, oslo, lajolla, bilbao, lisbon and broc are Fabio Crameri's maps; lichen is Yili Yang's own ramp.")
MAPS = {
    "bamako": ("sequential", "Default for continuous data: land, vegetation, anything without a closer match."),
    "oslo": ("sequential", "Ice, snow and water."),
    "lajolla": ("sequential", "Heat, fire, intensity."),
    "bilbao": ("sequential", "Soil and sediment."),
    "lisbon": ("diverging", "Below and above a middle, on dark pages: the middle sinks into the ground."),
    "broc": ("diverging", "Below and above a middle, on light pages and in papers."),
}
LICHEN = ["#1c2418", "#a3b86c", "#f2f3e6"]


def to_hex(rgb) -> str:
    return "#" + "".join(f"{round(float(v) * 255):02x}" for v in np.clip(rgb, 0, 1))


def lichen_ramp(n: int = 256) -> list[str]:
    """Through three colours, sampled at even steps of CAM02-UCS lightness, so equal data steps look equal."""
    pts = [cspace_convert(np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]), "sRGB1", "CAM02-UCS") for h in LICHEN]
    path = np.concatenate([np.linspace(pts[0], pts[1], 500, endpoint=False), np.linspace(pts[1], pts[2], 500)])
    targets = np.linspace(path[0, 0], path[-1, 0], n)
    out = np.array([np.interp(targets, path[:, 0], path[:, k]) for k in range(3)]).T
    return [to_hex(cspace_convert(p, "CAM02-UCS", "sRGB1")) for p in out]


def main() -> None:
    maps = {}
    for name, (kind, use) in MAPS.items():
        stops = getattr(cmc, name)(np.linspace(0, 1, 256))[:, :3]
        maps[name] = {"kind": kind, "use": use, "stops": [to_hex(c) for c in stops]}
    maps["lichen"] = {"kind": "sequential", "use": "Small interface charts that carry the home accent.", "stops": lichen_ramp()}
    OUT.write_text(json.dumps({"credit": CREDIT, "maps": maps}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
