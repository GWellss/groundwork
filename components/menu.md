# Menu

A menu is a short list of commands or settings that opens from a trigger button, on top of the page, and closes once the user has chosen. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme. The menu is a floating surface: look, placement, and opening and closing follow "Floating surface" in `docs/conventions.md`; this spec states what is specific to a menu.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `item`, `leading-icon`, `check-icon`, `dot`, `label`, `shortcut`, `group`, `group-title`, `separator` |
| Configurations | a flat list, or groups with optional titles and separators; items that run an action or are checkable |
| Item kinds | `action`, `checkbox`, `radio` |
| Variants | `default`, `danger` (for an item) |
| Sizes | none named; one item size, one minimum width, one maximum width |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` (for an item); visibility states `closed`, `open` |
| State properties | `disabled`, `checked` |
| Elevation | `level-2` when `open` (not a token, see Token contract) |

## Purpose

- Use a menu for a short list of commands tied to a trigger: "Rename", "Duplicate", "Delete".
- Use checkable items for settings the user flips or picks from the menu itself ("Show grid", "Sort by name").
- Use a select to choose a value that a form submits (see `components/select.md`). A menu runs commands, a select picks a value.
- Use a popover for free content such as text, a form, or buttons laid out freely (see `components/popover.md`).
- Do not use a menu for two or three actions the page has room to show: use buttons.
- Do not use a menu to move between pages: use links or tabs.
- Do not open a menu on hover: the trigger is activated.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | The floating panel that holds the items | yes | Carries fill, border, radius, elevation; role `menu` |
| `item` | One command or one checkable setting | yes | At least one; the whole row is the click target |
| `leading-icon` | Decorative icon before the label | no | Only on an `action` item |
| `check-icon` | Checkmark before the label | when `checked` | Only on a `checkbox` item; the library checkmark |
| `dot` | Filled circle before the label | when `checked` | Only on a `radio` item |
| `label` | Names the command | yes | Plain text; provides the accessible name |
| `shortcut` | The keyboard shortcut that does the same thing | no | Display only; at the end of the row |
| `group` | A set of related items | no | Role `group`, named by `group-title` |
| `group-title` | Names a group | no | Not focusable; not an item |
| `separator` | Line between two groups | no | A divider (see `components/divider.md`) |

The trigger is a button (see `components/button.md`). It is not a part of the menu.

### Configurations

| Configuration | Content | Allowed |
|---|---|---|
| flat | `item` rows only | yes |
| grouped | `group` blocks, each with an optional `group-title`, separated by `separator` | yes |
| checkable | `checkbox` or `radio` items, alone or mixed with `action` items | yes |
| empty | no `item` | no |
| icon-and-check | `leading-icon` and a checkable mark on the same item | no |
| nested | an item that opens another menu (submenu) | no |
| interactive-content | an input, a button, or a link inside the container | no |

Combination rules:

- An item has at most one leading element: a `leading-icon` (`action`), a `check-icon` (`checkbox`), or a `dot` (`radio`).
- When any item of a menu has a leading element, every item reserves the same leading space, so labels stay aligned.
- `radio` items always sit in a `group`: one group is one exclusive set, and exactly one of its items is checked.
- A `separator` sits between two groups; it is never the first or the last child.
- A `group-title` is optional. A group without a title still has an accessible name (`aria-label`).
- A `danger` item is placed last in its group, after a separator when the menu has other groups.
- `shortcut` shows a shortcut that the project binds elsewhere; the menu itself binds no key.

## Properties

Menu:

| Property | Values | Default | Description |
|---|---|---|---|
| `placement` | `top`, `right`, `bottom`, `left` | `bottom` | Preferred side of the trigger; flips if space runs out |
| `align` | `start`, `center`, `end` | `start` | Alignment along that side |

Item:

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | The command; accessible name |
| `kind` | `action`, `checkbox`, `radio` | `action` | What activating the item does |
| `checked` | `true`, `false` | `false` | The setting is on; only with `checkbox` or `radio` |
| `leading-icon` | icon reference | none | Only with `action` |
| `shortcut` | text | none | Display text such as "Ctrl+C" |
| `variant` | `default`, `danger` | `default` | `danger` marks a destructive command |
| `disabled` | `true`, `false` | `false` | Not activatable |

## Variants

The variant applies to an item, not to the menu.

| Variant | Content color | Intent |
|---|---|---|
| `default` | `{colors.on-surface}` | Any command or setting |
| `danger` | `{colors.danger}` | A command that deletes or cannot be undone; the label says so too |

## Sizes

### Decision

The menu has no named sizes. Every item has the same dimensions, and the panel has a minimum and a maximum width. Item height, padding, gap, and icons reuse control and spacing tokens, so density applies. Two spacing tokens are new: the minimum and the maximum width.

### Size table

| Dimension | Token |
|---|---|
| `item-min-height` | `{spacing.control-sm}` |
| `item-padding-inline` | `{spacing.md}` |
| `item-gap` | `{spacing.sm}` |
| `icon-size` | `{spacing.icon-md}` |
| `label-typography` | `{typography.label-md}` |

| Dimension | Token |
|---|---|
| `shortcut-typography` | `{typography.label-sm}` |
| `group-title-typography` | `{typography.label-sm}` |
| `container-padding-block` | `{spacing.xs}` |
| `min-width` | `{spacing.menu-min-width}` |
| `max-width` | `{spacing.floating-max-width}` |

Geometry rules:

- Items span the whole width of `container`; `container` clips the corners. Its radius is `{rounded.overlay}`.
- Width follows the widest row, between `min-width` and `max-width`. The border is reserved (`{spacing.border-width}`).
- `item-min-height` is the outer height of a one-line item. A `label` that exceeds the width wraps and the item grows; text is never truncated. `shortcut` never wraps.
- The leading space is `icon-size` wide, followed by `item-gap`. `leading-icon` and `check-icon` fill it; `dot` is `{spacing.sm}` wide (as the radio button dot) and centered in it.
- Between `label` and `shortcut` there is at least `{spacing.lg}`; `shortcut` aligns to the end.
- `group-title` has `item-padding-inline` and a padding block of `{spacing.xs}`.
- `separator` is a horizontal divider, `subtle`, not inset, with `{spacing.xs}` of space above and below.
- Placement, offset, and viewport padding: see "Floating surface" in `docs/conventions.md`.

## States

### Interactive states

For an item. `group-title` and `separator` have none.

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over the item | The fill gets the hover color; the content follows (see Token mapping) |
| `focus` | The item holds keyboard focus (focus visible) | Adds the focus ring inside the item; never changes fill or content |
| `pressed` | Pointer down or `Enter` or `Space` held on the item | The fill gets the pressed color |

`focus` combines with `hover` and `pressed`. The ring is drawn inside the item, because `container` clips what lies beyond its box. Hover does not move keyboard focus: the pointer and the keyboard may point at two different items.

Visibility states of the menu: `closed` (not rendered) and `open` (rendered, `level-2`).

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `checked` | None; the item stays activatable | `check-icon` or `dot` shown; the fill does not change |
| `disabled` | No hover, no pressed, not activatable; still reachable by the arrow keys | Disabled tokens; the focus ring still shows on keyboard focus |

Precedence: `disabled` overrides `hover` and `pressed`. `focus` applies on top of every state.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border).

### `default` item

| State | Fill | Label, icons, marks | Shortcut |
|---|---|---|---|
| `enabled` | `{colors.surface}` | `{colors.on-surface}` | `{colors.on-surface-muted}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` | `{colors.on-surface}` |

The shortcut is quieter than the label at rest, on the surface only. On a grayed fill it takes `{colors.on-surface}`, never `{colors.on-surface-muted}`.

### `danger` item

| State | Fill | Label, icons, marks, shortcut |
|---|---|---|
| `enabled` | `{colors.surface}` | `{colors.danger}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.danger-hover}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.danger-pressed}` |

The danger content darkens as its fill darkens, like a link: `danger` reaches 4.5:1 on the surface only, so on the grayed fills it takes the darker steps of the State colors rule.

### Container and text parts

| Part | Token |
|---|---|
| `container` fill | `{colors.surface}` |
| `container` border | `{colors.neutral-subtle-pressed}` |
| `group-title` | `{colors.on-surface-muted}` |
| `separator` | `{colors.neutral-subtle-pressed}` (divider `subtle`) |

`group-title` sits on the surface and is never hovered, so the muted color is allowed.

### `disabled`

| Part | Token |
|---|---|
| Fill | `none` (the surface shows through; it never changes) |
| Label, icons, marks, shortcut | `{colors.on-disabled}` |

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `none` (drawn inside the item) |

### Elevation

`container` is at `level-2` when `open`; `closed` is not rendered. Items have no elevation.

## Token contract

The theme must define every token below. The menu adds no color and two spacing tokens.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | `container` and item fill at rest |
| `colors.on-surface` | Label, icons, marks; shortcut on a grayed fill |
| `colors.on-surface-muted` | `group-title`; `shortcut` at rest, on the surface only |
| `colors.danger` | `danger` content at rest |
| `colors.danger-hover` | `danger` content on hover |
| `colors.danger-pressed` | `danger` content on pressed |
| `colors.neutral-subtle-hover` | Item hover fill |
| `colors.neutral-subtle-pressed` | Item pressed fill; `container` border; `separator` |
| `colors.on-disabled` | Disabled content |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-md` | `label` |
| `typography.label-sm` | `shortcut`, `group-title` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | `container` radius |

### Spacing

| Token | Role | New |
|---|---|---|
| `spacing.control-sm` | Item minimum height | no |
| `spacing.icon-md` | Icon size and leading space | no |
| `spacing.xs` | Container padding block; separator space; group-title padding block; offset | no |
| `spacing.sm` | Item gap; `dot` size; viewport padding | no |
| `spacing.md` | Item padding inline | no |
| `spacing.lg` | Minimum space between `label` and `shortcut` | no |
| `spacing.border-width` | Container border | no |
| `spacing.focus-ring-width` | Focus ring width | no |
| `spacing.menu-min-width` | Minimum width of `container`, so that a short menu does not look cramped | yes |
| `spacing.floating-max-width` | Maximum width of `container`, so that long labels wrap | yes |

### Components entries (contrast checks)

One entry per color pair of an item state, using only the standard `backgroundColor` and `textColor` properties. `disabled` pairs are never declared (WCAG 1.4.3 exemption, see `docs/conventions.md`). The select options and the popover reuse these entries or declare their own (see their specs).

| Entry | backgroundColor | textColor |
|---|---|---|
| `menu-item` | `{colors.surface}` | `{colors.on-surface}` |
| `menu-item-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `menu-item-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `menu-item-danger` | `{colors.surface}` | `{colors.danger}` |
| `menu-item-danger-hover` | `{colors.neutral-subtle-hover}` | `{colors.danger-hover}` |
| `menu-item-danger-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.danger-pressed}` |
| `menu-muted` | `{colors.surface}` | `{colors.on-surface-muted}` |
| `menu-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

The `menu-item-danger` states follow the fill-less rule of "State changes" in `docs/conventions.md`, with one extension: on a grayed fill, `danger-hover` serves `neutral-subtle-hover` and `danger-pressed` serves `neutral-subtle-pressed`, and no other pairing. The focus ring is also checked against the two grayed fills by `theme/theme.py` (see Focus ring in `docs/conventions.md`).

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `check-icon` is the library checkmark; `leading-icon` is chosen by the project; `dot` is a plain circle, not a library glyph.
- Elevation is not a token. The menu uses `level-2` of the elevation table in the `## Elevation & Depth` section of DESIGN.md.
- The container border is not a contrast pair and needs no 3:1 check (see "Floating surface" in `docs/conventions.md`).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | `container` has the `menu` role. An `action` item has `menuitem`, a `checkbox` item `menuitemcheckbox`, a `radio` item `menuitemradio`. A `group` has the `group` role, named by its `group-title` (`aria-labelledby`) or by `aria-label`. A `separator` has the `separator` role. |
| Trigger | The button has `aria-haspopup="menu"`, `aria-expanded`, and `aria-controls` (see "Floating surface" in `docs/conventions.md`). |
| Accessible name | `container` is named by its trigger (`aria-labelledby`). An item is named by its `label`; `shortcut` is referenced by `aria-keyshortcuts` and is not part of the name. |
| State | `checked` is exposed by `aria-checked` on checkable items. `disabled` is `aria-disabled="true"`, never the native `disabled`, so the item stays reachable. |
| Not by color alone | A checked item shows `check-icon` or `dot`. A `danger` item is also told by its wording and its position; color is never the only cue (WCAG 1.4.1). |
| Focus | Roving focus: items are not in the tab order, only one holds focus at a time. Opened with the keyboard, focus goes to the first item (`ArrowUp` on the trigger: the last item). Opened with the pointer, focus goes to `container`, and the first arrow key reaches the first item. |
| Focus visible | The focus ring shows on the focused item. It must never be removed. |
| Target size | Item height is at least 24 CSS pixels (WCAG 2.2 criterion 2.5.8): `{spacing.control-sm}` meets it in every density. |
| Contrast | Text and marks reach 4.5:1 against their fill (entries of the Token contract, checked by the lint). `disabled` is exempt. |

Keyboard:

| Key | Where | Effect |
|---|---|---|
| `Enter`, `Space`, `ArrowDown` | Trigger | Opens the menu; focus goes to the first item |
| `ArrowUp` | Trigger | Opens the menu; focus goes to the last item |
| `ArrowDown`, `ArrowUp` | Menu | Moves to the next or the previous item; wraps at the ends |
| `Home`, `End` | Menu | Moves to the first or the last item |
| A letter | Menu | Moves to the next item whose label starts with that letter, enabled items only; the same letter again cycles |
| `Enter`, `Space` | Item | Activates the item |
| `Escape` | Menu | Closes; focus returns to the trigger |
| `Tab` | Menu | Closes; focus moves on to the next focusable element after the trigger |

`ArrowRight` and `ArrowLeft` do nothing: there is no submenu.

## Behavior

- Opening: activating the trigger opens the menu on `placement`, with the flip and shift rules of "Floating surface". Activating the trigger again closes it.
- Activation: activating an item runs its action and closes the menu. A checkable item also changes: a `checkbox` item flips `checked`; a `radio` item becomes `checked` and unchecks the other items of its group. A project that wants a checkable item to keep the menu open decides it explicitly.
- Pointer: an item activates on release, if the pointer is still on it. Releasing outside the item cancels.
- `disabled` item: reachable by the arrow keys so that its existence is announced; activating it does nothing and the menu stays open.
- Long menu: `container` scrolls inside the viewport (see "Floating surface"); the focused item is scrolled into view.
- Closing: `Escape`, a press outside, activation of an item, `Tab`, or activating the trigger again.
- Text: a `label` wraps at `max-width`, never truncated.

## Do and don't

| Do | Don't |
|---|---|
| Write labels as verbs: "Rename", "Delete" | Write vague labels such as "More" or "Options" |
| Group related items and separate the groups | Put a separator between every item |
| Put a `danger` item last, after a separator | Put a `danger` item first, next to the most common command |
| Use `shortcut` to teach a real shortcut | Show a shortcut the project does not bind |
| Keep the list short, a dozen items at most | Use a menu for long lists of values: use a select |
| Use the leading space for an icon or a mark, consistently | Mix icons and checkmarks on the same item |

## Out of scope

Submenus (they need a pointer-direction safety area and left and right key rules, so they are not simple enough to include), context menus opened by right click or long press, menu bars, menus that hold inputs or free content (see `components/popover.md`), item descriptions and avatars, search inside a menu, items that are links to pages, animations, dark mode, and the choice of the trigger (a button, see `components/button.md`) are not covered by this spec; contrast is checked only against `{colors.surface}`, so on an image or a dark background the user retouches the menu colors after generation.
