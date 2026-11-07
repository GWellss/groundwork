# Switch

A switch turns one setting on or off and the change takes effect at once, with a visible label and optional help. It is built on the checkbox: it keeps its row, label, help, interactive states, and most tokens, and this spec states what changes. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Base | `components/checkbox.md`, read first; everything not stated here is unchanged |
| Parts | `choice`, `control` (the track), `thumb`, `label`, `helper-text` |
| Configurations | alone, with or without helper text; in a group: out of scope |
| Selection | `off`, `on`; no indeterminate |
| Variants | none by emphasis; two appearance groups: `off` and `on` |
| Sizes | `s`, `m` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `checked` (on), `disabled`; no `error` |

## Purpose

- Use a switch for a setting that applies as soon as the user flips it: "Notifications", "Airplane mode", "Dark appearance".
- Do not use a switch for an option that is applied when a form is submitted: use a checkbox (see `components/checkbox.md`). The test: if the user must press a button afterwards for the change to count, it is a checkbox.
- Do not use a switch for several choices or for exclusive choices: use checkboxes or radio buttons.
- Do not use a switch for an action ("Send"): use a button.

## Anatomy

### Parts

Parts inherited unchanged from the checkbox: `choice`, `label`, `helper-text`.

| Part | Role | Required | Notes |
|---|---|---|---|
| `control` | The track: a stadium-shaped bar that carries fill and border | yes | Fixed shape, whatever `{rounded.control}` is |
| `thumb` | Circle that slides inside `control`; its position shows the state | yes | At the start when off, at the end when on (mirrored in right-to-left layouts) |
| `label` | Names the setting, always visible, after `control` | yes | Part of the click target; provides the accessible name |

The checkbox parts `check-icon`, `indeterminate-icon`, `required-marker`, `error-icon`, `error-message`, `group`, and `legend` do not exist in the switch.

### Configurations

| Configuration | Elements | Status |
|---|---|---|
| alone | `choice` | allowed |
| alone-with-help | `choice`, `helper-text` under it | allowed |
| group | several switches in a `fieldset` | out-of-scope |
| no-label | any | forbidden |
| indeterminate | a mixed state | forbidden |
| error | `error-message` | out-of-scope |

Combination rules:

- A switch always has a visible `label`; one with no label is `forbidden`. It is stated as the setting, not as the action ("Notifications", not "Turn on notifications").
- A mixed state is `forbidden`: the `switch` role has no mixed state in ARIA.
- A list of switches (a settings page) is a layout of independent switches; it carries no group semantics and no group help.
- The state is carried by the position of the thumb and by the fill, never by color alone.

## Properties

The properties `label`, `helper-text`, `size`, and `disabled` are those of the checkbox, unchanged.

| Property | Values | Default | Description |
|---|---|---|---|
| `checked` | `true`, `false` | `false` | The setting is on |

`indeterminate`, `error-message`, and `required` of the checkbox do not exist: a switch has no mixed state, its value is never validated on submit, and it is never mandatory.

## Variants

None by emphasis. Two appearance groups, used as names in the `components` entries and in Token mapping.

| Variant | Used by | Track | Intent |
|---|---|---|---|
| `off` | `checked` false | No fill, `{colors.outline}` border | An empty track with a visible boundary at 3:1 or more |
| `on` | `checked` true | `{colors.primary}` fill, no border | The setting is on; fill plus thumb at the end |

## Sizes

### Decision

Two sizes, as the checkbox. The track height reuses the icon tokens and its width the control tokens, which gives a 2 to 1 track at every density; the thumb is inset by a spacing token. The row, the gap, and the label typography are those of the checkbox.

### Size table

| Size | Track height | Track width | Thumb inset |
|---|---|---|---|
| `s` | `{spacing.icon-md}` | `{spacing.control-md}` | `{spacing.xs}` |
| `m` | `{spacing.icon-lg}` | `{spacing.control-lg}` | `{spacing.xs}` |

Geometry rules:

- The track size is its outer size, border included. The border is always reserved (`{spacing.border-width}`), so no state moves the content.
- The thumb is a circle whose diameter is the track height minus twice the thumb inset, centered vertically, with the inset between it and the track edge at both ends. Its diameter is the same off and on: it does not grow on press.
- Row minimum height, gap, alignment on the first line of `label`, and label typography are those of the checkbox, for the same size name.
- Moving the thumb is an animation of the project; this spec defines the two end positions only.

## States

The interactive states are those of the checkbox, unchanged: `hover` and `pressed` apply to `choice`, `focus` adds the ring around `control` only (the ring follows the stadium shape).

State properties:

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `checked` | None; the switch stays interactive | `on` group; `thumb` at the end |
| `disabled` | No hover, no pressed, not focusable, not changeable | Disabled tokens; label and helper text included |

Precedence: `disabled` overrides `checked`; interactive states apply on top of the resulting group. There is no `error`: the effect is immediate, so there is no value to validate on submit. When the change fails (a network error, for example), the project returns the switch to its previous position and says so outside the switch.

## Token mapping

Cell vocabulary: a token reference, or `none`. The text parts and the focus ring are those of the checkbox, unchanged (`helper-text` sits under the row, on `{colors.surface}`).

### `off`

| State | Track fill | Track border | Thumb |
|---|---|---|---|
| `enabled` | `none` | `{colors.outline}` | `{colors.outline}` |
| `hover` | `none` | `{colors.on-surface}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.on-surface}` |

### `on`

| State | Track fill | Track border | Thumb |
|---|---|---|---|
| `enabled` | `{colors.primary}` | `none` | `{colors.on-primary}` |
| `hover` | `{colors.primary-hover}` | `none` | `{colors.on-primary}` |
| `pressed` | `{colors.primary-pressed}` | `none` | `{colors.on-primary}` |

### `disabled`

| Part | Token |
|---|---|
| Track fill, `off` | `none` |
| Track fill, `on` | `{colors.disabled-container}` |
| Track border | `{colors.on-disabled}` |
| `thumb` | `{colors.on-disabled}` |
| `label`, `helper-text` | `{colors.on-disabled}` |

## Token contract

The switch reuses the colors, typography, and focus ring tokens of the checkbox and adds no token. `rounded.control` is not used. The tokens used by the track and the thumb are:

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-md` | Track height for `s` |
| `spacing.icon-lg` | Track height for `m` |
| `spacing.control-md` | Track width for `s` |
| `spacing.control-lg` | Track width for `m` |
| `spacing.xs` | Thumb inset |

The other spacing tokens (`control-xs`, `control-sm`, `sm`, `border-width`, `focus-ring-width`, `focus-ring-offset`) are those of the checkbox. The checkbox `spacing.icon-sm` and `spacing.icon-md` for the control size are not used by the switch.

### Components entries (contrast checks)

The text entries are those of the checkbox, unchanged. The thumb on the `on` track adds one entry per state, using only the standard `backgroundColor` and `textColor` properties.

| Entry | backgroundColor | textColor |
|---|---|---|
| `switch-on` | `{colors.primary}` | `{colors.on-primary}` |
| `switch-on-hover` | `{colors.primary-hover}` | `{colors.on-primary}` |
| `switch-on-pressed` | `{colors.primary-pressed}` | `{colors.on-primary}` |

### Non-token requirement

The `off` track border and the `off` thumb are `colors.outline`, which reaches 3:1 against `colors.surface` (WCAG 1.4.11): the theme script already checks it (row `outline`, see `docs/conventions.md`); no new check is needed. The `on` track is `{colors.primary}`, at 4.5:1 or more against the surface by the State colors rule. The switch has no icon and no elevation (`level-0`).

## Accessibility

Everything in the checkbox Accessibility table applies, except the rows about group, indeterminate, invalid, and required. What changes or is added:

| Topic | Requirement |
|---|---|
| Role | A native `input` of type `checkbox` with `role="switch"`: assistive technologies announce "switch, on" or "off". No custom widget. |
| Accessible name | The visible `label`, associated natively; a click on the label toggles the switch. The name does not change with the state ("Notifications", never "Notifications on"). |
| Keyboard | `Tab` moves focus to the switch. `Space` toggles it. |
| State not by color alone | The position of the thumb (start or end) carries the state besides the fill (WCAG 1.4.1). |
| Target size | The click target is `choice` (track, gap, label), at least 24 by 24 CSS pixels, as the checkbox. |
| Contrast | Text as the checkbox; the thumb on the `on` track by the three `switch-on*` entries; the `off` border and thumb at 3:1 by the theme script. `disabled` is exempt. |

## Behavior

- Immediate effect: activating `choice` flips `checked` and applies the setting at once. The component emits a change event; there is no submit step.
- Failure: if the project cannot apply the change, it puts the switch back and announces the failure; the switch itself has no error state.
- Label: wraps if needed; it is never truncated.
- Several switches in a list are independent: changing one never changes another.

## Do and don't

| Do | Don't |
|---|---|
| Use a switch only when the change applies at once | Use a switch in a form that needs a submit button |
| Name the setting ("Notifications") | Name the action ("Turn on notifications") |
| Keep the label the same whatever the state | Change the label when the state changes |
| Use a checkbox for an option sent with a form | Use a switch to accept terms |
| Put the failure message outside the switch and return it to its previous position | Leave a switch that shows a state that was not applied |

## Out of scope

Animations (the thumb movement included), dark mode, icons inside the thumb, a label placed before the track (a layout choice), switches in a group, an error state, and a loading state are not covered by this spec.
