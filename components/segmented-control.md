# Segmented control

A segmented control is a row of two to five connected segments where exactly one is selected, and selecting it applies at once. It switches a view, a filter, or a mode of the same content. It reuses the look of the chip (`components/chip.md`, read first for the colors) and the behavior of a radio group (`components/radio.md`). This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `group`, `segment`, `label`, `leading-icon`, `check-icon`, `divider` |
| Configurations | label only, leading icon + label; two to five segments |
| Selection | single, always one segment selected |
| Variants | none by emphasis; two appearance groups, those of the chip: `default` and `selected` |
| Sizes | `s`, `m` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `selected` (derived from the group `value`), `disabled` (segment or group) |

## Purpose

- Use a segmented control to switch between two to five exclusive options that all fit in one row and that change at once the way the same content is shown: a view ("List", "Grid"), a period ("Day", "Week", "Month"), a filter ("All", "Unread").
- Use `tabs` when each option reveals a different panel of content, not another view of the same content (see `components/tabs.md`).
- Use radio buttons when the choice is part of a form sent later with a submit button, when options need a description, or when there are more than five (see `components/radio.md`).
- Use selectable chips when several options may be on at once, or when the options wrap over several lines (see `components/chip.md`).
- Use a switch for a single on and off setting (see `components/switch.md`).
- Do not use a segmented control to navigate between pages: use links.
- Do not use it for a long list or for options with long labels: use a select or a menu.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `group` | Holds the segments; carries the border and the radius, clips the segments to its shape | yes | Always present |
| `segment` | One option: a selectable area with its content | yes | Two to five |
| `label` | Text of the option | yes | Always visible; gives the accessible name of the segment |
| `leading-icon` | Icon before the label | no | Decorative |
| `check-icon` | Checkmark before the label | when selected | Replaces `leading-icon` while the segment is selected |
| `divider` | Vertical line between two neighboring segments | yes | A `strong` vertical divider (see `components/divider.md`); between segments only, never at the ends |

### Configurations

| Configuration | Elements of a segment | Status |
|---|---|---|
| label-only | `label` | allowed |
| leading-icon-label | `leading-icon`, `label` | allowed |
| icon-only | `leading-icon` | out-of-scope |
| mixed | some segments with an icon, some without | avoid |
| fewer-than-two | one segment | avoid |
| more-than-five | six segments or more | out-of-scope |
| no-selection | no segment selected | avoid |
| multiple-selection | several segments selected | out-of-scope |

Combination rules:

- A segment always has a visible `label`. Icon-only segments are `out-of-scope`: the selected segment shows `check-icon` in place of its icon, so an icon alone would lose its meaning exactly when it is selected.
- Either every segment has a `leading-icon` or none does, so the segments keep the same look. A mix is `avoid`: put an icon on every segment, or on none.
- Fewer than two segments is `avoid`: there is no choice to make. More than five segments is `out-of-scope`: use a select or a menu.
- Exactly one segment is selected at any time. The user cannot deselect it. The group always has a `value`. No selection is `avoid`: the control would not show the current view; set `value`.
- Selecting a segment deselects the previous one. A multi-selection control is `out-of-scope`: use selectable chips or a checkbox group.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` (group) | text | none, required | Accessible name of the group ("View"); it may be visually hidden |
| `value` (group) | the `value` of a segment | the first enabled segment | The selected segment; never empty |
| `size` | `s`, `m` | `m` | Named dimension set, shared by the group |
| `disabled` (group) | `true`, `false` | `false` | No segment can be selected or focused |
| `value` (segment) | text | none, required | Identity of the segment inside its group; unique |
| `label` (segment) | text | none, required | Text of the option; accessible name |
| `leading-icon` (segment) | icon reference | none | Optional icon before the label; all or none |
| `disabled` (segment) | `true`, `false` | `false` | This segment cannot be selected or focused |

## Variants

The segmented control has no emphasis variants. Its segments use the two appearance groups of the chip, as variant names.

| Variant | Used by | Container | Intent |
|---|---|---|---|
| `default` | a segment that is not selected | none | Neutral look, neutral feedback on hover and pressed |
| `selected` | the selected segment | soft fill | The option is on: fill plus `check-icon` |

## Sizes

### Decision

Two sizes, the dimensions of the `s` and `m` buttons, so a segmented control sits next to a button of the same size without a difference in height.

### Size table

| Size | Height | Padding inline | Gap | Icon size | Label typography |
|---|---|---|---|---|---|
| `s` | `{spacing.control-sm}` | `{spacing.md}` | `{spacing.xs}` | `{spacing.icon-sm}` | `{typography.label-sm}` |
| `m` | `{spacing.control-md}` | `{spacing.lg}` | `{spacing.sm}` | `{spacing.icon-md}` | `{typography.label-md}` |

Geometry rules:

- Height is the outer height of `group`, border included. Segments fill the inside of the border; content is centered vertically, with no vertical padding.
- `group` radius is `{rounded.control}` for every size. The segments are clipped to it; they have no radius of their own.
- All segments have the same width: the width of the widest segment, measured as if it were selected (with `check-icon`, or with `check-icon` added before its label when it has no icon). Selecting a segment therefore never moves or resizes anything.
- `check-icon` replaces `leading-icon` in the same slot, at the same size. Without `leading-icon`, the check is added before the label, with the gap.
- `divider` thickness is `{spacing.border-width}`; the group border has the same width.
- Icons inherit the content color of the current group and state.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens of the variant |
| `hover` | Pointer over the segment | Hover container token of the variant |
| `focus` | Keyboard focus (focus visible) on the segment | Adds the focus ring inside the segment; never changes container, content, or border |
| `pressed` | Pointer down or key held on the segment | Pressed container token of the variant |

`focus` combines with `hover` and `pressed`. The ring is drawn inside the segment, not outside, because `group` clips what lies beyond its border.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `selected` (derived from the group `value`) | None; the selected segment stays focusable | `selected` tokens, `check-icon` shown |
| `disabled` (segment) | No hover, no pressed, not focusable, not selectable | Disabled tokens on that segment |
| `disabled` (group) | As above for every segment | Disabled tokens, border and dividers included |

Precedence: `disabled` overrides `selected`, which overrides `default`; interactive states apply on top of the resulting variant. A selected segment keeps its `check-icon` when disabled.

## Token mapping

The colors are those of the chip: the `default` and `selected` tables of `components/chip.md` apply to a segment, with `container` as the segment fill. Only the group edge is specific.

Cell vocabulary: a token reference, or `none`.

### `default` segment

| State | Container | Content |
|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `disabled` | `none` | `{colors.on-disabled}` |

### `selected` segment

| State | Container | Content |
|---|---|---|
| `enabled` | `{colors.primary-container}` | `{colors.on-primary-container}` |
| `hover` | `{colors.primary-container-hover}` | `{colors.on-primary-container}` |
| `pressed` | `{colors.primary-container-pressed}` | `{colors.on-primary-container}` |
| `disabled` | `{colors.disabled-container}` | `{colors.on-disabled}` |

### Group edge

| State | Border of `group` | `divider` |
|---|---|---|
| `enabled` | `{colors.outline}` | `{colors.outline}` |
| `disabled` (group) | `{colors.disabled-container}` | `{colors.disabled-container}` |

Border and dividers are not affected by hover, focus, or pressed. A disabled segment inside an enabled group keeps the enabled edge.

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `none` (drawn inside the segment) |

The ring reaches 3:1 against both the `default` and the `selected` containers: `{colors.focus-ring}` is the brand `default` step (4.5:1 or more against the surface), and the container of the selected segment is a light step.

## Token contract

The segmented control adds no token. It uses the tokens of the chip and of the button sizes.

### Colors

| Token | Role |
|---|---|
| `colors.on-surface` | `default` content |
| `colors.neutral-subtle-hover` | `default` hover fill |
| `colors.neutral-subtle-pressed` | `default` pressed fill |
| `colors.primary-container`, `colors.primary-container-hover`, `colors.primary-container-pressed` | `selected` fill by state |
| `colors.on-primary-container` | `selected` content |
| `colors.outline` | Border of `group` and `divider` |
| `colors.disabled-container`, `colors.on-disabled` | Disabled fill, border, dividers, and content |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Label for `s` |
| `typography.label-md` | Label for `m` |

### Rounded

| Token | Role |
|---|---|
| `rounded.control` | Radius of `group` |

### Spacing

| Token | Role |
|---|---|
| `spacing.control-sm` | Height for `s` |
| `spacing.control-md` | Height for `m` |
| `spacing.icon-sm` | Icon size for `s` |
| `spacing.icon-md` | Icon size for `m` |
| `spacing.xs` | Gap for `s` |
| `spacing.sm` | Gap for `m` |
| `spacing.md` | Padding inline for `s` |
| `spacing.lg` | Padding inline for `m` |
| `spacing.border-width` | Border of `group`, `divider` thickness |
| `spacing.focus-ring-width` | Focus ring width |

### Components entries (contrast checks)

The segmented control declares no entry of its own: its text pairs are the `chip-default*` entries for `default` and the `chip-selected*` entries for `selected`, plus `chip-focus-ring`. They are already checked by the theme script and the lint.

### Non-token requirement

The border of `group` and the `divider` lines are `colors.outline`, which reaches 3:1 against `colors.surface` (WCAG 1.4.11): the theme script already checks it (row `outline`, see `docs/conventions.md`); no new check is needed. `check-icon` is the library checkmark (see `## Icons` of DESIGN.md). The segmented control has no elevation (`level-0`).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | One native `input` of type `radio` per segment, all sharing one `name`, in a container with `role="radiogroup"` named by the group `label`. The `label` of each segment is its native label. The inputs are visually hidden but stay focusable. |
| Accessible name | Group: `label`. Segment: its `label` text. |
| Icons | `leading-icon`, `check-icon`, and `divider` are hidden from assistive technologies; the selection is announced by the checked state. |
| Selection not by color alone | `selected` is shown by the fill and by `check-icon` (WCAG 1.4.1). |
| Keyboard | `Tab` moves focus into the group, to the selected segment, or to the first enabled one when the selected one is disabled; a second `Tab` leaves the group. `Arrow` keys (left and up for the previous, right and down for the next) move focus and select the segment, wrapping from the last to the first and the reverse; disabled segments are skipped. `Space` selects the focused segment. |
| Focus visible | The focus ring appears on keyboard focus, inside the segment. It must never be removed. |
| Disabled | Native `disabled` on the input: out of the tab order, not selectable. |
| Target size | The click target is the whole `segment`, at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). It is `{spacing.control-sm}` high or more, and wider than its label. |
| Contrast | Text and icons reach 4.5:1 against their container, delegated to the `chip-*` entries. The border and the dividers reach 3:1, checked by the theme script. `disabled` is exempt. |
| Reduced motion | Any change of fill or of `check-icon` is instant when the user asks for reduced motion (see Motion in `docs/conventions.md`). |

## Behavior

- Selection: activating a segment selects it and deselects the previous one. The effect applies at once; there is no submit button in the pattern.
- Arrow keys select as they move; the project does not delay the selection until `Space`.
- Activating the selected segment does nothing.
- Segments keep the order given by the project; the component never reorders them.
- Label: single line, no wrap. If the width runs out, the label is truncated with an ellipsis; the accessible name keeps the full text. Keep labels to one or two words: a label that does not fit means the options belong in a select.
- Motion: a transition of the fill between segments is the project's choice and is removed under reduced motion.

## Do and don't

| Do | Don't |
|---|---|
| Use it to switch how the same content is shown | Use it to show different content: use tabs |
| Keep two to five short, exclusive options | Put a sixth option, or long labels, in it |
| Preselect the current view or a safe default | Leave it without a selection |
| Name the group ("View") | Leave the group unnamed |
| Use a radio group for a form choice sent on submit | Use a segmented control to collect a form answer |
| Use selectable chips when several options can be on | Allow several segments to be selected |

## Out of scope

Animations (a sliding selection), dark mode, multiple selection, icon-only segments, more than five segments, vertical orientation, a badge or a description inside a segment, a full-width layout rule, and a group that scrolls are not covered by this spec.
