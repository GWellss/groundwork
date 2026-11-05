# Chip rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Two booleans instead of four types | Material 3 has four types (assist, filter, input, suggestion), but assist and suggestion differ only in intent, not in anatomy or behavior. `selectable` and `removable` cover filter and input; their absence covers assist and suggestion. Spectrum also models its Tag with booleans (`isRemovable`, `isDisabled`) |
| `selectable` and `removable` exclusive | Two competing targets on a small control; Material 3 shows the remove icon only on input chips, not on filter chips |
| Remove button as a separate focusable control | It has its own action and its own accessible name; merging it with the body would hide the removal from keyboard and screen reader users |
| Removable body not interactive | Keeps a single target per chip; editing an input chip is out of scope |
| Toggle semantics for `selectable` | A filter chip is an on and off control; a pressed state is the standard way to expose it |
| `check-icon` mandatory when selected | WCAG 1.4.1 forbids conveying selection by color alone; Material 3 filter chips show a leading checkmark |
| No avatar on `selectable` | The leading slot is needed for `check-icon`; an avatar swapped for a checkmark would lose the identity it shows |
| Sizes `s` and `m` only | Material 3 has a single height (32dp minimum); `m` maps to the second control height of the theme, `s` adds a dense option. A five-size range has no use for chips |
| Neutral `default` group | A chip that is off must not look like a chip that is on: the brand color is reserved for `selected`, which also removes any confusion between hover and selected |
| New `neutral-subtle-hover` and `neutral-subtle-pressed` | No existing token is a neutral fill for hover and pressed; the brand subtle tokens would tint the off state. Surface is neutral step 50, so the "Surface scale" case of the Contrast pairs rule gives surface, step 100, step 200 |
| New `on-surface` | No existing token is a dark neutral content color for text on the surface; `{colors.on-disabled}` is for disabled only. One token serves all states, as the Contrast pairs rule prefers |
| `colors.outline` reused | It is already the neutral border of the outlined button |
| `selected` reuses the tonal tokens | Steps 50, 100, 200 are the only `light` triple; steps 300 and above are `intermediate` and carry no text |
| Own `components` entries despite equal pairs | The contrast report names the chip, and each spec lists its own entries, so a theme stays valid whatever components it includes |
| Radius `{rounded.control}` | Chips match buttons, and a chip is always a single line, so every corner style, pill included, keeps a regular shape |
| Avatar fill `{colors.neutral-subtle-pressed}`, initials `{colors.on-surface}` | Reuses existing tokens: the pair is already checked as `chip-default-pressed`, and step `200` stays visible on the surface and on the hover container. Without a defined fill, generated code invented a color |
| Avatar fill constant across interactive states | The avatar identifies an entity; changing its fill on hover adds no feedback the container does not already give |
| `remove-button` ring without offset | With the shared offset, the ring would reach into the gap and could cover the label at small sizes or compact density |
