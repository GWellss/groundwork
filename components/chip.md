# Chip

A chip is a compact element that represents an action, a choice to toggle, or a removable item such as a filter value or a recipient. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `leading-icon`, `avatar`, `check-icon`, `label`, `remove-button` |
| Modes | `action` (default), `selectable`, `removable`, derived from two boolean properties |
| Configurations | label only, leading icon + label, avatar + label, each with or without remove button in `removable` mode |
| Variants | none by emphasis; two appearance groups: `default` and `selected` |
| Sizes | `s`, `m` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `selected`, `disabled` |
| Tokens required | 12 colors, 2 typography, 1 rounded, 11 spacing; 3 new colors, the rest reused from the button (see Token contract) |
| Contrast entries | 10 `components` entries, `backgroundColor` and `textColor` only (see Token contract) |

## Purpose

- Use an `action` chip for a contextual, low-emphasis action or a suggestion next to content ("Add to calendar", "Reply: Thanks").
- Use a `selectable` chip to toggle a filter or an option on and off, usually in a group of chips.
- Use a `removable` chip to show a value the user entered or picked (a tag, a recipient, an applied filter) and let them remove it.
- Do not use a chip as the main action of an area: use a `filled` button.
- Do not use a chip for a single choice among exclusive options: use radio buttons or a segmented control.
- Do not use a chip to display a static status: use a badge (not covered by this kit yet).

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | Holds all other parts, carries the fill, the border, and the radius | yes | Always present |
| `label` | Text that names the action, option, or item | yes | Always visible; provides the accessible name |
| `leading-icon` | Icon before the label | no | Decorative |
| `avatar` | Image or initials before the label, identifying a person or an entity | no | Decorative when the label names the entity |
| `check-icon` | Checkmark before the label | no | Shown only when `selected` is true; replaces `leading-icon` |
| `remove-button` | Control after the label that removes the chip | no | Only in `removable` mode; a separate focusable control |

### Configurations

| Configuration | Leading slot | Remove button | Modes | Allowed |
|---|---|---|---|---|
| label-only | none | no | `action`, `selectable` | yes |
| leading-icon-label | `leading-icon` | no | `action`, `selectable` | yes |
| avatar-label | `avatar` | no | `action` | yes |
| label-remove | none | yes | `removable` | yes |
| leading-icon-label-remove | `leading-icon` | yes | `removable` | yes |
| avatar-label-remove | `avatar` | yes | `removable` | yes |
| selectable-avatar | `avatar` | no | `selectable` | no |
| selectable-removable | any | yes | `selectable` | no |
| icon-and-avatar | `leading-icon` and `avatar` | any | any | no |
| no-label | any | any | any | no |

Combination rules:

- The mode is derived from two properties: `action` when `selectable` and `removable` are both false, `selectable` when `selectable` is true, `removable` when `removable` is true. `selectable` and `removable` are never both true.
- The leading slot holds at most one element: `leading-icon`, `avatar`, or `check-icon`.
- In `selectable` mode, `check-icon` replaces `leading-icon` while `selected` is true. Without `leading-icon`, `check-icon` is added before the label.
- `avatar` is not allowed in `selectable` mode, because the leading slot must stay free for `check-icon`.
- A chip always has a visible label. Icon-only chips are not allowed: use an icon-only button.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | Name of the action, option, or item; accessible name |
| `size` | `s`, `m` | `m` | Named dimension set |
| `leading-icon` | icon reference | none | Optional icon before the label |
| `avatar` | image or initials | none | Optional avatar before the label; not allowed with `selectable` |
| `selectable` | `true`, `false` | `false` | The chip toggles on and off |
| `selected` | `true`, `false` | `false` | The option is on; only with `selectable` |
| `removable` | `true`, `false` | `false` | Shows `remove-button`; not allowed with `selectable` |
| `remove-label` | text | "Remove" followed by `label` | Accessible name of `remove-button` |
| `disabled` | `true`, `false` | `false` | The chip and its remove button cannot be activated |

## Variants

The chip has no emphasis variants: a chip is always low emphasis. Its colors come from two appearance groups, used as variant names in the `components` entries.

| Variant | Used by | Container | Border | Intent |
|---|---|---|---|---|
| `default` | `action`, `removable`, and `selectable` with `selected` false | none | yes | Neutral look (dark neutral content, neutral border), neutral feedback on hover and pressed; the brand color is reserved for `selected` |
| `selected` | `selectable` with `selected` true | soft fill | none | The option is on; fill plus `check-icon` |

`remove-button` has its own state colors, declared as the `remove` group in the `components` entries.

## Sizes

### Decision

Two sizes, `s` and `m`, declared in an explicit table like the button. Material 3 has a single chip height and no size range; a second, smaller size covers dense contexts such as tables and toolbars. The `xs` to `xl` range of the button is not imposed (each component declares its own sizes). Every dimension reuses an existing spacing token of the theme, so density applies to chips without new tokens.

### Size table

| Size | Height | Padding inline | Padding next to an element | Gap |
|---|---|---|---|---|
| `s` | `{spacing.control-xs}` | `{spacing.sm}` | `{spacing.xs}` | `{spacing.xs}` |
| `m` | `{spacing.control-sm}` | `{spacing.md}` | `{spacing.sm}` | `{spacing.sm}` |

| Size | Icon size | Avatar size | Remove button size | Label typography |
|---|---|---|---|---|
| `s` | `{spacing.icon-sm}` | `{spacing.icon-md}` | `{spacing.icon-md}` | `{typography.label-sm}` |
| `m` | `{spacing.icon-md}` | `{spacing.icon-lg}` | `{spacing.icon-lg}` | `{typography.label-md}` |

Geometry rules:

- Height is fixed per size. Content is centered vertically; there is no vertical padding.
- Padding inline applies on a side without element. On a side that holds `leading-icon`, `avatar`, `check-icon`, or `remove-button`, the padding is the "padding next to an element" value.
- Gap separates the leading element from the label, and the label from `remove-button`.
- Icon size applies to `leading-icon`, `check-icon`, and the icon inside `remove-button`.
- `avatar` is always clipped to a circle; this is a fixed geometry, not a theme value.
- `remove-button` is a square of the "remove button size", with its icon centered. Its hover and pressed fill is a circle of the same size.
- Container radius is `{rounded.control}` for every size.
- The selected chip keeps the same outer height: its missing border does not change the size of the container.
- Icons inherit the content color of the current group and state.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens of the group |
| `hover` | Pointer over the chip (`action`, `selectable`) or over `remove-button` (`removable`) | Hover container token of the target; content token of the state |
| `focus` | Keyboard focus (focus visible) on the chip or on `remove-button` | Adds the focus ring around the focused element; never changes container, content, or border |
| `pressed` | Pointer down or key held on the same targets as `hover` | Pressed container token of the target; content token of the state |

`focus` combines with `hover` or `pressed`: the ring is drawn on top of their tokens. In `removable` mode the chip body is not interactive: only `remove-button` takes `hover`, `focus`, and `pressed`; the body keeps its `enabled` tokens.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `selected` | None; the chip stays interactive | `selected` group tokens; `check-icon` shown |
| `disabled` | No hover, no pressed, not focusable, not activatable; `remove-button` included | Disabled tokens; a selected chip keeps `check-icon` |

Precedence: `disabled` overrides `selected`, which overrides the `default` group; interactive states apply on top of the resulting group.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). Content covers the label, the icons, and the avatar initials.

### `default`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` | `{colors.outline}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.outline}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` | `{colors.outline}` |
| `disabled` | `none` | `{colors.on-disabled}` | `{colors.disabled-container}` |

Border width is `{spacing.border-width}`. In `removable` mode the body only uses the `enabled` and `disabled` rows.

### `selected`

| State | Container | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.primary-container}` | `{colors.on-primary-container}` | `none` |
| `hover` | `{colors.primary-container-hover}` | `{colors.on-primary-container}` | `none` |
| `pressed` | `{colors.primary-container-pressed}` | `{colors.on-primary-container}` | `none` |
| `disabled` | `{colors.disabled-container}` | `{colors.on-disabled}` | `none` |

### `remove-button`

| State | Fill | Icon |
|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `disabled` | `none` | `{colors.on-disabled}` |

`remove-button` sits on the `default` body, whose container is `none`: its pairs are checked against `{colors.surface}`. On a `selected` chip no `remove-button` exists (`selectable` and `removable` are exclusive).

### `avatar`

The avatar exists only in the `default` group (`action` and `removable` modes). Its fill does not follow the chip interactive states. Initials take the avatar content color; an image covers the fill.

| State | Fill | Initials |
|---|---|---|
| `enabled` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `hover` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `disabled` | `{colors.disabled-container}` | `{colors.on-disabled}` |

- The initials pair is the `chip-default-pressed` pair, already checked: no new `components` entry.
- On `pressed` in `action` mode, the avatar fill equals the chip container. The avatar is decorative and its edge carries no information, so this is accepted.
- Disabled image avatar: the image is shown unchanged; the disabled state is carried by the label and the border. No filter or opacity is defined by the kit.

### Focus ring (chip)

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

### Focus ring (`remove-button`)

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `none` |

- The ring follows the circular shape of `remove-button` and touches its edge (no offset), so that it stays inside the gap next to the label.
- The ring never covers the label. Theme requirement: the gap of each size is at least `{spacing.focus-ring-width}`; it holds with the default values of `theme/questionnaire.md` at every density.
- If a retouched theme breaks this requirement, draw the ring inside `remove-button` (inset) and report it to the user.
- The ring may overlap the chip border on the trailing side; it never overlaps the label or a neighbor chip.

## Token contract

The theme must define every token below. Nine colors already exist in the button token contract; the chip adds three colors (`on-surface`, `neutral-subtle-hover`, `neutral-subtle-pressed`). The existing `colors.outline` suits the neutral border and is reused. The brand tokens `primary`, `primary-subtle-hover`, `primary-subtle-pressed`, and `on-primary-subtle` are no longer used by the chip.

### Palette scales

The backgrounds follow the "Surface scale" case of the Contrast pairs rule of `docs/conventions.md`: surface, neutral step `100`, neutral step `200`. The content follows the Content step search of the same rule (neutral step `700`, `800`, or `900`). Scale steps are primitives: they are not counted in the totals below.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the `default` and `remove` contrast checks, where the container is `none` |
| `colors.on-surface` | New. `default` content, `remove-button` icon, and avatar initials on every state. Neutral step `700`, `800`, or `900`, chosen by the Content step search; one shared token because the darkest background (pressed) decides |
| `colors.neutral-subtle-hover` | New. `default` container and `remove-button` fill on hover. Default: neutral step `100` |
| `colors.neutral-subtle-pressed` | New. `default` container and `remove-button` fill on pressed; avatar fill. Default: neutral step `200` |
| `colors.primary-container` | `selected` container |
| `colors.primary-container-hover` | `selected` container on hover |
| `colors.primary-container-pressed` | `selected` container on pressed |
| `colors.on-primary-container` | `selected` content on every state |
| `colors.outline` | `default` border |
| `colors.disabled-container` | Disabled `selected` container; disabled `default` border; disabled avatar fill |
| `colors.on-disabled` | Disabled content, avatar initials included |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Label for size `s` |
| `typography.label-md` | Label for size `m` |

### Rounded

| Token | Role |
|---|---|
| `rounded.control` | Container radius, all sizes |

### Spacing

| Token | Role |
|---|---|
| `spacing.control-xs` | Height for `s` |
| `spacing.control-sm` | Height for `m` |
| `spacing.icon-sm` | Icon size for `s` |
| `spacing.icon-md` | Icon size for `m`; avatar and remove button size for `s` |
| `spacing.icon-lg` | Avatar and remove button size for `m` |
| `spacing.xs` | Padding next to an element and gap for `s` |
| `spacing.sm` | Padding inline for `s`; padding next to an element and gap for `m` |
| `spacing.md` | Padding inline for `m` |
| `spacing.border-width` | `default` border width |
| `spacing.focus-ring-width` | Focus ring width; minimum gap next to `remove-button` |
| `spacing.focus-ring-offset` | Gap between the chip and its focus ring; not used by `remove-button` |

### Components entries (contrast checks)

One entry per group and per `enabled`, `hover`, and `pressed` state, plus the focus ring, using only the standard `backgroundColor` and `textColor` properties. `disabled` pairs are never declared (WCAG 1.4.3 exemption, see `docs/conventions.md`). When the container is `none`, `backgroundColor` is `{colors.surface}`. Some pairs equal button pairs; the chip still declares its own entries so that the contrast report names the chip and a theme stays valid whatever components it includes.

| Entry | backgroundColor | textColor |
|---|---|---|
| `chip-default` | `{colors.surface}` | `{colors.on-surface}` |
| `chip-default-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `chip-default-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `chip-selected` | `{colors.primary-container}` | `{colors.on-primary-container}` |
| `chip-selected-hover` | `{colors.primary-container-hover}` | `{colors.on-primary-container}` |
| `chip-selected-pressed` | `{colors.primary-container-pressed}` | `{colors.on-primary-container}` |
| `chip-remove` | `{colors.surface}` | `{colors.on-surface}` |
| `chip-remove-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `chip-remove-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `chip-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

### Totals

| Category | Count | Reused from the button | New |
|---|---|---|---|
| Colors | 12 | 9 | 3 |
| Typography | 2 | 2 | 0 |
| Rounded | 1 | 1 | 0 |
| Spacing | 11 | 11 | 0 |
| Components entries | 10 | 0 | 10 |

### Non-token requirement

Icon style and library come from the `## Icons` section of DESIGN.md, as for the button. `check-icon` uses the library's checkmark and `remove-button` its close icon.

## Accessibility

| Topic | Requirement |
|---|---|
| Role, `action` | Native button semantics. |
| Role, `selectable` | Toggle button: native button semantics with a pressed state that reflects `selected` (`aria-pressed`). A group of selectable chips sits in a container with a group role and a visible or accessible group label. |
| Role, `removable` | The chip body is static text, not focusable. `remove-button` is a native button, a distinct focusable control. |
| Accessible name | Chip: the `label` text. `remove-button`: `remove-label`, which names the item ("Remove Paris"), never a bare "Remove" or "X". |
| Icons and avatar | `leading-icon`, `check-icon`, and `avatar` are hidden from assistive technologies; the selection is announced by the pressed state, not by `check-icon`. |
| Selection not by color alone | `selected` is shown by the fill and by `check-icon` (WCAG 1.4.1). |
| Focus visible | The focus ring appears on keyboard focus, around the chip or around `remove-button`. It must never be removed. |
| Keyboard | `Enter` and `Space` activate an `action` chip, toggle a `selectable` chip, and activate `remove-button`. `Tab` moves focus between interactive chips and remove buttons. `Delete` and `Backspace` on a focused `remove-button` also remove the chip. |
| Disabled | Removed from the tab order, not activatable; `remove-button` included. |
| Target size | Hit area at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8), for the chip and for `remove-button` separately. When `remove-button` is rendered smaller, extend its hit area invisibly, without overlapping the hit area of a neighbor. 44 by 44 is recommended on touch screens. |
| Contrast | Text and icons reach at least 4.5:1 against their container. Delegated to the DESIGN.md lint through the `components` entries of the Token contract. `hover` and `pressed` stay visually distinct from `enabled` and from each other; contrast is reached by adjusting the content, never by merging states. `disabled` is exempt (WCAG 1.4.3). |

## Behavior

- Toggle: activating a `selectable` chip flips `selected` and shows or hides `check-icon`. The chip width may grow by the size of `check-icon` and the gap when it has no `leading-icon`.
- Removal: activating `remove-button` removes the chip. Focus then moves to the next chip's remove button, otherwise the previous one, otherwise the field or the control that created the chips. Focus is never lost to the page.
- Removal is announced to assistive technologies (for example "Paris removed").
- Label: single line, no wrap. If space runs out, the label is truncated with an ellipsis; the accessible name keeps the full text.
- Groups: chips in a group wrap onto several lines; they do not scroll horizontally unless the layout requires it.

## Do and don't

| Do | Don't |
|---|---|
| Keep labels short: one to three words | Write sentences in a chip |
| Name the item in the remove button: "Remove Paris" | Leave the remove button unnamed or named "X" |
| Use `selectable` chips for independent on and off filters | Use chips for a single exclusive choice |
| Show the selection with fill and checkmark | Rely on color alone to show selection |
| Use a button for the main action of an area | Use a chip as the main call to action |
| Keep one mode per chip | Make a chip both selectable and removable |

## Out of scope

Animations, dark mode, single-choice chip sets, arrow-key navigation inside a chip group, editable chips, chips that are both selectable and removable, read-only display tags, and semantic color variants (success, warning, danger) are not covered by this spec.

## Rationale

| Decision | Reason |
|---|---|
| Two booleans instead of four types | Material 3 has four types (assist, filter, input, suggestion), but assist and suggestion differ only in intent, not in anatomy or behavior. `selectable` and `removable` cover filter and input; their absence covers assist and suggestion. Spectrum also models its Tag with booleans (`isRemovable`, `isDisabled`) |
| `selectable` and `removable` exclusive | Two competing targets on a small control; Material 3 shows the remove icon only on input chips, not on filter chips |
| Remove button as a separate focusable control | It has its own action and its own accessible name; merging it with the body would hide the removal from keyboard and screen reader users |
| Removable body not interactive | Keeps a single target per chip; editing an input chip is out of scope |
| Toggle semantics for `selectable` | A filter chip is an on and off control; a pressed state is the standard way to expose it |
| `check-icon` mandatory when selected | WCAG 1.4.1 forbids conveying selection by color alone; Material 3 filter chips show a leading checkmark |
| No avatar on `selectable` | The leading slot is needed for `check-icon`; an avatar swapped for a checkmark would lose the identity it shows |
| Sizes `s` and `m` only | Material 3 has a single height (32dp minimum); `m` maps to the second control height of the theme, `s` adds a dense option. A five-size range has no use for chips |
| Neutral `default` group | A chip that is off must not look like a chip that is on: the brand color is reserved for `selected`, which also removes any confusion between hover and selected |
| New `neutral-subtle-hover` and `neutral-subtle-pressed` | No existing token is a neutral fill for hover and pressed; the brand subtle tokens would tint the off state. Surface is neutral step 50, so the "Surface scale" case of the Contrast pairs rule gives surface, step 100, step 200 |
| New `on-surface` | No existing token is a dark neutral content color for text on the surface; `{colors.on-disabled}` is for disabled only. One token serves all states, as the Contrast pairs rule prefers |
| `colors.outline` reused | It is already the neutral border of the outlined button |
| `selected` reuses the tonal tokens | Steps 50, 100, 200 are the only `light` triple; steps 300 and above are `intermediate` and carry no text |
| Own `components` entries despite equal pairs | The contrast report names the chip, and each spec lists its own entries, so a theme stays valid whatever components it includes |
| Radius `{rounded.control}` | Chips match buttons, and a chip is always a single line, so every corner style, pill included, keeps a regular shape |
| Avatar fill `{colors.neutral-subtle-pressed}`, initials `{colors.on-surface}` | Reuses existing tokens: the pair is already checked as `chip-default-pressed`, and step `200` stays visible on the surface and on the hover container. Without a defined fill, generated code invented a color |
| Avatar fill constant across interactive states | The avatar identifies an entity; changing its fill on hover adds no feedback the container does not already give |
| `remove-button` ring without offset | With the shared offset, the ring would reach into the gap and could cover the label at small sizes or compact density |
