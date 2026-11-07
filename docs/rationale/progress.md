# Progress rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Linear and circular in one spec | They share the role, the properties, the modes, and the tokens; only the geometry differs. Material 3 documents them as one component |
| Mode derived from `value` | Two properties (`type`, `value`) cover four configurations; `aria-valuenow` is absent exactly when `value` is, so the markup follows the data |
| Separate from the button `spinner` | The button spinner is part of a button, sized by the icon size of the button and colored by its content. The progress is standalone and has its own sizes and name. The button spec is untouched |
| Indicator color on the surface, not on the track | The kit checks contrast against `{colors.surface}` only. With the State colors rule (4.5:1 on the surface), the indicator also reaches about 3:1 against a neutral step 200 track, because the surface is near white and the track is a light gray |
| Track `{colors.neutral-subtle-pressed}` | Reused token, quiet, and distinct from the surface so that the full range is visible. The track alone has no contrast requirement: the indicator carries the information |
| `danger` variant with a mandatory message | The color alone must not say "failed" (WCAG 1.4.1). Success and warning variants are not covered by the kit yet |
| Two sizes for linear, three for circular | A bar has a thickness and takes the container width; a ring has a diameter. Different dimensions justify different size sets |
| Circular stroke `{spacing.focus-ring-width}` for `s` | The button spinner uses the same stroke at icon size, which gives the same weight at 20 px |
| Motion slowed, not stopped, with reduced motion | An indeterminate progress without motion is indistinguishable from a stuck one; WCAG 2.2.2 exempts essential activity. Slowing it by about 2.5 to 3 times (checked on a demo) lowers the discomfort while it still shows that work is going on |
| Behavior constants not tokens | Same rule as the tooltip delays and the button spinner turn: invariant, never overridden by a theme |
| Completion announced by the project | The component cannot know the result of the operation, so it asks for a polite announcement and removal |
