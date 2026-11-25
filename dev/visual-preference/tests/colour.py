"""Colour measures the tests share: WCAG contrast, and distance under colour-vision simulation."""
import itertools

import numpy as np
from colorspacious import cspace_convert

CVD = [None] + [{"name": "sRGB1+CVD", "cvd_type": t, "severity": 100}
                for t in ("deuteranomaly", "protanomaly", "tritanomaly")]


def rgb(hex_colour: str) -> np.ndarray:
    h = hex_colour.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def luminance(hex_colour: str) -> float:
    c = rgb(hex_colour)
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def ucs(hex_colour: str, condition=None) -> np.ndarray:
    c = rgb(hex_colour)
    if condition is not None:
        c = np.clip(cspace_convert(c, condition, "sRGB1"), 0, 1)
    return cspace_convert(c, "sRGB1", "CAM02-UCS")


def min_cvd_distance(hexes: list[str]) -> float:
    """The smallest distance between any two colours, under normal vision and three simulated deficiencies."""
    points = {h: [ucs(h, c) for c in CVD] for h in hexes}
    return float(min(np.linalg.norm(points[a][k] - points[b][k])
                     for a, b in itertools.combinations(hexes, 2) for k in range(len(CVD))))
