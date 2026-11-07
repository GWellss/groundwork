# Dialog

A dialog is a modal panel that opens over the page, blocks it, and asks the user to read something or decide before going on. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme. The dialog is an overlay panel: its look follows "Overlay panel" in `docs/conventions.md`; this spec states what is specific to a dialog.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `scrim`, `container`, `title`, `body`, `actions`, `close-button` |
| Configurations | title + body + actions; with or without close button |
| Variants | `default` (role `dialog`), `confirmation` (role `alertdialog`) |
| Sizes | `sm`, `md` (widths) |
| Interactive states | none for the dialog itself; its content follows its own specs; visibility states `closed`, `open` |
| State properties | none |
| Behavior options | `variant`, `size` |
| Elevation | `level-3` when `open` (not a token, see Token contract) |

## Purpose

- Use a dialog when the user must decide or acknowledge before going on, when the content is long or has several steps, or when the page behind must not be used meanwhile: a short form, a confirmation, a choice with consequences.
- Use the `confirmation` variant to confirm an action that cannot be undone or that interrupts the user ("Delete this file?"). It has one question and one or two answers.
- Use a popover for a small amount of content tied to one element that does not block the page (see `components/popover.md`), a menu for a list of commands (see `components/menu.md`), an alert for a message that stays in the page (see `components/alert.md`), a toast for a brief confirmation (see `components/toast.md`).
- Do not use a dialog for what can be said inline or in a toast: it interrupts, so every dialog must be worth the interruption.
- Do not open a dialog from another dialog, and do not open one without a user action or an event the user expects.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `scrim` | Veil over the page, behind `container` | yes | Covers the viewport; shows that the page is blocked |
| `container` | The panel; carries fill, border, radius, elevation | yes | Role `dialog` or `alertdialog`, modal |
| `title` | Names the dialog | yes | A heading; also the accessible name |
| `body` | The content: text, controls | yes | Free content; every element follows its own spec; scrolls when long |
| `actions` | Row of buttons at the end of the dialog | yes | One to three buttons |
| `close-button` | Closes the dialog | no | A button with the library close icon, at the end of the first row; not in `confirmation` |

The trigger is the element that opened the dialog. It is not a part of the dialog.

### Configurations

| Configuration | Parts | Allowed |
|---|---|---|
| standard | `title`, `body`, `actions` | yes |
| with-close | `close-button` with `default` | yes |
| confirmation | `title`, `body`, `actions`, variant `confirmation` | yes |
| confirmation-with-close | `close-button` with `confirmation` | no |
| untitled | no `title` | no |
| no-actions | no `actions` | no |
| nested | a dialog opened from inside a dialog | no |
| non-modal | a dialog that leaves the page usable | no |

Combination rules:

- A dialog always has a `title`: it is the accessible name, and it tells the user at once why the page was blocked.
- `actions` holds one to three buttons, so that the user always has a visible way out or forward. A dialog that only informs has one button ("Close"). More than three choices are a page, a menu, or a list in `body`.
- Order of `actions`: the main action is the last one, the secondary action (usually "Cancel") comes before it, the tertiary action comes first. At most one button is `filled` or `danger` (see `components/button.md`).
- In `confirmation`, `actions` holds one or two buttons, `body` is plain text (no field, no list of options), and there is no `close-button`: the answer is one of the buttons.
- Floating surfaces opened from inside `container` (a select list, a menu, a popover, a tooltip) are allowed and belong to the dialog. The dialog itself is never nested.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `title` | text | none, required | Heading of the dialog |
| `variant` | `default`, `confirmation` | `default` | `confirmation` is the confirm-an-action dialog: role `alertdialog`, the rules above |
| `size` | `sm`, `md` | `md`; `sm` when `variant` is `confirmation` | Width of `container` |
| `closable` | `true`, `false` | `false` | Shows `close-button`; not allowed with `confirmation` |

The content of `body` and `actions` is given by the project. The destructive nature of a `confirmation` is expressed by the variant of the main button (`danger`), not by a property of the dialog.

## Variants

| Variant | Role | Typical use | Differences |
|---|---|---|---|
| `default` | `dialog` | A form, a choice, a detail view | Any body; may have `close-button`; a press on `scrim` closes it |
| `confirmation` | `alertdialog` | Confirm an irreversible or interrupting action | Plain text body; one or two actions; no `close-button`; a press on `scrim` does nothing; initial focus on the least destructive action |

Both variants share the same tokens. A dialog on a dark or tinted fill is out of scope.

## Sizes

### Decision

Two widths. `sm` suits a confirmation, `md` a form or a short document. A wider dialog is a page or a sheet, which is out of scope. Both are maximum widths: the width follows the content up to them, and the dialog never exceeds the viewport. Width tokens depend on font size and density, so they live in the theme. Padding and gaps reuse spacing tokens.

### Size table

| Size | Max width |
|---|---|
| `sm` | `{spacing.floating-max-width}` |
| `md` | `{spacing.dialog-max-width}` |

| Dimension | Token |
|---|---|
| `padding` | `{spacing.xl}` |
| `title-body-gap` | `{spacing.md}` |
| `body-actions-gap` | `{spacing.xl}` |
| `actions-gap` | `{spacing.sm}` |
| `viewport-padding` | `{spacing.xl}` |
| `title-typography` | `{typography.label-xl}` |
| `body-typography` | `{typography.label-md}` |
| `radius` | `{rounded.overlay}` |

Geometry rules:

- `container` is centered in the viewport, horizontally and vertically. Its width is the content width, up to `max-width`, and never more than the viewport minus twice `viewport-padding`.
- Its height follows the content. It never exceeds the viewport minus twice `viewport-padding`: beyond that, `body` scrolls inside (see Behavior) while `title` and `actions` stay in view.
- `padding` is measured inside the border, which is reserved (`{spacing.border-width}`).
- `close-button` is a `text` button, icon-only, size `s` (see `components/button.md`). It sits at the end of the first row, level with `title`. The `title` leaves room for it, so the two never overlap.
- `actions` is a row aligned to the end, with `actions-gap` between buttons; they are size `m` (see `components/button.md`). If they do not fit on one line, the row wraps and keeps its order.
- While `body` scrolls, a `subtle` horizontal divider (see `components/divider.md`) separates it from `title` above and from `actions` below.
- `scrim` fills the viewport, behind `container` and above the page.

## States

### Interactive states

None for the dialog itself: `container` is not a control. Each element inside follows its own spec.

| State | Trigger | Visual effect |
|---|---|---|
| `closed` | Default; after dismissal | Not rendered |
| `open` | The trigger is activated, or an expected event occurs | `scrim` shown, `default` tokens, `level-3` |

### State properties

None: a dialog has no `disabled` or `loading` property. An action button that runs a task uses its own `loading` property.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border).

### `default` and `confirmation`

| Part | Fill | Content | Border |
|---|---|---|---|
| `container` | `{colors.surface}` | `{colors.on-surface}` | `{colors.neutral-subtle-pressed}` |
| `scrim` | `{colors.inverse-surface}` at `scrim-opacity` | `none` | `none` |
| `title`, `body` | `none` | `{colors.on-surface}` | `none` |

The elements inside (buttons, fields, links) take the tokens of their own specs. Any text of the `body` that sits on the surface may use `{colors.on-surface-muted}`; on a grayed fill it takes `{colors.on-surface}`.

### Elevation

`container` is at `level-3` when `open`; `closed` is not rendered. `scrim` is flat.

## Token contract

The theme must define every token below. The dialog adds one spacing token, its maximum width, and no color: the scrim reuses `inverse-surface`.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | `container` fill |
| `colors.on-surface` | `title`, `body` |
| `colors.neutral-subtle-pressed` | `container` border |
| `colors.inverse-surface` | `scrim` fill (with the fixed opacity of Behavior) |

### Typography

| Token | Role |
|---|---|
| `typography.label-xl` | `title` |
| `typography.label-md` | `body` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | `container` radius |

### Spacing

| Token | Role |
|---|---|
| `spacing.sm` | Gap between buttons of `actions` |
| `spacing.md` | Title to body gap |
| `spacing.xl` | Padding; body to actions gap; viewport padding |
| `spacing.border-width` | Border width |
| `spacing.floating-max-width` | Maximum width of `container` for `sm` |
| `spacing.dialog-max-width` | Maximum width of `container` for `md` |

### Components entries (contrast checks)

One entry for the text of the dialog, using only the standard `backgroundColor` and `textColor` properties.

| Entry | backgroundColor | textColor |
|---|---|---|
| `dialog` | `{colors.surface}` | `{colors.on-surface}` |

The buttons and fields inside declare their own entries. The scrim carries no text and is not a pair.

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `close-button` shows the library close icon.
- Elevation is not a token. The dialog uses `level-3` of the elevation table in the `## Elevation & Depth` section of DESIGN.md.
- The container border and the scrim are not contrast pairs and need no 3:1 check: they set the panel apart for sighted users, and no information depends on them.

## Accessibility

| Topic | Requirement |
|---|---|
| Role | `container` has the `dialog` role (`alertdialog` for `confirmation`) and `aria-modal="true"`. The page behind is made inert: not reachable by keyboard, pointer, or assistive technology. |
| Accessible name | `title`, referenced by `aria-labelledby`. |
| Accessible description | `confirmation`: `body` is referenced by `aria-describedby`, so the question is read on opening. `default`: optional, for a short text body. |
| Trigger | The trigger has `aria-haspopup="dialog"`. It does not need `aria-expanded`: the dialog covers it. |
| Focus on open, `default` | Focus moves to the first focusable element of `body`; if there is none, to the main button of `actions`. |
| Focus on open, `confirmation` | Focus moves to the least destructive action: the secondary button ("Cancel"), or the only button. A reflex press on `Enter` must never confirm a destructive action. |
| Focus trap | `Tab` and `Shift+Tab` cycle through the focusable elements of `container` and never reach the page. After the last, focus returns to the first, and conversely. |
| Close | `Escape` closes the dialog, in both variants (it acts as the secondary action, never as the main one). A press on `close-button` closes it. |
| Focus on close | Focus returns to the trigger. If the trigger no longer exists or there was none, focus goes to the element that had it before opening, or to a logical point chosen by the project (never to the top of the page by default). |
| Scrollable body | A `body` that scrolls and holds no focusable element is itself focusable (`tabindex="0"`), so that keyboard users can scroll it. |
| Not by color alone | The dialog is told apart by its `scrim`, border, and shadow, and the destructive nature of a `confirmation` by its button label ("Delete"), never by the red alone. |
| Target size | Controls inside follow their own specs; `close-button` is a size `s` button, at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). |
| Contrast | Text reaches 4.5:1 against the surface. Delegated to the DESIGN.md lint through the `dialog` entry. |

## Behavior

- Opening: the dialog appears centered over `scrim`, focus moves as above, and the page behind stops scrolling. It never opens on hover and never from a timer.
- Closing: `Escape`, `close-button`, any button of `actions` that ends the task (the project decides which), or, for `default` only, a press on `scrim` (pointer down and release both on the scrim, so that a drag that ends there does not close it). `confirmation` ignores a press on `scrim`: the user must answer.
- While an action button is `loading`, `Escape`, `close-button` and a press on `scrim` are ignored, so that a running task is never abandoned by accident.
- Long content: `body` scrolls; `title` and `actions` stay in view. Scrolling the page behind is impossible.
- Floating surfaces opened from inside the dialog (select list, menu, popover) sit above `container`. `Escape` closes the innermost surface first, then the dialog on the next press.
- Toasts triggered while the dialog is open wait and appear when it closes (see `components/toast.md`).
- Only one dialog is open at a time. A project that needs a confirmation inside a dialog replaces the content of the open dialog (a step), or closes it first.
- Transitions: the fade of `scrim` and the entry of `container`, if any, are the project's choice and are removed under reduced motion (see Motion in `docs/conventions.md`).

| Constant | Value | Meaning |
|---|---|---|
| `scrim-opacity` | 50% | Opacity of the `inverse-surface` color over the page; invariant, not a theme token |

## Do and don't

| Do | Don't |
|---|---|
| Give a `title` that says why the page is blocked | Open a dialog with no heading |
| Name the buttons with verbs: "Delete", "Cancel" | Use "OK" and "Yes" as the only labels |
| Put the main action last, the secondary one before it | Put the destructive button first or left of "Cancel" |
| Use `confirmation` and a `danger` main button for an irreversible action | Use `confirmation` for a form or for a simple notice |
| Focus the least destructive action in an `confirmation` | Focus the destructive button |
| Keep the content short, and scroll the `body` when it is long | Let `container` grow beyond the viewport |
| Return focus to the trigger on close | Leave focus on a removed element |
| Use a popover or an inline message when the page may stay usable | Block the page for a small choice |

## Out of scope

Nested dialogs, non-modal dialogs, full-screen dialogs and bottom sheets on small screens, drawers and side panels, a dialog wider than `md`, a draggable or resizable dialog, a confirmation before closing a form with unsaved changes (the project's logic), animations, dark mode, and a dialog on an image or a tinted fill are not covered by this spec; contrast is checked only against `{colors.surface}`, so the user retouches the dialog colors after generation if the fill changes.
