# Badge rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Count, dot, and status text | Material 3 badges are count and dot. Smart Interface Design Patterns defines badges as always static and used for feedback indicators, notification counts, and status updates (draft, new, pending, -7%), so a short text form belongs to the badge family. Static data tags ("PDF 262 KB") sit in the same static family and use the `neutral` status badge |
| Text form named "status badge" | Naming it explicitly keeps it apart from the chip in specs, code, and conversation. Interactive components (chips) must look different from static ones |
| Status badge: no states, no border, no icon, smaller than any chip, radius `rounded.overlay` | The chip is the interactive one: it has hover, pressed, focus, a border, icons, and the control radius (a stadium in pill themes). The status badge shares none of these, is shorter than the smallest chip (`icon-md` or `icon-lg` against `control-xs`), and never takes a stadium shape, so it cannot be mistaken for a button |
| Status badge needs no host, count and dot do | A status stands next to the content it qualifies or in a table cell; a number or a dot means nothing without the element it counts |
| Status badge reuses `primary`, `danger`, `neutral` | No new color, no new `components` entry: the existing pairs already pass 4.5:1. Success and warning colors do not exist in the theme; adding semantic roles is a separate decision |
| Not a chip | A chip is an interactive control with a label. A badge is attached, passive, numeric; mixing them would blur two accessibility models (button semantics versus text attached to a host) |
| `dot` forbidden on `neutral` | Without text, the shape must reach 3:1 against its surroundings (WCAG 1.4.11). `primary` and `danger` do through the State colors rule; neutral step 200 does not |
| Fully rounded, fixed geometry | A badge is a pill by nature, as the chip avatar is a circle. It must not follow the corner style: a sharp theme would make a square dot |
| Two sizes, heights from icon tokens | `s` (16 px by default) suits a 20 px icon, `m` the usual hosts. Material 3 has two sizes (6 and 16 dp) |
| `label` required | A visible number alone does not say what it counts; the dot says nothing to assistive technologies without it |
| Visible digits hidden from assistive technologies | The number is read once, inside `label`, with its meaning |
| `max` 99 with "99+" | Matches Material 3 and keeps the badge narrow; `label` keeps the real number |
| Zero not rendered | A badge with 0 signals nothing and adds noise |
| Colors reused | `primary`, `danger`, and the chip neutral cover the three useful intents; no new token |
