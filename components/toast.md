# Toast

A toast is a brief message that appears over the page, outside the flow, to confirm something that just happened, and goes away by itself or when the user dismisses it. It is the only component of the kit for what other systems call a toast, a snackbar, or a flag. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme. The toast is an overlay panel: its look follows "Overlay panel" in `docs/conventions.md`; this spec states what is specific to a toast.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `icon`, `message`, `action`, `close-button` |
| Configurations | message only; with status icon; with action; with close button; any combination |
| Variants | `neutral`, `success`, `danger` (severity) |
| Sizes | none; one maximum width, padding and gaps from spacing tokens |
| Interactive states | none for the toast itself; `action` and `close-button` follow `components/button.md`; visibility states `closed`, `open` |
| State properties | none |
| Behavior options | `placement`, `duration` |
| Behavior constants | default duration, minimum duration, visible count (invariant, in this spec) |
| Elevation | `level-3` when `open` (not a token, see Token contract) |

## Purpose

- Use a toast for a brief result that needs no reading and no answer: "Message sent", "File deleted", "Copied", "Could not save". It confirms something the user just did, or reports an event that is not tied to a place in the page.
- Use an alert for a message that must stay in the page and be read at the user's pace, or that the user must not miss (see `components/alert.md`). If the message must still be there a minute later, it is an alert.
- Use a dialog when the user must answer before going on (see `components/dialog.md`).
- Use the field error for a problem with a field (see `components/text-field.md`).
- Do not use a toast to say something important only once: it may be gone before it is read, and screen reader and keyboard users may never reach it.
- Do not put in a toast the only way to do something: the `action` repeats something that exists elsewhere ("Undo" is also in the page).

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | The panel; carries fill, border, radius, elevation | yes | Always present |
| `icon` | Glyph of the severity | `success` and `danger` | Absent in `neutral` |
| `message` | The text | yes | Plain text, one sentence, no link, no formatting |
| `action` | One action about the message ("Undo", "Retry") | no | A `text` button, size `s`; one only |
| `close-button` | Dismisses the toast | see rules | A button with the library close icon, at the end of the row |

### Configurations

| Configuration | Parts | Allowed |
|---|---|---|
| message-only | `message` | yes |
| status | `icon`, `message` | yes, with `success` or `danger` |
| with-action | `action` with any of the above | yes |
| with-close | `close-button` with any of the above | yes |
| title | a heading above `message` | no |
| two-actions | two `action` parts | no |
| link-in-message | a link inside `message` | no |
| empty | no `message` | no |

Combination rules:

- A toast with an `action`, and a `danger` toast, never disappear by themselves (see Behavior) and always have `close-button`. Any other toast may omit it.
- `message` is short, a sentence at most, and fits on one or two lines. A longer message is an alert.
- `action` is a verb, and a single one. An action that opens a form or a page is a link or a dialog, not a toast action.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `message` | text | none, required | The text |
| `severity` | `neutral`, `success`, `danger` | `neutral` | Meaning; adds `icon` for `success` and `danger` |
| `action` | label and handler | none | The single action |
| `closable` | `true`, `false` | `true`; forced `true` with an `action` or `danger` | Shows `close-button` |
| `duration` | whole milliseconds, or `none` | the default duration; forced `none` with an `action` or `danger` | How long the toast stays before it goes away; at least the minimum duration |
| `placement` | `bottom-center`, `bottom-start`, `bottom-end`, `top-center` | `bottom-center` | Where the stack sits, one value per page |

A `warning` toast does not exist: a warning is something the user may need to read again and act on, which is an alert.

## Variants

| Variant | Meaning | Icon | Icon color |
|---|---|---|---|
| `neutral` | A plain confirmation or event | none | none |
| `success` | A task is done | the library check-in-circle glyph | `{colors.success}` |
| `danger` | A task failed | the library error glyph | `{colors.danger}` |

The container, border, text, and controls are the same in the three variants. Only the icon changes: the toast never takes a tonal or solid fill, so that its contrast stays that of the surface.

## Sizes

### Decision

The toast has no named sizes: its size follows its content, up to the maximum width shared with the menu, the select list, and the popover. Padding and gaps reuse spacing tokens, so density applies.

### Size table

| Dimension | Token |
|---|---|
| `max-width` | `{spacing.floating-max-width}` |
| `padding` | `{spacing.md}` |
| `icon-message-gap` | `{spacing.sm}` |
| `message-action-gap` | `{spacing.md}` |
| `stack-gap` | `{spacing.sm}` |
| `edge-offset` | `{spacing.lg}` |
| `icon-size` | `{spacing.icon-md}` |
| `message-typography` | `{typography.label-md}` |
| `radius` | `{rounded.overlay}` |

Geometry rules:

- Width fits the content, up to `max-width`. On a viewport narrower than `max-width` plus twice `edge-offset`, the toast takes the viewport width minus twice `edge-offset`. `message` wraps; it is never truncated.
- `padding` is measured inside the border, which is reserved (`{spacing.border-width}`).
- Row, from the start: `icon`, `message` (takes the free width), `action`, `close-button`. `icon` is aligned with the first line of `message`. `action` and `close-button` are centered vertically.
- `action` is a `text` button, size `s`, and `close-button` an icon-only `text` button, size `s` (see `components/button.md`).
- The stack sits at `edge-offset` from the edge of the viewport given by `placement`, and the toasts are separated by `stack-gap`.

## States

### Interactive states

None for the toast itself: `container` is not a control. `action` and `close-button` follow their own spec (`hover`, `focus`, `pressed`).

| State | Trigger | Visual effect |
|---|---|---|
| `closed` | Default; after the toast has gone | Not rendered |
| `open` | An event or a user action produces the message | `default` tokens, `level-3` |

### State properties

None: a toast has no `disabled` or `loading` property.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border).

### `neutral`, `success` and `danger`

| Part | Fill | Content | Border |
|---|---|---|---|
| `container` | `{colors.surface}` | `{colors.on-surface}` | `{colors.neutral-subtle-pressed}` |
| `message` | `none` | `{colors.on-surface}` | `none` |
| `icon`, `success` | `none` | `{colors.success}` | `none` |
| `icon`, `danger` | `none` | `{colors.danger}` | `none` |

`action` and `close-button` take the tokens of the `text` button (see `components/button.md`). The `message` may not use `{colors.on-surface-muted}`: the toast is short, and a quiet text would be easy to miss.

### Elevation

`container` is at `level-3` when `open`: it floats above the content while the page scrolls. `closed` is not rendered. The toast never rises on hover.

## Token contract

The theme must define every token below. The toast adds no color and no token.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | `container` fill |
| `colors.on-surface` | `message` |
| `colors.neutral-subtle-pressed` | `container` border |
| `colors.success` | `icon` of `success` |
| `colors.danger` | `icon` of `danger` |

### Typography

| Token | Role |
|---|---|
| `typography.label-md` | `message` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | `container` radius |

### Spacing

| Token | Role |
|---|---|
| `spacing.sm` | Icon to message gap; stack gap |
| `spacing.md` | Padding; message to action gap |
| `spacing.lg` | Distance to the viewport edge |
| `spacing.icon-md` | Icon size |
| `spacing.border-width` | Border width |
| `spacing.floating-max-width` | Maximum width of `container` |

### Components entries (contrast checks)

One entry for the text, and one for each status icon, using only the standard `backgroundColor` and `textColor` properties. `success` and `danger` reach 4.5:1 on the surface by the State colors rule, and the icon is checked at that level.

| Entry | backgroundColor | textColor |
|---|---|---|
| `toast` | `{colors.surface}` | `{colors.on-surface}` |
| `toast-success` | `{colors.surface}` | `{colors.success}` |
| `toast-danger` | `{colors.surface}` | `{colors.danger}` |

The buttons inside declare their own entries.

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `icon` shows the glyph of its severity; `close-button` shows the library close icon.
- Elevation is not a token. The toast uses `level-3` of the elevation table in the `## Elevation & Depth` section of DESIGN.md.
- The container border is not a contrast pair and needs no 3:1 check: no information depends on it.

## Accessibility

| Topic | Requirement |
|---|---|
| Live region | One region, present in the page from the start (never created with the first toast), holds all the toasts and has `aria-live="polite"`: a message is announced when the user is idle, without taking focus. |
| Urgency | `neutral` and `success` use the polite region. `danger` has `role="alert"` (assertive), because a failure of what the user just did must be known at once. No other toast is assertive. |
| Name | The region has an accessible name given by the project ("Notifications"). Each toast is read as its `message`, and `icon` has an accessible name for its severity ("Success", "Error"). |
| Focus | A toast never takes focus when it appears. `action` and `close-button` are focusable, in the order of the region in the page. |
| Reaching the action | The region sits at the end of the reading order, so a persistent toast with an `action` is reached by `Tab`; the project may add a documented key that moves focus to the region. Because the `action` is never the only way to do something, a user who never reaches it loses nothing. |
| Keyboard | `Escape` closes the toast that holds focus. `Enter` and `Space` activate `action` and `close-button`. |
| Time limit | A toast without `action` and not `danger` goes away after `duration`. The time is paused while the pointer or the focus is on it (WCAG 2.2.1 Timing Adjustable), and it carries nothing the user cannot find elsewhere. A toast that carries an action or an error has no limit. |
| Not by color alone | The meaning is in the message and in `icon`, never in the color of the icon alone (WCAG 1.4.1). |
| Target size | `action` and `close-button` follow their own spec: at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). |
| Contrast | Text and icons reach 4.5:1 against the surface. Delegated to the DESIGN.md lint through the `toast*` entries. |

## Behavior

- Appearing: the toast appears at `placement` and is announced by the region. It is never opened by hover.
- Duration: a toast that has neither an `action` nor the `danger` severity goes away after `duration`, which is `default-duration` unless the project sets another value that is at least `minimum-duration`. With an `action` or `danger`, it stays until the user closes it.
- Pause: the timer stops while the pointer is over the toast or focus is inside it, and while the page is hidden. When it resumes, the toast gets the full `duration` again.
- Stack: at most `visible-count` toasts are shown. The newest sits nearest the edge of the viewport; older ones move away from it. Extra toasts wait in order and appear when one goes away. A toast never replaces another one that holds an `action` or an error.
- Dialog: while a dialog is open, new toasts wait and appear when it closes (the page behind a dialog is inert, so a toast shown then would not be announced).
- Closing: `close-button`, `Escape` with focus inside, the end of `duration`, or the end of the action (the project decides if `action` closes the toast; it normally does). Focus never moves by itself; when the toast that held focus goes away, focus goes to the element that had it before, or to the next focusable element.
- Floating button: the stack is laid out so that it never covers the floating button of the page (see `components/button.md`); the layout leaves room.
- Transitions: entry and exit, if any, are the project's choice and are removed under reduced motion (see Motion in `docs/conventions.md`). The timer is not motion and does not change.

| Constant | Value | Meaning |
|---|---|---|
| `default-duration` | 6000 ms | Time before a toast goes away; invariant, not a theme token |
| `minimum-duration` | 5000 ms | Shortest duration a project may set |
| `visible-count` | 3 | Toasts shown at once |

## Do and don't

| Do | Don't |
|---|---|
| Keep the message to one short sentence | Write a paragraph in a toast |
| Use it to confirm what the user just did | Use it for something the user must read |
| Keep a toast with an action or an error until it is closed | Make an error disappear on a timer |
| Offer an action that repeats what exists elsewhere ("Undo") | Put the only way to do something in a toast |
| Keep the live region in the page from the start | Create the region together with the first toast |
| Use an alert for a message that must stay | Use a toast for a warning |
| Pause the timer on hover and focus | Remove a toast under the pointer |

## Out of scope

Toasts with a title, several actions, a link, a progress bar, or a custom content, a `warning` toast, a toast that takes focus, swipe to dismiss, a toast tied to an element (use a popover), a toast that survives page navigation (the project's choice), notification centers and history, a stack taller than `visible-count`, animations, dark mode, and a toast on an image or a tinted fill are not covered by this spec; contrast is checked only against `{colors.surface}`.
