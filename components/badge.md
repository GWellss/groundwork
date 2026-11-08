# Badge

A badge is a small, static indicator. It is either a count or a dot attached to another element (an icon, a tab, an avatar) to signal that something is new or pending, or a short text that states a status ("Paid", "Draft", "-7%"). This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

A badge is not a chip. A badge is never interactive. A chip is an interactive control with a text label. A static data tag ("PDF 262 KB") belongs to the same static family: use a `neutral` status badge for it.

The text form is named the **status badge** in this kit. Use that name in code and in conversation, so that it is never confused with a chip.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `value` |
| Types | `count` (number in the container), `dot` (no content), `status` (short text, autonomous) |
| Variants | `primary`, `danger`, `neutral`; `status` also `success`, `warning` |
| Sizes | `s`, `m` |
| Interactive states | none (never interactive) |
| State properties | none |

## Purpose

- Use a `count` badge to show a number of unread, new, or pending items on the element they belong to ("3" on an inbox icon).
- Use a `dot` badge to signal that something is new or needs attention when the number does not matter.
- Use a `status` badge (the status badge) to state a status or an update in a short static text, next to the content it qualifies or in a table cell ("Paid", "Draft", "New", "-7%"). It stands on its own: it does not need a host.
- Use a `neutral` status badge for a static data tag that only informs ("PDF 262 KB").
- Use `danger` for items that need action or signal an error, `primary` for new or unread items, `neutral` for a quiet count or tag.
- Do not use a badge for an action, a filter, a choice, or a removable value: use a chip. If the user can interact with it, it is not a badge.
- Do not use a `count` or `dot` badge alone, away from the element it describes.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | The filled shape; a circle for one digit and for `dot`, a stadium for more digits; a rounded rectangle for `status` | yes | Always present |
| `value` | The number, or the text of a `status` badge | `count` and `status` | Absent in `dot` |

The host is the element a `count` or `dot` badge is attached to. It is not a part of the badge. A `status` badge has no host.

### Configurations

| Configuration | Type | `value` | Variants | Status |
|---|---|---|---|---|
| count | `count` | yes | `primary`, `danger`, `neutral` | allowed |
| dot | `dot` | no | `primary`, `danger` | allowed |
| dot-neutral | `dot` | no | `neutral` | forbidden |
| status | `status` | yes, text | `primary`, `danger`, `success`, `warning`, `neutral` | allowed |
| count-text | `count` | text, not a number | any | avoid |
| status-empty | `status` | no | any | forbidden |
| standalone-count | `count` or `dot` | any | any | avoid |

Combination rules:

- In a `count`, `value` is a whole number. A text in a `count` is `avoid`: the count shape is made for digits, so use a `status` badge.
- In a `status`, `value` is a short text, a word or two, on one line. No icon, no remove button, no number-only content (use `count`). A `status` with no text is `forbidden`: nothing is announced.
- The `neutral` variant has no `dot`: a neutral `dot` is `forbidden`, because its fill is too close to the surface to reach the 3:1 contrast of a shape without text (WCAG 1.4.11).
- A `count` or `dot` badge is attached to a host. One alone is `avoid`: a number or a dot means nothing without the element it describes. Attach it to its host, or use a `status` badge with a text. A `status` badge never has a host.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `type` | `count`, `dot`, `status` | `count` | Number, dot, or status text |
| `value` | whole number, 0 or more (`count`); short text (`status`) | none, required for `count` and `status` | The number or the text shown |
| `max` | whole number, 1 or more | 99 | `count` only: highest number shown; above it the badge shows `max` followed by "+" |
| `variant` | `primary`, `danger`, `success`, `warning`, `neutral` | `primary` | Color group; `success` and `warning` only with `type` `status` |
| `size` | `s`, `m` | `m` | Named dimension set |
| `label` | text | none, required for `count` and `dot` | Accessible text that says what the number or dot means ("3 unread messages"). Not used by `status`: its text is the accessible text |

## Variants

| Variant | Container | Content | Intent |
|---|---|---|---|
| `primary` | solid brand | white | New or unread items |
| `danger` | solid danger | white | Items that need action, or an error |
| `success` | solid success | white | `status` only: a completed or positive status |
| `warning` | solid warning | white | `status` only: a status that needs attention soon |
| `neutral` | light neutral | dark neutral | A quiet count, or a data tag, that must not draw attention |

For `status`, the same three variants apply, plus `success` for a completed or positive status ("Paid") and `warning` for a status that needs attention soon ("Expiring"). `primary` is for a new or active status ("New"), `danger` for a status that needs action or an error ("Overdue"), `neutral` for a quiet status or tag ("Draft", "PDF 262 KB"). `success` and `warning` exist only for `status`: `count` and `dot` use `primary`, `danger` or `neutral`.

## Sizes

### Decision

Two sizes. `s` suits small hosts (a 20 px icon) and dense text, `m` the usual hosts. The height of a `count` badge reuses an icon size token, and the dot reuses a spacing token, so density applies to badges without new tokens. A `status` badge is taller than a `count` badge because it carries text, and always smaller than the smallest chip, so the two never look alike.

### Size table

| Size | Count height | Count padding inline | Dot diameter | Value typography |
|---|---|---|---|---|
| `s` | `{spacing.icon-sm}` | `{spacing.xs}` | `{spacing.sm}` | `{typography.label-sm}` |
| `m` | `{spacing.icon-md}` | `{spacing.xs}` | `{spacing.md}` | `{typography.label-md}` |

| Size | Status height | Status padding inline | Status typography |
|---|---|---|---|
| `s` | `{spacing.icon-md}` | `{spacing.sm}` | `{typography.label-sm}` |
| `m` | `{spacing.icon-lg}` | `{spacing.sm}` | `{typography.label-md}` |

Geometry rules:

- A `count` badge has a fixed height. Its minimum width equals its height, so one digit gives a circle. More digits widen the container into a stadium.
- The container of `count` and `dot` is always fully rounded. This is a fixed geometry, not a theme value: they never follow `{rounded.control}`.
- A `status` badge has a fixed height and no minimum width. Its radius is `{rounded.overlay}`: never a stadium, whatever the corner style, and never the chip radius `{rounded.control}`. Together with its smaller height, no border, and no icon, this keeps it visibly different from a chip, including in a theme with pill corners.
- The `status` text is centered, on one line, never wrapped or truncated.
- A `dot` is a circle of the dot diameter. It has no padding and no content.
- The value is centered in the container.
- A `count` or `dot` badge is anchored to the top-end corner of its host, centered on that corner. A round host may need a small adjustment, which belongs to the layout.
- A `count` or `dot` badge never changes the size or the layout of its host, with one exception: in a tab the badge sits in the flow after the label (see `components/tabs.md`). A `status` badge sits in the flow, aligned on the text baseline of its neighbor.

## States

### Interactive states

None: a badge is never interactive and never focusable. This holds for the `status` badge too: no `hover`, `pressed`, or `focus` appearance, no pointer cursor, no button-like look. This is what separates it from a chip.

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

### `success`

| Part | Fill | Content |
|---|---|---|
| `container` | `{colors.success}` | `{colors.on-success}` |

### `warning`

| Part | Fill | Content |
|---|---|---|
| `container` | `{colors.warning}` | `{colors.on-warning}` |

### `neutral`

| Part | Fill | Content |
|---|---|---|
| `container` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

The `status` badge uses the same fills and contents as the `count` badge, variant by variant, plus the two variants above. It has no border.

The badge is at `level-0`: its host carries the depth.

## Token contract

The theme must define every token below. The `success` and `warning` colors are new; every other color is reused from the button and the chip, and the `status` badge reuses the same colors and the same `components` entries as the `count` badge.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the contrast check of `dot` shapes |
| `colors.primary` | `primary` container |
| `colors.on-primary` | `primary` value |
| `colors.danger` | `danger` container |
| `colors.on-danger` | `danger` value |
| `colors.success` | `success` container (`status` only) |
| `colors.on-success` | `success` value |
| `colors.warning` | `warning` container (`status` only) |
| `colors.on-warning` | `warning` value |
| `colors.neutral-subtle-pressed` | `neutral` container. Default: neutral step `200` |
| `colors.on-surface` | `neutral` value |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Value for `s` |
| `typography.label-md` | Value for `m` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | `status` container radius |

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-sm` | Count height for `s` |
| `spacing.icon-md` | Count height for `m`; status height for `s` |
| `spacing.icon-lg` | Status height for `m` |
| `spacing.xs` | Count padding inline |
| `spacing.sm` | Dot diameter for `s`; status padding inline |
| `spacing.md` | Dot diameter for `m` |

### Components entries (contrast checks)

One entry per variant, shared by `count`, `dot`, and `status` (`success` and `warning` serve `status` only), using only the standard `backgroundColor` and `textColor` properties. The badge has no interactive state, so the entries have no state suffix. The `primary`, `danger`, `success` and `warning` fills are checked against `{colors.surface}` by the State colors rule of `docs/conventions.md`, which makes the `dot` shape visible.

| Entry | backgroundColor | textColor |
|---|---|---|
| `badge-primary` | `{colors.primary}` | `{colors.on-primary}` |
| `badge-danger` | `{colors.danger}` | `{colors.on-danger}` |
| `badge-success` | `{colors.success}` | `{colors.on-success}` |
| `badge-warning` | `{colors.warning}` | `{colors.on-warning}` |
| `badge-neutral` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

### Non-token requirement

The badge has no icon and no elevation.

## Accessibility

| Topic | Requirement |
|---|---|
| Role | None of its own: a badge is not interactive and has no landmark role. |
| Accessible text | `count` and `dot`: `label` says what the badge means ("3 unread messages"). It is exposed as text attached to the host, for example in its accessible name or description. The visible digits are hidden from assistive technologies so that the number is not read twice. `status`: the visible text is the accessible text, in reading order next to what it qualifies; it is not hidden and has no `label`. |
| `dot` | Has no visible text, so `label` is the only way to know about it. A `dot` without `label` is `forbidden`. |
| Not by color alone | The meaning is carried by the number, the text, or `label`, never by the color of the badge alone (WCAG 1.4.1). A `danger` status says what is wrong in its text. |
| Updates | A change of `value` is announced politely (a polite live region) when the host or the badge is on screen and the change matters to the user. |
| Focus | Never focusable; the host follows its own spec. |
| Target size | Not applicable: not interactive. |
| Contrast | The value (number or status text) reaches at least 4.5:1 against its container. Delegated to the DESIGN.md lint through the `components` entries of the Token contract. |

## Behavior

- Overflow: a `value` above `max` shows `max` followed by "+" ("99+"). `label` keeps the real number.
- A `count` of 0 is not rendered. A `count` or `dot` badge appears and disappears with its host.
- A `count` or `dot` badge stays inside the host's hit area: it never intercepts pointer events meant for the host. A `status` badge is not part of any hit area: clicking it does nothing.
- Value: single line, no wrap, no truncation. A `status` text that is too long is shortened by the author, never cut by the badge.

## Do and don't

| Do | Don't |
|---|---|
| Attach the badge to the element it describes | Place a badge alone |
| Give `label`: "3 unread messages" | Leave the number as the only information |
| Use `dot` when the number does not matter | Show a large number that nobody can act on |
| Use `danger` for something that needs action | Use `danger` for plain information |
| Use a chip for an action or a filter | Make a badge clickable |
| Name the text form "status badge" and keep it short ("Paid") | Give a `status` badge a hover or pressed look, a border, or an icon |
| Put the status next to the content it qualifies | Rely on the badge color alone to say "paid" or "late" |

## Out of scope

Interactive badges, animations, `success` and `warning` on `count` and `dot` badges, other semantic roles (info), light (tonal) status badges, icons inside a status badge, multi-line status text, outline around the badge to separate it from the host, badges on a colored or image host (contrast is checked only against `{colors.surface}`, so the user retouches the colors after generation), and the exact placement on round hosts are not covered by this spec.
