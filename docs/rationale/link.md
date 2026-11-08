# Link rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Two variants, `inline` and `standalone` | Underline rules differ: a link in a sentence needs a non-color cue (WCAG 1.4.1), a link in a list or footer does not need it at rest. Material 3 and Spectrum split links the same way |
| `inline` has no size and no icon | It follows the surrounding text, so it can never break the line height or mismatch its sentence |
| Content color moves between states | A link has no fill, so the "background moves first" rule has nothing to move. The color follows the State colors rule (`primary`, plus 2, plus 4 steps), which keeps each state darker than the previous one |
| Fill-less exception in the conventions | The script required a darker background per state; links keep the surface, so the content order is checked instead. The exception is limited to entries whose background is `{colors.surface}` in two consecutive states |
| `link-hover` and `link-pressed` use the brand hover and pressed colors | They are steps of the brand scale, darker than the default, so 4.5:1 on the surface holds by construction. `primary-hover` and `primary-pressed` join the accent tokens allowed on the surface |
| `visited` has its own token, `colors.link-visited`, a step of the `primary` scale | A distinct color is the only thing browsers allow for `:visited`. Reusing `on-surface` made a visited link look like body text, so the user could not tell it was a link. A dedicated violet (then an olive when the brand was violet) added a hue unrelated to the brand and a special case; a step of the brand scale keeps one hue. Only steps `600` to `900` reach 4.5:1 on the surface, and `default` is always `600` (a later default is refused, because hover and pressed would merge), whose hover and pressed are `800` and `900`. The only free step is `700`, so `link-visited` is `primary-d + 1`. It is distinct from the three, passes 4.5:1 because it is darker than `600`, and no search is needed. Downside, accepted: `700` is close to `600` (for example `blue-700` against `blue-600`), so the visited cue is subtle. Underline and context carry the meaning, and visited is an extra cue (WCAG 1.4.1). No lighter step is allowed, because steps below `600` fail 4.5:1 on the surface |
| `link-visited` is derived, not asked | No question is needed: it is a reference to a step of the brand scale, resolved by `theme.py` like the other state colors. The user can change the reference after generation |
| `link-visited` in dark mode is `primary` desaturated | In dark mode the step right after `primary` is the one of `primary-hover` (default minus 1), so the light rule would confuse a visited link with a hovered one. The visited link keeps the lightness and the hue of `primary` with half of its chroma: same contrast, still no second hue. See Dark mode in `docs/conventions.md` |
| `visited` is overridden by `hover` and `pressed` | The user is interacting: the feedback of the interaction wins, then the link returns to its visited look |
| Focus ring radius `{rounded.overlay}` | A text box has no radius of its own; `{rounded.control}` would give a stadium ring in the pill style, which looks wrong on a line of text |
| Inline exempt from target size | WCAG 2.5.8 exempts targets that sit inside a sentence; `standalone` must reach 24 by 24 |
| Own focus-ring entry | Same reason as the chip: the report names the component and the theme stays valid with any subset of components |
| Icon in an inline link `out-of-scope`, link without label `forbidden` | The inline link has no size, so no icon size exists, and the paragraph line height must not change. A link without a visible label has no clear name: use an icon-only button |
