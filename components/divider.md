# Divider

A divider is a thin line that separates groups of content. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `line` |
| Configurations | horizontal, vertical, each full or inset |
| Variants | `subtle`, `strong` |
| Sizes | none; one thickness |
| Interactive states | none (never interactive) |
| State properties | none |

## Purpose

- Use a divider to separate two groups of related content in a list, a menu, a card, or a toolbar.
- Prefer spacing alone when the groups are already clearly apart: a divider adds visual noise.
- Do not use a divider as a border of a control or of a container: use the border of that component.
- Do not use a divider to carry information alone (a section title, a status): it is a visual cue only.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `line` | The separating line | yes | Always present; no text, no icon |

### Configurations

| Configuration | `orientation` | `inset` | Status |
|---|---|---|---|
| horizontal-full | `horizontal` | `false` | allowed |
| horizontal-inset | `horizontal` | `true` | allowed |
| vertical-full | `vertical` | `false` | allowed |
| vertical-inset | `vertical` | `true` | allowed |
| with-label | any | any | out-of-scope |

Combination rules:

- A divider has no content. A divider with a label is `out-of-scope`: use a heading.
- A divider never sits alone: it separates two siblings, so it is never the first or the last child of its container.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `orientation` | `horizontal`, `vertical` | `horizontal` | Direction of the line |
| `inset` | `true`, `false` | `false` | Leaves a margin at both ends of the line |
| `variant` | `subtle`, `strong` | `subtle` | Visual weight of the line |
| `decorative` | `true`, `false` | `true` | When `false`, the divider is exposed to assistive technologies as a separator |

## Variants

| Variant | Color | Intent |
|---|---|---|
| `subtle` | quiet neutral | Separates groups the layout already makes clear |
| `strong` | control outline neutral | The line is the only cue between two groups; kept visible for users with low vision |

## Sizes

### Decision

The divider has no named sizes. It has one thickness, a theme token. Its length follows its container: the full length of the cross axis of the parent.

### Size table

| Dimension | Token |
|---|---|
| `thickness` | `{spacing.border-width}` |
| `inset-length` | `{spacing.lg}` |

Geometry rules:

- `thickness` is the height of a horizontal line and the width of a vertical line.
- `inset-length` is the margin left empty at each end of the line when `inset` is true.
- A vertical divider takes the height of its container; the container sets the height.
- The line has square ends. There is no radius.

## States

### Interactive states

None: a divider is never interactive, never focusable.

### State properties

None.

## Token mapping

### `subtle`

| Part | Color |
|---|---|
| `line` | `{colors.neutral-subtle-pressed}` |

### `strong`

| Part | Color |
|---|---|
| `line` | `{colors.outline}` |

The divider is at `level-0` in every variant.

## Token contract

The theme must define every token below. The divider adds no token: the colors already exist for the chip.

### Colors

| Token | Role |
|---|---|
| `colors.neutral-subtle-pressed` | `subtle` line. Default: neutral step `200` |
| `colors.outline` | `strong` line |

### Spacing

| Token | Role |
|---|---|
| `spacing.border-width` | Line thickness |
| `spacing.lg` | Inset length |

### Components entries (contrast checks)

None. The line carries no text and no icon, so it is not a pair (see "Contrast pairs" in `docs/conventions.md`).

### Non-token requirement

None. The divider has no icon and no elevation.

## Accessibility

| Topic | Requirement |
|---|---|
| Role, decorative | When `decorative` is true, the divider is hidden from assistive technologies (`role="none"` or `aria-hidden`). It is the default: spacing and structure already separate the groups. |
| Role, informative | When `decorative` is false, the divider has the `separator` role. A vertical divider adds `aria-orientation="vertical"`; the horizontal value is the default of the role. |
| Accessible name | None. A separator is not named. |
| Focus | Never focusable. |
| Keyboard | None. |
| Target size | Not applicable: not interactive. |
| Contrast | A decorative divider has no minimum contrast. A divider that alone separates groups for sighted users uses `strong`, which follows the 3:1 non-text contrast of the outline color (WCAG 1.4.11). |

## Behavior

- Inside a list, the divider is a sibling between two items, not an item: it does not count as an item of the list.
- In a menu, an informative divider keeps the `separator` role so that groups are announced.

## Do and don't

| Do | Don't |
|---|---|
| Separate groups of related items | Put a divider between every item of a list |
| Use `inset` when the content has a leading column (icon or avatar) | Use `inset` on a divider that spans a whole card |
| Use `strong` when the line is the only cue | Use `strong` for plain visual rhythm |
| Let the container set the length | Hard-code a length |
| Rely on spacing first | Stack a divider and a large gap |

## Out of scope

Dividers with a label or an icon, dashed or dotted lines, thickness variants, animations, dark mode, and the spacing around the divider (which belongs to the layout) are not covered by this spec.
