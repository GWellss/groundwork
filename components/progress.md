# Progress

A progress indicator shows that something is loading or advancing, either as a linear bar or as a circular spinner, with a known value (determinate) or without one (indeterminate). This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `track`, `indicator` |
| Types | `linear`, `circular` |
| Modes | `determinate`, `indeterminate`, derived from the presence of `value` |
| Variants | `primary`, `danger` |
| Sizes | `linear`: `s`, `m`; `circular`: `s`, `m`, `l` |
| Interactive states | none (never interactive) |
| State properties | none |

## Purpose

- Use a `determinate` progress when the share of work done is known (an upload, a multi-step flow).
- Use an `indeterminate` progress when the duration is unknown (waiting for a server).
- Use `linear` for a page, a card, or a long operation, and `circular` for a small area, a single control, or a centered wait.
- Use `danger` when the operation has failed or is at risk, together with a message that says so.
- Do not use a progress for a loading state inside a button: the button has its own `spinner` (see `components/button.md`).
- Do not use a progress for a quantity that is not an operation (a score, a rating, a stock level).

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `track` | The full path: a bar or a ring | yes | Always present, shows the whole range |
| `indicator` | The moving or filled part | yes | A bar segment or an arc; its length shows `value` |

### Configurations

| Configuration | `type` | Mode | Status |
|---|---|---|---|
| linear-determinate | `linear` | `determinate` | allowed |
| linear-indeterminate | `linear` | `indeterminate` | allowed |
| circular-determinate | `circular` | `determinate` | allowed |
| circular-indeterminate | `circular` | `indeterminate` | allowed |
| no-label | any | any | forbidden |

Combination rules:

- The mode is derived: `determinate` when `value` is set, `indeterminate` otherwise.
- A progress always has an accessible name (`label`); one without is `forbidden`. A visible text, such as a percentage or a message, is optional and belongs to the layout.
- A single progress describes a single operation.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `type` | `linear`, `circular` | `linear` | Bar or spinner |
| `value` | number from 0 to 100 | none | Percentage done; absent for `indeterminate` |
| `variant` | `primary`, `danger` | `primary` | Color group of the indicator |
| `size` | `linear`: `s`, `m`; `circular`: `s`, `m`, `l` | `m` | Named dimension set |
| `label` | text | none, required | Accessible name ("Uploading photos") |
| `value-text` | text | none | Human text of the value ("3 of 5 files"), for the accessible description |

## Variants

| Variant | Indicator | Track | Intent |
|---|---|---|---|
| `primary` | brand | quiet neutral | Normal progress |
| `danger` | danger | quiet neutral | Failed or at risk; always with a message |

## Sizes

### Decision

Linear and circular have their own sizes: the first is a thickness, the second a diameter. Dimensions reuse spacing tokens of the theme, so density applies without new tokens.

### Size table, `linear`

| Size | Thickness |
|---|---|
| `s` | `{spacing.xs}` |
| `m` | `{spacing.sm}` |

### Size table, `circular`

| Size | Diameter | Stroke |
|---|---|---|
| `s` | `{spacing.icon-md}` | `{spacing.focus-ring-width}` |
| `m` | `{spacing.control-sm}` | `{spacing.xs}` |
| `l` | `{spacing.control-lg}` | `{spacing.xs}` |

Geometry rules:

- `linear` takes the full width of its container; its length is never a theme value. The container sets the width.
- `linear` ends are rounded: this is a fixed geometry, not a theme value.
- `circular` is a ring drawn in a square of the diameter. The stroke is centered on the ring and stays inside the square.
- `circular` ends of the arc are rounded, a fixed geometry.
- Determinate `linear`: the indicator starts at the leading edge of the track and its length is `value` percent of the track. In a right-to-left layout it starts at the right.
- Determinate `circular`: the arc starts at the top and runs clockwise over `value` percent of the ring.
- The spinner is drawn by the implementation; it is not an icon of the `## Icons` library.

## States

### Interactive states

None: a progress is never interactive and never focusable.

### State properties

None. The mode (`determinate` or `indeterminate`) comes from `value`, not from a state.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). A progress has no border and no content text.

### `primary`

| Part | Color |
|---|---|
| `track` | `{colors.neutral-subtle-pressed}` |
| `indicator` | `{colors.primary}` |

### `danger`

| Part | Color |
|---|---|
| `track` | `{colors.neutral-subtle-pressed}` |
| `indicator` | `{colors.danger}` |

The progress is at `level-0`.

## Token contract

The theme must define every token below. The progress adds no token: every color is reused from the button and the chip.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the contrast checks |
| `colors.neutral-subtle-pressed` | `track`. Default: neutral step `200` |
| `colors.primary` | `primary` indicator |
| `colors.danger` | `danger` indicator |

### Spacing

| Token | Role |
|---|---|
| `spacing.xs` | `linear` thickness for `s`; `circular` stroke for `m` and `l` |
| `spacing.sm` | `linear` thickness for `m` |
| `spacing.icon-md` | `circular` diameter for `s` |
| `spacing.control-sm` | `circular` diameter for `m` |
| `spacing.control-lg` | `circular` diameter for `l` |
| `spacing.focus-ring-width` | `circular` stroke for `s` |

### Components entries (contrast checks)

One entry per variant, using only the standard `backgroundColor` and `textColor` properties. The indicator is a shape, not text: it is checked as the `textColor` of a pair against `{colors.surface}`, which gives the 3:1 non-text contrast of WCAG 1.4.11 and more (the State colors rule gives 4.5:1). The progress has no interactive state, so the entries have no state suffix.

| Entry | backgroundColor | textColor |
|---|---|---|
| `progress-primary` | `{colors.surface}` | `{colors.primary}` |
| `progress-danger` | `{colors.surface}` | `{colors.danger}` |

### Non-token requirement

The progress has no icon and no elevation. Its timing values are behavior constants, not tokens (see Behavior).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | The progress has the `progressbar` role, for `linear` and for `circular`. |
| Accessible name | `label`, set through `aria-label` or `aria-labelledby`. A bare "Loading" is acceptable only when nothing more specific exists. |
| Determinate | `aria-valuemin="0"`, `aria-valuemax="100"`, and `aria-valuenow` set to `value`. `value-text`, when given, sets `aria-valuetext`. |
| Indeterminate | The same role and name, with no `aria-valuenow`. This tells assistive technologies that the value is unknown. |
| Busy region | The region that is loading carries `aria-busy="true"` while the progress is shown. |
| Completion | When the operation ends, the project announces the result (for example "Upload complete") in a polite live region. The progress itself is removed. |
| Focus | Never focusable. |
| Keyboard | None. |
| Target size | Not applicable: not interactive. |
| Not by color alone | The `danger` variant is always paired with a text message; the color alone never says that the operation failed (WCAG 1.4.1). |
| Contrast | The indicator reaches at least 3:1 against `{colors.surface}` and against `track`. It reaches 4.5:1 against the surface through the `components` entries, delegated to the DESIGN.md lint. |

## Behavior

Behavior constants. They are invariant, they are not theme tokens, and the theme never overrides them.

| Constant | Value | Meaning |
|---|---|---|
| `circular-turn` | 1000 ms | Duration of one full turn of an indeterminate `circular` indicator |
| `linear-cycle` | 2000 ms | Duration of one pass of an indeterminate `linear` indicator across the track |
| `circular-arc` | 75 percent | Length of the arc of an indeterminate `circular` indicator |
| `linear-segment` | 40 percent | Length of the segment of an indeterminate `linear` indicator, as a share of the track |

- Indeterminate `circular`: the arc rotates continuously at constant speed.
- Indeterminate `linear`: the segment travels from the leading edge to the trailing edge of the track, then starts again.
- Motion is the signal that work is going on, so it is kept when the user prefers reduced motion (WCAG 2.2.2, essential activity), but slowed down: the `circular-turn` and `linear-cycle` durations become about 2.5 to 3 times longer, for both `circular` and `linear`. An indeterminate progress is never turned into a static shape.
- Determinate: a change of `value` moves the indicator to the new value. The transition is the project's choice.
- Value outside 0 to 100: refused or clamped and reported, never rendered silently as is.
- A progress that finishes is removed or replaced by the result; it does not stay at 100 percent.

## Do and don't

| Do | Don't |
|---|---|
| Give the progress a name: "Uploading photos" | Leave it unnamed |
| Use `determinate` when the value is known | Fake a percentage |
| Pair `danger` with a text message | Rely on color to say that it failed |
| Use `circular` for small areas, `linear` for long operations | Use several progress indicators for one operation |
| Announce completion in a live region | Leave a finished bar on screen at 100 percent |

## Out of scope

The button `spinner` (see `components/button.md`), buffer bars, steppers, a percentage label inside the indicator, success and warning variants, skeleton loaders, animations other than the indeterminate motion above, and progress on colored or image backgrounds (contrast is checked only against `{colors.surface}`) are not covered by this spec.
