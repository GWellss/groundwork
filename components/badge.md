# Badge

A badge is a small count or dot attached to another element (an icon, a tab, an avatar) to signal that something is new or pending. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

A badge is not a chip. A badge is never interactive, never stands alone, and shows a number or nothing. A chip is an interactive control with a text label.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `value` |
| Types | `count` (number in the container), `dot` (no content) |
| Variants | `primary`, `danger`, `neutral` |
| Sizes | `s`, `m` |
| Interactive states | none (never interactive) |
| State properties | none |

## Purpose

- Use a `count` badge to show a number of unread, new, or pending items on the element they belong to ("3" on an inbox icon).
- Use a `dot` badge to signal that something is new or needs attention when the number does not matter.
- Use `danger` for items that need action or signal an error, `primary` for new or unread items, `neutral` for a quiet count.
- Do not use a badge for a text label such as a status or a category: this kit has no component for it yet.
- Do not use a badge for an action, a filter, or a removable value: use a chip.
- Do not use a badge alone, away from the element it describes.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | The filled shape; a circle for one digit and for `dot`, a stadium for more | yes | Always present |
| `value` | The number | `count` only | Absent in `dot` |

The host is the element the badge is attached to. It is not a part of the badge.

### Configurations

| Configuration | Type | `value` | Variants | Allowed |
|---|---|---|---|---|
| count | `count` | yes | `primary`, `danger`, `neutral` | yes |
| dot | `dot` | no | `primary`, `danger` | yes |
| dot-neutral | `dot` | no | `neutral` | no |
| count-text | `count` | text, not a number | any | no |
| standalone | any | any | any | no |

Combination rules:

- `value` is a whole number. Text is not allowed.
- The `neutral` variant has no `dot`: its fill is too close to the surface to reach the 3:1 contrast of a shape without text (WCAG 1.4.11).
- A badge is always attached to a host. It never appears without one.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `type` | `count`, `dot` | `count` | Number or dot |
| `value` | whole number, 0 or more | none, required for `count` | The number shown |
| `max` | whole number, 1 or more | 99 | Highest number shown; above it the badge shows `max` followed by "+" |
| `variant` | `primary`, `danger`, `neutral` | `primary` | Color group |
| `size` | `s`, `m` | `m` | Named dimension set |
| `label` | text | none, required | Accessible text that says what the number or dot means ("3 unread messages") |

## Variants

| Variant | Container | Content | Intent |
|---|---|---|---|
| `primary` | solid brand | white | New or unread items |
| `danger` | solid danger | white | Items that need action, or an error |
| `neutral` | light neutral | dark neutral | A quiet count that must not draw attention |

## Sizes

### Decision

Two sizes. `s` suits small hosts (a 20 px icon), `m` the usual hosts. The height of a `count` badge reuses an icon size token, and the dot reuses a spacing token, so density applies to badges without new tokens.

### Size table

| Size | Count height | Count padding inline | Dot diameter | Value typography |
|---|---|---|---|---|
| `s` | `{spacing.icon-sm}` | `{spacing.xs}` | `{spacing.sm}` | `{typography.label-sm}` |
| `m` | `{spacing.icon-md}` | `{spacing.xs}` | `{spacing.md}` | `{typography.label-md}` |

Geometry rules:

- A `count` badge has a fixed height. Its minimum width equals its height, so one digit gives a circle. More digits widen the container into a stadium.
- The container is always fully rounded. This is a fixed geometry, not a theme value: a badge never follows `{rounded.control}`.
- A `dot` is a circle of the dot diameter. It has no padding and no content.
- The value is centered in the container.
- The badge is anchored to the top-end corner of its host, centered on that corner. A round host may need a small adjustment, which belongs to the layout.
- A badge never changes the size or the layout of its host.

## States

### Interactive states

None: a badge is never interactive and never focusable.

### State properties

None. A `count` of 0 is not rendered; the host is shown alone.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). A badge has no border. Content is the value; a `dot` has no content.

### `primary`

| Part | Fill | Content |
|---|---|---|
| `container` | `{colors.primary}` | `{colors.on-primary}` |

### `danger`

| Part | Fill | Content |
|---|---|---|
| `container` | `{colors.danger}` | `{colors.on-danger}` |

### `neutral`

| Part | Fill | Content |
|---|---|---|
| `container` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

The badge is at `level-0`: its host carries the depth.

## Token contract

The theme must define every token below. The badge adds no token: every color is reused from the button and the chip.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the contrast check of `dot` shapes |
| `colors.primary` | `primary` container |
| `colors.on-primary` | `primary` value |
| `colors.danger` | `danger` container |
| `colors.on-danger` | `danger` value |
| `colors.neutral-subtle-pressed` | `neutral` container. Default: neutral step `200` |
| `colors.on-surface` | `neutral` value |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Value for `s` |
| `typography.label-md` | Value for `m` |

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-sm` | Count height for `s` |
| `spacing.icon-md` | Count height for `m` |
| `spacing.xs` | Count padding inline |
| `spacing.sm` | Dot diameter for `s` |
| `spacing.md` | Dot diameter for `m` |

### Components entries (contrast checks)

One entry per variant, using only the standard `backgroundColor` and `textColor` properties. The badge has no interactive state, so the entries have no state suffix. The `primary` and `danger` fills are checked against `{colors.surface}` by the State colors rule of `docs/conventions.md`, which makes the `dot` shape visible.

| Entry | backgroundColor | textColor |
|---|---|---|
| `badge-primary` | `{colors.primary}` | `{colors.on-primary}` |
| `badge-danger` | `{colors.danger}` | `{colors.on-danger}` |
| `badge-neutral` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

### Non-token requirement

The badge has no icon and no elevation.

## Accessibility

| Topic | Requirement |
|---|---|
| Role | None of its own: a badge is not interactive and has no landmark role. |
| Accessible text | `label` says what the badge means ("3 unread messages"). It is exposed as text attached to the host, for example in its accessible name or description. The visible digits are hidden from assistive technologies so that the number is not read twice. |
| `dot` | Has no visible text, so `label` is the only way to know about it. A `dot` without `label` is not allowed. |
| Not by color alone | The meaning is carried by the number or by `label`, never by the color of the badge alone (WCAG 1.4.1). |
| Updates | A change of `value` is announced politely (a polite live region) when the host is on screen and the change matters to the user. |
| Focus | Never focusable; the host follows its own spec. |
| Target size | Not applicable: not interactive. |
| Contrast | The value reaches at least 4.5:1 against its container. Delegated to the DESIGN.md lint through the `components` entries of the Token contract. |

## Behavior

- Overflow: a `value` above `max` shows `max` followed by "+" ("99+"). `label` keeps the real number.
- A `count` of 0 is not rendered. A badge appears and disappears with its host.
- The badge stays inside the host's hit area: it never intercepts pointer events meant for the host.
- Value: single line, no wrap, no truncation.

## Do and don't

| Do | Don't |
|---|---|
| Attach the badge to the element it describes | Place a badge alone |
| Give `label`: "3 unread messages" | Leave the number as the only information |
| Use `dot` when the number does not matter | Show a large number that nobody can act on |
| Use `danger` for something that needs action | Use `danger` for plain information |
| Use a chip for an action or a filter | Make a badge clickable |

## Out of scope

Text badges (status, category), interactive badges, animations, dark mode, outline around the badge to separate it from the host, badges on a colored or image host (contrast is checked only against `{colors.surface}`, so the user retouches the colors after generation), and the exact placement on round hosts are not covered by this spec.
