# Avatar rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Fallback order image, initials, icon | An image can be missing or fail to load; the avatar must never show a broken image or change size. Spectrum and Material-style libraries use the same chain |
| Fill and content equal to the chip avatar | A chip and a standalone avatar of the same person look the same; the pair is already checked (`chip-default-pressed`) |
| One look, no variants | Colors derived from the name need a palette of identity colors, which is beyond this kit. One neutral look is always readable |
| Circle only | Matches the chip avatar. Square avatars (organizations) are a later extension and need a radius decision |
| Four sizes with own tokens | `xs` (24 px) for dense rows, `l` (56 px) for profile headers. Sizes reuse existing control and icon tokens, so density applies |
| `xs` shows one initial | Two letters do not fit a 24 px circle at the smallest label size; the chip uses the same fallback |
| Never interactive | A clickable avatar is a button or a link with its own focus ring and target size; the avatar stays a plain visual |
| `label` empty means decorative | Next to a written name, an alt text would be announced twice (WCAG technique for adjacent text); the spec makes the choice explicit |
| Own `components` entry despite equal pair | Same reason as the chip entries: the report names the avatar |
