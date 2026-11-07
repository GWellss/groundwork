# Link rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Two variants, `inline` and `standalone` | Underline rules differ: a link in a sentence needs a non-color cue (WCAG 1.4.1), a link in a list or footer does not need it at rest. Material 3 and Spectrum split links the same way |
| `inline` has no size and no icon | It follows the surrounding text, so it can never break the line height or mismatch its sentence |
| Content color moves between states | A link has no fill, so the "background moves first" rule has nothing to move. The color follows the State colors rule (`primary`, plus 2, plus 4 steps), which keeps each state darker than the previous one |
| Fill-less exception in the conventions | The script required a darker background per state; links keep the surface, so the content order is checked instead. The exception is limited to entries whose background is `{colors.surface}` in two consecutive states |
| `link-hover` and `link-pressed` use the brand hover and pressed colors | They are steps of the brand scale, darker than the default, so 4.5:1 on the surface holds by construction. `primary-hover` and `primary-pressed` join the accent tokens allowed on the surface |
| `visited` has its own token, `colors.link-visited` | A distinct color is the only thing browsers allow for `:visited`. Reusing `on-surface` made a visited link look like body text, so the user could not tell it was a link. A step of the brand scale could collide with default, hover, or pressed when the default step is later in the scale. A violet generated for the theme is the convention readers already know, and it is a different hue from the brand, so it never equals `primary` |
| `link-visited` is generated, not asked | The questionnaire stays at 8 questions. `theme.py` searches the OKLCH lightness from 0.54 downward until the color reaches 4.5:1 on the surface; the hue is violet (300), or the opposite of the brand hue when the brand is already within 40 degrees of violet. The user can change the value after generation |
| `visited` is overridden by `hover` and `pressed` | The user is interacting: the feedback of the interaction wins, then the link returns to its visited look |
| Focus ring radius `{rounded.overlay}` | A text box has no radius of its own; `{rounded.control}` would give a stadium ring in the pill style, which looks wrong on a line of text |
| Inline exempt from target size | WCAG 2.5.8 exempts targets that sit inside a sentence; `standalone` must reach 24 by 24 |
| Own focus-ring entry | Same reason as the chip: the report names the component and the theme stays valid with any subset of components |
