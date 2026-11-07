# Card rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Minimal anatomy: media, header, body, actions | Those four parts cover the cards of every major system. Anything more (a header menu, a subtitle, a badge) goes in the body, so the card stays a container and not a catch-all |
| Static or clickable, avoid both | A link or a button inside another link or button is invalid HTML, and two hit areas on one surface are ambiguous for keyboard and touch, which is why the kit says to avoid it. It is not forbidden: the "stretched link" form (the heading link covers the card, other controls sit above it as siblings) is valid HTML and works when done carefully. It is harder to get right (focus order, click target, hover feedback), so it is the exception and the spec lists its conditions. The simple, easy-to-check path stays: a clickable card has no actions |
| Clickable card is one native link or button around the whole card | The platform gives the role, the focus, and the keys. The name comes from the heading (`aria-labelledby`), so a screen reader does not read the whole card as the name |
| Two variants, `outlined` and `elevated` | The brief asked for either a border or an elevation. Both are common; they differ by depth only, so tokens and rules are shared |
| Quiet border for a static card, `outline` for a clickable one | The `outline` border (3:1) is the cue that tells a clickable card from a static one beside it, at no extra token. A static card needs no 3:1 border: nothing is interactive |
| Hover and pressed fill with the neutral fills, not only a shadow | Elevation never carries feedback alone, so users who lose the shadow still see the change. The neutral fills are the ones menu items and accordion headers already use, so there are no new pairs |
| `on-surface-muted` only in a static card | Hover turns the fill gray, where muted text falls under 4.5:1 (see Muted text in the conventions). A clickable card therefore uses `on-surface` for all text |
| Elevated rest `level-1`, hover `level-4`, pressed back to `level-1` | The resting levels are 0 to 3 and interaction levels are 4 and 5, so hover must use `level-4`; `level-2` and `level-3` are resting roles. Pressed returns to rest, as the floating button does. The jump is visible but the fill also changes |
| No text over media | Contrast is checked against the surface only; a text over an image cannot be checked by the kit |
| Radius `overlay` | The card is a container, not a control, and the pill style would turn it into a stadium |
| No card inside a card, no wrapper for a section | A card groups one subject among others. Wrapping everything makes grouping meaningless; spacing and a divider are the tools for sections |
| No new color, no new token | The card is made only of tokens that already exist |
