# Popover

A popover is a small panel anchored to a trigger that holds free, interactive content (a title, text, controls, actions) and stays on the page without blocking it. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme. The popover is a floating surface: look, placement, and opening and closing follow "Floating surface" in `docs/conventions.md`; this spec states what is specific to a popover.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `arrow`, `title`, `body`, `actions`, `close-button` |
| Configurations | body only; with title; with actions; with close button; each with or without arrow |
| Variants | `default` |
| Sizes | none; one maximum width, padding and gaps from spacing tokens |
| Interactive states | none for the popover itself; its content follows its own specs; visibility states `closed`, `open` |
| State properties | none |
| Behavior options | `placement`, `align`, `arrow` |
| Elevation | `level-2` when `open` (not a token, see Token contract) |

## Purpose

- Use a popover for a small amount of content tied to one element that the user may act on, without leaving the page: a short form, a list of options with explanations, a confirmation with two buttons, a help text with a link.
- Use a tooltip for a short description that is not interactive (see `components/tooltip.md`). A tooltip opens on hover and focus and holds no control; a popover opens on activation and may hold controls.
- Use a dialog when the user must decide before going on, when the content is long or has several steps, or when the page behind should be blocked (see `components/dialog.md`). A popover never blocks the page.
- Use a menu for a list of commands (see `components/menu.md`), and a select to pick a value (see `components/select.md`).
- Do not open a popover on hover alone, and do not use it for an error or a message the user must read: show it inline.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | The floating surface; carries fill, border, radius, elevation | yes | Role `dialog`, not modal |
| `arrow` | Triangle pointing to the trigger | no | Same fill and border as `container`; shown only when `arrow` is true |
| `title` | Names the popover | no | A heading; also the accessible name |
| `body` | The content: text, links, controls | yes | Free content; every element follows its own spec |
| `actions` | Row of buttons at the end of the popover | no | At most two buttons |
| `close-button` | Closes the popover | no | A button with the library close icon, at the end of the top row |

The trigger is a button, a link, or any element the user can activate. It is not a part of the popover.

### Configurations

| Configuration | Parts | Status |
|---|---|---|
| body-only | `body` | allowed |
| titled | `title`, `body` | allowed |
| with-actions | `body`, `actions`, optional `title` | allowed |
| with-close | `close-button` with any of the above | allowed |
| with-arrow | `arrow` with any of the above | allowed |
| empty | no `body` | forbidden |
| nested | a popover or a menu opened from inside a popover | out-of-scope |
| modal | a popover that blocks the page | out-of-scope |

Combination rules:

- A popover with no `body` is `forbidden`: it would be announced empty.
- A popover always has an accessible name: `title`, or `aria-label` when there is no title.
- `actions` holds at most two buttons: the main one at the end, the secondary one before it. More choices are a dialog or a menu.
- `close-button` is recommended when the popover holds controls or long text, so that the way out is visible. `Escape` and a press outside always close it.
- The popover never holds another floating surface: a menu or a select list opened from inside would close the popover under the "one surface at a time" rule (see "Floating surface"). Such a case is `out-of-scope`, like a popover that blocks the page.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `title` | text | none | Heading of the popover |
| `placement` | `top`, `right`, `bottom`, `left` | `bottom` | Preferred side of the trigger; flips if space runs out |
| `align` | `start`, `center`, `end` | `center` | Alignment along that side |
| `arrow` | `true`, `false` | `false` | Shows `arrow` pointing to the trigger |
| `closable` | `true`, `false` | `false` | Shows `close-button` |

The content of `body` and `actions` is given by the project.

## Variants

| Variant | Container | Content | Typical use |
|---|---|---|---|
| `default` | `{colors.surface}` fill, quiet border | `{colors.on-surface}` | Interactive content tied to a trigger |

A popover on a dark or tinted fill is out of scope.

## Sizes

### Decision

The popover has no named sizes: its size follows its content, up to one maximum width, a theme token shared with the menu and the select list. Padding and gaps reuse spacing tokens, so density applies.

### Size table

| Dimension | Token |
|---|---|
| `max-width` | `{spacing.floating-max-width}` |
| `padding` | `{spacing.md}` |
| `title-body-gap` | `{spacing.xs}` |
| `body-actions-gap` | `{spacing.md}` |
| `actions-gap` | `{spacing.sm}` |

| Dimension | Token |
|---|---|
| `title-typography` | `{typography.label-lg}` |
| `body-typography` | `{typography.label-md}` |
| `arrow-width` | `{spacing.md}` |
| `radius` | `{rounded.overlay}` |

Geometry rules:

- Width fits the content, up to `max-width`. Beyond it, text wraps; it is never truncated.
- `padding` is measured inside the border, which is reserved (`{spacing.border-width}`).
- `close-button` is a `text` button, icon-only, size `s` (see `components/button.md`). It sits at the end of the first row, level with `title`. The `title` leaves room for it, so the two never overlap.
- `actions` is a row aligned to the end; the buttons are size `s` (see `components/button.md`), with `actions-gap` between them.
- `arrow` is an isosceles triangle, `arrow-width` wide at its base and half as high, pointing to the center of the trigger. It stays at least `{spacing.md}` away from a corner of `container`. The distance from the trigger to the container edge is the offset plus the arrow height; the tip sits at the offset from the trigger (as the tooltip).
- The arrow continues the fill of `container`; the border runs along its two sides and is open at its base, so there is no seam.
- Offset, viewport padding, flipping, and shifting: see "Floating surface" in `docs/conventions.md`.

## States

### Interactive states

None for the popover itself: `container` is not a control. Each element inside follows its own spec (a button has its `hover` and `pressed`, a field its `focus`).

| State | Trigger | Visual effect |
|---|---|---|
| `closed` | Default; after dismissal | Not rendered |
| `open` | The trigger is activated | `default` tokens, `level-2` |

### State properties

None: a popover has no `disabled` or `loading` property. A disabled trigger does not open it.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border).

### `default`

| Part | Fill | Content | Border |
|---|---|---|---|
| `container` | `{colors.surface}` | `{colors.on-surface}` | `{colors.neutral-subtle-pressed}` |
| `arrow` | `{colors.surface}` | `none` | `{colors.neutral-subtle-pressed}` |
| `title`, `body` | `none` | `{colors.on-surface}` | `none` |

The elements inside (buttons, fields, links) take the tokens of their own specs. Any text of the `body` that sits on the surface may use `{colors.on-surface-muted}`; on a grayed fill it takes `{colors.on-surface}`.

### Elevation

`container` is at `level-2` when `open`; `closed` is not rendered. With `arrow`, the shadow follows the same rule as the tooltip: the combined outline of container and arrow when the platform can, otherwise the container alone, and never a shadow between arrow and container. In dark mode there is no shadow: the `container` takes the `surface-level-2` fill and keeps its border (see Dark mode in `docs/conventions.md`).

## Token contract

The theme must define every token below. The popover adds no color and no token: the maximum width is the one of the menu.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | `container` and `arrow` fill |
| `colors.on-surface` | `title`, `body` |
| `colors.neutral-subtle-pressed` | `container` and `arrow` border |

### Typography

| Token | Role |
|---|---|
| `typography.label-lg` | `title` |
| `typography.label-md` | `body` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | `container` radius |

### Spacing

| Token | Role |
|---|---|
| `spacing.xs` | Title to body gap; offset |
| `spacing.sm` | Gap between buttons of `actions`; viewport padding |
| `spacing.md` | Padding; body to actions gap; `arrow` width and distance to a corner |
| `spacing.border-width` | Border width |
| `spacing.floating-max-width` | Maximum width of `container` |

### Components entries (contrast checks)

One entry for the text of the popover, using only the standard `backgroundColor` and `textColor` properties.

| Entry | backgroundColor | textColor |
|---|---|---|
| `popover` | `{colors.surface}` | `{colors.on-surface}` |

The buttons and fields inside declare their own entries.

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `close-button` shows the library close icon.
- Elevation is not a token. The popover uses `level-2` of the elevation table in the `## Elevation & Depth` section of DESIGN.md.
- The container border is not a contrast pair and needs no 3:1 check (see "Floating surface" in `docs/conventions.md`).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | `container` has the `dialog` role, not modal (no `aria-modal`, the page behind stays reachable). |
| Accessible name | `title`, referenced by `aria-labelledby`; with no title, an `aria-label`. |
| Trigger | The trigger has `aria-haspopup="dialog"`, `aria-expanded`, and `aria-controls` (see "Floating surface" in `docs/conventions.md`). A trigger that is not a button also has a role and a key handler. |
| Focus on open | Focus moves into the popover: to its first focusable element, or to `container` (focusable by script only) when it has none. |
| Focus order | `container` follows its trigger in the reading order, so `Tab` goes from the trigger into it. Focus is not trapped. |
| Leaving | `Tab` past the last focusable element, or `Shift+Tab` before the first, closes the popover; focus goes on to the next element in order, or back to the trigger. |
| Focus on close | `Escape` and `close-button` close the popover and return focus to the trigger. A press outside closes it and leaves focus where the user pressed. |
| Not by color alone | The popover is told apart by its border and shadow, and its content by its own parts. |
| Target size | Controls inside follow their own specs; `close-button` is a size `s` button, at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). |
| Contrast | Text reaches 4.5:1 against the surface. Delegated to the DESIGN.md lint through the `popover` entry. |

## Behavior

- Opening: activating the trigger opens the popover on `placement` and `align`, with the flip and shift rules of "Floating surface". Activating the trigger again closes it. It never opens on hover alone.
- Closing: `Escape`, `close-button`, a press outside the popover and its trigger, leaving it with `Tab`, activating the trigger again, or an action of the project (a confirm button, for example). A project that keeps the popover open after an action decides it explicitly.
- Scroll: scrolling the page or the popover does not close it. The popover follows its trigger, with the same placement rules.
- Only one popover (or other interactive floating surface) is open at a time.
- Content change: the project may change the content while open; the popover keeps its placement and does not move focus on its own.

## Do and don't

| Do | Don't |
|---|---|
| Keep the content small and tied to the trigger | Put a long form or several steps in a popover: use a dialog |
| Give the popover a `title`, or an `aria-label` | Leave it without a name |
| Show `close-button` when it holds controls | Rely on `Escape` as the only visible way out |
| Limit `actions` to two buttons, main one last | Stack many buttons |
| Open it on activation of the trigger | Open it on hover |
| Return focus to the trigger on close | Leave focus on a removed element |

## Out of scope

Modal behavior and focus trapping (see `components/dialog.md`), popovers that open on hover or on a long press, popovers inside popovers, a menu or select opened inside a popover, a popover on a dark or tinted fill, a popover that follows the pointer, a full-screen sheet on small screens, and animations are not covered by this spec; contrast is checked only against `{colors.surface}`, so on an image or a dark background the user retouches the popover colors after generation.
