# Radio rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Built on the checkbox, differences only | Same row, label, help, error, group, and tokens; repeating them would let the two drift |
| Never alone | A lone radio button cannot be unselected, which makes it a trap; a single option is a checkbox |
| Group `value` instead of `checked` per option | The selection is a property of the group (at most one), so one source of truth and no way to select two |
| Arrows move and select | Native radio behavior; delaying the selection to `Space` would differ from what keyboard users expect and from the platform |
| `fieldset` with `role="radiogroup"` | `aria-invalid` is supported on a radio group but not on a plain group or on a radio, so the error needs the role on the container |
| Circle and dot are fixed geometry | A radio button is a circle by definition; using the theme radius would turn it into a square in a sharp theme |
| Dot size `spacing.sm` for both sizes | An existing token that gives 40 to 50 percent of the circle at the default density; no new token |
| Same fills as the checkbox | Selected in primary with a white dot, unselected as an empty circle: the two controls read as a family |
