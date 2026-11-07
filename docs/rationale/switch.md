# Switch rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Distinguished from the checkbox by immediate effect | The two look alike; the difference is when the change counts. A switch applies at once, a checkbox on submit. The test in Purpose ("must the user press a button afterwards") settles ambiguous cases |
| `role="switch"` on a native checkbox input | The native input keeps the keyboard and form behavior; the role makes assistive technologies announce on and off instead of checked |
| No `error` state | The effect is immediate, so there is no value to validate on submit and nothing for the user to fix in the control. A failed change is undone and reported by the project, outside the switch |
| No indeterminate | A setting is on or off; a mixed state would hide that one of the two is applied |
| Label does not change with the state | Assistive technologies already announce on and off; "Notifications on" would be read twice |
| Thumb position carries the state besides the fill | WCAG 1.4.1: the state must not rely on color alone |
| Track 2 to 1 from existing tokens | `icon-md` and `control-md` (and `icon-lg` and `control-lg`) are in a 2 to 1 ratio at every density, so no new token is needed |
| Thumb same size on and off | A smaller off thumb is a style choice that adds a second diameter to the spec; the position already says which state it is |
| Off thumb in `outline` | The thumb has no text, so it must still reach 3:1 against the surface; `outline` is already checked by the script |
| Stadium track whatever the corners | The switch shape is recognized by its fully rounded track; the theme radius would give a square track in a sharp theme |
| No group | A list of switches is a settings layout of independent controls; a fieldset would suggest a shared value |
