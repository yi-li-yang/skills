"""Derive the light-theme data colours from the dark ones.

The design fixed the data colours on the dark stone ground. Papers and READMEs on a light page need the same
colours, darker. This keeps each colour's hue and chroma in CAM02-UCS, lowers its lightness until it reaches
3:1 on the paper ground, then lowers further, one set at a time, until both sets stay distinct under colour-vision
simulation. It prints the result; the hexes are then written into tokens.json by hand, so they become source.

    python dev/visual-preference/derive_light_data.py
"""
import sys
from pathlib import Path

import numpy as np
from colorspacious import cspace_convert

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
from colour import CVD, contrast, ucs  # noqa: E402
import functools  # noqa: E402
import itertools  # noqa: E402

PAPER = "#f2f3ef"
ITER = 4000
DARK = {"data-sky": "#a9cfe6", "data-rust": "#c4573a", "data-spruce": "#4f9a7d", "data-sand": "#d8c48e",
        "data-dusk": "#8a7fb8", "data-ochre": "#c9962e", "data-glacier": "#86b2d4", "data-rose": "#d98ca0",
        "data-olive": "#b0ac5a"}
EARTH6 = ["data-sky", "data-rust", "data-spruce", "data-sand", "data-dusk", "data-ochre"]
EARTH8 = ["data-glacier", "data-rust", "data-spruce", "data-sand", "data-dusk", "data-rose", "data-olive", "data-sky"]


def jab_of(hex_colour: str) -> np.ndarray:
    return cspace_convert(np.array([int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]), "sRGB1", "CAM02-UCS")


def to_hex(jab) -> str:
    rgb = np.nan_to_num(np.clip(cspace_convert(jab, "CAM02-UCS", "sRGB1"), 0, 1))
    return "#" + "".join(f"{round(v * 255):02x}" for v in rgb)


def in_gamut(jab) -> bool:
    rgb = cspace_convert(jab, "CAM02-UCS", "sRGB1")
    return bool(np.all(np.isfinite(rgb)) and np.all(rgb >= -1e-3) and np.all(rgb <= 1 + 1e-3))


def make(hex_colour: str, j: float, chroma: float, dh: float) -> str | None:
    """The colour at lightness j, its chroma scaled, its hue turned by dh degrees; None outside sRGB."""
    _, a, b = jab_of(hex_colour)
    c, h = np.hypot(a, b) * chroma, np.arctan2(b, a) + np.radians(dh)
    jab = np.array([j, c * np.cos(h), c * np.sin(h)])
    return to_hex(jab) if in_gamut(jab) else None


@functools.lru_cache(maxsize=None)
def points(hex_colour: str) -> np.ndarray:
    return np.array([ucs(hex_colour, c) for c in CVD])


def min_cvd_distance(hexes: list[str]) -> float:
    return float(min(np.linalg.norm(points(a) - points(b), axis=1).min() for a, b in itertools.combinations(hexes, 2)))


def score(light: dict[str, str]) -> float:
    return min(min_cvd_distance([light[n] for n in EARTH6]) / 11.0,
               min_cvd_distance([light[n] for n in EARTH8]) / 10.0)


def derive(seed: int = 7) -> dict[str, str]:
    """Search each colour's lightness, chroma (0.7-1.6x) and hue (within 20 degrees) for the most distinct set,
    with 3:1 to 6:1 on paper, so a line reads as a colour and never as text. The family's character comes from the hue, which stays close to the dark set."""
    rng = np.random.default_rng(seed)
    state = {n: [jab_of(v)[0] - 15, 1.0, 0.0] for n, v in DARK.items()}

    def build(st):
        out = {}
        for n, (j, c, dh) in st.items():
            col = make(DARK[n], j, c, dh)
            if col is None or not 3.0 <= contrast(col, PAPER) <= 6.0:
                return None
            out[n] = col
        return out

    for n in state:   # start each colour just dark enough: lower lightness, and chroma when out of sRGB
        j, c, _ = state[n]
        while True:
            col = make(DARK[n], j, c, 0.0)
            if col is None:
                c *= 0.95
            elif contrast(col, PAPER) < 3.0:
                j -= 0.5
            elif contrast(col, PAPER) > 6.0:
                j += 0.5
            else:
                break
        state[n] = [j, c, 0.0]
    def value(st, built):
        # Meet both targets first; past them, prefer the set that stays closest to the dark colours.
        drift = sum(abs(dh) * 0.05 + abs(c - 1) * 2 for _, c, dh in st.values())
        return min(score(built), 1.05) * 100 - drift

    light = build(state)
    best = value(state, light)
    for it in range(ITER):
        n = list(DARK)[rng.integers(len(DARK))]
        trial = {k: list(v) for k, v in state.items()}
        scale = 1 - it / ITER
        trial[n][0] += rng.normal(0, 6 * scale + 0.5)
        trial[n][1] = float(np.clip(trial[n][1] + rng.normal(0, .15 * scale + .02), 0.7, 1.6))
        trial[n][2] = float(np.clip(trial[n][2] + rng.normal(0, 6 * scale + .5), -20, 20))
        built = build(trial)
        if built is None:
            continue
        s = value(trial, built)
        if s > best:
            state, light, best = trial, built, s
    final = score(light)
    print(f"score {final:.3f} (1.0 meets both targets)")
    if final < 1.0:
        raise SystemExit("no set met the targets")
    return light


if __name__ == "__main__":
    for name, value in derive().items():
        print(f"{name}: {value}  contrast {contrast(value, PAPER):.2f}")
