# Badge rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Count and dot only, no text | Material 3 badges are exactly these two forms. A text badge is a status label: a different job (and the chip spec used to point at it), kept out of this lot |
| Not a chip | A chip is an interactive control with a label. A badge is attached, passive, numeric; mixing them would blur two accessibility models (button semantics versus text attached to a host) |
| `dot` forbidden on `neutral` | Without text, the shape must reach 3:1 against its surroundings (WCAG 1.4.11). `primary` and `danger` do through the State colors rule; neutral step 200 does not |
| Fully rounded, fixed geometry | A badge is a pill by nature, as the chip avatar is a circle. It must not follow the corner style: a sharp theme would make a square dot |
| Two sizes, heights from icon tokens | `s` (16 px by default) suits a 20 px icon, `m` the usual hosts. Material 3 has two sizes (6 and 16 dp) |
| `label` required | A visible number alone does not say what it counts; the dot says nothing to assistive technologies without it |
| Visible digits hidden from assistive technologies | The number is read once, inside `label`, with its meaning |
| `max` 99 with "99+" | Matches Material 3 and keeps the badge narrow; `label` keeps the real number |
| Zero not rendered | A badge with 0 signals nothing and adds noise |
| Colors reused | `primary`, `danger`, and the chip neutral cover the three useful intents; no new token |
