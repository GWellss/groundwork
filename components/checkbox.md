# Checkbox

A checkbox lets the user turn one option on or off, or pick any number of options in a group, with a visible label and optional help and error. It is also the base of the choice controls: `components/radio.md` and `components/switch.md` reuse its row, label, help, error, and group anatomy and state this only once, here. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `choice`, `control`, `check-icon`, `indeterminate-icon`, `label`, `required-marker`, `helper-text`, `error-icon`, `error-message`; for a group: `group`, `legend` |
| Configurations | alone, or in a group (`fieldset` and `legend`); each with or without helper text |
| Selection | `unchecked`, `checked`, `indeterminate` |
| Variants | none by emphasis; two appearance groups: `unselected` and `selected` |
| Sizes | `s`, `m` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `disabled`, `error` (derived from `error-message`) |

## Purpose

- Use a checkbox for an option that is applied when the form is submitted: "I accept the terms", "Send me a copy".
- Use a group of checkboxes when the user may pick zero, one, or several options among a short list.
- Use the `indeterminate` selection only to show that some, not all, of the options it controls are checked (a "select all" parent).
- Do not use a checkbox for a setting that takes effect at once: use a switch (see `components/switch.md`).
- Do not use checkboxes for exactly one choice among exclusive options: use radio buttons (see `components/radio.md`).
- Do not use a checkbox to toggle a filter shown as a tag: use a `selectable` chip (see `components/chip.md`).

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `choice` | Row that holds `control` and `label`; the whole row is the click target | yes | Hover and pressed apply to it; `helper-text` is outside |
| `control` | The box: carries fill, border, and radius | yes | Square; holds the mark when selected |
| `check-icon` | Checkmark inside `control` | when `checked` | The library checkmark; decorative |
| `indeterminate-icon` | Dash inside `control` | when `indeterminate` | The library minus glyph; decorative |
| `label` | Names the option, always visible, after `control` | yes | Part of the click target; provides the accessible name |
| `required-marker` | Shows that the box must be checked | no | Inside `label`; only when `required` is true |
| `helper-text` | Hint under the row | no | Aligned with the start of `label`; replaced by `error-message` while in error |
| `error-icon` | Icon before `error-message` | with `error-message` | Decorative; the second cue besides color |
| `error-message` | Text that says what is wrong and how to fix it | no | Present exactly when the checkbox or the group is in error |
| `group` | Container of the options of a group | for a group | A native `fieldset` |
| `legend` | Visible name of the group | for a group | The native `legend` of `group` |

### Configurations

| Configuration | Elements | Status |
|---|---|---|
| alone | `choice` | allowed |
| alone-with-help | `choice`, `helper-text` or `error-message` under it | allowed |
| group | `group`, `legend`, two or more `choice`, optional `helper-text` or `error-message` under the options | allowed |
| group-option-help | `helper-text` or `error-message` attached to one option of a group | avoid |
| group-without-legend | `group` | forbidden |
| no-visible-label | any, with an accessible name | out-of-scope |
| no-label | any, with no accessible name | forbidden |
| error-and-disabled | `error-message` with `disabled` | forbidden |

Combination rules:

- A checkbox always has a visible `label`. Checkboxes without a visible label (row selection in a table) are `out-of-scope`; one with no accessible name at all is `forbidden`.
- In a group, `helper-text`, `error-icon`, and `error-message` belong to the group and sit once under the last option; the options carry none. `required-marker` is not available in a group. Help or error on one option is `avoid`: the message concerns the whole choice, so a message per option repeats it and moves the layout. Put it in the group's `helper-text` or `error-message`.
- A group without a `legend` is `forbidden`: the group has no accessible name.
- `error-message` with `disabled` is `forbidden`: a disabled checkbox leaves the tab order, so its error cannot be reached by keyboard.
- An error always shows `error-icon` and `error-message`. Color alone never says "error".
- `error-message` replaces `helper-text` in the same slot.
- `indeterminate` is set by the project, never by the user's click: activating an `indeterminate` checkbox makes it `checked`.
- The options of a group are stacked vertically by default; a horizontal arrangement is a layout choice.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | Visible name of the option; accessible name |
| `checked` | `true`, `false` | `false` | The option is on |
| `indeterminate` | `true`, `false` | `false` | Some, not all, of the controlled options are on; wins over `checked` for display |
| `helper-text` | text | none | Hint under the row |
| `error-message` | text | none | Non-empty puts the checkbox in `error` |
| `size` | `s`, `m` | `m` | Named dimension set |
| `required` | `true`, `false` | `false` | The box must be checked; shows `required-marker`; alone only |
| `disabled` | `true`, `false` | `false` | Not focusable, not changeable, not submitted |

A group has its own properties: `legend` (text, required), `helper-text`, `error-message`, `size`, and `disabled` (disables every option). The `size` of a group applies to all its options.

## Variants

The checkbox has no emphasis variants. Its colors come from two appearance groups, used as names in the `components` entries and in Token mapping.

| Variant | Used by | Control | Intent |
|---|---|---|---|
| `unselected` | `unchecked` | No fill, `{colors.outline}` border | An empty box with a visible boundary at 3:1 or more |
| `selected` | `checked` and `indeterminate` | `{colors.primary}` fill, no border | The option is on; fill plus a mark |

## Sizes

### Decision

Two sizes. The control and the mark reuse icon tokens; the row reuses control heights, so density applies without new tokens. The row is never smaller than 24 CSS pixels.

### Size table

| Size | Control size | Row minimum height | Gap | Label typography |
|---|---|---|---|---|
| `s` | `{spacing.icon-sm}` | `{spacing.control-xs}` | `{spacing.sm}` | `{typography.label-sm}` |
| `m` | `{spacing.icon-md}` | `{spacing.control-sm}` | `{spacing.sm}` | `{typography.label-md}` |

Geometry rules:

- Control size is the outer size of `control`, border included. The border is always reserved (`{spacing.border-width}`), so no state moves the content. The mark has the control size.
- Gap separates `control` from `label`. The row is the click target and has no dead zone between them.
- Row minimum height: `control` is centered on the first line of `label`; when `label` wraps, `control` stays aligned with the first line and the row grows.
- Radius is `{rounded.control}`, never more than a quarter of the control size, so a checkbox never looks like a radio button, whatever the corner style.
- Support typography (`helper-text`, `error-message`, `legend`) is the label typography of the size. `helper-text` and `error-message` start at the start of `label` (control size plus gap), in a group at the start of the group.
- Vertical space between the row and `helper-text` or `error-message` is `{spacing.xs}`; between the options of a group `{spacing.xs}`; between `legend` and the first option `{spacing.sm}`.
- `error-icon` uses `{spacing.icon-sm}` at size `s` and `{spacing.icon-md}` at size `m` and sits before `error-message` with the gap.
- Width comes from the layout, never from a theme value.
- Text overflow: `label` wraps; it is never truncated.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens of the group |
| `hover` | Pointer over `choice` (control or label) | `unselected`: the border gets the hover color; `selected`: the fill gets the hover color |
| `focus` | Keyboard focus (focus visible) on the input | Adds the focus ring around `control`; never changes fill, mark, or border |
| `pressed` | Pointer down or key held on `choice` | `unselected`: adds a quiet fill; `selected`: the fill gets the pressed color |

`focus` combines with `hover` and `pressed`: the ring is drawn on top of their tokens. The ring surrounds `control` only, not `label`.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `checked`, `indeterminate` | None; the control stays interactive | `selected` group; `check-icon` or `indeterminate-icon` shown |
| `error` | None. Derived: `error-message` is non-empty | Danger border on an `unselected` control, or a danger ring around a `selected` control; `error-icon`, `error-message` |
| `disabled` | No hover, no pressed, not focusable, not changeable | Disabled tokens; label and helper text included |

Precedence: `disabled` overrides `error`, which overrides `selected` and `unselected`; interactive states apply on top of the resulting group. `error` is never combined with `disabled` (see Anatomy). A `selected` control in error keeps its `selected` fill and mark and adds the error ring (see `error` ring below): the ring, the icon, and the message show the error.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). A radio button and a switch use these tables with the changes stated in their own spec.

### `unselected`

| State | Fill | Border |
|---|---|---|
| `enabled` | `none` | `{colors.outline}` |
| `hover` | `none` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |

### `selected`

| State | Fill | Mark |
|---|---|---|
| `enabled` | `{colors.primary}` | `{colors.on-primary}` |
| `hover` | `{colors.primary-hover}` | `{colors.on-primary}` |
| `pressed` | `{colors.primary-pressed}` | `{colors.on-primary}` |

The `selected` border is `none` in every state (the width stays reserved).

### `error` (`unselected` control only)

| State | Fill | Border |
|---|---|---|
| `enabled` | `none` | `{colors.danger}` |
| `hover` | `none` | `{colors.danger-hover}` |
| `pressed` | `{colors.neutral-subtle-hover}` | `{colors.danger-pressed}` |

`error-icon` and `error-message` use `{colors.danger}` in every state. `{colors.danger-hover}` and `{colors.danger-pressed}` are darker than `{colors.danger}`, so the 3:1 border requirement holds without its own check.

### `error` ring (`selected` control only)

A `selected` control in error keeps the `selected` fill and mark of its state and adds a ring drawn outside `control`, separated from it by a gap of the surface color, so the danger color never touches the brand color.

| State | Ring color | Width | Gap to `control` |
|---|---|---|---|
| `enabled` | `{colors.danger}` | `{spacing.focus-ring-width}` | `{spacing.focus-ring-offset}` |
| `hover` | `{colors.danger-hover}` | same | same |
| `pressed` | `{colors.danger-pressed}` | same | same |

The ring is a rounded square that follows the radius of `control`; like the focus ring it never changes the layout. Error and focus together: the error ring stays next to `control`; the focus ring moves outward and is drawn around the error ring, at `{spacing.focus-ring-offset}` from it. The result, from the inside out, is the control, a gap, the danger ring, a gap, the focus ring. The two are told apart by order and color (danger, then focus), and the error is never carried by the ring alone (`error-icon` and `error-message` stay).

### `disabled`

| Part | Token |
|---|---|
| Fill, `unselected` | `none` |
| Fill, `selected` | `{colors.disabled-container}` |
| Border | `{colors.on-disabled}` |
| Mark | `{colors.on-disabled}` |
| `label`, `legend`, `helper-text` | `{colors.on-disabled}` |

### Text parts

| Part | Token |
|---|---|
| `label`, `legend`, `required-marker` | `{colors.on-surface}` |
| `helper-text` | `{colors.on-surface-muted}` |
| `error-icon`, `error-message` | `{colors.danger}` |

`helper-text` sits under the row, on `{colors.surface}`: `{colors.on-surface-muted}` is used on the surface only, never on a grayed fill.

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

## Token contract

The theme must define every token below. The checkbox adds no token: every one is reused.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the text pairs; the surface shows through an `unselected` control |
| `colors.on-surface` | `label`, `legend`, hover and pressed border |
| `colors.on-surface-muted` | `helper-text`, on the surface only |
| `colors.outline` | `unselected` border; at least 3:1 against `colors.surface` (see Non-token requirement) |
| `colors.primary` | `selected` fill |
| `colors.primary-hover` | `selected` fill on hover |
| `colors.primary-pressed` | `selected` fill on pressed |
| `colors.on-primary` | Mark on the `selected` fill |
| `colors.danger` | `error` border and ring, `error-icon`, `error-message` |
| `colors.danger-hover` | `error` border and ring on hover |
| `colors.danger-pressed` | `error` border and ring on pressed |
| `colors.neutral-subtle-hover` | `unselected` fill on pressed |
| `colors.disabled-container` | `selected` fill when disabled |
| `colors.on-disabled` | Disabled border, mark, and text |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Label and support text for `s` |
| `typography.label-md` | Label and support text for `m` |

### Rounded

| Token | Role |
|---|---|
| `rounded.control` | Control radius, capped at a quarter of the control size |

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-sm` | Control size and mark for `s`; `error-icon` for `s` |
| `spacing.icon-md` | Control size and mark for `m`; `error-icon` for `m` |
| `spacing.control-xs` | Row minimum height for `s` |
| `spacing.control-sm` | Row minimum height for `m` |
| `spacing.xs` | Space between the row and its support line, and between the options of a group |
| `spacing.sm` | Gap between `control` and `label`; space between `legend` and the first option |
| `spacing.border-width` | Control border width |
| `spacing.focus-ring-width` | Focus ring width; `error` ring width |
| `spacing.focus-ring-offset` | Gap between the control and its `error` ring; between the `error` ring (or the control) and the focus ring |

### Components entries (contrast checks)

One entry per text color and one per `selected` state, using only the standard `backgroundColor` and `textColor` properties. `disabled` pairs are never declared (WCAG 1.4.3 exemption, see `docs/conventions.md`). The text entries (`checkbox`, `checkbox-muted`, `checkbox-error`, `checkbox-focus-ring`) are also those of the radio button, the switch, and the slider: they declare none of their own.

| Entry | backgroundColor | textColor |
|---|---|---|
| `checkbox` | `{colors.surface}` | `{colors.on-surface}` |
| `checkbox-muted` | `{colors.surface}` | `{colors.on-surface-muted}` |
| `checkbox-error` | `{colors.surface}` | `{colors.danger}` |
| `checkbox-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |
| `checkbox-selected` | `{colors.primary}` | `{colors.on-primary}` |
| `checkbox-selected-hover` | `{colors.primary-hover}` | `{colors.on-primary}` |
| `checkbox-selected-pressed` | `{colors.primary-pressed}` | `{colors.on-primary}` |

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `check-icon` is the library checkmark, `indeterminate-icon` its minus (remove) glyph, and `error-icon` its error glyph (a circle with an exclamation mark).
- Border contrast (WCAG 1.4.11): the `unselected` border must reach 3:1 against `{colors.surface}`. It is `colors.outline`, the pair the theme script already checks outside the lint (row `outline` of its report; see `docs/conventions.md`); no new check is needed. The `selected` fill is `{colors.primary}`, which the State colors rule keeps at 4.5:1 or more against the surface, and the `error` border and ring are `{colors.danger}`, at 4.5:1 or more against the surface by the same rule (the ring is surrounded by the surface, so it is never read against the `selected` fill; covered by `checkbox-error`). No non-standard property is added to `components`.
- The checkbox has no elevation (`level-0`).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | Native `input` of type `checkbox`. No custom role. |
| Accessible name | The visible `label`, associated natively (`label` linked to the input, so a click on the label toggles it). A bare `aria-label` is never the only name. |
| Group | A native `fieldset` with a `legend`, which names the group. `aria-describedby` on the `fieldset` references the group `helper-text` or `error-message`. |
| Description | `helper-text` or `error-message` of a lone checkbox is referenced by `aria-describedby` on the input. |
| Indeterminate | Set through the native `indeterminate` property of the input, so assistive technologies announce "mixed". It is never set by the user's click. |
| Invalid | `aria-invalid="true"` on the input exactly when it is in error; in a group, on every option in error, with the group description on the `fieldset`. |
| Required | The native `required` attribute when `required` is true. `required-marker` is hidden from assistive technologies; the form explains it in visible text. |
| Not by color alone | The selection is shown by the fill and by `check-icon` or `indeterminate-icon` (WCAG 1.4.1). An error shows `error-icon` and `error-message` besides the danger border or ring. |
| Focus visible | The focus ring appears on keyboard focus. It must never be removed. |
| Keyboard | `Tab` moves focus to each checkbox. `Space` toggles the focused checkbox. |
| Disabled | Native `disabled`: out of the tab order, value not submitted. |
| Target size | The click target is `choice` (control, gap, label), at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8): the row minimum height of every size meets it. 44 by 44 is recommended on touch screens. |
| Contrast | Text and marks reach 4.5:1 against their background (entries of the Token contract, checked by the lint). The `unselected` border reaches 3:1 against `{colors.surface}` (checked by the theme script, see Non-token requirement). `disabled` is exempt. |

## Behavior

- Toggle: activating `choice` (the control or the label) flips `checked` and clears `indeterminate`. The value is applied when the form is submitted, never at once.
- Parent and children: a "select all" checkbox is `indeterminate` while some children are checked; the project keeps it in step with its children. Activating it checks all children when it was `unchecked` or `indeterminate`, and unchecks them when it was `checked`.
- Validation: the project decides the rules. Show `error-message` after the user submits, not before; clear it as soon as the value becomes valid. When an error appears after a submit, focus moves to the first checkbox in error (or the first of the group).
- Label: wraps if needed; it is never truncated.
- A pointer that goes down on `choice` and leaves it before release does not toggle (native behavior).

## Do and don't

| Do | Don't |
|---|---|
| Write the label as a statement the user agrees with ("Send me a copy") | Write a negative or ambiguous label ("Don't not send") |
| Group related checkboxes in a `fieldset` with a `legend` | Leave a list of checkboxes without a group name |
| Say what is wrong and how to fix it ("Accept the terms to continue") | Write "Invalid" or only turn the border red |
| Use a switch for a setting that applies at once | Use a checkbox for an immediate effect |
| Use radio buttons for exclusive choices | Use checkboxes where only one option can be selected |
| Keep `indeterminate` for a parent of several options | Let the user set `indeterminate` by clicking |

## Out of scope

Animations, checkboxes without a visible label (table row selection), a nested tree of checkboxes, option descriptions inside a group, a "select all" helper, and custom marks are not covered by this spec.
