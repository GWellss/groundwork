#!/usr/bin/env python3
"""Generate a DESIGN.md theme (and a contrast report) from the 10 questionnaire answers.

Python 3 standard library only, single file. Rules come from theme/questionnaire.md,
docs/conventions.md and the component specs in components/.

Usage (terminal):
    python3 theme.py --out DESIGN.md                      # all defaults
    python3 theme.py --name Acme --brand "#7C3AED" --corners pill --out DESIGN.md
    python3 theme.py --out DESIGN.md --css tokens.css     # explicit CSS path
    python3 theme.py --palettes --out palettes.md         # palette reference for agents without tools
    python3 theme.py --selftest

Usage (code execution sandbox, no shell): paste the file, then call
    main(["--brand", "#7C3AED", "--out", "DESIGN.md"])

Input: one option per answer (--name --brand --danger --success --warning --neutral --font --corners --density --icons).
Colors are hex codes (#RRGGBB); resolving a color name to hex is left to the caller.
Output: DESIGN.md (use --out -  for stdout), tokens.css (default: next to the DESIGN.md; with --out -
only if --css is given) and a contrast report on stdout. tokens.css is generated here, without the CLI.
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


def issues(scale, d, base_chroma):
    if d is None:
        return ["no step from 600 to 900 reaches 4.5:1 against white and the surface"]
    out = []
    if min(d + 2, 9) == min(d + 4, 9):
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
        problems = issues(scale, d, c)
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
            (k, ref(names[k], info["idx"][k])), ("on-" + k, WHITE),
            (k + "-hover", ref(names[k], info["idx"][k] + 2)), (k + "-pressed", ref(names[k], info["idx"][k] + 4)))},
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
    assert len(sem) == 47
    flat.update(sem)
    # focus ring drawn inside a control or on a fill: 3:1 on every fill it can meet (WCAG 1.4.11); darker brand step if needed, as outline
    sem["focus-ring"] = flat["focus-ring"] = ref(b, next((i for i in range(bd, 9) if ring_ok(flat, ref(b, i))), 9))
    for tok, sc in (("on-primary-container", b), ("on-primary-subtle", b), ("on-surface", "neutral"),
                    *(("on-%s-container" % k, names[k]) for k in ROLES[1:])):
        bgs = [resolve(flat, "{colors.%s}" % bg) for _, bg, fg in components() if fg == tok]  # darkest decides
        flat[tok] = ref(sc, content_index(colors[sc], bgs) or 9)  # 900 failing is reported by check()
    check_muted(flat)
    return flat, info


RING_FILLS = ("surface", "neutral-subtle-hover", "neutral-subtle-pressed",  # segments, tabs, chip remove, search clear: rest, hover, pressed
              "primary-container", "primary-container-hover", "primary-container-pressed",  # selected segment, info alert controls
              *("%s-container%s" % (k, s) for k in ROLES[1:] for s in ("", "-hover", "-pressed")))  # alert controls, other severities


def ring_ok(flat, ring):
    return all(contrast(resolve(flat, ring), resolve(flat, "{colors.%s}" % f)) >= 3 for f in RING_FILLS)


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
        m = re.fullmatch(r"(.+)-(\d+)", tok)
        found = (m.group(1), int(m.group(2))) if m else found
    return found


def check(colors, comps):
    """Every components entry: 4.5:1, background family, content step, states distinct and darker. Returns rows."""
    rows, prev = [], {}
    for name, bg, fg in comps:
        a, b = resolve(colors, "{colors.%s}" % bg), resolve(colors, "{colors.%s}" % fg)
        r, sb, sf, why = contrast(a, b), step_of(colors, bg), step_of(colors, fg), []
        if r < 4.5:
            why.append("below 4.5:1")
        if sb and 300 <= sb[1] <= 500:
            why.append("intermediate background")
        elif sb and sb[1] <= 200:  # light: steps 700-900 of the same scale; accent token on surface only
            if not (sf and sf[0] == sb[0] and sf[1] >= 700) and not (bg == "surface" and fg in ACCENT) and ON_FILL.get(fg) != bg:
                why.append("content is not step 700-900 of the background scale")
        elif sb and not (b == WHITE or (sf and sf[0] == sb[0] and sf[1] == 50)):
            why.append("content on solid is not white or step 50")
        group = re.sub(r"-(hover|pressed)$", "", name)
        if group in prev:
            pa, pb, pbg = prev[group]
            if bg == pbg == "surface":  # fill-less component (link): the content moves, each state darker
                if lum(b) >= lum(pb):
                    why.append("content not darker than the previous state")
            elif lum(a) >= lum(pa):
                why.append("background not darker than the previous state")
        prev[group] = (a, b, bg)
        rows.append((name, sb, sf, r, why))
    return rows


NONTEXT = ("outline",)  # tokens that draw a component boundary: 3:1 on the surface (WCAG 1.4.11); the lint cannot check them


def report(colors, comps):
    lines = ["Contrast report (WCAG 2.x, threshold 4.5:1, families and states checked)", ""]
    bad = 0
    fmt = lambda t: "%s-%d" % t if t else "white/other"
    for name, sb, sf, r, why in check(colors, comps):
        bad += bool(why)
        lines.append("%-24s bg %-12s text %-12s %5.2f  %s" % (name, fmt(sb), fmt(sf), r, "PASS" if not why else "FAIL: " + "; ".join(why)))
    for tok in NONTEXT:
        r = contrast(resolve(colors, "{colors.%s}" % tok), resolve(colors, "{colors.surface}"))
        bad += r < 3
        lines.append("%-24s non-text on surface (3:1)           %5.2f  %s" % (tok, r, "PASS" if r >= 3 else "FAIL: below 3:1"))
    fr = resolve(colors, "{colors.focus-ring}")
    for f in RING_FILLS:
        r = contrast(fr, resolve(colors, "{colors.%s}" % f))
        bad += r < 3
        lines.append("%-24s non-text on %-24s (3:1) %5.2f  %s" % ("focus-ring", f, r, "PASS" if r >= 3 else "FAIL: below 3:1"))
    total = len(comps) + len(NONTEXT) + len(RING_FILLS)
    lines += ["", "%d of %d pairs pass." % (total - bad, total)]
    return "\n".join(lines), bad


def design_md(a, colors, info, comps):
    q = json.dumps
    ni, ix = info["names"], info["idx"]
    di = DENSITIES.index(a.density)
    sizes = FONT_SIZE[a.density]
    style, _, lib = a.icons.partition(",")
    style, lib = style.strip(), lib.strip() or "an icon library of your choice"
    y = ["---", "name: " + q(a.name), "colors:"]
    y += ["  %s: %s" % (k, q(v)) for k, v in colors.items()]
    y.append("typography:")
    for s, px in zip(SIZES, sizes):
        y += ["  label-" + s + ":", "    fontFamily: " + q(a.font), "    fontSize: %dpx" % px, "    fontWeight: 500",
              "    lineHeight: %dpx" % math.floor(px * 1.25 + 0.5), "    letterSpacing: 0px"]
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
    return "\n".join(y) + "\n" + body


def font_stack(font):
    """The entered font first, then generic fallbacks."""
    f = font.strip().strip("\"'")
    generic = ("system-ui", "sans-serif", "serif", "monospace")
    return ", ".join(([f] if f.lower() in generic else ['"%s"' % f]) + [g for g in ("system-ui", "sans-serif") if g != f.lower()])


def tokens_css(a, colors):
    """Fixed-name CSS custom properties, one :root block, values resolved (no nested references)."""
    di = DENSITIES.index(a.density)
    v = ["/* %s - generated by theme.py, do not edit by hand." % a.name,
         "   Names: --color-<token>, --spacing-<token>, --rounded-<token>, --typography-<token>-<property>, --elevation-level-<0-5>.",
         "   All values are resolved (no nested references): semantic colors hold the hex of the step they point to. */", ":root {"]
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
    return "\n".join(v + ["}"]) + "\n"


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

def palettes_md():
    gray = neutral_scale("neutral", 0)
    surface = gray[0]
    tints = (("gray", gray), ("cool-gray", neutral_scale("cool", 0)), ("warm-gray", neutral_scale("warm", 0)))
    named = []
    for n, b in PALETTE_BASES:
        _, c, h = to_oklch(b)
        named.append((n, make_scale(LIGHT, [c * s for s in SHARE], h, b), c))
    out = ["# Palettes", "",
           "Ready-made 10-step scales for agents that cannot run code. Pick the hue closest to the user's color and copy its steps (approximations: the exact color is not in the scale).",
           "Each step shows its contrast ratio against white and against neutral-50 (the surface, %s). The default step is the first step reaching 4.5:1 against both." % surface,
           "Default is searched in steps 600 to 900; hover is default plus 2 steps and pressed is default plus 4 steps, stopped at 900. Rows on-subtle (backgrounds 50, 100) and on-container (backgrounds 50, 100, 200) are the first step 700 to 900 reaching 4.5:1 on all of them. For a visited link, take the brand range step right after its default (default 600 gives 700).",
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
    assert (colors["success-hover"], colors["warning-pressed"]) == ("{colors.green-800}", "{colors.orange-900}")
    assert colors["primary-pressed"] == "{colors.blue-900}"
    assert issues(color_scale(a.brand)[0], None, 0.1) and issues(color_scale(a.brand)[0], 7, 0.0)
    assert (colors["primary-container-pressed"], colors["primary-subtle-pressed"]) == ("{colors.blue-200}", "{colors.blue-100}")
    assert report(colors, components())[1] == 0
    bad = dict(colors, **{"primary-subtle-pressed": "{colors.blue-50}"})  # same background as hover: must fail
    assert report(bad, components())[1] == 2
    bad = dict(colors, **{"on-primary-subtle": "{colors.blue-600}"})  # step 600 on a light background: must fail
    assert report(bad, components())[1] == 4
    bad = dict(colors, **{"primary-hover": "{colors.blue-600}"})  # link hover equal to enabled: must fail
    assert any(w for n, _, _, _, w in check(bad, components()) if n == "link-hover")
    assert len(colors) - 50 == 47 and len(components()) == 101, "47 semantic colors, 101 components entries"
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
        comps = components()
        rep, bad = report(colors, comps)
        text, rc = design_md(a, colors, info, comps), int(bad > 0)
        css = a.css or (None if out == "-" else os.path.join(os.path.dirname(out), "tokens.css"))
        if css:
            with open(css, "w", encoding="utf-8") as f:
                f.write(tokens_css(a, colors))
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
