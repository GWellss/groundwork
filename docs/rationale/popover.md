# Popover rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Surface fill and quiet border, `level-2` | Same floating surface as the menu; see `docs/conventions.md`. Material 3 and Carbon use a raised surface for it |
| Opens on activation, never on hover | A hover-only panel with controls cannot be reached by keyboard or touch, which is why the tooltip holds none (WCAG 1.4.13); a popover holds controls, so it needs an explicit open |
| Role `dialog`, not modal, named by its title | WAI-ARIA has no popover role; a non-modal dialog is what assistive technologies understand for interactive panels. `aria-modal` stays off because the page remains usable |
| Focus moves in on open, returns on `Escape` and close button | Interactive content must be reachable from the keyboard; returning focus avoids losing the user's place |
| Not trapped, `Tab` leaves and closes | A trap is for modal dialogs (lot C6); a popover is light, so leaving it is natural, and it follows its trigger in the reading order |
| Press outside leaves focus where it is | The user moved on deliberately; pulling focus back would steal it |
| At most two actions | More choices make a decision that belongs in a dialog or a menu |
| `close-button` optional, recommended with controls | `Escape` and an outside press always work, but a visible exit helps pointer and touch users |
| No nested menu or select | The "one surface at a time" rule would close the popover; modeling the exception is not simple, so it is left out |
| Arrow optional, off by default | As the tooltip; the arrow is useful when several triggers sit close together |
| Align `center` by default | As the tooltip; the arrow points to the trigger center |
| Same maximum width as the menu | One token for all interactive floating surfaces; a popover needing more is probably a dialog |
| Title typography `label-lg`, body `label-md` | Existing typography tokens; no new size just for the popover |
