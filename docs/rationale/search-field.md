# Search field rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Separate spec that points to the text field | A search field is a restricted text field. Repeating the anatomy and the tokens would let the two drift; the spec states only the differences |
| No error, no required, no read-only, no multiline | A query has no wrong value and is never mandatory, and a read-only or multi-line search makes no sense; fewer states, fewer tokens |
| Visible label optional | The only exception to the text field rule. The magnifier, the placeholder, the search landmark, and a visible submit button state the purpose (WCAG 3.3.2 is met by these cues); the accessible name stays mandatory. `show-label` brings the label back when a design wants it |
| Landmark on the container, not on the input | The landmark role is for a region; a role on the input would replace its native role. The landmark label avoids repeating "search" because assistive technologies already say it |
| Own clear button, native one hidden | Browsers draw a clear control only in some engines and cannot be named or themed; one controlled button works everywhere |
| Clear button reuses the chip remove pattern | Same fills, same circular hover, same ring without offset; three entries named for the search field so the contrast report names it |
| Clear does not submit; `Escape` clears | Emptying a field is a local edit; submitting an empty query is the project's choice |
| Suggestions left to a later menu spec | Suggestions need a list, keyboard navigation inside it, and live announcements: that is the menu pattern, not a field property |
| Explicit submit only | Instant filtering needs a debounce and a result announcement strategy that depend on the project |
