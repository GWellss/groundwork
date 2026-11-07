# Dialog rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Modal, with a scrim, an inert page, and a focus trap | A dialog that leaves the page usable is a popover. Blocking is the point: the user decides first. The WAI-ARIA dialog pattern asks for the trap and for `aria-modal` |
| Scrim is `inverse-surface` at 50%, no new color | A veil needs no contrast pair (it carries no text). The darkest neutral already exists and follows the theme tint. The opacity is a behavior constant, like a duration, because DESIGN.md colors have no alpha channel; 50% is a common value that dims the page clearly without hiding it |
| Surface fill, quiet border, `level-3` | Same panel look as the popover, so the kit has one family of panels. `level-3` (above the `level-2` of a surface tied to a trigger) tells the user this panel sits over everything; `level-4` and `level-5` stay for interaction |
| Title required, actions required (one to three) | The title is the accessible name and the reason for the interruption. At least one button guarantees a visible way out or forward, also on touch |
| Main action last, secondary before it, tertiary first | The end of the row is where the eye and the reading direction finish, so the forward action sits there; it is also the rule of the popover. The order in the page equals the visual order, so keyboard order matches what is seen, and a wrapped row keeps it |
| Three actions at most | Beyond that the choice is a menu or a list inside the body |
| `confirmation` variant, role `alertdialog` | A question that interrupts needs the assistive technology to read the message at once. Plain text, one or two answers, no close button: the user answers with a button, so a cross would add a third, ambiguous answer |
| Initial focus: first field (`default`), least destructive action (`confirmation`) | A form should put the cursor where typing starts. A confirmation focuses "Cancel": a reflex `Enter` on a dialog that just appeared must not delete anything. The APG recommends the same for destructive actions |
| `Escape` closes both variants | Expected by every keyboard user. In a confirmation it acts as "Cancel", never as the main action. The one exception is a running task (`loading`), where closing would abandon it |
| Press on the scrim closes `default`, not `confirmation` | A deliberate pointer gesture, not an accessibility requirement since `Escape` and the buttons exist. A confirmation needs an explicit answer |
| No nested dialogs | A second modal over the first makes focus, `Escape` and inertness ambiguous. A step inside the same dialog does the same job |
| Floating surfaces inside a dialog allowed | A select or a menu in a form is common. Without an exception, the "one surface at a time" rule would forbid it. They close first on `Escape` |
| Two widths, `sm` reuses `floating-max-width`, `md` adds `dialog-max-width` | One new token only. A confirmation fits the 320px width; a form needs about 480px; wider content is a page |
| Body scrolls, title and actions stay | The question and the buttons must stay visible; long content must not push the buttons off screen. A subtle divider appears while it scrolls |
| Toasts wait while a dialog is open | The page behind a dialog is inert, so a live region there is not announced; the toast shows when it closes |
| Title typography `label-xl` | The largest existing label size; no new typography token for a heading |
