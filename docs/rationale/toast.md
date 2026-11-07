# Toast rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| One component for toast, snackbar and flag | They differ by name and by small visual details, not by function: a short message that goes away. One spec avoids three look-alikes |
| Surface fill, not the dark inverse fill | The tooltip is the only dark surface of the kit; a second one would need a second set of rules for muted text and for buttons on a dark fill (buttons inside would have to be restyled). The surface keeps every button entry valid |
| `level-3`, quiet border | The role of `level-3` is floating above content while it scrolls. A toast is not tied to a trigger, so it sits one level above the popover |
| Status shown by an icon only, `neutral`, `success`, `danger` | The toast stays on the surface, so its contrast stays that of the surface. The icon color is `success` or `danger`, which already reach 4.5:1 there (a new `success` accent on the surface, nothing off the surface). No `warning`: a warning must be read again, which is an alert |
| Default duration 6000 ms, minimum 5000 ms | WCAG 2.2.1 asks that time limits can be adjusted or extended; the toast pauses on hover and focus, and 5 to 6 seconds is the commonly accepted lower bound for a short sentence. The values are behavior constants, not theme tokens |
| No timer with an action or an error | A user who needs to reach the button, or to read an error, must not be rushed; a keyboard user may need many seconds to reach the action. Forces the close button so that it can be dismissed |
| The action is never the only way to do something | A transient control cannot be the only path: a user may never see it. "Undo" repeats an option that exists in the page |
| Pause also when the page is hidden, restart with the full duration | A toast that expires while the user is in another tab was never read; a partial remaining time after a hover is too short to be useful |
| Polite region present from the start, `role="alert"` on `danger` only | Live regions are announced reliably only if they exist before the content. Polite avoids interrupting; a failed action is the one case where interrupting is justified |
| Waits while a dialog is open | The page behind a dialog is inert, so a message there would not be announced |
| At most three visible, newest nearest the edge | A tall stack covers the page and floods screen reader users. Others queue |
| `bottom-center` by default, four placements | A common default, away from the floating button at the end of the bottom edge; one placement per page, so a user always looks in the same place |
| Reuses `floating-max-width` | One token for the width of every panel of this kind; a toast needing more is an alert |
