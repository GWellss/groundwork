#!/usr/bin/env python3
"""Generate a DESIGN.md theme (and a contrast report) from the 10 questionnaire answers.

Python 3 standard library only, single file. Rules come from theme/questionnaire.md,
docs/conventions.md and the component specs in components/.

Usage (terminal):
    python3 theme.py --out DESIGN.md                      # all defaults
    python3 theme.py --name Acme --brand "#7C3AED" --corners pill --out DESIGN.md
    python3 theme.py --out DESIGN.md --css tokens.css     # explicit CSS path
    python3 theme.py --dark --out DESIGN.md               # also DESIGN.dark.md and a two-block tokens.css
    python3 theme.py --palettes --out palettes.md         # palette reference for agents without tools
    python3 theme.py --selftest

Usage (code execution sandbox, no shell): paste the file, then call
    main(["--brand", "#7C3AED", "--out", "DESIGN.md"])

Input: one option per answer (--name --brand --danger --success --warning --neutral --font --corners --density --icons).
Colors are hex codes (#RRGGBB); resolving a color name to hex is left to the caller.
Output: DESIGN.md (use --out -  for stdout), tokens.css (default: next to the DESIGN.md; with --out -
only if --css is given) and a contrast report on stdout. tokens.css is generated here, without the CLI.
Dark mode (option --dark, off by default): also writes DESIGN.dark.md (--dark-out), and tokens.css gets a :root block
(light) plus a [data-theme="dark"] block. --dark-tint slightly-tinted|neutral picks the surface tint; --dark-brand
accept|keep answers the proposal made when the brand color fails in dark mode (without it the script stops, exit 2).
Exit code: 0 ok, 1 a components pair fails 4.5:1, 2 unusable color (nothing written, proposal printed).
"""
import argparse
import json
import math
import os
import re
import sys

STEPS = (50, 100, 200, 300, 400, 500, 600, 700, 800, 900)
LIGHT = (0.97, 0.93, 0.87, 0.79, 0.70, 0.62, 0.54, 0.46, 0.38, 0.30)
SHARE = (0.15, 0.30, 0.50, 0.75, 0.90, 1.0, 1.0, 1.0, 0.90, 0.75)
NEUTRAL_TINT = {"neutral": (0.0, 0), "warm": (0.010, 70), "cool": (0.010, 250)}
WHITE = "#FFFFFF"
ACCENT = ("primary", "primary-hover", "primary-pressed", "danger", "focus-ring", "link-visited", "on-surface-muted", "success")
ON_FILL = {"danger-hover": "neutral-subtle-hover", "danger-pressed": "neutral-subtle-pressed"}  # destructive menu item: danger content darkens on the grayed fill it meets
ROLES = ("brand", "danger", "success", "warning")  # one scale each; states derived by the same rule
LEVELS = tuple("surface-level-%d" % i for i in range(1, 6))  # dark mode: level-0 is `surface`
LEVEL5 = LEVELS[-1]  # the lightest surface, the most unfavorable one for light content
DARK_L0, DARK_STEP, DARK_CHROMA = 0.18, 0.025, 0.010  # OKLCH lightness of the dark surface, gain per level, constant tint
BRIGHT_BG = ("primary", "primary-hover", "primary-pressed", "danger", "danger-hover", "danger-pressed", "success", "warning")

SIZES = ("sm", "md", "lg", "xl")
FONT_SIZE = {"compact": (12, 13, 14, 16), "default": (12, 14, 16, 18), "comfortable": (13, 15, 17, 20)}
ROUNDED = {"sharp": "0px", "soft": "4px", "rounded": "8px", "pill": "9999px"}
AVATAR_RADIUS = "9999px"  # rounded.avatar: round by default whatever the corners; the user edits it after generation
OVERLAY = {**ROUNDED, "pill": "8px"}  # never a stadium shape
SPACING = {  # token: (compact, default, comfortable)
    "control-xs": (24, 28, 32), "control-sm": (28, 32, 40), "control-md": (32, 40, 48),
    "control-lg": (40, 48, 56), "control-xl": (48, 56, 64),
    "icon-sm": (14, 16, 20), "icon-md": (16, 20, 24), "icon-lg": (20, 24, 28), "icon-xl": (24, 28, 32),
    "xs": (2, 4, 6), "sm": (6, 8, 10), "md": (8, 12, 16), "lg": (12, 16, 20), "xl": (16, 20, 24), "2xl": (20, 24, 32),
    "tooltip-max-width": (200, 240, 280),
    "menu-min-width": (128, 160, 192), "floating-max-width": (280, 320, 360), "dialog-max-width": (400, 480, 560),
}
DENSITIES = ("compact", "default", "comfortable")

ELEVATION = (  # level, role, box-shadow (questionnaire.md, "Elevation")
    ("level-0", "At rest, flat on the surface", "none"),
    ("level-1", "At rest, slightly raised", "0 1px 2px rgba(0, 0, 0, 0.30), 0 1px 3px 1px rgba(0, 0, 0, 0.15)"),
    ("level-2", "At rest, overlay tied to a trigger", "0 1px 2px rgba(0, 0, 0, 0.30), 0 2px 6px 2px rgba(0, 0, 0, 0.15)"),
    ("level-3", "At rest, floating above scrolling content", "0 1px 3px rgba(0, 0, 0, 0.30), 0 4px 8px 3px rgba(0, 0, 0, 0.15)"),
    ("level-4", "Interaction only, one step above a resting level", "0 2px 3px rgba(0, 0, 0, 0.30), 0 6px 10px 4px rgba(0, 0, 0, 0.15)"),
    ("level-5", "Interaction only, highest", "0 4px 4px rgba(0, 0, 0, 0.30), 0 8px 12px 6px rgba(0, 0, 0, 0.15)"),
)

# Hue ranges in OKLCH degrees: (upper bound exclusive, name). Hues >= 336 or < 12 are pink.
HUE_NAMES = ((12, "pink"), (37, "red"), (52, "orange"), (70, "amber"), (110, "yellow"), (165, "green"),
             (195, "teal"), (240, "cyan"), (270, "blue"), (285, "indigo"), (336, "violet"))

# Representative base per hue for palettes.md (blue and red are the questionnaire defaults).
PALETTE_BASES = (("red", "#DC2626"), ("orange", "#EA580C"), ("amber", "#D97706"), ("yellow", "#CA8A04"),
                 ("green", "#16A34A"), ("teal", "#0D9488"), ("cyan", "#0891B2"), ("blue", "#2563EB"),
                 ("indigo", "#4F46E5"), ("violet", "#7C3AED"), ("pink", "#DB2777"))


# ---------- color math ----------

def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb(hx):
    return [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def to_oklch(hx):
    r, g, b = [lin(c) for c in rgb(hx)]
    l = max(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b, 0) ** (1 / 3)
    m = max(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b, 0) ** (1 / 3)
    s = max(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b, 0) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    b = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def lrgb(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l, m, s = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, \
              (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def in_gamut(L, C, h):
    return all(-1e-6 <= v <= 1 + 1e-6 for v in lrgb(L, C, h))


def fit_chroma(L, C, h):
    """Largest chroma <= C that fits the sRGB gamut (bisection)."""
    if in_gamut(L, C, h):
        return C
    lo, hi = 0.0, C
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if in_gamut(L, mid, h) else (lo, mid)
    return lo


def to_hex(L, C, h):
    out = "#"
    for v in lrgb(L, fit_chroma(L, C, h), h):
        v = min(max(v, 0), 1)
        v = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out += "%02X" % round(v * 255)
    return out


def lum(hx):
    r, g, b = [lin(c) for c in rgb(hx)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hue_name(hx):
    _, c, h = to_oklch(hx)
    if c < 0.02:
        return "gray"
    return next((n for top, n in HUE_NAMES if h < top), "pink")


# ---------- scales and states ----------

def make_scale(lights, chromas, hue, base=None):
    """10 hex steps. If base is given, the step closest in lightness becomes exactly base."""
    scale = [to_hex(L, C, hue) for L, C in zip(lights, chromas)]
    if base:
        bl = to_oklch(base)[0]
        scale[min(range(10), key=lambda i: abs(lights[i] - bl))] = base
    return scale


def color_scale(base):
    _, c, h = to_oklch(base)
    return make_scale(LIGHT, [c * s for s in SHARE], h, base), c


def neutral_scale(kind, brand_hue):
    c, h = NEUTRAL_TINT.get(kind, (0.010, brand_hue))
    return make_scale((0.99,) + LIGHT[1:], [c] * 10, h)


def default_index(scale, surface):
    """First step from 600 to 900 reaching 4.5:1 in the worse case between white and the surface."""
    return next((i for i in range(6, 10) if min(contrast(scale[i], WHITE), contrast(scale[i], surface)) >= 4.5), None)


def content_index(scale, bgs):
    """First step 700, 800, 900 reaching 4.5:1 against every background of bgs, else None."""
    return next((i for i in (7, 8, 9) if all(contrast(scale[i], x) >= 4.5 for x in bgs)), None)


def issues(scale, d, base_chroma, states=True):  # states: the role has solid hover and pressed (brand, danger)
    if d is None:
        return ["no step from 600 to 900 reaches 4.5:1 against white and the surface"]
    out = []
    if states and min(d + 2, 9) == min(d + 4, 9):
        out.append("default step is %d: hover and pressed would collapse onto the same step" % STEPS[d])
    if to_oklch(scale[d])[1] < base_chroma / 2:
        out.append("chroma at the default step is below half of the base chroma (muddy color)")
    return out


def proposal(hx):
    h = to_oklch(hx)[2]
    return to_hex(0.54, 0.4, h)  # to_hex reduces the chroma to the highest value that fits sRGB


# ---------- theme ----------

def derive(a):
    """Return (colors, info). Raise ValueError (unusable color) with the message to show."""
    names = {k: hue_name(getattr(a, k)) for k in ROLES}
    if names["brand"] in (names["danger"], names["success"], names["warning"]):
        names["brand"] = "brand"
    if len({names[k] for k in ROLES}) < 4:
        raise ValueError("The danger, success and warning colors must have different hues (got %s): give another color." %
                         ", ".join(names[k] for k in ROLES[1:]))
    neutral = neutral_scale(a.neutral, to_oklch(a.brand)[2])
    surface = neutral[0]
    info = {"names": names, "idx": {}}
    colors = {}
    for key in ROLES:
        name, base = names[key], getattr(a, key)
        scale, c = color_scale(base)
        d = default_index(scale, surface)
        problems = issues(scale, d, c, key in ("brand", "danger"))
        if problems:
            raise ValueError("The %s color %s cannot give accessible buttons with white text: %s.\n"
                             "Proposed alternative (same hue, lightness 0.54, highest chroma in sRGB): %s\n"
                             "Accept it or give another color." % (key, base, "; ".join(problems), proposal(base)))
        colors[name] = scale
        info["idx"][key] = d
    colors["neutral"] = neutral
    flat = {}
    for name, scale in colors.items():
        for step, hx in zip(STEPS, scale):
            flat["%s-%d" % (name, step)] = hx

    def ref(name, i):
        return "{colors.%s-%d}" % (name, STEPS[min(i, 9)])

    b, bd = names["brand"], info["idx"]["brand"]
    sem = {
        "surface": "{colors.neutral-50}",
        "primary": ref(b, bd), "on-primary": WHITE,
        "primary-hover": ref(b, bd + 2), "primary-pressed": ref(b, bd + 4),
        "primary-container": ref(b, 0), "on-primary-container": None,
        "primary-container-hover": ref(b, 1), "primary-container-pressed": ref(b, 2),
        "primary-subtle-hover": ref(b, 0), "primary-subtle-pressed": ref(b, 1), "on-primary-subtle": None,
        **{tok: v for k in ROLES[1:] for tok, v in (
            (k, ref(names[k], info["idx"][k])), ("on-" + k, WHITE))},
        # only danger has a solid hover and pressed (success and warning have no interactive solid component)
        "danger-hover": ref(names["danger"], info["idx"]["danger"] + 2), "danger-pressed": ref(names["danger"], info["idx"]["danger"] + 4),
        # tonal containers of the alert (the info alert reuses primary-container*): steps 50, 100, 200 with content searched like on-primary-container
        **{tok: v for k in ROLES[1:] for tok, v in (
            (k + "-container", ref(names[k], 0)), (k + "-container-hover", ref(names[k], 1)),
            (k + "-container-pressed", ref(names[k], 2)), ("on-%s-container" % k, None))},
        "outline": ref("neutral", next((i for i in (5, 6) if contrast(neutral[i], surface) >= 3), 6)),  # 3:1 on the surface (WCAG 1.4.11)
        "disabled-container": "{colors.neutral-100}",
        "on-disabled": "{colors.neutral-500}", "focus-ring": ref(b, bd),
        "on-surface": None, "on-surface-muted": ref("neutral", next((i for i in (6, 7) if contrast(neutral[i], surface) >= 4.5), 7)),
        "neutral-subtle-hover": "{colors.neutral-100}", "neutral-subtle-pressed": "{colors.neutral-200}",
        "inverse-surface": "{colors.neutral-900}", "on-inverse-surface": WHITE,
        # visited: the brand step between default (600, the only usable default) and hover (800): distinct from default, hover and pressed
        "link-visited": ref(b, bd + 1),
    }
    assert len(sem) == 43
    flat.update(sem)
    # focus ring drawn inside a control or on a fill: 3:1 on every fill it can meet (WCAG 1.4.11); darker brand step if needed, as outline
    sem["focus-ring"] = flat["focus-ring"] = ref(b, next((i for i in range(bd, 9) if ring_ok(flat, ref(b, i))), 9))
    for tok, sc in (("on-primary-container", b), ("on-primary-subtle", b), ("on-surface", "neutral"),
                    *(("on-%s-container" % k, names[k]) for k in ROLES[1:])):
        bgs = [resolve(flat, "{colors.%s}" % bg) for _, bg, fg in components() if fg == tok]  # darkest decides
        flat[tok] = ref(sc, content_index(colors[sc], bgs) or 9)  # 900 failing is reported by check()
    check_muted(flat)
    return flat, info


def dark_surfaces(a):
    """Level-0 to level-5 surface hex: OKLCH lightness up by DARK_STEP per level, tint constant at every level."""
    if a.dark_tint == "neutral":
        c, h = 0.0, 0
    elif a.neutral in ("warm", "cool"):
        c, h = NEUTRAL_TINT[a.neutral]
    else:
        c, h = DARK_CHROMA, to_oklch(a.brand)[2]
    return [to_hex(DARK_L0 + i * DARK_STEP, c, h) for i in range(6)]


def dark_components():
    """The light pairs (checked on level-5 by lvl) plus the text on levels 1 to 4, so every surface role is used (the lint flags unreferenced hex tokens)."""
    return components() + [("text-on-level-%d" % i, "surface-level-%d" % i, "on-surface") for i in range(1, 5)]


def dark_ok(sc, i, top):
    """Accent step i passes in dark mode: from step 300, 4.5:1 on the lightest surface and against its content (step 900)."""
    return i >= 3 and contrast(sc[i], top) >= 4.5 and contrast(sc[i], sc[9]) >= 4.5


def derive_dark(a, light, info):
    """Dark colors by role correspondence (docs/conventions.md, Dark mode). Same palettes, other steps per role.
    Raise ValueError (nothing written) when the brand needs the user's answer or a color is unusable."""
    names, idx = info["names"], {}
    palette = dict(list(light.items())[:50])
    _, c, h = to_oklch(palette["neutral-900"])  # neutral-900 is the one shared step that changes: darker than every dark surface, so that scrim
    palette["neutral-900"] = to_hex(0.10, c, h)  # (neutral-900 in both files) dims the page; the lint flags a scrim that no component uses unless it aliases a used step
    flat = dict(palette)
    surf = dark_surfaces(a)
    flat["surface"] = surf[0]
    flat.update(zip(LEVELS, surf[1:]))
    top = surf[5]
    scale = lambda n: [palette["%s-%d" % (n, s)] for s in STEPS]
    ref = lambda n, i: "{colors.%s-%d}" % (n, STEPS[min(max(i, 0), 9)])
    # accent default: first step from 300 to 600 searched from the lightest, 4.5:1 on level-5 and against its content (step 900);
    # from 300 (a brand lighter than 300 is never kept), hover (default - 1) and pressed (default - 2, stopped at 50) are distinct, one step at a time
    ok = lambda sc, i: dark_ok(sc, i, top)
    note = ""
    for key in ROLES:
        sc = scale(names[key])
        d = next((i for i in range(3, 7) if ok(sc, i)), None)
        if key == "brand":
            bi = sc.index(a.brand)
            if ok(sc, bi):
                d = bi  # the brand color passes: kept as is
            elif d is not None:
                p = min((i for i in range(3, 7) if ok(sc, i)), key=lambda i: (abs(i - bi), i))
                if a.dark_brand is None:
                    raise ValueError("The brand color %s does not pass in dark mode (%.2f:1 on %s, 4.5:1 needed; its palette step must also keep distinct hover and pressed steps).\n"
                                     "Nearest step of its palette that passes: %s-%d %s (%.2f:1 on %s).\n"
                                     "Accept it with --dark-brand accept, or refuse with --dark-brand keep (the failing pairs are then reported)." %
                                     (a.brand, contrast(a.brand, top), top, names[key], STEPS[p], sc[p], contrast(sc[p], top), top))
                d = p if a.dark_brand == "accept" else bi
                note = "brand %s: %s" % (a.brand, "proposed step %s-%d accepted" % (names[key], STEPS[p]) if d == p else "refused, kept as is")
        if d is None:
            raise ValueError("The %s color has no step from 300 to 600 reaching 4.5:1 on the dark surface and against its content: give another color." % key)
        idx[key] = d
    b, nu = names["brand"], scale("neutral")
    sem = {
        "surface": surf[0],
        "primary": ref(b, idx["brand"]), "on-primary": ref(b, 9),
        "primary-hover": ref(b, idx["brand"] - 1), "primary-pressed": ref(b, idx["brand"] - 2),
        "primary-container": ref(b, 9), "on-primary-container": None,
        "primary-container-hover": ref(b, 8), "primary-container-pressed": ref(b, 7),
        "primary-subtle-hover": ref(b, 9), "primary-subtle-pressed": ref(b, 8), "on-primary-subtle": None,
        **{tok: v for k in ROLES[1:] for tok, v in (
            (k, ref(names[k], idx[k])), ("on-" + k, ref(names[k], 9)))},
        "danger-hover": ref(names["danger"], idx["danger"] - 1), "danger-pressed": ref(names["danger"], idx["danger"] - 2),
        **{tok: v for k in ROLES[1:] for tok, v in (
            (k + "-container", ref(names[k], 9)), (k + "-container-hover", ref(names[k], 8)),
            (k + "-container-pressed", ref(names[k], 7)), ("on-%s-container" % k, None))},
        "outline": ref("neutral", next((i for i in (6, 5, 4) if contrast(nu[i], top) >= 3), 3)),  # 3:1 on level-5, darkest step that passes
        "disabled-container": "{colors.neutral-800}",
        "on-disabled": "{colors.neutral-500}", "focus-ring": None,
        "on-surface": None, "on-surface-muted": ref("neutral", next((i for i in (4, 3, 2) if contrast(nu[i], top) >= 4.5), 2)),
        "neutral-subtle-hover": "{colors.neutral-800}", "neutral-subtle-pressed": "{colors.neutral-700}",
        "inverse-surface": "{colors.neutral-100}", "on-inverse-surface": "{colors.neutral-900}",  # tooltip inverted: light fill, dark content
        "link-visited": None,
    }
    assert len(sem) == 43
    flat.update(sem)
    L, C, h = to_oklch(resolve(flat, sem["primary"]))  # visited: the default step with half its chroma, distinct from hover (default - 1) at the same contrast
    flat["link-visited"] = sem["link-visited"] = to_hex(L, C / 2, h)
    fi = idx["brand"]  # ring: lightest side moves up from the default until 3:1 on every fill
    flat["focus-ring"] = sem["focus-ring"] = ref(b, next((i for i in range(fi, -1, -1) if ring_ok(flat, ref(b, i), DARK_FILLS)), 0))
    for tok, sc in (("on-primary-container", b), ("on-primary-subtle", b), ("on-surface", "neutral"),
                    *(("on-%s-container" % k, names[k]) for k in ROLES[1:])):
        bgs = [resolve(flat, "{colors.%s}" % lvl(bg)) for _, bg, fg in components() if fg == tok]  # lightest decides
        sca = scale(sc)
        flat[tok] = ref(sc, next((i for i in (2, 1, 0) if all(contrast(sca[i], x) >= 4.5 for x in bgs)), 0))  # 200, 100, then 50; failure reported by check()
    check_muted(flat)
    flat["scrim"] = "{colors.neutral-900}"
    return {k: flat[k] for k in (*palette, *list(light)[50:], *LEVELS, "scrim")}, {"idx": idx, "note": note}


def add_dark_roles(light):
    """Light file of a theme with a dark mode: same roles as the dark file. surface-level-n equals surface, the scrim keeps the light dialog veil."""
    light.update({**{l: "{colors.surface}" for l in LEVELS}, "scrim": "{colors.neutral-900}"})


RING_FILLS = ("surface", "neutral-subtle-hover", "neutral-subtle-pressed",  # segments, tabs, chip remove, search clear: rest, hover, pressed
              "primary-container", "primary-container-hover", "primary-container-pressed",  # selected segment, info alert controls
              *("%s-container%s" % (k, s) for k in ROLES[1:] for s in ("", "-hover", "-pressed")))  # alert controls, other severities


DARK_FILLS = tuple(LEVEL5 if f == "surface" else f for f in RING_FILLS)


def lvl(bg):
    """Dark mode checks contrast on the most unfavorable surface: a pair that passes on level-5 passes on every lower level."""
    return LEVEL5 if bg == "surface" else bg


def ring_ok(flat, ring, fills=RING_FILLS):
    return all(contrast(resolve(flat, ring), resolve(flat, "{colors.%s}" % f)) >= 3 for f in fills)


def check_muted(flat):
    """on-surface-muted must read quieter than on-surface: the same step is an error, never a silent fallback."""
    if resolve(flat, flat["on-surface"]) == resolve(flat, flat["on-surface-muted"]):
        raise ValueError("on-surface and on-surface-muted fall on the same neutral step (%s-%d): the muted text would not be "
                         "quieter than the main text. Give another neutral tint." % step_of(flat, "on-surface"))


def components():
    out = []
    for v, bg, fg in (("filled", "primary", "on-primary"), ("tonal", "primary-container", "on-primary-container"),
                      ("outlined", None, "primary"), ("text", None, "primary"), ("danger", "danger", "on-danger")):
        for st, suffix in (("", ""), ("hover", "-hover"), ("pressed", "-pressed")):
            if bg:
                b = bg + suffix
            else:
                b = "surface" if not st else "primary-subtle-" + st
            out.append(("button-%s%s" % (v, "-" + st if st else ""), b, "on-primary-subtle" if st and not bg else fg))
    out.append(("button-focus-ring", "surface", "focus-ring"))
    assert len(out) == 16
    for v, bgs, fg in (("default", ("surface", "neutral-subtle-hover", "neutral-subtle-pressed"), "on-surface"),
                       ("selected", ("primary-container", "primary-container-hover", "primary-container-pressed"), "on-primary-container"),
                       ("remove", ("surface", "neutral-subtle-hover", "neutral-subtle-pressed"), "on-surface")):
        for st, bg in zip(("", "hover", "pressed"), bgs):
            out.append(("chip-%s%s" % (v, "-" + st if st else ""), bg, fg))
    out.append(("chip-focus-ring", "surface", "focus-ring"))
    out.append(("tooltip-plain", "inverse-surface", "on-inverse-surface"))
    for n, fg in (("link", "primary"), ("link-hover", "primary-hover"), ("link-pressed", "primary-pressed"),
                  ("link-visited", "link-visited"), ("link-focus-ring", "focus-ring")):
        out.append((n, "surface", fg))  # no fill: the content color moves, not the background
    out += [("badge-primary", "primary", "on-primary"), ("badge-danger", "danger", "on-danger"),
            ("badge-success", "success", "on-success"), ("badge-warning", "warning", "on-warning"),
            ("badge-neutral", "neutral-subtle-pressed", "on-surface"), ("avatar-default", "neutral-subtle-pressed", "on-surface"),
            ("progress-primary", "surface", "primary"), ("progress-danger", "surface", "danger")]
    out += [("text-field", "surface", "on-surface"), ("text-field-muted", "surface", "on-surface-muted"),
            ("text-field-error", "surface", "danger"), ("text-field-read-only", "neutral-subtle-hover", "on-surface"),
            ("text-field-focus-ring", "surface", "focus-ring")]
    for st, bg in (("", "surface"), ("-hover", "neutral-subtle-hover"), ("-pressed", "neutral-subtle-pressed")):
        out.append(("search-field-clear" + st, bg, "on-surface"))
    for n, bg, fg in (("checkbox", "surface", "on-surface"), ("checkbox-muted", "surface", "on-surface-muted"),
                      ("checkbox-error", "surface", "danger"), ("checkbox-focus-ring", "surface", "focus-ring")):
        out.append((n, bg, fg))
    for c in ("checkbox-selected", "radio-selected", "switch-on"):
        for st, suffix in (("", ""), ("-hover", "-hover"), ("-pressed", "-pressed")):
            out.append((c + st, "primary" + suffix, "on-primary"))  # mark on the selected fill, same pairs as button-filled
    for st, suffix in (("", ""), ("-hover", "-hover"), ("-pressed", "-pressed")):
        out.append(("slider" + st, "surface", "primary" + suffix))  # fill-less: the thumb and fill color moves, each state darker
    for st, bg in (("", "surface"), ("-hover", "neutral-subtle-hover"), ("-pressed", "neutral-subtle-pressed")):
        out.append(("tab" + st, bg, "on-surface-muted" if not st else "on-surface"))  # unselected label: quiet on the surface only
        out.append(("tab-selected" + st, bg, "on-surface"))
    out.append(("tab-focus-ring", "surface", "focus-ring"))
    for st, bg in (("", "surface"), ("-hover", "neutral-subtle-hover"), ("-pressed", "neutral-subtle-pressed")):
        out.append(("accordion" + st, bg, "on-surface"))
    out.append(("accordion-focus-ring", "surface", "focus-ring"))
    for st, bg in (("", "surface"), ("-hover", "neutral-subtle-hover"), ("-pressed", "neutral-subtle-pressed")):
        out.append(("menu-item" + st, bg, "on-surface"))  # menu items and select options
        out.append(("menu-item-danger" + st, bg, "danger" + st))  # destructive item: the content darkens with its fill
    out += [("menu-muted", "surface", "on-surface-muted"), ("menu-focus-ring", "surface", "focus-ring"), ("popover", "surface", "on-surface")]
    for k in ROLES[1:]:  # alert (info reuses button-tonal*): its close button and action take the hover and pressed fills
        for st in ("", "-hover", "-pressed"):
            out.append(("alert-%s%s" % (k, st), "%s-container%s" % (k, st), "on-%s-container" % k))
    for st, bg in (("", "surface"), ("-hover", "neutral-subtle-hover"), ("-pressed", "neutral-subtle-pressed")):
        out.append(("card" + st, bg, "on-surface"))  # clickable card: grayed fills, so on-surface only
    out.append(("card-focus-ring", "surface", "focus-ring"))
    out += [("dialog", "surface", "on-surface"), ("toast", "surface", "on-surface"),
            ("toast-success", "surface", "success"), ("toast-danger", "surface", "danger")]  # status icon, on the surface
    assert len(out) == 101
    return out


def resolve(colors, v):
    while v.startswith("{colors."):
        v = colors[v[8:-1]]
    return v


def step_of(colors, tok):
    """(scale, step) of the last palette step a token resolves through, or None (raw hex)."""
    v, found = "{colors.%s}" % tok, None
    while v.startswith("{colors."):
        tok = v[8:-1]
        v = colors[tok]
        m = None if tok in LEVELS else re.fullmatch(r"(.+)-(\d+)", tok)  # surface-level-n is a role, not a palette step
        found = (m.group(1), int(m.group(2))) if m else found
    return found


def check(colors, comps, dark=False):
    """Every components entry: 4.5:1, background family, content step, states distinct and darker (lighter in dark mode). Returns rows."""
    rows, prev = [], {}
    worse = (lambda x, y: x <= y) if dark else (lambda x, y: x >= y)
    way = "lighter" if dark else "darker"
    for name, bg, fg in comps:
        a, b = resolve(colors, "{colors.%s}" % bg), resolve(colors, "{colors.%s}" % fg)  # a: fill, for the order of states
        r = contrast(resolve(colors, "{colors.%s}" % (lvl(bg) if dark else bg)), b)
        sb, sf, why = step_of(colors, bg), step_of(colors, fg), []
        if r < 4.5:
            why.append("below 4.5:1")
        if dark and bg != "inverse-surface":  # the tooltip is the one component that keeps the light rules, inverted
            if bg in BRIGHT_BG:  # bright: step 900 of the same scale
                if not (sf and sf == (sb[0], 900)):
                    why.append("content on a bright fill is not step 900 of its scale")
            elif sb and sb[1] < 700:
                why.append("intermediate background")
            elif not (fg == "on-surface" or (sf and sb and sf[0] == sb[0] and sf[1] <= 200) or (bg == "surface" and fg in ACCENT) or ON_FILL.get(fg) == bg):
                why.append("content is not step 50-200 of the background scale or on-surface")  # dark: surface roles, steps 700-900
        elif sb and 300 <= sb[1] <= 500:
            why.append("intermediate background")
        elif sb and sb[1] <= 200:  # light: steps 700-900 of the same scale; accent token on surface only
            if not (sf and sf[0] == sb[0] and sf[1] >= 700) and not (bg == "surface" and fg in ACCENT) and ON_FILL.get(fg) != bg:
                why.append("content is not step 700-900 of the background scale")
        elif sb and not (b == WHITE or (sf and sf[0] == sb[0] and sf[1] == 50)):
            why.append("content on solid is not white or step 50")
        group = re.sub(r"-(hover|pressed)$", "", name)
        if group in prev:
            pa, pb, pbg = prev[group]
            if bg == pbg == "surface":  # fill-less component (link): the content moves, each state darker (lighter in dark mode)
                if worse(lum(b), lum(pb)):
                    why.append("content not %s than the previous state" % way)
            elif worse(lum(a), lum(pa)):
                why.append("background not %s than the previous state" % way)
        prev[group] = (a, b, bg)
        rows.append((name, sb, sf, r, why))
    return rows


NONTEXT = ("outline",)  # tokens that draw a component boundary: 3:1 on the surface (WCAG 1.4.11); the lint cannot check them


def report(colors, comps, dark=False):
    lines = ["Contrast report (WCAG 2.x, threshold 4.5:1, families and states checked)" + (", dark mode, on %s" % LEVEL5 if dark else ""), ""]
    bad = 0
    fmt = lambda t: "%s-%d" % t if t else "white/other"
    surf, fills = (LEVEL5, DARK_FILLS) if dark else ("surface", RING_FILLS)
    for name, sb, sf, r, why in check(colors, comps, dark):
        bad += bool(why)
        lines.append("%-24s bg %-12s text %-12s %5.2f  %s" % (name, fmt(sb), fmt(sf), r, "PASS" if not why else "FAIL: " + "; ".join(why)))
    for tok in NONTEXT:
        r = contrast(resolve(colors, "{colors.%s}" % tok), resolve(colors, "{colors.%s}" % surf))
        bad += r < 3
        lines.append("%-24s non-text on %-24s%5.2f  %s" % (tok, "%s (3:1)" % surf, r, "PASS" if r >= 3 else "FAIL: below 3:1"))
    fr = resolve(colors, "{colors.focus-ring}")
    for f in fills:
        r = contrast(fr, resolve(colors, "{colors.%s}" % f))
        bad += r < 3
        lines.append("%-24s non-text on %-24s (3:1) %5.2f  %s" % ("focus-ring", f, r, "PASS" if r >= 3 else "FAIL: below 3:1"))
    total = len(comps) + len(NONTEXT) + len(fills)
    if dark:  # each surface strictly lighter than the previous one
        ls = [lum(resolve(colors, "{colors.%s}" % t)) for t in ("surface",) + LEVELS]
        order = all(x < y for x, y in zip(ls, ls[1:]))
        bad, total = bad + (not order), total + 1
        lines.append("%-24s strictly lighter from level-0 to level-5          %s" % ("surface levels", "PASS" if order else "FAIL: not strictly lighter"))
    lines += ["", "%d of %d pairs pass." % (total - bad, total)]
    return "\n".join(lines), bad


def typography_yaml(a):
    q = json.dumps
    y = ["typography:"]
    for s, px in zip(SIZES, FONT_SIZE[a.density]):
        y += ["  label-" + s + ":", "    fontFamily: " + q(a.font), "    fontSize: %dpx" % px, "    fontWeight: 500",
              "    lineHeight: %dpx" % math.floor(px * 1.25 + 0.5), "    letterSpacing: 0px"]
    return y


def design_md(a, colors, info, comps, dark=False):
    q = json.dumps
    ni, ix = info["names"], info["idx"]
    di = DENSITIES.index(a.density)
    sizes = FONT_SIZE[a.density]
    style, _, lib = a.icons.partition(",")
    style, lib = style.strip(), lib.strip() or "an icon library of your choice"
    y = ["---", "name: " + q(a.name), "colors:"]
    y += ["  %s: %s" % (k, q(v)) for k, v in colors.items()]
    y += typography_yaml(a)
    y += ["rounded:", "  control: " + ROUNDED[a.corners], "  overlay: " + OVERLAY[a.corners], "  avatar: " + AVATAR_RADIUS, "spacing:"]
    y += ["  %s: %dpx" % (k, v[di]) for k, v in SPACING.items()]
    y += ["  border-width: 1px", "  focus-ring-width: 2px", "  focus-ring-offset: 2px", "components:"]
    for n, bg, fg in comps:
        y += ["  %s:" % n, "    backgroundColor: " + q("{colors.%s}" % bg), "    textColor: " + q("{colors.%s}" % fg)]
    y.append("---")
    sc = lambda k: "`%s-50` to `%s-900`" % ((ni.get(k, k),) * 2)
    ctl = ", ".join("%s %dpx" % (k[8:], v[di]) for k, v in SPACING.items() if k.startswith("control"))
    sp = ", ".join("%s %dpx" % (k, v[di]) for k, v in SPACING.items() if k in ("xs", "sm", "md", "lg", "xl", "2xl"))
    elev = "\n".join("| `%s` | %s | %s |" % (l, r, "`%s`" % s if s != "none" else s) for l, r, s in ELEVATION)
    body = f"""
## Overview

{a.name} is a design system theme for buttons, chips, tooltips, dividers, links, badges, avatars, progress indicators, text fields, search fields, checkboxes, radio buttons, switches, sliders, segmented controls, tabs, accordions, menus, selects, popovers, dialogs, alerts, toasts, cards and the components built on them. It uses a {ni['brand']} brand color ({a.brand}), a {ni['danger']} danger color ({a.danger}), a {ni['success']} success color ({a.success}), a {ni['warning']} warning color ({a.warning}), {a.neutral} grays, the {a.font} font, {a.corners} corners and {a.density} density. Every value lives in this file; component specs only reference tokens.

## Colors

The theme has five primitive scales: {sc('brand')} for the brand, {sc('danger')} for destructive actions, {sc('success')} for success, {sc('warning')} for warnings, and {sc('neutral')} for grays and backgrounds. State colors are semantic tokens that point to scale steps. The `default` step is the first step from 600 to 900 reaching 4.5:1 in the worse case between white and `{{colors.surface}}`; `hover` is `default` plus 2 steps and `pressed` is `default` plus 4 steps, stopped at 900. Here the `default` steps are `{ni['brand']}-{STEPS[ix['brand']]}` (brand), `{ni['danger']}-{STEPS[ix['danger']]}` (danger), `{ni['success']}-{STEPS[ix['success']]}` (success) and `{ni['warning']}-{STEPS[ix['warning']]}` (warning). Content on a filled brand, danger, success or warning color (`on-primary`, `on-danger`, `on-success`, `on-warning`) is always white. Tonal containers use steps 50, 100 and 200 (enabled, hover, pressed); `on-primary-container` and `on-primary-subtle` are the first step from 700 to 900 reaching 4.5:1 on every background they serve. The neutral chip uses `surface`, `neutral-subtle-hover` and `neutral-subtle-pressed` (neutral 50, 100, 200) with `on-surface`, found by the same search on the neutral scale. The tooltip is `inverse-surface` (neutral 900) with white `on-inverse-surface`. Links, badges, avatars and progress indicators reuse these tokens: the link moves its content color (`primary`, `primary-hover`, `primary-pressed`, then `link-visited`, the brand step just after `primary`, when visited) on the surface, the status badge adds `success` and `warning` fills, the avatar and the neutral badge use `neutral-subtle-pressed` with `on-surface`, and the progress indicator is `primary` or `danger` on the surface. The text field adds one color, `on-surface-muted` (neutral step 600, or 700 if 600 is below 4.5:1), for the placeholder, the helper text, the counter and the affixes; its value and label use `on-surface`, its error uses `danger`, and a read-only field is filled with `neutral-subtle-hover`. The field border is `outline`, kept at 3:1 or more on the surface (neutral step 500, or 600), a non-text check that the script reports and the lint cannot. The focus ring (`focus-ring`, the brand `default` step, moved to a darker step if needed) is checked the same way at 3:1 against every fill it can sit on: the surface, the neutral hover and pressed fills, and the selected container in its three states, because segments, tabs and the small round buttons draw it inside. The search field reuses the text field tokens. `on-surface-muted` is used on the surface only, never on a grayed fill, and the script refuses a theme where it equals `on-surface`. The checkbox, radio and switch select with `primary` (white mark), draw their unselected border in `outline` and reuse `danger` for errors; the slider track is `outline` and its fill and thumb are `primary`. Segmented controls reuse the chip tokens (`outline` for their border and dividers). Tabs show their selected tab with a `primary` indicator and keep the label on `on-surface` (quiet `on-surface-muted` for an unselected tab at rest, on the surface only); accordion headers use the neutral chip fills with `on-surface`. The divider has no text and declares no pair. Menus, select lists and popovers float on `surface` with a quiet `neutral-subtle-pressed` border and the `level-2` shadow, so they add no color: items and options use the neutral fills (`surface`, `neutral-subtle-hover`, `neutral-subtle-pressed`) with `on-surface`, quiet `on-surface-muted` for group titles and for a shortcut at rest (on the surface only), and a destructive item moves from `danger` to `danger-hover` and `danger-pressed` as its fill darkens. Two spacing tokens size them: `menu-min-width` and `floating-max-width`. Dialogs, toasts and cards reuse the same surface, border and neutral fills, with `level-3` for the dialog and the toast; the dialog adds one width token, `dialog-max-width`, and its scrim is `inverse-surface` at a fixed opacity. The alert adds tonal containers for `danger`, `success` and `warning` (`<role>-container`, `-hover` and `-pressed` are steps 50, 100 and 200, with `on-<role>-container`, the first step from 700 to 900 reaching 4.5:1 on all three), as `primary-container` does for the brand, which the information alert reuses. The toast icon uses `success` or `danger` on the surface.

## Typography

The interface font is {a.font}. Four label sizes serve the button sizes: {', '.join('%s %dpx' % (s, px) for s, px in zip(SIZES, sizes))}. Weight is 500 and line height is 1.25 times the font size.

## Layout

Density is {a.density}. Control heights: {ctl}. Spacing scale: {sp}. Borders are 1px and the focus ring is 2px wide with a 2px offset.

## Elevation & Depth

This theme defines no shadow token: the elevation scale is this table.

| Level | Role | Shadow |
|---|---|---|
{elev}

## Shapes

Corners are {a.corners}: `rounded.control` is {ROUNDED[a.corners]} and `rounded.overlay` (tooltip, menu, select list, popover, dialog, alert, toast, card) is {OVERLAY[a.corners]}. `rounded.avatar` is {AVATAR_RADIUS} (a circle) whatever the corners; edit it to change the avatar shape.

## Icons

Icon style: {style}. Icon library: {lib}.

## Components

The `components` entries declare one `backgroundColor` and `textColor` pair per button variant, per chip group and per `enabled`, `hover` and `pressed` state, plus the focus rings against the surface, the tooltip pair, the link states against the surface, the badge variants, the avatar, the progress indicators, the text field (value, muted text, error, read-only, focus ring), the search field clear button, the mark on the selected fill of the checkbox, radio and switch, the choice control text (label, muted, error, focus ring), the slider thumb, the tab labels (unselected and selected, with their focus ring), the accordion headers, the menu items and select options (neutral and destructive, with their muted text and focus ring), the popover, dialog and toast text, the toast status icons, the alert tonal fills (danger, success, warning; the information alert reuses the tonal button entries) and the card states with its focus ring, so the lint checks contrast. The segmented control declares nothing of its own: it reuses the `chip-*` entries. Disabled pairs are exempt (WCAG 1.4.3) and are not declared. See the component specs in the kit: `button.md`, `chip.md`, `tooltip.md`, `divider.md`, `link.md`, `badge.md`, `avatar.md`, `progress.md`, `text-field.md`, `search-field.md`, `checkbox.md`, `radio.md`, `switch.md`, `slider.md`, `segmented-control.md`, `tabs.md`, `accordion.md`, `menu.md`, `select.md`, `popover.md`, `dialog.md`, `alert.md`, `toast.md`, `card.md`.

## Do's and Don'ts

- Do use semantic tokens such as `{{colors.primary}}`, never raw hex values.
- Do keep the state rule: `default`, then plus 2 steps for hover, then plus 4 steps for pressed.
- Don't add non-standard properties to `components`.
- Don't declare disabled pairs in `components`.
"""
    if dark:
        body = body.replace("\n\n## Typography", " The theme has a dark mode (DESIGN.dark.md, applied under `data-theme=\"dark\"`): `surface-level-1` to `surface-level-5` equal `surface` here and only differ in dark mode, and `scrim`, the veil behind the dialog, is `neutral-900`.\n\n## Typography", 1)
    return "\n".join(y) + "\n" + body


def design_md_dark(a, colors, info, dinfo):
    """DESIGN.dark.md: same role names as DESIGN.md, other values. Valid alone: it defines every token it references."""
    q = json.dumps
    ni, ix = info["names"], dinfo["idx"]
    y = ["---", "name: " + q(a.name + " (dark)"), "colors:"]
    y += ["  %s: %s" % (k, q(v)) for k, v in colors.items()]
    y += typography_yaml(a)  # the lint warns (missing-typography) on a file without typography tokens
    y.append("components:")
    for n, bg, fg in dark_components():
        y += ["  %s:" % n, "    backgroundColor: " + q("{colors.%s}" % lvl(bg)), "    textColor: " + q("{colors.%s}" % fg)]
    y.append("---")
    tint = "pure gray" if a.dark_tint == "neutral" else "gray with a weak, constant tint of the theme color"
    elev = "\n".join("| `level-%d` | `%s` |" % (i, "surface" if i == 0 else "surface-level-%d" % i) for i in range(6))
    body = f"""
## Overview

Dark mode of {a.name}, applied under `data-theme="dark"`. It has the same role names as DESIGN.md and other values; spacing, rounded and icons stay in DESIGN.md; typography is repeated because the lint warns on a file without it. Each pair of `components` is checked against `surface-level-5`, the lightest surface.

## Colors

The five primitive scales are the same as in DESIGN.md, except `neutral-900`, darker here so that `scrim` (`neutral-900`, as in DESIGN.md) dims the dark page; each role takes the step that suits the dark mode. Surfaces are {tint}: `surface` is {colors['surface']} and each level is a notch lighter, up to `surface-level-5` ({colors['surface-level-5']}). The accent `default` step is the first step from 300 to 600 searched from the lightest, reaching 4.5:1 on `surface-level-5` and against its content: here `{ni['brand']}-{STEPS[ix['brand']]}` (brand), `{ni['danger']}-{STEPS[ix['danger']]}` (danger), `{ni['success']}-{STEPS[ix['success']]}` (success) and `{ni['warning']}-{STEPS[ix['warning']]}` (warning). Hover is `default` minus 1 step and pressed is `default` minus 2 steps, stopped at 50: each state is lighter than the previous one. Content on an accent fill (`on-primary`, `on-danger`, `on-success`, `on-warning`) is step 900 of the same scale. Tonal containers use steps 900, 800 and 700 (enabled, hover, pressed), with content searched among steps 200, 100 and 50. Text is `on-surface`, a neutral step 200, 100 or 50; `on-surface-muted` and `outline` (3:1) are checked on `surface-level-5`. The tooltip is inverted: `inverse-surface` is a light neutral step with a dark `on-inverse-surface`. `scrim` is the veil behind the dialog.{(chr(10) + chr(10) + "Brand note: " + dinfo['note'] + ".") if dinfo['note'] else ""}

## Elevation & Depth

This theme has no shadow in dark mode: each elevation level has its own surface, a notch lighter than the previous level.

| Level | Surface role |
|---|---|
{elev}

## Components

The `components` entries are the same as in DESIGN.md, with `surface-level-5` in place of `surface` as background, so the lint checks the most unfavorable surface; four `text-on-level-<n>` entries add the text pair on `surface-level-1` to `surface-level-4`. Disabled pairs are exempt (WCAG 1.4.3) and are not declared.
"""
    return "\n".join(y) + "\n" + body


def font_stack(font):
    """The entered font first, then generic fallbacks."""
    f = font.strip().strip("\"'")
    generic = ("system-ui", "sans-serif", "serif", "monospace")
    return ", ".join(([f] if f.lower() in generic else ['"%s"' % f]) + [g for g in ("system-ui", "sans-serif") if g != f.lower()])


def tokens_css(a, colors, dark=None):
    """Fixed-name CSS custom properties, values resolved (no nested references). One :root block; with a dark mode, a second block under data-theme="dark"."""
    di = DENSITIES.index(a.density)
    v = ["/* %s - generated by theme.py, do not edit by hand." % a.name,
         "   Names: --color-<token>, --spacing-<token>, --rounded-<token>, --typography-<token>-<property>, --elevation-level-<0-5>.",
         "   All values are resolved (no nested references): semantic colors hold the hex of the step they point to." +
         ("\n   Dark mode: the [data-theme=\"dark\"] block overrides the colors and removes the shadows. */" if dark else " */"), ":root {"]
    v += ["  color-scheme: light;"] * bool(dark)
    v += ["  --color-%s: %s;" % (k, resolve(colors, c)) for k, c in colors.items()]
    v += ["  --spacing-%s: %dpx;" % (k, x[di]) for k, x in SPACING.items()]
    v += ["  --spacing-border-width: 1px;", "  --spacing-focus-ring-width: 2px;", "  --spacing-focus-ring-offset: 2px;"]
    v += ["  --rounded-control: %s;" % ROUNDED[a.corners], "  --rounded-overlay: %s;" % OVERLAY[a.corners],
          "  --rounded-avatar: %s;" % AVATAR_RADIUS]
    for s, px in zip(SIZES, FONT_SIZE[a.density]):
        t = "  --typography-label-%s-" % s
        v += [t + "font-family: %s;" % font_stack(a.font), t + "font-size: %dpx;" % px, t + "font-weight: 500;",
              t + "line-height: %dpx;" % math.floor(px * 1.25 + 0.5), t + "letter-spacing: 0px;"]
    v += ["  --elevation-%s: %s;" % (l, sh) for l, _, sh in ELEVATION]
    v.append("}")
    if dark:  # no shadow in dark mode: the surface levels carry the depth
        v += ["", '[data-theme="dark"] {', "  color-scheme: dark;"]
        v += ["  --color-%s: %s;" % (k, resolve(dark, c)) for k, c in dark.items()]
        v += ["  --elevation-%s: none;" % l for l, _, _ in ELEVATION]
        v.append("}")
    return "\n".join(v) + "\n"


def color_warnings(a, colors, info):
    out = []
    for key in ROLES:
        used = resolve(colors, colors["primary" if key == "brand" else key])
        entered = getattr(a, key)
        if used != entered:
            out.append("Warning: %s color entered %s, buttons use %s (%s-%d): the entered color does not reach 4.5:1 "
                       "with white text (contrast), so the first step that does is used." %
                       (key, entered, used, info["names"][key], STEPS[info["idx"][key]]))
    return out


# ---------- palettes.md ----------

def dark_palette(name, scale, top, neutral):
    """Dark mode block of palettes.md for one scale on the lightest dark surface `top` (same rules as derive_dark)."""
    nm = lambda i: "`%s-%d`" % (name, STEPS[i])
    out = ["| Step | On %s |" % top, "|---|---|"]
    out += ["| `%s-%d` | %.2f |" % (name, s, contrast(x, top)) for s, x in zip(STEPS, scale)]
    out += ["", "| Dark state | Step | Hex |", "|---|---|---|"]
    d = next((i for i in range(3, 7) if dark_ok(scale, i, top)), None)
    if d is None:
        out.append("| `default` | `none` | `none` |")
    else:
        out += ["| `%s` | %s | `%s` |" % (st, nm(max(d - k, 0)), scale[max(d - k, 0)]) for st, k in (("default", 0), ("hover", 1), ("pressed", 2))]
        if not neutral:
            out.append("| `on-default` | %s | `%s` |" % (nm(9), scale[9]))
    if neutral:  # same searches as derive_dark: darkest step reaching the ratio, searched from the dark side
        for label, steps, r in (("outline", (6, 5, 4), 3), ("on-surface-muted", (4, 3, 2), 4.5)):
            i = next((i for i in steps if contrast(scale[i], top) >= r), steps[-1] - 1)
            out.append("| `%s` | %s | `%s` |" % (label, nm(i), scale[i]))
    i = next((i for i in (2, 1, 0) if contrast(scale[i], scale[7]) >= 4.5), 0)  # lightest container state (700) decides
    out.append("| `on-container` | %s | `%s` |" % (nm(i), scale[i]))
    return out


def palettes_md():
    gray = neutral_scale("neutral", 0)
    surface = gray[0]
    tints = (("gray", gray), ("cool-gray", neutral_scale("cool", 0)), ("warm-gray", neutral_scale("warm", 0)))
    named, hues = [], {}
    for n, b in PALETTE_BASES:
        _, c, h = to_oklch(b)
        named.append((n, make_scale(LIGHT, [c * s for s in SHARE], h, b), c))
        hues[n] = h
    out = ["# Palettes", "",
           "Ready-made 10-step scales for agents that cannot run code. Pick the hue closest to the user's color and copy its steps (approximations: the exact color is not in the scale).",
           "Each step shows its contrast ratio against white and against neutral-50 (the surface, %s). The default step is the first step reaching 4.5:1 against both." % surface,
           "Default is searched in steps 600 to 900; hover is default plus 2 steps and pressed is default plus 4 steps, stopped at 900. Rows on-subtle (backgrounds 50, 100) and on-container (backgrounds 50, 100, 200) are the first step 700 to 900 reaching 4.5:1 on all of them. For a visited link, take the brand range step right after its default (default 600 gives 700).",
           "Each scale also has a dark mode block, with contrast against the lightest dark surface (surface-level-5): a step passing there passes on every darker surface. Dark default is the first step 300 to 600 reaching 4.5:1 on it and against its content (step 900, the on-default row); hover is default minus 1 step and pressed is default minus 2. The brand color of the user is kept instead of the default when it passes there and is step 300 or darker in its own scale (the other roles always take the default). Rows outline (3:1) and on-surface-muted (4.5:1) are given for the grays only, on-container (container states 900, 800, 700) is the first of steps 200, 100, 50 reaching 4.5:1 on step 700.",
           "The dark surface is tinted with the hue of the theme color (slightly-tinted, the default) or pure gray (neutral): the gamut blocks give both and the grays give their own tint. The tinted values use the hue of this scale's base color, so they are approximations for another hue.",
           "Generated by `theme.py --palettes`; do not edit by hand.", ""]
    for name, scale, c in [(n, s, 0.0) for n, s in tints] + named:
        d = default_index(scale, surface)
        out += ["## " + name, "",
                "| Step | Hex | On white | On neutral-50 |", "|---|---|---|---|"]
        out += ["| `%s-%d` | `%s` | %.2f | %.2f |" % (name, s, x, contrast(x, WHITE), contrast(x, surface))
                for s, x in zip(STEPS, scale)]
        out += ["", "| State | Step | Hex |", "|---|---|---|"]
        for st, k in (("default", 0), ("hover", 2), ("pressed", 4)):
            if d is None:
                out.append("| `%s` | `none` | `none` |" % st)
            else:
                i = min(d + k, 9)
                out.append("| `%s` | `%s-%d` | `%s` |" % (st, name, STEPS[i], scale[i]))
        for label, bgs in (("on-subtle", scale[:2]), ("on-container", scale[:3])):
            i = content_index(scale, bgs)
            out.append("| `%s` | `none` | `none` |" % label if i is None else "| `%s` | `%s-%d` | `%s` |" % (label, name, STEPS[i], scale[i]))
        notes = issues(scale, d, c)
        if notes:
            out += ["", "Note: %s." % "; ".join(notes) + (" No AA step." if d is None else "")]
        l5 = lambda c, h: to_hex(DARK_L0 + 5 * DARK_STEP, c, h)
        if name in dict(tints):
            tc, th = NEUTRAL_TINT[{"gray": "neutral", "cool-gray": "cool", "warm-gray": "warm"}[name]]
            variants = [("", l5(tc, th))]
        else:
            variants = [(" (slightly-tinted)", l5(DARK_CHROMA, hues[name])), (" (neutral)", l5(0.0, 0))]
        for tag, top in variants:
            out += ["", "Dark mode%s" % tag, ""] + dark_palette(name, scale, top, name in dict(tints))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ---------- entry point ----------

def selftest():
    assert abs(contrast(WHITE, "#000000") - 21) < 1e-9
    for hx in ("#2563EB", "#DC2626", "#16A34A"):
        assert to_hex(*to_oklch(hx)) == hx, hx
    assert hue_name("#2563EB") == "blue" and hue_name("#DC2626") == "red"
    assert all(hue_name(b) == n for n, b in PALETTE_BASES), "palette base hue names"
    a = parser().parse_args([])
    colors, info = derive(a)
    assert [info["idx"][k] for k in ROLES] == [6, 6, 6, 6], info
    assert (colors["danger-hover"], colors["danger-pressed"]) == ("{colors.red-800}", "{colors.red-900}") and "success-hover" not in colors and "warning-pressed" not in colors
    assert colors["primary-pressed"] == "{colors.blue-900}"
    sc = color_scale(a.success)[0]  # default at 700: refused where hover and pressed exist, accepted for success and warning
    assert any("collapse" in m for m in issues(sc, 7, 0.0, True)) and not any("collapse" in m for m in issues(sc, 7, 0.0, False))
    assert derive(parser().parse_args(["--success", "#14532D"]))
    assert issues(color_scale(a.brand)[0], None, 0.1) and issues(color_scale(a.brand)[0], 7, 0.0)
    assert (colors["primary-container-pressed"], colors["primary-subtle-pressed"]) == ("{colors.blue-200}", "{colors.blue-100}")
    assert report(colors, components())[1] == 0
    bad = dict(colors, **{"primary-subtle-pressed": "{colors.blue-50}"})  # same background as hover: must fail
    assert report(bad, components())[1] == 2
    bad = dict(colors, **{"on-primary-subtle": "{colors.blue-600}"})  # step 600 on a light background: must fail
    assert report(bad, components())[1] == 4
    bad = dict(colors, **{"primary-hover": "{colors.blue-600}"})  # link hover equal to enabled: must fail
    assert any(w for n, _, _, _, w in check(bad, components()) if n == "link-hover")
    assert len(colors) - 50 == 43 and len(components()) == 101, "43 semantic colors, 101 components entries"
    bad = dict(colors, **{"on-danger-container": "{colors.red-600}"})  # alert content on a light fill below step 700: must fail on its 3 states
    assert sum(1 for n, _, _, _, w in check(bad, components()) if n.startswith("alert-danger") and w) == 3
    assert (colors["danger-container-pressed"], colors["warning-container"]) == ("{colors.red-200}", "{colors.orange-50}")
    assert not check(colors, [("x", "surface", "success")])[0][4] and check(colors, [("x", "surface", "warning")])[0][4], "success is an accent on the surface, warning is not"
    assert not any(w for *_, w in check(colors, [("x", "neutral-subtle-hover", "danger-hover")])), "destructive item hover pair"
    assert check(colors, [("x", "neutral-subtle-pressed", "danger-hover")])[0][4], "danger-hover only serves neutral-subtle-hover"
    bad = dict(colors, **{"danger-hover": "{colors.red-400}"})  # destructive hover content too light on its fill: must fail
    assert any(w for n, _, _, _, w in check(bad, components()) if n == "menu-item-danger-hover")
    for c in (colors, derive(parser().parse_args(["--brand", "#7C3AED"]))[0]):  # visited: a step of the primary scale, never colliding
        lv = resolve(c, c["link-visited"])
        assert contrast(lv, c["neutral-50"]) >= 4.5, lv
        assert lv not in [resolve(c, c[k]) for k in ("primary", "on-surface", "primary-hover", "primary-pressed")], lv
    assert colors["link-visited"] == "{colors.blue-700}"
    assert (colors["outline"], colors["on-surface-muted"]) == ("{colors.neutral-500}", "{colors.neutral-600}")
    bad = dict(colors, outline="{colors.neutral-300}")  # field border below 3:1 (non-text check): must fail
    assert report(bad, components())[1] == 1
    assert ring_ok(colors, colors["focus-ring"]) and not ring_ok(dict(colors), "{colors.neutral-300}")  # weak ring must be refused
    assert not ring_ok(dict(colors, **{"warning-container-pressed": colors["focus-ring"]}), colors["focus-ring"])  # tonal alert fill is checked too
    bad = dict(colors, **{"focus-ring": "{colors.neutral-300}"})  # ring below 3:1 on the fills: must fail (once per fill it misses)
    assert report(bad, components())[1] >= 1
    hues = "#FFEB3B #84CC16 #22D3EE #FACC15 #4ADE80 #E11D48 #2563EB #7C3AED #F97316 #14B8A6 #EC4899 #A3E635".split()
    for h in hues:  # every brand color, every neutral tint: the generated ring passes on all fills
        for tint in ("warm", "cool", "tinted"):
            c = derive(parser().parse_args(["--brand", h, "--neutral", tint]))[0]
            assert ring_ok(c, c["focus-ring"]) and report(c, components())[1] == 0, (h, tint)
    try:  # muted text on the same step as the main text: must raise
        check_muted(dict(colors, **{"on-surface-muted": colors["on-surface"]}))
        raise AssertionError("check_muted accepted identical on-surface and on-surface-muted")
    except ValueError:
        pass
    check_muted(colors)
    for tint in ("warm", "cool", "tinted"):  # the 3:1 border and the muted text hold for every tint
        c = derive(parser().parse_args(["--neutral", tint]))[0]
        assert report(c, components())[1] == 0 and c["on-surface-muted"] != c["on-surface"], tint
    assert colors["on-surface"].startswith("{colors.neutral-") and colors["inverse-surface"] == "{colors.neutral-900}"
    text = design_md(a, colors, info, components())
    front = text.split("---")[1]
    assert not re.search(r"shadow|elevation", front, re.I), "no shadow key in the front matter or in components"
    rows = re.findall(r"^\| `(level-\d)` \|.*\| (.+) \|$", text, re.M)
    assert [r[0] for r in rows] == ["level-%d" % i for i in range(6)] and rows[0][1] == "none", rows
    assert "  overlay: 4px" in front and "  avatar: 9999px" in front and "  tooltip-max-width: 240px" in front and "  floating-max-width: 320px" in front
    css = tokens_css(a, colors)
    for pre in ("--color-primary:", "--color-blue-600:", "--spacing-control-md:", "--rounded-control:", "--rounded-avatar: 9999px;",
                "--typography-label-md-font-size:", "--typography-label-md-font-family: system-ui, sans-serif;",
                "--typography-label-xl-letter-spacing:", "--elevation-level-0: none;", "--elevation-level-5:"):
        assert "  " + pre in css, pre
    assert all("--elevation-level-%d:" % i in css for i in range(6)) and css.count(":root") == 1 and "var(" not in css
    assert font_stack("Inter") == '"Inter", system-ui, sans-serif'
    ad = parser().parse_args(["--dark"])  # dark mode: the brand needs an answer, then both files hold the same roles and pass
    try:
        derive_dark(ad, colors, info)
        raise AssertionError("a failing brand was accepted silently in dark mode")
    except ValueError as e:
        assert "--dark-brand" in str(e)
    for tint in ("slightly-tinted", "neutral"):
        ad = parser().parse_args(["--dark", "--dark-brand", "accept", "--dark-tint", tint])
        dark, dinfo = derive_dark(ad, colors, info)
        light = dict(colors)
        add_dark_roles(light)
        assert list(light) == list(dark) and len(dark) == 50 + 43 + 6, "same roles in both files"
        assert report(light, components())[1] == 0 and report(dark, dark_components(), dark=True)[1] == 0, tint
        assert dinfo["idx"]["brand"] == 4 and dark["primary-hover"] == "{colors.blue-300}" and dark["primary-pressed"] == "{colors.blue-200}"
        assert resolve(dark, "{colors.scrim}") != resolve(dark, dark["surface"]) and lum(resolve(dark, "{colors.scrim}")) < lum(dark["surface"])
        ls = [lum(dark[k]) for k in ("surface",) + LEVELS]
        assert ls == sorted(set(ls)), "surface levels strictly lighter"
        if tint == "neutral":
            assert len({dark[k][1:3] for k in ("surface",) + LEVELS} | {dark[k][3:5] for k in ("surface",) + LEVELS}) == 6, "pure gray"
        bad = dict(dark, **{"primary-hover": dark["primary"]})  # same background as default: must fail (states distinct, lighter)
        assert report(bad, dark_components(), dark=True)[1] > 0
        bad = dict(dark, **{"surface-level-3": dark["surface-level-2"]})  # levels not strictly lighter: must fail
        assert report(bad, dark_components(), dark=True)[1] > 0
        bad = dict(dark, outline="{colors.neutral-700}")  # 3:1 on level-5: must fail
        assert report(bad, dark_components(), dark=True)[1] > 0
        bad = dict(dark, **{"on-primary": "{colors.blue-600}"})  # content on a bright fill below step 900: must fail
        assert report(bad, dark_components(), dark=True)[1] > 0
        css = tokens_css(a, light, dark)
        assert css.count("{") == 2 and "  color-scheme: light;" in css and "  color-scheme: dark;" in css and '[data-theme="dark"] {' in css
        assert css.split('[data-theme="dark"]')[1].count("--elevation-level-") == 6 and "--elevation-level-5: none;" in css
        assert "var(" not in css and tokens_css(a, colors) == tokens_css(a, colors, None) and "color-scheme" not in tokens_css(a, colors)
    kept = parser().parse_args(["--dark", "--brand", "#93C5FD"])  # a light brand reaches 4.5:1 on level-5: kept without a question
    kc, ki = derive(kept)
    assert derive_dark(kept, kc, ki)[1]["note"] == ""
    refused = parser().parse_args(["--dark", "--dark-brand", "keep"])
    rd, _ = derive_dark(refused, colors, info)
    assert report(rd, dark_components(), dark=True)[1] > 0, "a refused brand is reported failing"
    a2 = parser().parse_args(["--danger", "#E11D48"])
    c2, i2 = derive(a2)
    assert color_warnings(a2, c2, i2) and not color_warnings(a, colors, info)
    print("selftest ok")


def parser():
    p = argparse.ArgumentParser(description="Generate a DESIGN.md theme and tokens.css from the 10 questionnaire answers.",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("--name", default="Design System", help="theme name")
    p.add_argument("--brand", default="#2563EB", help="hex #RRGGBB")
    p.add_argument("--danger", default="#DC2626", help="hex #RRGGBB")
    p.add_argument("--success", default="#15803D", help="hex #RRGGBB")
    p.add_argument("--warning", default="#B45309", help="hex #RRGGBB")
    p.add_argument("--neutral", default="neutral", choices=("neutral", "warm", "cool", "tinted"), help="gray tint")
    p.add_argument("--font", default="system-ui", help="font family; system-ui for the system UI font")
    p.add_argument("--corners", default="soft", choices=tuple(ROUNDED), help="corner style")
    p.add_argument("--density", default="default", choices=DENSITIES, help="control and font sizes")
    p.add_argument("--icons", default="outlined, Material Symbols", help='"<style>, <library>"')
    p.add_argument("--dark", action="store_true", help="also generate the dark mode: DESIGN.dark.md and a tokens.css with a dark block")
    p.add_argument("--dark-tint", default="slightly-tinted", choices=("slightly-tinted", "neutral"), help="dark surfaces: weak tint of the theme color, or pure gray")
    p.add_argument("--dark-brand", choices=("accept", "keep"), help="brand color failing in dark mode: accept the proposed palette step, or refuse (pairs reported failing)")
    p.add_argument("--dark-out", help="DESIGN.dark.md path (next to the DESIGN.md if not given; none with --out -)")
    p.add_argument("--out", help="output file, - for stdout (DESIGN.md, or palettes.md with --palettes if not given)")
    p.add_argument("--css", help="tokens.css path (tokens.css next to the DESIGN.md if not given; none with --out -)")
    p.add_argument("--palettes", action="store_true", help="generate the palette reference instead of a theme")
    p.add_argument("--selftest", action="store_true", help="run the built-in checks")
    return p


def main(argv=None):
    p = parser()
    a = p.parse_args(argv)
    if a.selftest:
        return selftest()
    for k in ROLES:
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", getattr(a, k)):
            p.error("--%s must be a hex code like #2563EB" % k)
        setattr(a, k, getattr(a, k).upper())
    out = a.out or ("palettes.md" if a.palettes else "DESIGN.md")
    if a.palettes:
        text, rep, rc = palettes_md(), "", 0
    else:
        try:
            colors, info = derive(a)
        except ValueError as e:
            print(e)
            return 2
        dark = dinfo = None
        if a.dark:
            try:
                dark, dinfo = derive_dark(a, colors, info)
            except ValueError as e:
                print(e)
                return 2
            add_dark_roles(colors)
        comps = components()
        rep, bad = report(colors, comps)
        text = design_md(a, colors, info, comps, bool(dark))
        if dark:
            drep, dbad = report(dark, dark_components(), dark=True)
            rep, bad = rep + "\n\n" + drep, bad + dbad
            dout = a.dark_out or (None if out == "-" else re.sub(r"(\.md)?$", ".dark.md", out, count=1))
            if dout:
                with open(dout, "w", encoding="utf-8") as f:
                    f.write(design_md_dark(a, dark, info, dinfo))
                print("Wrote " + dout)
            if dinfo["note"]:
                print("Note: " + dinfo["note"])
        rc = int(bad > 0)
        css = a.css or (None if out == "-" else os.path.join(os.path.dirname(out), "tokens.css"))
        if css:
            with open(css, "w", encoding="utf-8") as f:
                f.write(tokens_css(a, colors, dark))
            print("Wrote " + css)
        for w in color_warnings(a, colors, info):
            print(w)
    if out == "-":
        print(text)
    else:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print("Wrote " + out)
    if rep:
        print(rep)
    return rc


if __name__ == "__main__":
    sys.exit(main())
