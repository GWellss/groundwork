# Select

A select lets the user pick one value from a list of options, with a visible label and optional help and error. The closed select is a field built like the text field; the open list is a floating surface of options. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme. It builds on `components/text-field.md` (the field) and `components/menu.md` (the option rows), and states only what differs.

## At a glance

| Aspect | Summary |
|---|---|
| Base | `components/text-field.md` for the field, `components/menu.md` for the rows; everything not stated here is unchanged |
| Parts | `label`, `required-marker`, `field`, `value`, `placeholder`, `chevron`, `helper-text`, `error-icon`, `error-message`, `listbox`, `option`, `leading-icon`, `option-label`, `check-icon` |
| Configurations | with or without helper text; options with or without icons |
| Selection | one option at most; no multiple selection |
| Variants | none; one appearance, `default`, as the text field |
| Sizes | `s`, `m`, `l` for the field, as the text field; one size for the options |
| Interactive states | `enabled`, `hover`, `focus` for the field; `enabled`, `hover`, `focus`, `pressed` for an option; visibility states `closed`, `open` |
| State properties | `disabled`, `error` (derived from `error-message`), `filled` (derived from `value`), `selected` (for an option) |
| Elevation | `level-2` for `listbox` when `open` (not a token, see Token contract) |

## Purpose

- Use a select to pick one value from a known list of about seven options or more, when the list does not need to stay visible.
- Prefer the native `select` element: it gives a platform picker on touch screens, the full keyboard, type-ahead, and announcements at no cost. Style its closed field with the tokens of this spec; the open list is the platform's and is not themed.
- Use the custom listbox of this spec only when options need an icon, or when the open list must follow the theme. It must then reproduce the behavior below in full.
- Use radio buttons for fewer than about seven options that can all stay visible (see `components/radio.md`).
- Use a menu to run commands (see `components/menu.md`): a menu does something, a select sets a value.
- Do not use a select to pick several values, to type and filter a long list, or to enter free text: see Out of scope.

## Anatomy

### Parts

Parts inherited unchanged from the text field: `label`, `required-marker`, `field`, `helper-text`, `error-icon`, `error-message`. The select has no `prefix`, `suffix`, `counter`, `leading-icon` of the field, or `trailing-icon`.

| Part | Role | Required | Notes |
|---|---|---|---|
| `value` | The label of the chosen option | when a value exists | Single line, ellipsis when it overflows |
| `placeholder` | Hint while no option is chosen | no | Replaces `value`; never the only label |
| `chevron` | Shows that a list opens | yes | The library chevron-down glyph; decorative; at the end of `field` |
| `listbox` | The floating surface that holds the options | yes | Role `listbox`; a floating surface |
| `option` | One choosable value | yes | At least one |
| `leading-icon` | Decorative icon before the option label | no | Option only |
| `option-label` | Visible text of an option | yes | Provides the accessible name of the option; wraps |
| `check-icon` | Checkmark after the option label | when selected | The library checkmark; its space is reserved on every option |

### Configurations

| Configuration | Content | Status |
|---|---|---|
| plain | `field`, `listbox` of text options | allowed |
| with-icons | options with `leading-icon` | allowed |
| with-help | `helper-text` or `error-message` under `field` | allowed |
| no-label | any | forbidden |
| multiple | several options selected | out-of-scope |
| filterable | a text input inside `field` that filters the list | out-of-scope |
| option-groups | titled groups of options | out-of-scope |
| error-and-disabled | `error-message` with `disabled` | forbidden |

Combination rules:

- A select always has a visible `label`; one with no label is `forbidden`. `placeholder` never replaces it.
- `error-message` with `disabled` is `forbidden`: a disabled select leaves the tab order, so its error cannot be reached by keyboard.
- A field in `error` always shows `error-message` with `error-icon`. Color alone never says "error".
- `error-message` replaces `helper-text` in the same slot.
- A user cannot clear a chosen value. When "no value" is valid, the project adds an explicit option for it ("None").
- If `value` matches no option, the field shows `placeholder`.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | Visible name of the field; accessible name |
| `options` | list of options | none, required | The choices, in display order |
| `value` | an option `value` | none | The chosen option; none shows `placeholder` |
| `placeholder` | text | none | Hint while no option is chosen |
| `helper-text` | text | none | Hint under the field |
| `error-message` | text | none | Non-empty puts the field in `error` |
| `size` | `s`, `m`, `l` | `m` | Named dimension set of the field |
| `placement` | `top`, `right`, `bottom`, `left` | `bottom` | Preferred side of the field for `listbox`; flips if space runs out |
| `required` | `true`, `false` | `false` | A value is required; shows `required-marker` |
| `disabled` | `true`, `false` | `false` | Not focusable, not changeable, not submitted |

Option:

| Property | Values | Default | Description |
|---|---|---|---|
| `value` | text | none, required | The submitted value, unique in the list |
| `label` | text | none, required | The visible text |
| `leading-icon` | icon reference | none | Optional icon before `label` |
| `disabled` | `true`, `false` | `false` | Not selectable |

`listbox` is aligned `start` on `field`, and not configurable.

## Variants

The select has one appearance, `default`: the outlined field of the text field. Error and disabled are states, not variants. An option has no variant.

## Sizes

### Decision

The field has the three sizes of the text field, unchanged: height, padding, gap, icon size, and typography. The `chevron` has the icon size of the field and sits after `value` with the gap of the size. The options have one size, that of the menu items. The list has no size of its own: it is at least as wide as `field`.

### Size table

| Dimension | Token or rule |
|---|---|
| Field `s`, `m`, `l` | Size table of `components/text-field.md` |
| `chevron` size | The icon size of the field size |
| Option row | Size table of `components/menu.md` (`item-min-height`, `item-padding-inline`, `item-gap`, `icon-size`, `label-typography`) |
| `listbox` `min-width` | The width of `field` |
| `listbox` `max-width` | `{spacing.floating-max-width}`, never less than the width of `field` |

Geometry rules:

- `value` and `placeholder` are single line; `value` is truncated with an ellipsis when it overflows. An `option` label wraps and the row grows, so the full text is always readable.
- `check-icon` is at the end of the row and its space (`icon-size` plus `item-gap`) is reserved on every option, so selecting never moves a label. `leading-icon` fills the leading space of the menu rows.
- `listbox` is open below `field` with the offset of "Floating surface" in `docs/conventions.md`, aligned to its start edge.
- Radius, border, container padding, offset, and viewport padding are those of the menu container.
- The border of `field` is always reserved (`{spacing.border-width}`), so no state moves the content.

## States

### Interactive states

Field:

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over `field` | The border gets the hover color; fill and text do not change |
| `focus` | Keyboard or pointer focus on `field` | Adds the focus ring around `field`; never changes fill, text, or border |

Option:

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default | Base tokens |
| `hover` | Pointer over the option | The fill gets the hover color |
| `focus` | The option is the active option (keyboard) | Adds the focus ring inside the option |
| `pressed` | Pointer down on the option | The fill gets the pressed color |

The field has no `pressed` state: pressing it opens the list. While the list is `open` the field keeps its focus and takes the border of `hover`, so it reads as active. The ring of an option is drawn inside, as in the menu. Keyboard focus never leaves the field: the active option is announced through `aria-activedescendant`.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `filled` | None. Derived: `value` is not empty | `placeholder` hidden; `value` shown |
| `error` | None. Derived: `error-message` is non-empty | Danger border, `error-icon`, `error-message` |
| `disabled` (field) | No hover, not focusable, does not open | Disabled tokens; label included |
| `selected` (option) | None; the option stays selectable | `check-icon` shown; the fill does not change |
| `disabled` (option) | No hover, no pressed, not selectable; still reachable by the arrow keys | Disabled tokens |

Precedence for the field: `disabled` overrides `error`, which overrides the `default` group; interactive states apply on top of the resulting group. `error` is never combined with `disabled` (see Anatomy). For an option: `disabled` overrides `hover` and `pressed`.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border).

### Field

The field uses the `default`, `error`, `disabled`, and text parts tables of `components/text-field.md` unchanged. `value` takes the value color, `placeholder` the muted color, and `chevron` the color of `trailing-icon` (`{colors.on-surface-muted}`; `{colors.on-disabled}` when disabled). There is no `read-only` group. While `open`, the border is that of `hover`.

### Options

An option uses the `default` item table of `components/menu.md` (fill, label, icons) with these changes: there is no `shortcut`, and `check-icon` takes the label color. `listbox` takes the container tokens of the menu (fill, border) and `level-2` while `open`. The disabled option takes the `disabled` table of the menu.

### Focus ring

| Part | Token | Width | Offset |
|---|---|---|---|
| `field` | `{colors.focus-ring}` | `{spacing.focus-ring-width}` | `{spacing.focus-ring-offset}` |
| active option | `{colors.focus-ring}` | `{spacing.focus-ring-width}` | `none` (inside) |

## Token contract

The theme must define every token of the text field and of the menu. The select adds no token.

### Colors

| Token | Role |
|---|---|
| `colors.surface`, `colors.on-surface`, `colors.on-surface-muted`, `colors.outline`, `colors.danger`, `colors.disabled-container`, `colors.on-disabled`, `colors.focus-ring` | Field, as the text field |
| `colors.neutral-subtle-hover`, `colors.neutral-subtle-pressed` | Option hover and pressed fills; `listbox` border |

### Typography, rounded, spacing

Those of the text field (field) and of the menu (rows and `listbox`). `spacing.floating-max-width` bounds the list; `spacing.menu-min-width` does not apply (the minimum is the width of `field`).

### Components entries (contrast checks)

The select declares no entry of its own. It reuses `text-field`, `text-field-muted`, `text-field-error`, and `text-field-focus-ring` for the field, and `menu-item`, `menu-item-hover`, `menu-item-pressed`, and `menu-focus-ring` for the options.

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `chevron` is the library chevron-down glyph; `check-icon` is the library checkmark; `error-icon` is the library error glyph.
- Border contrast (WCAG 1.4.11): the field border is `colors.outline`, already checked at 3:1 by `theme/theme.py` (see `docs/conventions.md`).
- Elevation is not a token. `listbox` uses `level-2` of the elevation table in the `## Elevation & Depth` section of DESIGN.md. The field has no elevation (`level-0`). In dark mode `listbox` has no shadow and takes the `surface-level-2` fill (see Dark mode in `docs/conventions.md`).

## Accessibility

| Topic | Requirement |
|---|---|
| Role of the field | `combobox` with no text input (the select-only combobox pattern of WAI-ARIA), focusable, with `aria-haspopup="listbox"`, `aria-expanded`, and `aria-controls` on `listbox`. A native `select` needs none of this. |
| Role of the list | `listbox` for `listbox`, `option` for each option. Never `menu` or `menuitem`: a select picks a value, a menu runs commands. |
| Accessible name | The visible `label` (`aria-labelledby` on `field`, and on `listbox`). A placeholder is never the only name. |
| Value | The chosen option is the value of the combobox. Each option has `aria-selected="true"` when chosen. |
| Active option | `aria-activedescendant` on `field` points to the active option while `open`. Focus stays on `field`. |
| Description | `helper-text` or `error-message` is referenced by `aria-describedby`; `aria-invalid="true"` exactly when `error-message` is present. |
| Required | `aria-required="true"` (native `required` on a native `select`). `required-marker` is hidden from assistive technologies; the form explains it in visible text. |
| Disabled option | `aria-disabled="true"`, never the native `disabled`. |
| Not by color alone | The chosen option shows `check-icon`. An error shows `error-icon` and `error-message` besides the danger border (WCAG 1.4.1). |
| Focus visible | The focus ring shows on `field`, and on the active option. It must never be removed. |
| Target size | The field height of every size and the option height are at least 24 CSS pixels (WCAG 2.2 criterion 2.5.8). Clicking `label` focuses `field`. |
| Contrast | Text reaches 4.5:1, the field border 3:1 (see Components entries and Non-token requirement). `disabled` is exempt. |

Keyboard:

| Key | Where | Effect |
|---|---|---|
| `Enter`, `Space`, `ArrowDown`, `ArrowUp` | Closed | Opens the list; the active option is the chosen one, or the first |
| A letter | Closed | Opens the list on the first enabled option that starts with that letter |
| `ArrowDown`, `ArrowUp` | Open | Moves the active option; does not wrap |
| `Home`, `End` | Open | First or last option |
| A letter | Open | Moves to the next enabled option that starts with that letter; the same letter again cycles |
| `Enter`, `Space` | Open | Chooses the active option, closes, focus stays on `field` |
| `Escape` | Open | Closes without changing the value; focus stays on `field` |
| `Tab` | Open | Chooses the active option, closes, and focus moves on |

## Behavior

- Opening: pressing `field` opens `listbox` on `placement` with the flip and shift rules of "Floating surface". The list opens with the chosen option active and scrolled into view.
- Choosing: releasing the pointer on an option chooses it and closes the list. Releasing outside cancels. A `disabled` option does nothing and the list stays open.
- Closing: choosing, `Escape`, a press outside, `Tab`, or pressing `field` again. Closing never counts as leaving the field for validation.
- Validation: the project decides the rules. Show `error-message` after the user leaves the field or submits, never on an untouched field before submit; clear it once a value is chosen. After a submit, focus moves to the first field in error.
- Long list: `listbox` scrolls inside the viewport (see "Floating surface").
- Form value: the project submits the chosen `value` (for example through a hidden input or a native `select`).

## Do and don't

| Do | Don't |
|---|---|
| Use a native `select` for plain text options | Rebuild the list when the platform picker is enough |
| Keep a visible label above the field | Use the placeholder as the label |
| Add a "None" option when an empty value is valid | Expect users to clear a choice |
| Order options as users expect (alphabetical, by frequency) | Leave a long list in random order |
| Use radio buttons for a few options | Hide three options behind a list |
| Say how to fix an error ("Choose a country") | Write "Invalid" or only turn the border red |

## Out of scope

Multiple selection (it needs a list that stays open, a summary of several values in `field`, and checkable rows), a filterable select (combobox), option groups, option descriptions, a clear button, a read-only field, animations, and creating new options are not covered by this spec. A filterable select, and the suggestions of the search field (see `components/search-field.md`), will reuse `listbox`, its options, its tokens, and its geometry unchanged; what they add is a text input with the `combobox` role, `aria-controls` on `listbox`, `aria-activedescendant` for the active option, filtering of the options, and a polite announcement of the number of results. None of that is defined here.
