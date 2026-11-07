# Checkbox rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| The checkbox spec is the base of radio and switch | The row, the label, the help, the error, the group, and the state tables are identical for the three controls. Stating them once avoids drift; radio and switch only state their differences, as the search field does for the text field |
| Whole row is the click target | A box of 16 to 20 pixels is hard to hit; the label belongs to the target (WCAG 2.5.8 and common usage), and there is no dead zone between control and label. The helper text is outside, so reading it does not toggle anything |
| Group help and error once, none on an option | In a group the message concerns the whole choice ("pick at least one"). An error per option would repeat it and move the layout. Option descriptions are out of scope for now |
| Group is a native `fieldset` with `legend` | It is the native way to name a group; a visible legend is the group label and no `aria-label` is needed |
| `indeterminate` is set by the project | It summarizes children; it is not a third value the user can pick. A click goes to `checked` |
| Selection in primary, unselected is an empty box | The brand color is the "on" color of every choice control, as the chip `selected` group. The off box has a border only, so the fill carries the meaning |
| Unselected hover moves the border, pressed adds a quiet fill | There is no text to move and no fill to darken: the border moves first (fill-less rule applied to a border), then a neutral fill appears on pressed so that hover and pressed differ. Neither is a pair |
| Pressed border is `on-surface`, not `outline` | `outline` on the pressed fill (neutral 100) falls below 3:1; `on-surface` keeps the boundary visible |
| Error: danger border when unselected, danger ring when selected | What matters is the gap between the normal state and the error state. Changing the fill of a selected box from `primary` to `danger` moves it by only 1.07:1 (default theme): almost invisible, and invisible to many people with color vision deficiency. Adding a danger ring where there was only the surface moves it by 4.71:1. Secondary benefit: the box keeps its primary fill, so it still reads as checked |
| A surface gap between the selected control and its error ring | Danger and primary side by side are 1.07:1 apart and merge. The gap shows the surface, against which danger reaches 4.71:1 and primary 5.0:1, so each color is read on its own |
| Error ring reuses the focus ring width and offset | No new token, same visual language. Focus is drawn outside the error ring so the two stay readable together (control, gap, danger, gap, focus) |
| Ring contrast is covered by `checkbox-error` | The ring is `danger` on the surface, the pair already declared at 4.5:1, above the 3:1 required for a non-text part. No script change |
| No `outline` check of its own | The unselected border is `colors.outline`, already checked at 3:1 by the script; `primary` and `danger` are at 4.5:1 or more against the surface by the State colors rule. No new non-text pair exists |
| Radius capped at a quarter of the control size | With `rounded` or `pill` corners the theme radius would turn a 16 or 20 pixel box into a circle, which reads as a radio button. A rounded square keeps the two controls apart in every theme |
| Control size `icon-sm` and `icon-md`, mark as large as the control | Existing tokens; the library glyph already has internal margins. Heights of the row come from control tokens so the click target is at least 24 pixels at every density |
| Label typography as the text field | A checkbox and a text field sit in the same form and should read at the same size |
| Disabled border is `on-disabled` | A disabled unchecked box with a `disabled-container` border is almost invisible; the disabled tokens are exempt from contrast but the shape should stay recognizable |
| Own entries for the selected mark, text entries shared | The mark on the primary fill is the same pair as the filled button, but the report names the checkbox. The text pairs are the same for the four controls: declared once under the checkbox name |
