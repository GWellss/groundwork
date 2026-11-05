# Button

A button triggers an action when activated. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `label`, `leading-icon`, `trailing-icon`, `spinner` |
| Configurations | label only, leading icon + label, label + trailing icon, both icons + label, icon-only |
| Variants | `filled`, `tonal`, `outlined`, `text`, `danger` |
| Sizes | `xs`, `s`, `m`, `l`, `xl` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `disabled`, `loading` |
| Behavior options | `full-width` |
| Tokens required | 19 colors, 4 typography, 1 rounded, 18 spacing (see Token contract) |
| Contrast entries | 16 `components` entries, `backgroundColor` and `textColor` only (see Token contract) |

## Purpose

- Use a button to trigger an action in place: submit, save, open, confirm, cancel.
- Do not use a button to navigate to another page: use a link.
- The variant expresses emphasis. One screen area should have at most one `filled` button.
- Use `danger` for a destructive action (delete, remove, discard). It is not an emphasis level: it signals risk.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | Holds all other parts, carries the fill, the border, and the radius | yes | Always present |
| `label` | Text that names the action | yes | Visually hidden in icon-only; still provides the accessible name |
| `leading-icon` | Icon before the label | no | Decorative when the label is visible |
| `trailing-icon` | Icon after the label | no | Decorative when the label is visible |
| `spinner` | Progress indicator | no | Shown only when `loading` is true; replaces the visible content |

### Configurations

| Configuration | `leading-icon` | `label` visible | `trailing-icon` | Allowed |
|---|---|---|---|---|
| label-only | no | yes | no | yes |
| leading-icon-label | yes | yes | no | yes |
| label-trailing-icon | no | yes | yes | yes |
| leading-icon-label-trailing-icon | yes | yes | yes | yes |
| icon-only | yes | no | no | yes |
| empty | no | no | no | no |
| icon-only-two-icons | yes | no | yes | no |

Combination rules:

- A button always has a label, visible or not. The label is the accessible name.
- Icon-only is a property of the same component, not a separate component: the label is visually hidden, exactly one icon is shown in the `leading-icon` slot, and the accessible name is mandatory.
- A button with no visible label and no icon is invalid.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `variant` | `filled`, `tonal`, `outlined`, `text`, `danger` | `filled` | Emphasis level, or destructive action for `danger` |
| `size` | `xs`, `s`, `m`, `l`, `xl` | `m` | Named dimension set |
| `label` | text | none, required | Action name; accessible name |
| `leading-icon` | icon reference | none | Optional icon before the label |
| `trailing-icon` | icon reference | none | Optional icon after the label; not allowed with `icon-only` |
| `icon-only` | `true`, `false` | `false` | Hides the label visually; requires `leading-icon` |
| `disabled` | `true`, `false` | `false` | Button cannot be activated |
| `loading` | `true`, `false` | `false` | Action in progress; button cannot be activated |
| `full-width` | `true`, `false` | `false` | Container fills the width of its parent |

## Variants

| Variant | Emphasis | Container | Border | Typical use |
|---|---|---|---|---|
| `filled` | highest | solid fill | none | Main action of an area |
| `tonal` | high | soft fill | none | Important action next to a `filled` one |
| `outlined` | medium | none | yes | Secondary action |
| `text` | low | none | none | Tertiary or inline action |
| `danger` | highest | solid fill | none | Destructive action |

## Sizes

### Decision

Sizes are declared in an explicit table, one row per size, and each cell is a token reference. A computed rule (base unit times a coefficient) was rejected: real systems do not scale linearly from xs to xl, and an explicit table is readable by a human and convertible by an agent without arithmetic.

Structural dimensions (height, padding, gap, icon size) belong to the theme, not to the invariant kit. Density is a theme choice, as heights differ from one design system to another. Keeping them in the theme also keeps every value in one file, as required by the token reference convention.

### Size table

| Size | Height | Padding inline | Gap | Icon size | Label typography |
|---|---|---|---|---|---|
| `xs` | `{spacing.control-xs}` | `{spacing.sm}` | `{spacing.xs}` | `{spacing.icon-sm}` | `{typography.label-sm}` |
| `s` | `{spacing.control-sm}` | `{spacing.md}` | `{spacing.xs}` | `{spacing.icon-sm}` | `{typography.label-sm}` |
| `m` | `{spacing.control-md}` | `{spacing.lg}` | `{spacing.sm}` | `{spacing.icon-md}` | `{typography.label-md}` |
| `l` | `{spacing.control-lg}` | `{spacing.xl}` | `{spacing.sm}` | `{spacing.icon-lg}` | `{typography.label-lg}` |
| `xl` | `{spacing.control-xl}` | `{spacing.2xl}` | `{spacing.md}` | `{spacing.icon-xl}` | `{typography.label-xl}` |

Geometry rules:

- Height is fixed per size. Content is centered vertically; there is no vertical padding.
- Padding inline applies on both sides. Gap separates icons from the label.
- Icon-only: the container is square, width equals height, padding inline does not apply, the icon is centered.
- Container radius is `{rounded.control}` for every size.
- Icons inherit the content color of the current variant and state.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over the button | Hover container token |
| `focus` | Keyboard focus (focus visible) | Adds the focus ring; never changes container, content, or border |
| `pressed` | Pointer down or key held | Pressed container token |

`focus` combines with `hover` or `pressed`: the ring is drawn on top of their tokens.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `disabled` | No hover, no pressed, not focusable, not activatable | Disabled tokens |
| `loading` | Focusable, no hover, no pressed, not activatable | Enabled tokens; `spinner` replaces visible content |

Precedence: `disabled` overrides `loading`, which overrides interactive states.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). Content covers the label, the icons, and the spinner.

### `filled`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.primary}` | `{colors.on-primary}` | `none` |
| `hover` | `{colors.primary-hover}` | `{colors.on-primary}` | `none` |
| `pressed` | `{colors.primary-pressed}` | `{colors.on-primary}` | `none` |
| `disabled` | `{colors.disabled-container}` | `{colors.on-disabled}` | `none` |
| `loading` | `{colors.primary}` | `{colors.on-primary}` | `none` |

### `tonal`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.primary-container}` | `{colors.on-primary-container}` | `none` |
| `hover` | `{colors.primary-container-hover}` | `{colors.on-primary-container}` | `none` |
| `pressed` | `{colors.primary-container-pressed}` | `{colors.on-primary-container}` | `none` |
| `disabled` | `{colors.disabled-container}` | `{colors.on-disabled}` | `none` |
| `loading` | `{colors.primary-container}` | `{colors.on-primary-container}` | `none` |

### `outlined`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `none` | `{colors.primary}` | `{colors.outline}` |
| `hover` | `{colors.primary-subtle-hover}` | `{colors.primary}` | `{colors.outline}` |
| `pressed` | `{colors.primary-subtle-pressed}` | `{colors.primary}` | `{colors.outline}` |
| `disabled` | `none` | `{colors.on-disabled}` | `{colors.disabled-container}` |
| `loading` | `none` | `{colors.primary}` | `{colors.outline}` |

Border width is `{spacing.border-width}`.

### `text`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `none` | `{colors.primary}` | `none` |
| `hover` | `{colors.primary-subtle-hover}` | `{colors.primary}` | `none` |
| `pressed` | `{colors.primary-subtle-pressed}` | `{colors.primary}` | `none` |
| `disabled` | `none` | `{colors.on-disabled}` | `none` |
| `loading` | `none` | `{colors.primary}` | `none` |

### `danger`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.danger}` | `{colors.on-danger}` | `none` |
| `hover` | `{colors.danger-hover}` | `{colors.on-danger}` | `none` |
| `pressed` | `{colors.danger-pressed}` | `{colors.on-danger}` | `none` |
| `disabled` | `{colors.disabled-container}` | `{colors.on-disabled}` | `none` |
| `loading` | `{colors.danger}` | `{colors.on-danger}` | `none` |

### Focus ring (all variants)

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

## Token contract

The theme must define every token below. The questionnaire asks for them; the generator fails if one is missing.

### Palette scales

Each state color of `primary` and `danger` points to a step of a primitive scale in `colors` (for example a blue scale and a red scale, from lightest to darkest). The scales and the derivation of default, hover, and pressed steps are defined in `docs/conventions.md`. Scale steps are primitives: they are not counted in the totals below, and unused steps are tolerated.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Surface behind the button; background of contrast checks when the container is `none` |
| `colors.primary` | `filled` container; `outlined` and `text` content |
| `colors.on-primary` | Content on `colors.primary` |
| `colors.primary-hover` | `filled` container on hover |
| `colors.primary-pressed` | `filled` container on pressed |
| `colors.primary-container` | `tonal` container |
| `colors.on-primary-container` | Content on `colors.primary-container` |
| `colors.primary-container-hover` | `tonal` container on hover |
| `colors.primary-container-pressed` | `tonal` container on pressed |
| `colors.primary-subtle-hover` | `outlined` and `text` container on hover |
| `colors.primary-subtle-pressed` | `outlined` and `text` container on pressed |
| `colors.danger` | `danger` container |
| `colors.on-danger` | Content on `colors.danger` |
| `colors.danger-hover` | `danger` container on hover |
| `colors.danger-pressed` | `danger` container on pressed |
| `colors.outline` | `outlined` border |
| `colors.disabled-container` | Disabled container; disabled `outlined` border |
| `colors.on-disabled` | Disabled content |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Label for sizes `xs` and `s` |
| `typography.label-md` | Label for size `m` |
| `typography.label-lg` | Label for size `l` |
| `typography.label-xl` | Label for size `xl` |

### Rounded

| Token | Role |
|---|---|
| `rounded.control` | Container radius, all sizes |

### Spacing

| Token | Role |
|---|---|
| `spacing.xs` | Gap for `xs` and `s` |
| `spacing.sm` | Padding inline for `xs`; gap for `m` and `l` |
| `spacing.md` | Padding inline for `s`; gap for `xl` |
| `spacing.lg` | Padding inline for `m` |
| `spacing.xl` | Padding inline for `l` |
| `spacing.2xl` | Padding inline for `xl` |
| `spacing.control-xs` | Height for `xs` |
| `spacing.control-sm` | Height for `s` |
| `spacing.control-md` | Height for `m` |
| `spacing.control-lg` | Height for `l` |
| `spacing.control-xl` | Height for `xl` |
| `spacing.icon-sm` | Icon size for `xs` and `s` |
| `spacing.icon-md` | Icon size for `m` |
| `spacing.icon-lg` | Icon size for `l` |
| `spacing.icon-xl` | Icon size for `xl` |
| `spacing.border-width` | `outlined` border width |
| `spacing.focus-ring-width` | Focus ring width |
| `spacing.focus-ring-offset` | Gap between container and focus ring |

### Components entries (contrast checks)

The DESIGN.md contrast rule checks only the `components` key. The kit therefore declares one entry per variant and per `enabled`, `hover`, and `pressed` state, using only the standard `backgroundColor` and `textColor` properties, and never any other property. `loading` reuses the `enabled` entry because its tokens are identical. `disabled` pairs are never declared in `components`, because WCAG 1.4.3 exempts inactive components and the lint would otherwise flag them; the disabled token mapping stays described in the Token mapping section, and `colors.disabled-container` and `colors.on-disabled` remain in the Colors token contract. When the container is `none`, `backgroundColor` is `{colors.surface}`.

| Entry | backgroundColor | textColor |
|---|---|---|
| `button-filled` | `{colors.primary}` | `{colors.on-primary}` |
| `button-filled-hover` | `{colors.primary-hover}` | `{colors.on-primary}` |
| `button-filled-pressed` | `{colors.primary-pressed}` | `{colors.on-primary}` |
| `button-tonal` | `{colors.primary-container}` | `{colors.on-primary-container}` |
| `button-tonal-hover` | `{colors.primary-container-hover}` | `{colors.on-primary-container}` |
| `button-tonal-pressed` | `{colors.primary-container-pressed}` | `{colors.on-primary-container}` |
| `button-outlined` | `{colors.surface}` | `{colors.primary}` |
| `button-outlined-hover` | `{colors.primary-subtle-hover}` | `{colors.primary}` |
| `button-outlined-pressed` | `{colors.primary-subtle-pressed}` | `{colors.primary}` |
| `button-text` | `{colors.surface}` | `{colors.primary}` |
| `button-text-hover` | `{colors.primary-subtle-hover}` | `{colors.primary}` |
| `button-text-pressed` | `{colors.primary-subtle-pressed}` | `{colors.primary}` |
| `button-danger` | `{colors.danger}` | `{colors.on-danger}` |
| `button-danger-hover` | `{colors.danger-hover}` | `{colors.on-danger}` |
| `button-danger-pressed` | `{colors.danger-pressed}` | `{colors.on-danger}` |
| `button-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

### Totals

| Category | Count |
|---|---|
| Colors | 19 |
| Typography | 4 |
| Rounded | 1 |
| Spacing | 18 |
| Components entries | 16 |

### Non-token requirement

Icon style (for example outlined, filled, or rounded, plus the icon library) is not a token. The theme records it in a free `## Icons` Markdown section of DESIGN.md.

## Accessibility

| Topic | Requirement |
|---|---|
| Role | Native button semantics. If the action navigates, use a link instead. |
| Accessible name | The `label` text. In icon-only, the label is visually hidden but remains the accessible name. |
| Icons | Decorative when the label is visible: hidden from assistive technologies. |
| Focus visible | The focus ring appears on keyboard focus. It must never be removed. |
| Keyboard | `Enter` and `Space` activate the button. `Tab` moves focus to and from it. |
| Disabled | Removed from the tab order, not activatable. |
| Loading | Stays focusable, not activatable, announced as busy; the accessible name does not change. |
| Target size | Hit area at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). For sizes rendered smaller, extend the hit area invisibly. 44 by 44 is recommended on touch screens. |
| Contrast | Text and icons reach at least 4.5:1 against their container. Delegated to the DESIGN.md lint through the `components` entries of the Token contract: each variant and `enabled`, `hover`, `pressed` pair, and `{colors.focus-ring}` against the surface. `disabled` is exempt (WCAG 1.4.3). |

## Behavior

- Activation: fires once per press. While `loading` is true, activation is ignored.
- Loading: the `spinner` is centered and the other visible parts are hidden, but the button keeps its width so the layout does not shift.
- Full width: with `full-width`, the container fills its parent and the content stays centered. Height still follows the size.
- Label: single line, no wrap. If space runs out, the label is truncated with an ellipsis; the accessible name keeps the full text.

## Do and don't

| Do | Don't |
|---|---|
| Use a verb for the label: "Save", "Send" | Use vague labels: "OK", "Click here" |
| Keep one `filled` button per area | Put several `filled` buttons side by side |
| Give every icon-only button an accessible name | Ship an icon-only button without a name |
| Use `disabled` only when the reason is visible nearby | Disable without explaining why |
| Use a link for navigation | Use a button to change page |
| Reserve `danger` for destructive actions | Use `danger` for emphasis only |

## Out of scope

Animations, dark mode, button groups, split buttons, and semantic color variants other than `danger` (such as success or warning) are not covered by this spec.

## Rationale

| Decision | Reason |
|---|---|
| Five sizes `xs` to `xl` | Matches Material 3; Spectrum and Radix use four |
| Two optional icons | Explicit need; Spectrum only offers a leading icon |
| Icon-only as a property | Same approach as Spectrum `isLabelHidden`: variants, states, and tokens stay shared; only geometry changes. Material 3 and Radix use a separate component |
| `loading` as a state property | Present in Spectrum (pending) and Radix (loading) |
| Emphasis variants | Material 3 naming (filled, tonal, outlined, text); Radix uses solid, soft, outline, ghost |
| Explicit state color tokens | Every cell is a real color the lint can check, no opacity rule hidden in the kit |
| `danger` variant | Destructive actions need a distinct, recognizable signal; it has its own tokens and matrix |
| State colors from palette scales | Hover and pressed come from a rule on a primitive scale, so the user only gives a base color |
| Standard-only `components` entries | The lint checks contrast only there; standard properties keep the theme valid and the kit non-intrusive |
