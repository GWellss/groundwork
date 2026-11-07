# Alert rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| One component, `inline` and `banner` layouts | Parts, colors, roles, and behavior are the same; only the geometry of the container differs. Two components would duplicate every rule and drift |
| Four severities: `info`, `success`, `warning`, `danger` | The usual set. Each has a color role in the theme except `info` |
| `info` uses the brand tonal container | No new color for a neutral meaning. A gray info alert would sit on the surface step and be nearly invisible; the brand tint reads as a message. Cost: a brand hue close to the warning or danger hue blurs them, which the out-of-scope note flags. The icon and the text carry the meaning anyway |
| Tonal fill (steps 50 to 200) with dark content, no solid fill | A solid alert shouts and needs white content on large areas; the tonal model already exists for the brand (`primary-container`) and keeps the whole kit consistent. Text contrast is the plain `light` family rule: no exception |
| 12 new tokens (three roles times container, hover, pressed, and content) | The controls inside the alert need hover and pressed fills, and a no-fill control cannot move its content (it is already the darkest step). Reusing the tonal model avoids any contrast exception; the cost is twelve tokens, which the script derives |
| `action` and `close-button` are parts of the alert, not `button` or `link` components | The button spec's `primary` content is checked on the surface only; on a green or red tint it would be an unchecked pair. Their own content color is checked on the three tonal fills |
| Focus ring in the content color | `focus-ring` is checked at 3:1 on a fixed list of fills. Adding twelve more fills would make that list fragile (some brand hues would fail on some tints). The content color is at least 4.5:1 on all of them, so the ring is at least 3:1 with no new check. This is the one place the ring color changes, and it is stated in the conventions |
| Icon required, with an accessible name | Color alone cannot carry severity (WCAG 1.4.1). The icon is the non-color cue, and screen reader users need its name |
| `danger` is `role="alert"`, the others `status` | A failure the user must know now is announced assertively; the rest waits until the user is idle. An alert rendered with the page takes no live role, because live roles announce changes, not initial content |
| `banner` layout never takes the `banner` landmark role | That role is the page header; reusing the word would mislead assistive technology |
| One action, no link in the message | A link in the message would be an unchecked accent on a tonal fill. One action is enough; several choices are a dialog |
| Not closable by default, never auto-dismissed | An alert states something that is true; it should not vanish by itself. A message that disappears on a timer is a toast |
| Radius `overlay`, flat banner | The pill style would make a multi-line alert a stadium. A banner touches the edges of the page, so it has no radius and only a bottom border |
