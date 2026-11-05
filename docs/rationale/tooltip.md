# Tooltip rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| `plain` only | Material 3 separates plain and rich tooltips; a rich tooltip holds actions, which a tooltip must never hold (Carbon), so it belongs to a popover spec |
| Dark solid container, light text | "Dark background with light content" case of the Contrast pairs rule; Material 3 plain tooltips use an inverse surface |
| Neutral step `900` | The step farthest from `{colors.surface}`, so the tooltip separates from light screens; white on it has the highest margin above 4.5:1 |
| New `inverse-surface` and `on-inverse-surface` tokens | No existing token is a dark neutral; reusing `{colors.on-primary}` for the text would tie the tooltip to the brand color by name |
| No sizes, one maximum width | A tooltip follows its text; Spectrum (160) and Radix Themes (360) both cap the width |
| Maximum width as a theme token | It depends on font size and density, which are theme choices |
| New `rounded.overlay` | A tooltip can wrap onto several lines; with a pill theme, `{rounded.control}` would turn a multi-line tooltip into a stadium shape |
| Padding and offset reuse `{spacing.sm}` and `{spacing.xs}` | Spectrum uses an offset of 4 and a container padding of 8; the theme's small spacing steps match without new tokens |
| Elevation `level-2` | The tooltip is an overlay tied to a trigger and shown briefly, the role of `level-2`; Material 3 menus use level 2. `level-3` is kept for elements that stay above content while it scrolls. `level-4` and `level-5` are interaction levels, and the tooltip is never interactive |
| Arrow optional, off by default | Radix makes the arrow optional; Material 3 plain tooltips have none |
| Shadow on the outline when possible, on the container otherwise | A single shape shadow is not available on every platform; the arrow is small, so a shadow on the container alone keeps the depth cue, while a seam between arrow and container would break the shape |
| Default placement `top`, aligned center, flip when space runs out | Radix and Spectrum default to `top`; Radix aligns center by default |
| Delays are behavior constants in the spec | DESIGN.md has no duration token type, and adding a non-standard key breaks the kit's rule of standard-only tokens. Delays serve accessibility and usability, not brand identity, so they are invariant |
| Open delay 700 ms, skip delay 300 ms | Radix defaults (`delayDuration`, `skipDelayDuration`) |
| Opens at once on focus | Keyboard focus is a deliberate action; a delay would slow keyboard users |
| Hover and focus, `Escape`, hoverable, persistent | WCAG 1.4.13 Content on Hover or Focus; Carbon requires hover and focus and `Escape` to close |
| Description, not name | Carbon allows one or two words for an icon-only button; the button must still carry its own accessible name, so the tooltip never becomes the only source of it |
