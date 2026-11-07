# Slider

A slider lets the user pick one numeric value, or a minimum and a maximum (range variant), in a bounded range by moving a thumb along a track, with a visible label, the current value, and optional help and error. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `label`, `value-label`, `track`, `fill`, `thumb` (two in the range variant), `helper-text`, `error-icon`, `error-message` |
| Configurations | with or without visible value, with or without helper text; horizontal only |
| Variants | none by emphasis; one appearance, `default`; two value modes: single (one thumb) and `range` (two thumbs) |
| Sizes | `s`, `m` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `disabled`, `error` (derived from `error-message`) |

## Purpose

- Use a slider to choose a value in a bounded range where an approximate position is fine and the exact value matters less than the direction: volume, brightness, a price ceiling.
- Use a text field with `type` number when the user must type an exact value, or the range is very wide (see `components/text-field.md`).
- Do not use a slider for a short list of named options: use radio buttons (see `components/radio.md`).
- Do not use a slider for a progress that the user does not control: use a progress indicator (see `components/progress.md`).
- Use the `range` variant to choose an interval, a minimum and a maximum: a price range, a date-free duration.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `label` | Names the slider, always visible, above the track | yes | Associated with the input; provides the accessible name |
| `value-label` | Shows the current value, at the end of the label line | no | Shown by default; see `show-value` |
| `track` | The full path from `min` to `max` | yes | Always present; the whole slider width |
| `fill` | The part of `track` from `min` up to the thumb; in the `range` variant, only the part between the two thumbs | yes | Its length shows the value |
| `thumb` | Circle the user moves | yes | The control; carries the focus ring. Two in the `range` variant: `thumb-min` and `thumb-max` |
| `helper-text` | Hint under the track | no | Replaced by `error-message` while in error |
| `error-icon` | Icon before `error-message` | with `error-message` | Decorative; the second cue besides color |
| `error-message` | Text that says what is wrong and how to fix it | no | Present exactly when the slider is in error |

### Configurations

| Configuration | Elements | Status |
|---|---|---|
| plain | `label`, `track`, `fill`, `thumb`, `value-label` | allowed |
| no-value-label | the same without `value-label` (`show-value` false) | allowed |
| with-help | any of the above plus `helper-text` or `error-message` | allowed |
| range | `label`, `track`, `fill` between the thumbs, `thumb-min`, `thumb-max`, `value-label` showing both values | allowed |
| vertical | a vertical track | out-of-scope |
| no-label | any | forbidden |
| error-and-disabled | `error-message` with `disabled` | forbidden |

Combination rules:

- A slider always has a visible `label`; one with no label is `forbidden`.
- `error-message` with `disabled` is `forbidden`: a disabled slider leaves the tab order, so its error cannot be reached by keyboard.
- The value is always one number: `min` less than or equal to the value, which is less than or equal to `max`, and a multiple of `step` from `min`. In the `range` variant the value is two numbers, `value-min` and `value-max`, each obeying that rule, with `value-min` at least one `min-gap` below `value-max` (see Range variant).
- An error always shows `error-icon` and `error-message`. Color alone never says "error".
- `error-message` replaces `helper-text` in the same slot.
- `show-value` false is allowed only when the value is shown elsewhere (the project's layout) or meaningless to the user; the accessible value stays.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | Visible name of the slider; accessible name |
| `value` | number from `min` to `max` | `min` | Current value; single only |
| `range` | `true`, `false` | `false` | Two thumbs: a minimum and a maximum |
| `value-min`, `value-max` | numbers from `min` to `max` | `min`, `max` | Current values of the `range` variant |
| `label-min`, `label-max` | text | none, required with `range` | Accessible names of the two thumbs ("Minimum price", "Maximum price"); `label` names the group |
| `min-gap` | number, a multiple of `step`, at least `step` | `step` | Smallest allowed distance between the two thumbs; `range` only |
| `min` | number | `0` | Lowest value |
| `max` | number, greater than `min` | `100` | Highest value |
| `step` | number, greater than 0 | `1` | Increment; the value snaps to it |
| `show-value` | `true`, `false` | `true` | Shows `value-label` (both values in the `range` variant) |
| `value-text` | text | none | Human text of the value ("3 stars", "$20"), shown in `value-label` and read by assistive technologies instead of the bare number; in the `range` variant, one text per thumb (`value-text-min`, `value-text-max`) |
| `helper-text` | text | none | Hint under the track |
| `error-message` | text | none | Non-empty puts the slider in `error` |
| `size` | `s`, `m` | `m` | Named dimension set |
| `disabled` | `true`, `false` | `false` | Not focusable, not changeable, not submitted |

## Variants

The slider has one appearance, `default`: a thin track, a `fill` from the start to the thumb, and a round thumb. Error and disabled are states, not variants.

### Range variant

With `range` true, the slider has two thumbs on one `track`. It keeps every rule, token, size, and state of the single slider; only the following changes.

- Names: `label` names the whole control (for example "Price"). Each thumb has its own accessible name, `label-min` and `label-max` ("Minimum price", "Maximum price"); the two are never the same text.
- No crossing: the thumbs never cross or swap. `thumb-min` never goes above `value-max` less `min-gap`, and `thumb-max` never goes below `value-min` plus `min-gap`; the thumb being moved stops at that limit. `min-gap` is `step` by default, so the two values are never equal.
- Press on the track: the nearest thumb moves to that position and starts the drag. On a tie, the thumb that moves in the direction of the press is the one that moves; when the press is exactly midway between the thumbs, both directions fit and `thumb-min` moves.
- Fill: only the part of `track` between the two thumbs is colored (`fill`); the parts outside stay the `track` color.
- Values: `value-label` shows both values at the end of the label line, minimum first, separated by a dash or a visible "to" ("$20 to $80"), or the two `value-text`.
- Thumb states: `hover`, `pressed`, and `focus` apply to the thumb that is under the pointer, dragged, or focused; `fill` takes the color of the state when either thumb is `hover` or `pressed`. The focus ring surrounds the focused thumb only. When the thumbs are close, the focused or dragged thumb is drawn above the other.
- Geometry: each thumb has the thumb size; the thumb centers travel between the two ends of `track` as for the single thumb. The row, as in the single slider, is the pointer hit area.

## Sizes

### Decision

Two sizes. The thumb reuses icon tokens, the track thickness a spacing token, the row height the control tokens, so density applies without new tokens.

### Size table

| Size | Thumb size | Track thickness | Row height | Label typography |
|---|---|---|---|---|
| `s` | `{spacing.icon-md}` | `{spacing.xs}` | `{spacing.control-xs}` | `{typography.label-sm}` |
| `m` | `{spacing.icon-lg}` | `{spacing.sm}` | `{spacing.control-sm}` | `{typography.label-md}` |

Geometry rules:

- Row height is the height of the interactive row: `track` and `thumb` centered vertically in it. The whole row, over the full slider width, is the pointer hit area: pressing on the track moves the thumb there.
- `track` and `fill` have fully rounded ends and the same thickness; `thumb` is a circle of the thumb size. Both are fixed geometry, not theme values; `{rounded.control}` is not used.
- The thumb center travels between the two ends of `track`; at `min` and `max` the thumb stays inside the slider width (the track starts and ends one thumb radius inside the width).
- `label` and `value-label` sit on one line above the row, `label` at the start and `value-label` at the end, with `{spacing.xs}` between that line and the row. The same typography applies to `label`, `value-label`, `helper-text`, and `error-message`.
- Vertical space between the row and `helper-text` or `error-message` is `{spacing.xs}`.
- `error-icon` uses `{spacing.icon-sm}` at size `s` and `{spacing.icon-md}` at size `m`, before `error-message` with `{spacing.sm}`.
- Width comes from the layout, never from a theme value.
- Text overflow: `label` wraps and `value-label` stays on one line; neither is truncated.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over the row | `fill` and `thumb` get the hover color |
| `focus` | Keyboard focus (focus visible) on the input | Adds the focus ring around `thumb`; never changes fill, thumb, or track |
| `pressed` | Pointer down on the row, kept while the thumb is dragged | `fill` and `thumb` get the pressed color |

`focus` combines with `hover` and `pressed`: the ring is drawn on top of their tokens and follows the thumb. A drag keeps `pressed` until release, even if the pointer leaves the row.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `error` | None. Derived: `error-message` is non-empty | `fill` and every `thumb` in the danger group, `error-icon`, `error-message` |
| `disabled` | No hover, no pressed, not focusable, not changeable | Disabled tokens; label, value, and help included |

Precedence: `disabled` overrides `error`, which overrides the `default` group; interactive states apply on top of the resulting group. `error` is never combined with `disabled` (see Anatomy).

## Token mapping

Cell vocabulary: a token reference, or `none`. The track is never a pair: it reaches 3:1 through `{colors.outline}`.

### `default`

| State | Track | Fill | Thumb |
|---|---|---|---|
| `enabled` | `{colors.outline}` | `{colors.primary}` | `{colors.primary}` |
| `hover` | `{colors.outline}` | `{colors.primary-hover}` | `{colors.primary-hover}` |
| `pressed` | `{colors.outline}` | `{colors.primary-pressed}` | `{colors.primary-pressed}` |

### `error`

| State | Track | Fill | Thumb |
|---|---|---|---|
| `enabled` | `{colors.outline}` | `{colors.danger}` | `{colors.danger}` |
| `hover` | `{colors.outline}` | `{colors.danger-hover}` | `{colors.danger-hover}` |
| `pressed` | `{colors.outline}` | `{colors.danger-pressed}` | `{colors.danger-pressed}` |

`error-icon` and `error-message` use `{colors.danger}` in every state. The `danger` states are darker than `{colors.danger}`, which reaches 4.5:1 against the surface, so no own check is needed.

### `disabled`

| Part | Token |
|---|---|
| `track` | `{colors.disabled-container}` |
| `fill` | `{colors.on-disabled}` |
| `thumb` | `{colors.on-disabled}` |
| `label`, `value-label`, `helper-text` | `{colors.on-disabled}` |

### Text parts

| Part | Token |
|---|---|
| `label`, `value-label` | `{colors.on-surface}` |
| `helper-text` | `{colors.on-surface-muted}` |
| `error-icon`, `error-message` | `{colors.danger}` |

All text sits on `{colors.surface}`: `{colors.on-surface-muted}` is used on the surface only, never on a grayed fill.

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

The ring surrounds `thumb` only, as a circle, not `label` or the track.

## Token contract

The theme must define every token below. The slider adds no token: every one is reused.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of every pair; the surface shows through the slider |
| `colors.on-surface` | `label`, `value-label` |
| `colors.on-surface-muted` | `helper-text`, on the surface only |
| `colors.outline` | `track`; at least 3:1 against `colors.surface` (see Non-token requirement) |
| `colors.primary` | `fill` and `thumb` |
| `colors.primary-hover` | `fill` and `thumb` on hover |
| `colors.primary-pressed` | `fill` and `thumb` on pressed |
| `colors.danger` | `error` `fill` and `thumb`, `error-icon`, `error-message` |
| `colors.danger-hover` | `error` on hover |
| `colors.danger-pressed` | `error` on pressed |
| `colors.disabled-container` | Disabled `track` |
| `colors.on-disabled` | Disabled `fill`, `thumb`, and text |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Label, value, and support text for `s` |
| `typography.label-md` | Label, value, and support text for `m` |

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-sm` | `error-icon` for `s` |
| `spacing.icon-md` | Thumb size for `s`; `error-icon` for `m` |
| `spacing.icon-lg` | Thumb size for `m` |
| `spacing.xs` | Track thickness for `s`; space between the label line, the row, and the support line |
| `spacing.sm` | Track thickness for `m`; gap before `error-message` |
| `spacing.control-xs` | Row height for `s` |
| `spacing.control-sm` | Row height for `m` |
| `spacing.focus-ring-width` | Focus ring width |
| `spacing.focus-ring-offset` | Gap between the thumb and its focus ring |

### Components entries (contrast checks)

The text entries (`checkbox`, `checkbox-muted`, `checkbox-error`, `checkbox-focus-ring`) are those of the checkbox, unchanged. The `fill` and `thumb` have no text, but they are drawn on the surface in the primary color and must stay distinct, each state darker than the previous; they get one entry per state, using only the standard `backgroundColor` and `textColor` properties (fill-less exception of `docs/conventions.md`: the color moves, the background stays the surface).

| Entry | backgroundColor | textColor |
|---|---|---|
| `slider` | `{colors.surface}` | `{colors.primary}` |
| `slider-hover` | `{colors.surface}` | `{colors.primary-hover}` |
| `slider-pressed` | `{colors.surface}` | `{colors.primary-pressed}` |

### Non-token requirement

- Track contrast (WCAG 1.4.11): `track` must reach 3:1 against `{colors.surface}`. It is `colors.outline`, the pair the theme script already checks outside the lint (row `outline` of its report; see `docs/conventions.md`); no new check is needed. `fill` and `thumb` are `{colors.primary}`, at 4.5:1 or more against the surface, covered by the three `slider*` entries. No non-standard property is added to `components`.
- Icon style and library come from the `## Icons` section of DESIGN.md. `error-icon` is the library error glyph.
- The slider has no elevation (`level-0`).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | Native `input` of type `range`, which exposes `role="slider"`, `aria-valuemin`, `aria-valuemax`, and `aria-valuenow` from `min`, `max`, `value`. No custom widget. The `range` variant has two such sliders in one `group` named by `label` (see Range variant). |
| Accessible name | The visible `label`, associated natively. |
| Range thumbs | Each thumb is a slider with its own accessible name (`label-min`, `label-max`) and its own `aria-valuenow`. The bounds exposed to assistive technologies are the real limits of the thumb: `aria-valuemax` of `thumb-min` is `value-max` less `min-gap`, and `aria-valuemin` of `thumb-max` is `value-min` plus `min-gap`. |
| Value text | When `value-text` is set, `aria-valuetext` carries it, so assistive technologies read "3 stars" instead of "3". Without it, the number is read. |
| Description | `helper-text` or `error-message` is referenced by `aria-describedby` on the input. |
| Invalid | `aria-invalid="true"` exactly when `error-message` is present, with the `aria-describedby` link to that message. |
| Not by color alone | The value is shown by the position and length of `fill`, and by `value-label` when shown. An error shows `error-icon` and `error-message` besides the danger color (WCAG 1.4.1). |
| Focus visible | The focus ring appears on `thumb` on keyboard focus. It must never be removed. |
| Keyboard | `Tab` moves focus to the slider (in the `range` variant, to `thumb-min`, then to `thumb-max`; Shift+Tab goes back; the tab order is always minimum then maximum, even when the thumbs are close). `Right` and `Up` increase the value by `step`; `Left` and `Down` decrease it by `step`; `PageUp` and `PageDown` change it by a page step (about a tenth of the range, at least one `step`, a multiple of `step`); `Home` sets `min`; `End` sets `max`. In the `range` variant each thumb follows the same keys, stopping at the no-crossing limit: `Home` on `thumb-max` goes to `value-min` plus `min-gap`, `End` on `thumb-min` goes to `value-max` less `min-gap`. |
| Pointer alternative | Every pointer action (press on the track, drag the thumb) has the keyboard equivalent above, with no path-based gesture required (WCAG 2.5.1, 2.5.7). |
| Disabled | Native `disabled`: out of the tab order, value not submitted. |
| Target size | The hit area is the row, at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8): the row height of every size meets it. 44 by 44 is recommended on touch screens. |
| Contrast | Text reaches 4.5:1 against the surface (entries of the checkbox, checked by the lint). `fill` and `thumb` by the three `slider*` entries. `track` reaches 3:1 against the surface (checked by the theme script). `disabled` is exempt. |

## Behavior

- Pointer: pressing on the row moves the thumb (in the `range` variant, the nearest thumb, see Range variant) to the nearest valid value and starts a drag; dragging follows the pointer; the value snaps to `step`; release ends `pressed`. The value never leaves `min` to `max`.
- Change events: the component emits a change event while the user drags (the project may wait for the release to apply it) and when a key changes the value.
- Value label: `value-label` shows `value-text` when set, otherwise the number; it updates as the value changes. It is part of the visible text and not announced at every change beyond the native slider announcement.
- Validation: the project decides the rules (for example a minimum). Show `error-message` after the user releases the thumb or submits; clear it as soon as the value becomes valid.
- Label: wraps if needed; it is never truncated.
- Initial value: `value` outside `min` to `max` or off `step` is clamped and snapped, never rendered as is.

## Do and don't

| Do | Don't |
|---|---|
| Show the current value next to the label | Make the user guess the value from the thumb position |
| Give `value-text` when the number needs a unit | Leave "20" where the user needs "$20" |
| Choose a `step` that matches the precision the user needs | Use a slider for an exact value with many digits |
| Offer a text field when the exact value matters | Make precision depend on a pointer alone |
| Keep the full keyboard support of the native range | Replace the native input with a custom widget that loses it |
| Give each range thumb its own name ("Minimum price", "Maximum price") | Name both thumbs "Price" |

## Out of scope

Animations, dark mode, vertical sliders, more than two thumbs, tick marks and discrete labels along the track, a value tooltip over the thumb, end labels for `min` and `max`, a centered origin for the fill, and an input field linked to the slider are not covered by this spec.
