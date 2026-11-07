# Text field

A text field lets the user type free text on a single line or on several lines (the `multiline` variant, also known as a textarea), with a visible label and optional help, error, and counter. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `label`, `required-marker`, `field`, `input`, `placeholder`, `leading-icon`, `prefix`, `suffix`, `trailing-icon`, `helper-text`, `error-icon`, `error-message`, `counter` |
| Configurations | single line or `multiline`; each with or without icons, affixes, helper text, counter |
| Variants | none by emphasis; one appearance, `default` |
| Sizes | `s`, `m`, `l` |
| Interactive states | `enabled`, `hover`, `focus` |
| State properties | `disabled`, `read-only`, `error` (derived from `error-message`), `filled` (derived from `value`) |

## Purpose

- Use a text field for free text that the user types: a name, an email address, a message.
- Use `multiline` for text that may exceed one line (a comment, a description).
- Use a search field for a search query (see `components/search-field.md`).
- Do not use a text field to pick among known values: use a choice control.
- Do not use a text field to show text that is never editable and never focusable: use plain text. A `read-only` field is for a value the user must be able to focus, select, and copy inside a form.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `label` | Names the field, always visible, above the field | yes | Associated with `input`; never replaced by `placeholder` |
| `required-marker` | Shows that a value is required | no | Inside `label`; only when `required` is true |
| `field` | Box around the input and its elements; carries fill, border, radius | yes | The whole box is the click target that focuses `input` |
| `input` | The editable text | yes | A single line, or several lines when `multiline` |
| `placeholder` | Short hint inside `input` while it is empty | no | Never the only label; never carries required information |
| `leading-icon` | Decorative icon before the input | no | Not in `multiline` |
| `prefix` | Fixed text before the value ("$", "https://") | no | Not in `multiline` |
| `suffix` | Fixed text after the value ("kg", "@example.com") | no | Not in `multiline` |
| `trailing-icon` | Decorative icon after the input | no | Not interactive; not in `multiline` |
| `helper-text` | Hint under the field | no | Replaced by `error-message` while the field is in error |
| `error-icon` | Icon before `error-message` | with `error-message` | Decorative; the second cue besides color |
| `error-message` | Text that says what is wrong and how to fix it | no | Present exactly when the field is in error |
| `counter` | Characters typed and maximum ("12 / 80") | no | Only with `max-length` and `show-counter`; aligned to the end under the field |

### Configurations

| Configuration | Elements in `field` | Allowed |
|---|---|---|
| plain | `input` | yes |
| leading-icon | `leading-icon`, `input` | yes |
| trailing-icon | `input`, `trailing-icon` | yes |
| affixes | `prefix` and/or `suffix` around `input` | yes |
| icon-and-affix | an icon and an affix on the same side | no |
| multiline-plain | `input` | yes |
| multiline-with-elements | icon, `prefix`, or `suffix` | no |
| no-label | any | no |
| error-and-disabled | `error-message` with `disabled` | no |
| error-and-read-only | `error-message` with `read-only` | no |

Combination rules:

- A field always has a visible `label`. A placeholder never replaces it.
- A side holds at most one element: an icon or an affix.
- `multiline` holds only `input`; icons and affixes are single line features.
- A field in `error` always shows `error-message` with `error-icon`. Color alone never says "error".
- `error-message` replaces `helper-text` in the same slot. `counter` stays visible next to it.
- `counter` requires `max-length`.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | Visible name of the field; accessible name |
| `value` | text | empty | Current text |
| `placeholder` | text | none | Hint while empty |
| `helper-text` | text | none | Hint under the field |
| `error-message` | text | none | Non-empty puts the field in `error` |
| `size` | `s`, `m`, `l` | `m` | Named dimension set |
| `multiline` | `true`, `false` | `false` | Several lines (textarea) |
| `rows` | integer, 2 or more | `3` | Visible lines at rest; only with `multiline` |
| `type` | `text`, `email`, `tel`, `url` | `text` | Kind of value (keyboard, validation); `text` only with `multiline` |
| `autocomplete` | token | none | Purpose of the value for autofill (WCAG 1.3.5), for example a name or an email |
| `leading-icon` | icon reference | none | Not with `multiline`, `prefix`, or on a side that holds `suffix` |
| `trailing-icon` | icon reference | none | Not with `multiline` or `suffix` |
| `prefix` | text | none | Not with `multiline` or `leading-icon` |
| `suffix` | text | none | Not with `multiline` or `trailing-icon` |
| `max-length` | integer | none | Maximum characters, enforced |
| `show-counter` | `true`, `false` | `false` | Shows `counter`; requires `max-length` |
| `required` | `true`, `false` | `false` | A value is required; shows `required-marker` |
| `read-only` | `true`, `false` | `false` | Value visible, focusable, copyable, not editable |
| `disabled` | `true`, `false` | `false` | Not focusable, not editable, not submitted |

## Variants

The text field has one appearance, `default`: an outlined box without fill. Error, read-only, and disabled are states, not variants.

| Variant | Container | Border | Intent |
|---|---|---|---|
| `default` | none (the surface shows through) | yes, `{colors.outline}` | Outlined field; a visible boundary at 3:1 or more |

## Sizes

### Decision

Three sizes. Heights reuse the control tokens; text, icons, and gaps reuse existing spacing and typography tokens, so density applies without new tokens.

### Size table

| Size | Height | Padding inline | Gap | Padding block, `multiline` |
|---|---|---|---|---|
| `s` | `{spacing.control-sm}` | `{spacing.sm}` | `{spacing.xs}` | `{spacing.sm}` |
| `m` | `{spacing.control-md}` | `{spacing.md}` | `{spacing.sm}` | `{spacing.sm}` |
| `l` | `{spacing.control-lg}` | `{spacing.md}` | `{spacing.sm}` | `{spacing.md}` |

| Size | Icon size | Value typography | Label and support typography |
|---|---|---|---|
| `s` | `{spacing.icon-sm}` | `{typography.label-md}` | `{typography.label-sm}` |
| `m` | `{spacing.icon-md}` | `{typography.label-md}` | `{typography.label-md}` |
| `l` | `{spacing.icon-lg}` | `{typography.label-lg}` | `{typography.label-md}` |

Geometry rules:

- Height is the outer height of `field`, border included. It is fixed for a single line; content is centered vertically and there is no vertical padding.
- `multiline`: the minimum height is `rows` lines of the value typography plus twice the padding block, never less than the single-line height of the size. The field takes the full width of its container; the user may resize it vertically only, never horizontally.
- Gap separates the icon or affix from `input`.
- "Label and support typography" applies to `label`, `helper-text`, `error-message`, `counter`, `prefix`, and `suffix`.
- The vertical space between `label`, `field`, and the support line (`helper-text` or `error-message`, with `counter` at the end) is `{spacing.xs}`.
- Width comes from the layout, never from a theme value.
- `error-icon` uses the icon size of the field and sits before `error-message` with the gap of the size.
- Container radius is `{rounded.control}` at every size.
- The border is always reserved (`{spacing.border-width}`), so no state moves the content.
- Text overflow: the value of a single-line field scrolls inside `input`; `placeholder` is truncated with an ellipsis.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over `field` | The border gets the hover color; fill and text do not change |
| `focus` | Keyboard or pointer focus inside `input` | Adds the focus ring around `field`; never changes fill, text, or border |

`focus` combines with `hover` and with every state property: the ring is drawn on top of their tokens. A text field has no `pressed` state: pointer down only places the caret.

The field has no fill, so `hover` moves the border (a non-text part) and leaves every text pair unchanged. The state is still distinct from `enabled`.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `filled` | None. Derived: `value` is not empty | `placeholder` hidden; value shown |
| `read-only` | Focusable and selectable; not editable; no `hover` effect | Fill and border of the `read-only` group; no placeholder |
| `error` | None. Derived: `error-message` is non-empty | Danger border, `error-icon` and `error-message` |
| `disabled` | No hover, not focusable, not editable | Disabled tokens; label included |

Precedence: `disabled` overrides `read-only`, which overrides `error`, which overrides the `default` group. Interactive states apply on top of the resulting group. `error` is never combined with `disabled` or `read-only` (see Anatomy).

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border).

### `default`

| State | Fill | Value | Border |
|---|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` | `{colors.outline}` |
| `hover` | `none` | `{colors.on-surface}` | `{colors.on-surface}` |
| `focus` | `none` | `{colors.on-surface}` | `{colors.outline}` |

### `error`

| State | Fill | Value | Border |
|---|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` | `{colors.danger}` |
| `hover` | `none` | `{colors.on-surface}` | `{colors.danger-hover}` |
| `focus` | `none` | `{colors.on-surface}` | `{colors.danger}` |

`error-icon` and `error-message` use `{colors.danger}` in every state. `{colors.danger-hover}` is darker than `{colors.danger}`, so the 3:1 border requirement holds without its own check.

### `read-only`

| State | Fill | Value | Border |
|---|---|---|---|
| `enabled` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.outline}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.outline}` |
| `focus` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.outline}` |

### `disabled`

| Part | Token |
|---|---|
| Fill | `{colors.disabled-container}` |
| Value, `label`, `helper-text`, `counter`, icons, affixes | `{colors.on-disabled}` |
| Border | `none` |

### Text parts (`default`, `error`, `read-only`)

| Part | Token |
|---|---|
| `label`, `required-marker` | `{colors.on-surface}` |
| `placeholder`, `helper-text`, `counter`, `prefix`, `suffix` | `{colors.on-surface-muted}` |
| `leading-icon`, `trailing-icon` | `{colors.on-surface-muted}` |

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

The ring surrounds `field` only, not `label` or the support line.

## Token contract

The theme must define every token below. The text field adds one color, `on-surface-muted`; every other token is reused.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the text pairs; the surface shows through the field |
| `colors.on-surface` | Value, `label`, hover border |
| `colors.on-surface-muted` | New. Placeholder, `helper-text`, `counter`, affixes, icons. A quieter neutral than `on-surface`: step `600` of the neutral scale, or `700` when `600` is below 4.5:1 against `colors.surface`. Distinct from `on-surface`, which is step `700` or later |
| `colors.outline` | Field border; at least 3:1 against `colors.surface` (see Non-token requirement) |
| `colors.danger` | `error` border, `error-icon`, `error-message` |
| `colors.danger-hover` | `error` border on hover |
| `colors.neutral-subtle-hover` | `read-only` fill |
| `colors.disabled-container` | `disabled` fill |
| `colors.on-disabled` | `disabled` content |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Label and support text for `s` |
| `typography.label-md` | Value for `s` and `m`; label and support text for `m` and `l` |
| `typography.label-lg` | Value for `l` |

### Rounded

| Token | Role |
|---|---|
| `rounded.control` | Field radius, all sizes |

### Spacing

| Token | Role |
|---|---|
| `spacing.control-sm` | Height for `s` |
| `spacing.control-md` | Height for `m` |
| `spacing.control-lg` | Height for `l` |
| `spacing.icon-sm` | Icon size for `s` |
| `spacing.icon-md` | Icon size for `m` |
| `spacing.icon-lg` | Icon size for `l` |
| `spacing.xs` | Gap for `s`; vertical space between label, field, and support line |
| `spacing.sm` | Padding inline for `s`; gap for `m` and `l`; padding block for `s`, `m` |
| `spacing.md` | Padding inline for `m` and `l`; padding block for `l` |
| `spacing.border-width` | Border width |
| `spacing.focus-ring-width` | Focus ring width |
| `spacing.focus-ring-offset` | Gap between the field and its focus ring |

### Components entries (contrast checks)

One entry per text color, using only the standard `backgroundColor` and `textColor` properties. `disabled` pairs are never declared (WCAG 1.4.3 exemption, see `docs/conventions.md`). The states `hover` and `focus` change only the border or the ring, never a text color, so they need no entry of their own.

| Entry | backgroundColor | textColor |
|---|---|---|
| `text-field` | `{colors.surface}` | `{colors.on-surface}` |
| `text-field-muted` | `{colors.surface}` | `{colors.on-surface-muted}` |
| `text-field-error` | `{colors.surface}` | `{colors.danger}` |
| `text-field-read-only` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `text-field-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `error-icon` is the library's error glyph (a circle with an exclamation mark); `leading-icon` and `trailing-icon` are chosen by the project.
- Border contrast (WCAG 1.4.11): the field border must reach 3:1 against `{colors.surface}`. The DESIGN.md lint only checks `components` pairs of `backgroundColor` and `textColor` at 4.5:1, so it cannot check a border. The kit checks it outside the lint: `theme/theme.py` computes `colors.outline` against `colors.surface` at 3:1 and lists it in its contrast report (`outline`); when the theme is written without the script, compute that one pair by hand. No non-standard property is added to `components`. The `danger` and `on-surface` borders are already covered by the 4.5:1 entries above.
- The text field has no elevation (`level-0`).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | Native text input (`input`, or `textarea` when `multiline`). No custom role. |
| Accessible name | The visible `label`, associated natively (`label` linked to the input). A placeholder or an `aria-label` is never the only name. |
| Description | `helper-text` or `error-message` is referenced by `aria-describedby` on `input`. `counter` is not referenced, so it is not read at every keystroke. |
| Invalid | `aria-invalid="true"` exactly when `error-message` is present, together with the `aria-describedby` link to that message. |
| Required | The native `required` attribute when `required` is true. `required-marker` (for example an asterisk) is hidden from assistive technologies; the form explains the marker in visible text. |
| Not by color alone | An error shows `error-icon` and `error-message` besides the danger border and text (WCAG 1.4.1). Read-only is shown by the fill. |
| Focus visible | The focus ring appears when `input` has focus. It must never be removed. |
| Keyboard | `Tab` moves focus to the field. In a single-line field `Enter` submits the form; in `multiline` `Enter` inserts a line break. |
| Autofill | `autocomplete` is set when the purpose of the value is known (WCAG 1.3.5). |
| Disabled | Native `disabled`: out of the tab order, value not submitted. |
| Read-only | Native `readonly`: focusable and selectable, value submitted. |
| Target size | Hit area at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8); the field height of every size meets it. Clicking `label` focuses `input`. |
| Contrast | Text reaches 4.5:1 against its background (entries of the Token contract, checked by the lint). The border reaches 3:1 against `{colors.surface}` (checked by the theme script, see Non-token requirement). Placeholder text counts as text. `disabled` is exempt. |

## Behavior

- Validation: the project decides the rules. Show `error-message` after the user leaves the field or submits, not while they type for the first time; clear it as soon as the value becomes valid. Never show an error on an untouched empty field before submit.
- Error message: says what is wrong and how to fix it ("Enter an email address like name@example.com"). When an error appears after a submit, focus moves to the first field in error.
- Counter: shows the number of characters typed and `max-length`. With `max-length`, typing past the limit is refused. The counter is not announced at every keystroke; announce it politely only at limits the project chooses.
- Placeholder: disappears as soon as there is a value; it is a hint, never an instruction required to complete the field.
- Label: wraps if needed; it is never truncated.
- `multiline`: the field shows `rows` lines and a vertical resize handle; when the text exceeds the height, `input` scrolls. Growing with the content is not defined by this spec.
- `read-only` and `disabled` differ: a read-only value is part of the tab order, selectable, and submitted; a disabled one is none of these.

## Do and don't

| Do | Don't |
|---|---|
| Keep a visible label above every field | Use the placeholder as the label |
| Say what is wrong and how to fix it | Write "Invalid input" or only turn the border red |
| Mark the required fields with text the form explains | Rely on color to mark required fields |
| Use `helper-text` for format hints that must stay visible | Put required hints in the placeholder |
| Use `type` and `autocomplete` that match the value | Use a single-line field for long text |
| Keep one field per piece of information | Combine several values in one field |

## Out of scope

Animations, dark mode, floating or inside labels, filled field appearance, password reveal, number steppers, input masks, auto-growing height, rich text, inline clear button (see `components/search-field.md`), and suggestion lists are not covered by this spec.
