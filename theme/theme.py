#!/usr/bin/env python3
"""Generate a DESIGN.md theme (and a contrast report) from the 8 questionnaire answers.

Python 3 standard library only, single file. Rules come from theme/questionnaire.md,
docs/conventions.md and components/button.md.

Usage (terminal):
    python3 theme.py --out DESIGN.md                      # all defaults
    python3 theme.py --name Acme --brand "#7C3AED" --corners pill --out DESIGN.md
    python3 theme.py --palettes --out palettes.md         # palette reference for agents without tools
    python3 theme.py --selftest

Usage (code execution sandbox, no shell): paste the file, then call
    main(["--brand", "#7C3AED", "--out", "DESIGN.md"])

Input: one option per answer (--name --brand --danger --neutral --font --corners --density --icons).
Colors are hex codes (#RRGGBB); resolving a color name to hex is left to the caller.
Output: DESIGN.md (use --out -  for stdout) and a contrast report on stdout.
Exit code: 0 ok, 1 a components pair fails 4.5:1, 2 unusable color (nothing written, proposal printed).
"""
import argparse
import json
import math
import re
import sys

STEPS = (50, 100, 200, 300, 400, 500, 600, 700, 800, 900)
LIGHT = (0.97, 0.93, 0.87, 0.79, 0.70, 0.62, 0.54, 0.46, 0.38, 0.30)
SHARE = (0.15, 0.30, 0.50, 0.75, 0.90, 1.0, 1.0, 1.0, 0.90, 0.75)
NEUTRAL_TINT = {"neutral": (0.0, 0), "warm": (0.010, 70), "cool": (0.010, 250)}
WHITE = "#FFFFFF"
ACCENT = ("primary", "danger", "focus-ring")

SIZES = ("sm", "md", "lg", "xl")
FONT_SIZE = {"compact": (12, 13, 14, 16), "default": (12, 14, 16, 18), "comfortable": (13, 15, 17, 20)}
ROUNDED = {"sharp": "0px", "soft": "4px", "rounded": "8px", "pill": "9999px"}
SPACING = {  # token: (compact, default, comfortable)
    "control-xs": (24, 28, 32), "control-sm": (28, 32, 40), "control-md": (32, 40, 48),
    "control-lg": (40, 48, 56), "control-xl": (48, 56, 64),
    "icon-sm": (14, 16, 20), "icon-md": (16, 20, 24), "icon-lg": (20, 24, 28), "icon-xl": (24, 28, 32),
    "xs": (2, 4, 6), "sm": (6, 8, 10), "md": (8, 12, 16), "lg": (12, 16, 20), "xl": (16, 20, 24), "2xl": (20, 24, 32),
}
DENSITIES = ("compact", "default", "comfortable")

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
    return make_scale(LIGHT, [c * s for s in SHARE], h, base), c, h


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
    _, c, h = to_oklch(hx)
    return to_hex(0.54, 0.4, h)  # to_hex reduces the chroma to the highest value that fits sRGB


# ---------- theme ----------

def derive(a):
    """Return (colors, info). Raise ValueError (unusable color) with the message to show."""
    bname, dname = hue_name(a.brand), hue_name(a.danger)
    bname = "brand" if bname == dname else bname
    neutral = neutral_scale(a.neutral, to_oklch(a.brand)[2])
    surface = neutral[0]
    info = {"names": {}, "idx": {}}
    colors = {}
    for key, name, base in (("brand", bname, a.brand), ("danger", dname, a.danger)):
        scale, c, _ = color_scale(base)
        d = default_index(scale, surface)
        problems = issues(scale, d, c)
        if problems:
            raise ValueError("The %s color %s cannot give accessible buttons with white text: %s.\n"
                             "Proposed alternative (same hue, lightness 0.54, highest chroma in sRGB): %s\n"
                             "Accept it or give another color." % (key, base, "; ".join(problems), proposal(base)))
        colors[name] = scale
        info["names"][key] = name
        info["idx"][key] = d
    colors["neutral"] = neutral
    flat = {}
    for name, scale in colors.items():
        for step, hx in zip(STEPS, scale):
            flat["%s-%d" % (name, step)] = hx

    def ref(name, i):
        return "{colors.%s-%d}" % (name, STEPS[min(i, 9)])

    b, bd = info["names"]["brand"], info["idx"]["brand"]
    d, dd = info["names"]["danger"], info["idx"]["danger"]
    sem = {
        "surface": "{colors.neutral-50}",
        "primary": ref(b, bd), "on-primary": WHITE,
        "primary-hover": ref(b, bd + 2), "primary-pressed": ref(b, bd + 4),
        "primary-container": ref(b, 0), "on-primary-container": None,
        "primary-container-hover": ref(b, 1), "primary-container-pressed": ref(b, 2),
        "primary-subtle-hover": ref(b, 0), "primary-subtle-pressed": ref(b, 1), "on-primary-subtle": None,
        "danger": ref(d, dd), "on-danger": WHITE,
        "danger-hover": ref(d, dd + 2), "danger-pressed": ref(d, dd + 4),
        "outline": "{colors.neutral-500}", "disabled-container": "{colors.neutral-100}",
        "on-disabled": "{colors.neutral-500}", "focus-ring": ref(b, bd),
    }
    assert len(sem) == 20
    flat.update(sem)
    for tok in ("on-primary-container", "on-primary-subtle"):  # darkest background of the token decides
        bgs = [resolve(flat, "{colors.%s}" % bg) for _, bg, fg in components() if fg == tok]
        flat[tok] = ref(b, content_index(colors[b], bgs) or 9)  # 900 failing is reported by check()
    return flat, info


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
            if not (sf and sf[0] == sb[0] and sf[1] >= 700) and not (bg == "surface" and fg in ACCENT):
                why.append("content is not step 700-900 of the background scale")
        elif sb and not (b == WHITE or (sf and sf[0] == sb[0] and sf[1] == 50)):
            why.append("content on solid is not white or step 50")
        group = re.sub(r"-(hover|pressed)$", "", name)
        if group in prev and lum(a) >= lum(prev[group]):
            why.append("background not darker than the previous state")
        prev[group] = a
        rows.append((name, sb, sf, r, why))
    return rows


def report(colors, comps):
    lines = ["Contrast report (WCAG 2.x, threshold 4.5:1, families and states checked)", ""]
    bad = 0
    fmt = lambda t: "%s-%d" % t if t else "white/other"
    for name, sb, sf, r, why in check(colors, comps):
        bad += bool(why)
        lines.append("%-24s bg %-12s text %-12s %5.2f  %s" % (name, fmt(sb), fmt(sf), r, "PASS" if not why else "FAIL: " + "; ".join(why)))
    lines += ["", "%d of %d pairs pass." % (len(comps) - bad, len(comps))]
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
    y += ["rounded:", "  control: " + ROUNDED[a.corners], "spacing:"]
    y += ["  %s: %dpx" % (k, v[di]) for k, v in SPACING.items()]
    y += ["  border-width: 1px", "  focus-ring-width: 2px", "  focus-ring-offset: 2px", "components:"]
    for n, bg, fg in comps:
        y += ["  %s:" % n, "    backgroundColor: " + q("{colors.%s}" % bg), "    textColor: " + q("{colors.%s}" % fg)]
    y.append("---")
    sc = lambda k: "`%s-50` to `%s-900`" % ((ni.get(k, k),) * 2)
    ctl = ", ".join("%s %dpx" % (k[8:], v[di]) for k, v in SPACING.items() if k.startswith("control"))
    sp = ", ".join("%s %dpx" % (k, v[di]) for k, v in SPACING.items() if k in ("xs", "sm", "md", "lg", "xl", "2xl"))
    body = f"""
## Overview

{a.name} is a design system theme for buttons and the components built on them. It uses a {ni['brand']} brand color ({a.brand}), a {ni['danger']} danger color ({a.danger}), {a.neutral} grays, the {a.font} font, {a.corners} corners and {a.density} density. Every value lives in this file; component specs only reference tokens.

## Colors

The theme has three primitive scales: {sc('brand')} for the brand, {sc('danger')} for destructive actions, and {sc('neutral')} for grays and backgrounds. State colors are semantic tokens that point to scale steps. The `default` step is the first step from 600 to 900 reaching 4.5:1 in the worse case between white and `{{colors.surface}}`; `hover` is `default` plus 2 steps and `pressed` is `default` plus 4 steps, stopped at 900. Here the brand `default` is `{ni['brand']}-{STEPS[ix['brand']]}` and the danger `default` is `{ni['danger']}-{STEPS[ix['danger']]}`. Content on a filled brand or danger color (`on-primary`, `on-danger`) is always white. Tonal containers use steps 50, 100 and 200 (enabled, hover, pressed); `on-primary-container` and `on-primary-subtle` are the first step from 700 to 900 reaching 4.5:1 on every background they serve.

## Typography

The interface font is {a.font}. Four label sizes serve the button sizes: {', '.join('%s %dpx' % (s, px) for s, px in zip(SIZES, sizes))}. Weight is 500 and line height is 1.25 times the font size.

## Layout

Density is {a.density}. Control heights: {ctl}. Spacing scale: {sp}. Borders are 1px and the focus ring is 2px wide with a 2px offset.

## Elevation & Depth

This theme defines no shadow or elevation token.

## Shapes

Corners are {a.corners}: `rounded.control` is {ROUNDED[a.corners]}.

## Icons

Icon style: {style}. Icon library: {lib}.

## Components

The `components` entries declare one `backgroundColor` and `textColor` pair per button variant and per `enabled`, `hover` and `pressed` state, plus the focus ring against the surface, so the lint checks contrast. Disabled pairs are exempt (WCAG 1.4.3) and are not declared. See the component specs in the kit, starting with `button.md`.

## Do's and Don'ts

- Do use semantic tokens such as `{{colors.primary}}`, never raw hex values.
- Do keep the state rule: `default`, then plus 2 steps for hover, then plus 4 steps for pressed.
- Don't add non-standard properties to `components`.
- Don't declare disabled pairs in `components`.
"""
    return "\n".join(y) + "\n" + body


# ---------- palettes.md ----------

def palettes_md():
    gray = neutral_scale("neutral", 0)
    surface = gray[0]
    tints = (("gray", gray), ("cool-gray", neutral_scale("cool", 0)), ("warm-gray", neutral_scale("warm", 0)))
    named = [(n, make_scale(LIGHT, [c * s for s in SHARE], h, b), c) for n, b in PALETTE_BASES
             for _, c, h in [to_oklch(b)]]
    out = ["# Palettes", "",
           "Ready-made 10-step scales for agents that cannot run code. Pick the hue closest to the user's color and copy its steps (approximations: the exact color is not in the scale).",
           "Each step shows its contrast ratio against white and against neutral-50 (the surface, %s). The default step is the first step reaching 4.5:1 against both." % surface,
           "Default is searched in steps 600 to 900; hover is default plus 2 steps and pressed is default plus 4 steps, stopped at 900. Rows on-subtle (backgrounds 50, 100) and on-container (backgrounds 50, 100, 200) are the first step 700 to 900 reaching 4.5:1 on all of them.",
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
    assert (info["idx"]["brand"], info["idx"]["danger"]) == (6, 6), info
    assert colors["primary-pressed"] == "{colors.blue-900}"
    assert issues(color_scale(a.brand)[0], None, 0.1) and issues(color_scale(a.brand)[0], 7, 0.0)
    assert (colors["primary-container-pressed"], colors["primary-subtle-pressed"]) == ("{colors.blue-200}", "{colors.blue-100}")
    assert report(colors, components())[1] == 0
    bad = dict(colors, **{"primary-subtle-pressed": "{colors.blue-50}"})  # same background as hover: must fail
    assert report(bad, components())[1] == 2
    bad = dict(colors, **{"on-primary-subtle": "{colors.blue-600}"})  # step 600 on a light background: must fail
    assert report(bad, components())[1] == 4
    print("selftest ok")


def parser():
    p = argparse.ArgumentParser(description="Generate a DESIGN.md theme from the 8 questionnaire answers.")
    p.add_argument("--name", default="Design System")
    p.add_argument("--brand", default="#2563EB", help="hex #RRGGBB")
    p.add_argument("--danger", default="#DC2626", help="hex #RRGGBB")
    p.add_argument("--neutral", default="neutral", choices=("neutral", "warm", "cool", "tinted"))
    p.add_argument("--font", default="system-ui", help="font family; system-ui for the system UI font")
    p.add_argument("--corners", default="soft", choices=tuple(ROUNDED))
    p.add_argument("--density", default="default", choices=DENSITIES)
    p.add_argument("--icons", default="outlined, Material Symbols", help='"<style>, <library>"')
    p.add_argument("--out", help="output file, - for stdout (default DESIGN.md, or palettes.md with --palettes)")
    p.add_argument("--palettes", action="store_true", help="generate the palette reference instead of a theme")
    p.add_argument("--selftest", action="store_true")
    return p


def main(argv=None):
    p = parser()
    a = p.parse_args(argv)
    if a.selftest:
        return selftest()
    for k in ("brand", "danger"):
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
