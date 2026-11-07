# Avatar rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Fallback order image, initials, icon | An image can be missing or fail to load; the avatar must never show a broken image or change size. Spectrum and Material-style libraries use the same chain |
| Fill and content equal to the chip avatar | A chip and a standalone avatar of the same person look the same; the pair is already checked (`chip-default-pressed`) |
| One look, no variants | Colors derived from the name need a palette of identity colors, which is beyond this kit. One neutral look is always readable |
| Shape follows its own radius token, `rounded.avatar` | A hard-coded circle could not be changed in the theme. Reusing `rounded.control` would turn avatars into rounded squares in the default soft theme, and the default must stay round. A dedicated token defaults to the largest radius (a circle, not asked in the questionnaire) and lets a theme that wants squarer avatars (organizations) change one value. The chip avatar stays a circle inside its chip |
| Four sizes with own tokens | `xs` (24 px) for dense rows, `l` (56 px) for profile headers. Sizes reuse existing control and icon tokens, so density applies |
| `xs` shows one initial | Two letters do not fit a 24 px circle at the smallest label size; the chip uses the same fallback |
| Never interactive | A clickable avatar is a button or a link with its own focus ring and target size; the avatar stays a plain visual |
| `label` empty means decorative | Next to a written name, an alt text would be announced twice (WCAG technique for adjacent text); the spec makes the choice explicit |
| Own `components` entry despite equal pair | Same reason as the chip entries: the report names the avatar |
| Several contents, or none, are `out-of-scope` | The fallback order shows one content at a time and always ends with the person glyph, so the kit has no layering and no empty look to specify |
