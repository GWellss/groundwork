# Search field

A search field is a single-line text field dedicated to a search query, with a search icon, a clear button, and a search landmark. It is built on the text field: it keeps its anatomy, sizes, states, and tokens, and this spec only states what changes. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Base | `components/text-field.md`, read first; everything not stated here is unchanged |
| Parts | those of the text field that apply, plus `search-icon` (replaces `leading-icon`) and `clear-button` (replaces `trailing-icon`) |
| Configurations | with or without helper text; `clear-button` shown only while a value exists |
| Variants | none; one appearance, `default`, as the text field |
| Sizes | `s`, `m`, `l`, as the text field |
| Interactive states | `enabled`, `hover`, `focus`; plus `enabled`, `hover`, `pressed` for `clear-button` |
| State properties | `disabled`, `filled` (derived); no `error`, no `read-only` |

## Purpose

- Use a search field to let the user type a query and submit it: a site search, a filter box above a list.
- Do not use a search field for free text that is not a query: use a text field.
- Do not use it for a choice among known values: use a choice control.
- Suggestions, autocomplete lists, and recent searches are not part of this spec. They build on the listbox of `components/select.md` (a combobox is a text input that drives that list) and are not defined here.

## Anatomy

### Parts

Parts inherited unchanged from the text field: `label`, `field`, `input`, `placeholder`, `helper-text`.

| Part | Role | Required | Notes |
|---|---|---|---|
| `search-icon` | Magnifier icon before the input | yes | Decorative; replaces the text field `leading-icon` |
| `clear-button` | Control that empties the field | yes, but shown only while a value exists | A separate focusable button; replaces the text field `trailing-icon` |
| `label` | Accessible name of the field | yes | Visually hidden by default, see Properties |

The text field parts `required-marker`, `prefix`, `suffix`, `error-icon`, `error-message`, and `counter` do not exist in the search field.

### Configurations

| Configuration | Elements | Status |
|---|---|---|
| empty | `search-icon`, `input` with `placeholder` | allowed |
| filled | `search-icon`, `input`, `clear-button` | allowed |
| with-helper-text | any of the above plus `helper-text` | allowed |
| multiline | any | out-of-scope |
| custom-icon | an icon other than `search-icon` | avoid |
| affix | `prefix` or `suffix` | out-of-scope |
| error | `error-message` | out-of-scope |
| read-only | `read-only` true | out-of-scope |

Combination rules:

- The search field is single line, always. `multiline`, `type`, `max-length`, `required`, `prefix`, `suffix`, `trailing-icon`, `error-message`, and `read-only` of the text field are not available (`out-of-scope`).
- An icon other than `search-icon` is `avoid`: the magnifier is what tells that the field is a search. Keep `search-icon`.
- `clear-button` is shown only while `value` is not empty and the field is not `disabled`.
- The search field sits inside a search landmark (see Accessibility).
- A visible submit button, when the design wants one, is a button of `components/button.md` placed next to the field by the layout. It is not a part of the search field.

## Properties

The properties `value`, `placeholder`, `helper-text`, `size`, and `disabled` are those of the text field, unchanged.

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | Accessible name of the input ("Search products") |
| `show-label` | `true`, `false` | `false` | Shows `label` above the field as in the text field; otherwise it is visually hidden but still the accessible name |
| `landmark-label` | text | none | Name of the search landmark; required when a page has more than one search landmark |
| `clear-label` | text | "Clear search" | Accessible name of `clear-button` |

`placeholder` is a short hint ("Search"). It never replaces `label`.

## Variants

None, as the text field: one `default` appearance, an outlined box without fill.

## Sizes

### Decision

The sizes, heights, paddings, gaps, icon sizes, and typography are those of the text field (`s`, `m`, `l`), unchanged. Only `clear-button` has its own size.

### Size table

| Size | Clear button size | Clear button icon size |
|---|---|---|
| `s` | `{spacing.icon-lg}` | `{spacing.icon-sm}` |
| `m` | `{spacing.icon-xl}` | `{spacing.icon-md}` |
| `l` | `{spacing.icon-xl}` | `{spacing.icon-lg}` |

Geometry rules:

- `search-icon` uses the icon size of the text field size, at the leading side, with the padding inline and the gap of that size.
- `clear-button` is a square of the size above, its icon centered, at the trailing side. Its hover and pressed fill is a circle of the same size.
- On the side of `clear-button`, the padding next to it is `{spacing.xs}` instead of the padding inline, so that the button stays inside the field.
- Showing or hiding `clear-button` never changes the size of the field; the input shrinks and grows.
- The hit area of `clear-button` is at least 24 by 24 CSS pixels, extended invisibly if the rendered size is smaller.

## States

### Interactive states

The field states `enabled`, `hover`, and `focus` are those of the text field, unchanged (the border moves on hover; the ring appears on focus).

`clear-button` has its own states:

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default | Base tokens |
| `hover` | Pointer over `clear-button` | Hover fill |
| `focus` | Keyboard focus on `clear-button` | Adds the focus ring; never changes fill or icon |
| `pressed` | Pointer down or key held on `clear-button` | Pressed fill |

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `filled` | None. Derived: `value` is not empty | `placeholder` hidden; `clear-button` shown |
| `disabled` | As the text field; `clear-button` is hidden | Disabled tokens of the text field |

There is no `error` and no `read-only`. Precedence: `disabled` overrides the `default` group.

## Token mapping

The field itself (fill, value, border, text parts, focus ring, disabled) uses the `default` and `disabled` tables of the text field, unchanged. `search-icon` uses `{colors.on-surface-muted}`; its disabled color is `{colors.on-disabled}`.

### `clear-button`

| State | Fill | Icon |
|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

`clear-button` sits on the field, which has no fill: its pairs are checked against `{colors.surface}`. It does not exist when `disabled`.

### Focus ring (`clear-button`)

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `none` |

The ring follows the circular shape of the button and stays inside the field. The focus ring of the field itself is unchanged.

## Token contract

The search field adds no token: it reuses the colors, typography, rounded, and spacing tokens of the text field and of the chip `remove-button` pattern. The tokens used only by `clear-button` are listed here.

### Colors

| Token | Role |
|---|---|
| `colors.on-surface` | `clear-button` icon |
| `colors.neutral-subtle-hover` | `clear-button` hover fill |
| `colors.neutral-subtle-pressed` | `clear-button` pressed fill |
| `colors.on-surface-muted` | `search-icon` (defined by the text field) |
| `colors.focus-ring` | Focus ring of `clear-button` |

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-lg` | `clear-button` size for `s`; icon size for `l` |
| `spacing.icon-xl` | `clear-button` size for `m` and `l` |
| `spacing.icon-sm` | `clear-button` icon size for `s` |
| `spacing.icon-md` | `clear-button` icon size for `m` |
| `spacing.xs` | Padding next to `clear-button` |

### Components entries (contrast checks)

The field text uses the `text-field` entries unchanged. `clear-button` adds one entry per state, using only the standard `backgroundColor` and `textColor` properties.

| Entry | backgroundColor | textColor |
|---|---|---|
| `search-field-clear` | `{colors.surface}` | `{colors.on-surface}` |
| `search-field-clear-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `search-field-clear-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

### Non-token requirement

Icon style and library come from the `## Icons` section of DESIGN.md. `search-icon` is the library's search (magnifier) glyph and `clear-button` its close glyph. The field border keeps the 3:1 requirement of the text field (`colors.outline` against `colors.surface`). The search field has no elevation (`level-0`).

## Accessibility

Everything in the text field Accessibility table applies, except the rows about required, invalid, and read-only, which do not exist here. What changes or is added:

| Topic | Requirement |
|---|---|
| Landmark | The field and its optional submit button sit in a container with the search landmark role (the native `search` element or `role="search"`), never on the input itself. With more than one search landmark on a page, each has a distinct `landmark-label` that does not repeat the word "search". |
| Role of the input | Native text input of type `search`. Its accessible name is `label` ("Search products"), also when `show-label` is false (visually hidden, never removed). The placeholder is never the only name. |
| Visible label | A visible label is optional here, because the magnifier icon, the placeholder, and the landmark state the purpose. This is the only exception to the visible label rule of the text field. |
| Clear button | A native button named by `clear-label`, hidden from the tab order and from assistive technologies while it does not exist. The native clear control of the browser is hidden so that only one clear control exists. |
| Keyboard | `Enter` submits. `Escape` clears a non-empty field. `Tab` moves from the input to `clear-button`, when shown, then on. |
| Focus visible | The focus ring appears on `input` (around the field) and on `clear-button` (around the button). It must never be removed. |
| Target size | Hit area of `clear-button` at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). |
| Contrast | As the text field for the text (entries `text-field*`) and the border (3:1, theme script). `clear-button` is checked by the three `search-field-clear*` entries. `disabled` is exempt. |

## Behavior

- Submit: `Enter` in the input, or the optional submit button, submits the current value. The component emits the submit event with the value; what is searched and how results appear belong to the project. An empty value is submitted as empty: the component does not block it.
- Instant filtering while typing is a choice of the project; this spec defines the explicit submit only.
- Clear: activating `clear-button`, or pressing `Escape` in a non-empty field, empties the value. Focus then goes to `input`, never lost to the page. Clearing does not submit.
- `clear-button` appears as soon as the value is not empty and disappears when it is empty.
- Results announcement: when results change after a submit, the project announces the result count politely (for example "12 results"); the component cannot know it.
- Placeholder: single line, truncated with an ellipsis; it disappears as soon as there is a value.

## Do and don't

| Do | Don't |
|---|---|
| Give the field an accessible name, even when no label is shown | Rely on the placeholder as the only name |
| Put the search landmark around the field and its button | Put the search role on the input |
| Keep the clear button inside the field | Add a second, browser-native clear control |
| Announce the result count after a submit | Leave the user without feedback after a submit |
| Use a text field for anything that is not a query | Use a search field for a form value |

## Out of scope

Animations, a multiline field, a prefix or a suffix, an error or read-only state, suggestions, autocomplete lists, recent searches, voice input, filters and scopes inside the field, instant filtering rules, and a field that expands or collapses are not covered by this spec.
