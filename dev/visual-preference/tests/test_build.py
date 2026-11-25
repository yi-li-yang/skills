"""The colour maps, the build and the web files it writes."""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

import build
from colour import ucs

SKILL = build.SKILL


@pytest.fixture(scope="module")
def cmaps():
    return json.loads((SKILL / "colormaps.json").read_text(encoding="utf-8"))


def lightness(stops):
    return np.array([ucs(h)[0] for h in stops])


def test_colormaps_credit(cmaps):
    assert "Crameri" in cmaps["credit"]
    assert "10.5281/zenodo.1243862" in cmaps["credit"]
    assert set(cmaps["maps"]) == {"bamako", "oslo", "lajolla", "bilbao", "lichen", "lisbon", "broc"}
    for m in cmaps["maps"].values():
        assert len(m["stops"]) == 256


def test_sequential_monotonic(cmaps):
    for name, m in cmaps["maps"].items():
        if m["kind"] != "sequential":
            continue
        j = lightness(m["stops"][::8])
        steps = np.diff(j)
        assert np.all(steps > 0) or np.all(steps < 0), name
    j = lightness(cmaps["maps"]["lichen"]["stops"][::16])
    steps = np.abs(np.diff(j))
    assert steps.max() / steps.min() <= 1.5


def test_diverging_symmetric(cmaps):
    for name, m in cmaps["maps"].items():
        if m["kind"] != "diverging":
            continue
        # Each half runs one way in lightness and meets the other at the middle. Crameri's published ends
        # differ by up to about 6.5 in J', so exact mirror symmetry is not the property to test.
        j = lightness(m["stops"][::8] + [m["stops"][-1]])
        mid = int(np.argmin(j)) if j[len(j) // 2] < j[0] else int(np.argmax(j))
        assert 0.4 * len(j) <= mid <= 0.6 * len(j), name
        assert np.all(np.diff(j[:mid + 1]) * np.sign(j[mid] - j[0]) > 0), name
        assert np.all(np.diff(j[mid:]) * np.sign(j[-1] - j[mid]) > 0), name


def test_css_has_every_token():
    css = (SKILL / "web" / "tokens.css").read_text(encoding="utf-8")
    tokens, _ = build.load()
    for family, body in tokens.items():
        if isinstance(body, dict) and "tokens" in body:
            for t in body["tokens"]:
                assert f"--{t['name']}:" in css, t["name"]
    assert '[data-theme="light"]' in css
    assert '@media (prefers-color-scheme: light)' in css
    assert ':root:not([data-theme="dark"])' in css


def test_tailwind_outputs():
    v4 = (SKILL / "web" / "tailwind-v4.css").read_text(encoding="utf-8")
    assert "@theme" in v4 and "--color-lichen:" in v4
    out = subprocess.run(["node", "-e", f"console.log(JSON.stringify(require({json.dumps(str(SKILL / 'web' / 'tailwind-v3.cjs'))})))"],
                         capture_output=True, text=True, check=True).stdout
    preset = json.loads(out)
    assert preset["theme"]["extend"]["colors"]["lichen"]


def test_generated_files_start_with_the_source_line():
    for rel, text in build.outputs(*build.load()).items():
        # A file with front matter must open with "---", so its source line is the first line inside it.
        head = text.splitlines()[1] if text.startswith("---\n") else text.splitlines()[0]
        assert "generated from tokens.json by dev/visual-preference/build.py" in head, rel


def test_check_detects_stale(tmp_path):
    root = tmp_path / "skill"
    shutil.copytree(SKILL, root)
    assert build.main(["--check", "--root", str(root)]) == 0
    t = json.loads((root / "tokens.json").read_text(encoding="utf-8"))
    t["color"]["tokens"][0]["value"]["dark"] = "#000000"
    (root / "tokens.json").write_text(json.dumps(t), encoding="utf-8")
    assert build.main(["--check", "--root", str(root)]) == 1


def test_cdn_url_resolves_to_installed_path():
    url = build.cdn_url("visual-preference-v1.0.0", "web/tokens.css")
    assert url.startswith("https://cdn.jsdelivr.net/gh/yi-li-yang/skills@visual-preference-v1.0.0/")
    rel = url.split("@visual-preference-v1.0.0/", 1)[1]
    assert (build.REPO / rel).is_file()


def test_tailwind_v4_has_no_self_reference():
    """A theme variable defined as itself is a cycle: it breaks when tokens.css is layered or in a shadow root."""
    import re
    v4 = (SKILL / "web" / "tailwind-v4.css").read_text(encoding="utf-8")
    for name, ref in re.findall(r"--([\w-]+):\s*var\(--([\w-]+)\)", v4):
        assert name != ref, name
