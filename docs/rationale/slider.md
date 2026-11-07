# Slider rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Native `input` of type `range` | It already gives the role, the value properties, the keyboard (arrows, Page, Home, End), and the form value. The spec describes the look and the expectations around it |
| Visible value by default | A thumb position alone gives an approximate value; the number is the exact feedback and the accessible value stays the same |
| `value-text` | The bare number is often meaningless ("20" for a price); `aria-valuetext` and the visible label carry the unit |
| Row is the hit area | The thumb (16 to 24 pixels) is small on touch screens; the whole row accepts pressing and dragging, and meets 24 pixels at every density |
| Track in `outline`, fill and thumb in `primary` | The unfilled track must reach 3:1 (WCAG 1.4.11): `outline` already does and is checked by the script. The primary fill is at 4.5:1 or more by the State colors rule |
| Three `slider*` entries for the fill and thumb | Not text, but the color moves on hover and pressed, as the link. The entries make the script check that each state is darker than the previous one |
| Error on fill and thumb in the danger group | A slider with a validation rule (a minimum price) needs an error. The track stays neutral and the icon and message carry the meaning besides the color |
| Range variant in the slider spec, not a separate component | Track, fill, thumb, label, error, tokens, sizes, and states are the same; only the thumb count, the names, the collision rule, and the fill span change. A second spec would duplicate them |
| Thumbs never cross, minimum gap `min-gap` (default `step`) | Swapping thumbs makes the names lie ("Minimum" above "Maximum"); a gap of at least one step keeps both thumbs visible and separately reachable by keyboard. The limit is exposed in `aria-valuemin` and `aria-valuemax` so assistive technologies announce the real bounds |
| Two accessible names plus a group name | A screen reader user hears which thumb they are on ("Minimum price") and the group ("Price"); two thumbs named alike cannot be told apart |
| Press moves the nearest thumb | The user does not choose a thumb before pressing; the nearest is the least surprising. Midway presses go to `thumb-min` because the direction rule cannot decide there |
| Tab order minimum then maximum, whatever the positions | The order never depends on where the thumbs are, so it is predictable even when they are close |
| Fill between the thumbs only | The colored part is the selected interval; coloring from `min` would suggest a single value |
| Circle thumb and rounded track are fixed geometry | A theme radius would square the thumb in a sharp theme and change the control's recognizable shape |
| No tick marks, no tooltip over the thumb, no end labels | Each adds parts and tokens; the visible value label already shows the value. They can be added later without changing this spec |
| Pointer alternative stated | WCAG 2.5.7 asks that a drag has a single-pointer alternative: pressing the track moves the thumb, and the keyboard covers the rest |
