# Radio

A radio button lets the user pick exactly one option among a short list of exclusive options. Radio buttons always come in a group. It is built on the checkbox: it keeps its row, label, group, help, error, sizes, and tokens, and this spec only states what changes. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Base | `components/checkbox.md`, read first; everything not stated here is unchanged |
| Parts | those of the checkbox that apply, with `dot` replacing `check-icon`; no `indeterminate-icon` |
| Configurations | always a group (`group`, `legend`, two or more options); never alone |
| Selection | `unselected`, `selected`; one `selected` option at most per group |
| Variants | none by emphasis; two appearance groups: `unselected` and `selected`, as the checkbox |
| Sizes | `s`, `m`, as the checkbox |
| Interactive states | `enabled`, `hover`, `focus`, `pressed`, as the checkbox |
| State properties | `disabled` (option or group), `error` (group, derived from `error-message`) |

## Purpose

- Use radio buttons to choose exactly one option among two to about seven that the user must compare, all visible at once.
- Use a checkbox group when several options may be selected (see `components/checkbox.md`).
- Use a switch for a single on and off setting that applies at once (see `components/switch.md`).
- Use a segmented control instead when the choice applies at once and switches a view or a filter (see `components/segmented-control.md`).
- Do not use radio buttons for a long list: use a select or a menu.
- Do not use a single radio button: a lone option is a checkbox.

## Anatomy

### Parts

Parts inherited unchanged from the checkbox: `choice`, `control`, `label`, `helper-text`, `error-icon`, `error-message`, `group`, `legend`.

| Part | Role | Required | Notes |
|---|---|---|---|
| `control` | The circle: carries fill and border | yes | Always a circle, whatever `{rounded.control}` is |
| `dot` | Filled circle inside `control` | when selected | Decorative; replaces the checkbox `check-icon` |
| `legend` | Visible name of the group | yes | The native `legend` of `group` |

The checkbox parts `check-icon`, `indeterminate-icon`, and `required-marker` do not exist in the radio button (the group `required` is shown in the legend by the project, see Properties).

### Configurations

| Configuration | Elements | Allowed |
|---|---|---|
| group | `group`, `legend`, two or more `choice`, optional group `helper-text` or `error-message` | yes |
| single | one `choice` | no |
| option-help | `helper-text` or `error-message` attached to one option | no |
| no-selection | a group with no option selected | yes |
| indeterminate | a mixed state | no |
| error-and-disabled | `error-message` with `disabled` | no |

Combination rules:

- A radio button is never rendered alone. A group has at least two options and a `legend`.
- At most one option is selected. Selecting one deselects the others; the user cannot deselect the selected option.
- The group may start with no selection (no default). When a safe default exists, select it.
- Help and error belong to the group, once, as in the checkbox group.

## Properties

The properties `label`, `size`, and `disabled` of an option, and `legend`, `helper-text`, `error-message`, `size`, `disabled` of a group, are those of the checkbox, unchanged.

| Property | Values | Default | Description |
|---|---|---|---|
| `value` (group) | the `value` of an option | none | The selected option; absent means no selection |
| `value` (option) | text | none, required | Identity of the option inside its group |
| `required` (group) | `true`, `false` | `false` | A selection is required; the project states it in the legend text or beside it |

The properties `checked` and `indeterminate` of the checkbox do not exist: the selection is the `value` of the group. An option can be `disabled` on its own; the group `disabled` disables every option.

## Variants

None by emphasis. The two appearance groups `unselected` and `selected` are those of the checkbox, with a circle instead of a square.

## Sizes

### Decision

The sizes, row heights, gap, label typography, and spacing are those of the checkbox (`s`, `m`), unchanged. Only the mark has its own size.

### Size table

| Size | Control size | Dot size |
|---|---|---|
| `s` | `{spacing.icon-sm}` | `{spacing.sm}` |
| `m` | `{spacing.icon-md}` | `{spacing.sm}` |

Geometry rules:

- `control` is a circle of the control size, border included; `dot` is a circle centered in it. Both are fixed geometry, not theme values.
- The radius token is not used.
- The rest of the geometry is that of the checkbox: reserved border, row minimum height, alignment on the first line of `label`, gaps, help and error alignment.

## States

The interactive states and the precedence are those of the checkbox, unchanged: `hover` and `pressed` apply to `choice`, `focus` adds the ring around `control` only.

State properties:

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `selected` (derived from the group `value`) | None | `selected` group; `dot` shown |
| `error` | None. Derived: group `error-message` is non-empty | Danger border on every `unselected` control of the group, `error-icon`, `error-message` |
| `disabled` | As the checkbox | Disabled tokens |

## Token mapping

The `unselected`, `error`, text parts, and focus ring tables of the checkbox apply unchanged to `control` and its group. The `selected` table applies with `dot` in place of the mark (the dot color is the mark color), and the `disabled` table with `dot` in place of the mark.

## Token contract

The radio button adds no token: it reuses those of the checkbox. `spacing.sm` also serves as `dot` size.

### Spacing

| Token | Role |
|---|---|
| `spacing.sm` | `dot` size, besides the checkbox roles |

### Components entries (contrast checks)

The text entries are those of the checkbox, unchanged. The dot adds one entry per `selected` state, using only the standard `backgroundColor` and `textColor` properties.

| Entry | backgroundColor | textColor |
|---|---|---|
| `radio-selected` | `{colors.primary}` | `{colors.on-primary}` |
| `radio-selected-hover` | `{colors.primary-hover}` | `{colors.on-primary}` |
| `radio-selected-pressed` | `{colors.primary-pressed}` | `{colors.on-primary}` |

### Non-token requirement

The `unselected` border keeps the 3:1 requirement of the checkbox (`colors.outline` against `colors.surface`, checked by the theme script). The radio button has no icon and no elevation (`level-0`); `error-icon` is the library error glyph, as in the checkbox.

## Accessibility

Everything in the checkbox Accessibility table applies, except the rows about indeterminate and required on a single checkbox. What changes or is added:

| Topic | Requirement |
|---|---|
| Role | Native `input` of type `radio`, all options of a group sharing one `name`. The `fieldset` carries `role="radiogroup"`, with `legend` as its name. |
| Invalid | `aria-invalid="true"` and `aria-describedby` on the `radiogroup` `fieldset`, exactly when the group has an `error-message`. |
| Required | The native `required` attribute on the radio inputs when `required` is true. |
| Keyboard | `Tab` moves focus into the group, to the selected option, or to the first enabled option when none is selected; a second `Tab` leaves the group. `Arrow` keys (left and up for the previous, right and down for the next) move focus and select the option, wrapping from the last to the first and the reverse; disabled options are skipped. `Space` selects the focused option when it is not selected. |
| Not by color alone | The selection is shown by the fill and by `dot` (WCAG 1.4.1). |
| Target size | The click target is `choice`, at least 24 by 24 CSS pixels, as the checkbox. |
| Contrast | As the checkbox for text, plus the three `radio-selected*` entries. The `unselected` border is checked by the theme script. |

## Behavior

- Selection: activating `choice` (the circle or the label) selects the option and deselects the previously selected one. The value is applied when the form is submitted.
- Arrow keys select as they move: the project does not delay the selection until `Space`.
- Validation: as the checkbox. When an error appears after a submit, focus moves to the first option of the group (the selected one if any).
- Options keep the order given by the project; the component never reorders them.
- Label: wraps if needed; it is never truncated.

## Do and don't

| Do | Don't |
|---|---|
| Give the group a visible `legend` | Leave a group of radio buttons unnamed |
| Keep options short and mutually exclusive | Offer options that overlap |
| Preselect a safe default when one exists | Preselect an option the user may not notice |
| Use a select or a menu for a long list | Stack more than about seven radio buttons |
| Use checkboxes when several options can be on | Use radio buttons for independent options |

## Out of scope

Animations, dark mode, radio buttons rendered as cards (for a segmented look, see `components/segmented-control.md`), option descriptions, a deselect action, and a horizontal-wrapping layout rule are not covered by this spec.
