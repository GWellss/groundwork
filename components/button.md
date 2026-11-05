# Button

A button triggers an action when activated. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `label`, `leading-icon`, `trailing-icon`, `spinner` |
| Configurations | label only, leading icon + label, label + trailing icon, both icons + label, icon-only; floating: icon-only or leading icon + label (extended) |
| Variants | `filled`, `tonal`, `outlined`, `text`, `danger`; floating: `filled`, `tonal` only |
| Sizes | `xs`, `s`, `m`, `l`, `xl`; floating: `l`, `xl` only |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `disabled`, `loading` |
| Behavior options | `full-width`, `floating` |
| Elevation | `level-0`; floating: `level-3` at rest, `level-4` on hover (not a token, see Token contract) |
| Tokens required | 20 colors, 4 typography, 1 rounded, 18 spacing (see Token contract) |
| Contrast entries | 16 `components` entries, `backgroundColor` and `textColor` only (see Token contract) |

## Purpose

- Use a button to trigger an action in place: submit, save, open, confirm, cancel.
- Do not use a button to navigate to another page: use a link.
- The variant expresses emphasis. One screen area should have at most one `filled` button.
- Use `danger` for a destructive action (delete, remove, discard). It is not an emphasis level: it signals risk.
- Use `floating` for the single most important constructive action of a screen, kept reachable while the content scrolls (create, compose). Do not use it for secondary or destructive actions.

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

### Floating configurations

`floating` is a property of the same component, like `icon-only`: it combines with a base configuration and changes elevation, allowed variants, and allowed sizes. Tokens and states stay shared.

| Configuration | Base configuration | Allowed |
|---|---|---|
| floating-icon-only | icon-only | yes |
| floating-extended | leading-icon-label | yes |
| floating-label-only | label-only | no |
| floating-trailing-icon | label-trailing-icon or leading-icon-label-trailing-icon | no |

Floating combination rules:

- A floating button always shows an icon in the `leading-icon` slot: the icon keeps the action recognizable at a glance over any content.
- `trailing-icon` is not allowed with `floating`: a trailing icon reads as a menu or navigation cue, which a floating action is not.
- `full-width` is not allowed with `floating`: a floating button never fills its parent.
- Only `filled` and `tonal` are allowed with `floating` (see Variants), and only sizes `l` and `xl` (see Sizes).

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `variant` | `filled`, `tonal`, `outlined`, `text`, `danger` | `filled` | Emphasis level, or destructive action for `danger` |
| `size` | `xs`, `s`, `m`, `l`, `xl` | `m`; `l` when `floating` is true | Named dimension set; `l` or `xl` only when `floating` is true |
| `label` | text | none, required | Action name; accessible name |
| `leading-icon` | icon reference | none | Optional icon before the label |
| `trailing-icon` | icon reference | none | Optional icon after the label; not allowed with `icon-only` |
| `icon-only` | `true`, `false` | `false` | Hides the label visually; requires `leading-icon` |
| `disabled` | `true`, `false` | `false` | Button cannot be activated |
| `loading` | `true`, `false` | `false` | Action in progress; button cannot be activated |
| `full-width` | `true`, `false` | `false` | Container fills the width of its parent; not allowed with `floating` |
| `floating` | `true`, `false` | `false` | Button floats above the content, resting at `level-3`; requires `leading-icon`, `filled` or `tonal`, size `l` or `xl` |

## Variants

| Variant | Emphasis | Container | Border | Typical use |
|---|---|---|---|---|
| `filled` | highest | solid fill | none | Main action of an area |
| `tonal` | high | soft fill | none | Important action next to a `filled` one |
| `outlined` | medium | none | yes | Secondary action |
| `text` | low | none | none | Tertiary or inline action |
| `danger` | highest | solid fill | none | Destructive action |

Variants with `floating`:

| Variant | Allowed with `floating` | Reason |
|---|---|---|
| `filled` | yes | Default floating look: the solid fill stands out over any content |
| `tonal` | yes | Softer floating look; its fill still covers the content behind |
| `outlined` | no | No fill: the content behind would show through the container and break the contrast pair, which is checked against `{colors.surface}` |
| `text` | no | Same reason as `outlined`, with no border to outline the shape |
| `danger` | no | A floating button is the most prominent action of a screen; a destructive action must not be the one kept always at hand |

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

Spinner:

| Dimension | Value |
|---|---|
| `spinner-size` | Icon size of the button size (size table above) |
| `spinner-stroke` | `{spacing.focus-ring-width}` |
| `spinner-color` | Content color of the current variant and state |
| `spinner-shape` | An open circular arc (a ring with a gap), inside a square of `spinner-size` |

- The spinner is drawn by the implementation; it is not an icon of the `## Icons` library.
- It is centered in the container, in every configuration, icon-only included.

Floating sizes:

| Size | Allowed with `floating` |
|---|---|
| `xs` | no |
| `s` | no |
| `m` | no |
| `l` | yes, default |
| `xl` | yes |

Floating geometry rules:

- Sizes and their tokens are those of the size table: no new dimension.
- Floating icon-only follows the icon-only rule: square container, width equals height. With `{rounded.control}` it is a circle when the corner style is pill, a rounded square otherwise.
- Floating extended follows the size table like any labeled button, with the same radius.
- Position (corner, distance to the viewport edge, behavior on scroll) belongs to the page layout, not to this component.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over the button | Hover container token; content token of the state |
| `focus` | Keyboard focus (focus visible) | Adds the focus ring; never changes container, content, or border |
| `pressed` | Pointer down or key held | Pressed container token; content token of the state |

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
| `hover` | `{colors.primary-subtle-hover}` | `{colors.on-primary-subtle}` | `{colors.outline}` |
| `pressed` | `{colors.primary-subtle-pressed}` | `{colors.on-primary-subtle}` | `{colors.outline}` |
| `disabled` | `none` | `{colors.on-disabled}` | `{colors.disabled-container}` |
| `loading` | `none` | `{colors.primary}` | `{colors.outline}` |

Border width is `{spacing.border-width}`.

### `text`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `none` | `{colors.primary}` | `none` |
| `hover` | `{colors.primary-subtle-hover}` | `{colors.on-primary-subtle}` | `none` |
| `pressed` | `{colors.primary-subtle-pressed}` | `{colors.on-primary-subtle}` | `none` |
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

### Elevation

A button without `floating` is at `level-0` in every state. A floating button uses the `filled` or `tonal` color tables above, plus the elevation below. Cell vocabulary: a level name.

| State | Elevation |
|---|---|
| `enabled` | `level-3` |
| `hover` | `level-4` |
| `pressed` | `level-3` |
| `disabled` | `level-3` |
| `loading` | `level-3` |

- At rest, the floating button is at `level-3`. On hover it rises one level, to `level-4`, an interaction level.
- `pressed` returns to `level-3`: the press reads as pushing the button back toward its resting height. `level-5` is reserved for drag.
- `disabled` and `loading` have no hover, so they stay at the resting `level-3`: the button still floats above the scrolling content.
- `focus` adds the focus ring and never changes elevation.

## Token contract

The theme must define every token below. The questionnaire asks for them; the generator fails if one is missing.

### Palette scales

Each state color of `primary` and `danger` points to a step of a primitive scale in `colors` (for example a blue scale and a red scale, from lightest to darkest). The scales, the derivation of default, hover, and pressed steps, and the contrast pair rule (background families, state changes, content step search) are defined in `docs/conventions.md`. Scale steps are primitives: they are not counted in the totals below, and unused steps are tolerated.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Surface behind the button; background of contrast checks when the container is `none` |
| `colors.primary` | `filled` container; `outlined` and `text` content on `enabled` and `loading` |
| `colors.on-primary` | Content on `colors.primary` |
| `colors.primary-hover` | `filled` container on hover |
| `colors.primary-pressed` | `filled` container on pressed |
| `colors.primary-container` | `tonal` container |
| `colors.on-primary-container` | `tonal` content on every state; shared by the enabled, hover, and pressed containers |
| `colors.primary-container-hover` | `tonal` container on hover |
| `colors.primary-container-pressed` | `tonal` container on pressed |
| `colors.primary-subtle-hover` | `outlined` and `text` container on hover |
| `colors.primary-subtle-pressed` | `outlined` and `text` container on pressed |
| `colors.on-primary-subtle` | `outlined` and `text` content on hover and pressed; shared by both subtle containers |
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
| `spacing.icon-sm` | Icon and spinner size for `xs` and `s` |
| `spacing.icon-md` | Icon and spinner size for `m` |
| `spacing.icon-lg` | Icon and spinner size for `l` |
| `spacing.icon-xl` | Icon and spinner size for `xl` |
| `spacing.border-width` | `outlined` border width; reserved, transparent, on the other variants (see `docs/implementation.md`) |
| `spacing.focus-ring-width` | Focus ring width; spinner stroke |
| `spacing.focus-ring-offset` | Gap between container and focus ring |

### Components entries (contrast checks)

The DESIGN.md contrast rule checks only the `components` key. The kit therefore declares one entry per variant and per `enabled`, `hover`, and `pressed` state, using only the standard `backgroundColor` and `textColor` properties, and never any other property. `loading` reuses the `enabled` entry because its tokens are identical. `disabled` pairs are never declared in `components`, because WCAG 1.4.3 exempts inactive components and the lint would otherwise flag them; the disabled token mapping stays described in the Token mapping section, and `colors.disabled-container` and `colors.on-disabled` remain in the Colors token contract. When the container is `none`, `backgroundColor` is `{colors.surface}`. Every pair follows the contrast pair rule of `docs/conventions.md`: the backgrounds of `enabled`, `hover`, and `pressed` stay distinct, and the content token adapts to them, never the reverse. A floating button adds no entry: its `filled` and `tonal` pairs are those of `button-filled` and `button-tonal`.

| Entry | backgroundColor | textColor |
|---|---|---|
| `button-filled` | `{colors.primary}` | `{colors.on-primary}` |
| `button-filled-hover` | `{colors.primary-hover}` | `{colors.on-primary}` |
| `button-filled-pressed` | `{colors.primary-pressed}` | `{colors.on-primary}` |
| `button-tonal` | `{colors.primary-container}` | `{colors.on-primary-container}` |
| `button-tonal-hover` | `{colors.primary-container-hover}` | `{colors.on-primary-container}` |
| `button-tonal-pressed` | `{colors.primary-container-pressed}` | `{colors.on-primary-container}` |
| `button-outlined` | `{colors.surface}` | `{colors.primary}` |
| `button-outlined-hover` | `{colors.primary-subtle-hover}` | `{colors.on-primary-subtle}` |
| `button-outlined-pressed` | `{colors.primary-subtle-pressed}` | `{colors.on-primary-subtle}` |
| `button-text` | `{colors.surface}` | `{colors.primary}` |
| `button-text-hover` | `{colors.primary-subtle-hover}` | `{colors.on-primary-subtle}` |
| `button-text-pressed` | `{colors.primary-subtle-pressed}` | `{colors.on-primary-subtle}` |
| `button-danger` | `{colors.danger}` | `{colors.on-danger}` |
| `button-danger-hover` | `{colors.danger-hover}` | `{colors.on-danger}` |
| `button-danger-pressed` | `{colors.danger-pressed}` | `{colors.on-danger}` |
| `button-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

### Totals

| Category | Count |
|---|---|
| Colors | 20 |
| Typography | 4 |
| Rounded | 1 |
| Spacing | 18 |
| Components entries | 16 |

### Non-token requirement

Icon style (for example outlined, filled, or rounded, plus the icon library) is not a token. The theme records it in a free `## Icons` Markdown section of DESIGN.md.

Elevation is not a token either. A floating button uses `level-3` at rest and `level-4` on hover, from the elevation table in the `## Elevation & Depth` section of DESIGN.md (see Elevation in `docs/conventions.md`); it is not counted in the totals.

## Accessibility

| Topic | Requirement |
|---|---|
| Role | Native button semantics. If the action navigates, use a link instead. |
| Accessible name | The `label` text. In icon-only, the label is visually hidden but remains the accessible name. |
| Icons | Decorative when the label is visible: hidden from assistive technologies. |
| Focus visible | The focus ring appears on keyboard focus. It must never be removed. |
| Keyboard | `Enter` and `Space` activate the button. `Tab` moves focus to and from it. |
| Disabled | Removed from the tab order, not activatable. |
| Loading | Stays focusable, not activatable, announced as busy (`aria-busy`); not native disabled, which would remove focus. The accessible name does not change and stays exposed. |
| Loading, hidden parts | The label and icons are hidden visually only: they keep their space and stay in the accessibility tree. A method that removes the label from the accessibility tree is not allowed. The spinner is decorative and hidden from assistive technologies. |
| Target size | Hit area at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). For sizes rendered smaller, extend the hit area invisibly. 44 by 44 is recommended on touch screens; it is required for a floating button, whose hit area is extended invisibly when its size renders smaller. |
| Floating, accessible name | Floating icon-only: the visually hidden `label` is mandatory and names the action ("Compose"). Floating extended: the visible label is the name. A tooltip may repeat the name but never replaces it. |
| Floating, focus order | The floating button sits in the focus order where its action belongs in the reading order of the screen, usually after the content it acts on. Its visual position never changes its place in the focus order, and it is never forced first. |
| Floating, content not hidden | It never permanently hides essential content or controls: the layout leaves room at the end of the scroll area so the last content can scroll out from under it, and a focused element is never hidden behind it (WCAG 2.2 criterion 2.4.11). |
| Contrast | Text and icons reach at least 4.5:1 against their container. Delegated to the DESIGN.md lint through the `components` entries of the Token contract: each variant and `enabled`, `hover`, `pressed` pair, and `{colors.focus-ring}` against the surface. `hover` and `pressed` stay visually distinct from `enabled` and from each other; contrast is reached by adjusting the content, never by merging states. `disabled` is exempt (WCAG 1.4.3). |

## Behavior

- Activation: fires once per press. While `loading` is true, activation is ignored.
- Loading: the `spinner` is centered and the other visible parts are hidden, but the button keeps its width so the layout does not shift.
- Spinner motion: the spinner rotates continuously, one full turn per `spinner-turn` (behavior constant below), at constant speed, for as long as `loading` is true.
- Reduced motion: when the user asks the platform for reduced motion, the rotation stops and the arc stays visible, static. The busy state still announces the loading.

| Constant | Value | Meaning |
|---|---|---|
| `spinner-turn` | 1000 ms | Duration of one full turn of the spinner; invariant, not a theme token |
- Full width: with `full-width`, the container fills its parent and the content stays centered. Height still follows the size.
- Label: single line, no wrap. If space runs out, the label is truncated with an ellipsis; the accessible name keeps the full text.
- Floating: at most one floating button per screen. It rests at `level-3` and rises to `level-4` on hover only; hover and pressed feedback still comes first from the color tokens, as for any button. Its position is set by the page layout.

## Do and don't

| Do | Don't |
|---|---|
| Use a verb for the label: "Save", "Send" | Use vague labels: "OK", "Click here" |
| Keep one `filled` button per area | Put several `filled` buttons side by side |
| Give every icon-only button an accessible name | Ship an icon-only button without a name |
| Use `disabled` only when the reason is visible nearby | Disable without explaining why |
| Use a link for navigation | Use a button to change page |
| Reserve `danger` for destructive actions | Use `danger` for emphasis only |
| Keep one floating button for the main constructive action of a screen | Stack several floating buttons, or float a destructive action |
| Leave room under a floating button so the last content can scroll into view | Let a floating button cover content or a focused control |

## Out of scope

Animations other than the spinner rotation, dark mode, button groups, split buttons, semantic color variants other than `danger` (such as success or warning), floating button menus (speed dial), extended floating buttons that collapse to icon-only on scroll, and the placement of the floating button on the page are not covered by this spec; contrast is checked only against `{colors.surface}`, so on an image or a dark background the user retouches the floating button colors after generation.

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
| Content darkens on `outlined` and `text` hover and pressed | The tinted hover and pressed backgrounds are `light` steps, which carry only steps `700` to `900`; keeping `{colors.primary}` would fail 4.5:1 or force the pressed background back to the hover one, hiding the press feedback |
| Content adjusts to the background, also on `tonal` | The rule "the content adjusts to the background, never the reverse" applies to `tonal` as well, not only to `outlined` and `text`: `{colors.on-primary-container}` is searched in steps `700`, `800`, then `900` against the `50`, `100`, and `200` backgrounds, and the backgrounds stay fixed |
| One shared `{colors.on-primary-subtle}` | One token is computed against the darker of the two subtle backgrounds, so it is valid for both; a token per state would add a color for no visible gain |
| Standard-only `components` entries | The lint checks contrast only there; standard properties keep the theme valid and the kit non-intrusive |
| Floating as a property, not a component | User decision, same approach as icon-only: variants, states, and tokens stay shared; only elevation, allowed variants, and allowed sizes change. Material 3 uses a separate FAB component |
| Floating icon-only and extended | Material 3 offers both the FAB and the extended FAB; both map to existing configurations of the button |
| Floating `filled` and `tonal` only | A floating button covers content, so it needs its own fill; Material 3 FAB colors are filled containers. `danger` is excluded so a destructive action is never the one always at hand |
| Floating sizes `l` and `xl` only | A floating button is the main action and is often used on touch; Material 3 FAB is 56dp by default, larger than a standard button, and `l` and `xl` are the closest control heights |
| Floating at `level-3` at rest, `level-4` on hover | Material 3 FAB: resting level 3, raised one level on hover; `level-3` is the highest resting level of the scale |
| Floating `pressed` at `level-3` | Material 3 FAB pressed returns to its resting level (unverified against the current Material 3 spec); `level-5` stays reserved for drag |
| Floating `disabled` and `loading` at `level-3` | Neither state has hover, so both keep the resting level; the button keeps floating above the content. Material 3 FAB has no disabled state, so this is a kit decision |
| No new `components` entry for floating | The floating colors are the `filled` and `tonal` pairs, already declared |
| Spinner size and stroke from existing tokens | The icon size keeps the spinner in proportion with the content it replaces; `{spacing.focus-ring-width}` gives a visible stroke at icon sizes, where `{spacing.border-width}` is too thin, without a new token |
| Spinner stops under reduced motion | Continuous rotation is motion the user asked to avoid; the busy state and the visible arc still convey loading |
| `spinner-turn` as a behavior constant | Same reason as the tooltip delays: DESIGN.md has no duration token type, and the speed serves usability, not brand identity |
| `aria-busy` instead of native disabled for `loading` | Native disabled removes focus, which the Loading requirement keeps; the style reads the same attribute, so there is one source of truth |
