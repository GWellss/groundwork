# Divider rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| No new token | The `subtle` line reuses `{colors.neutral-subtle-pressed}` (neutral step 200) and `strong` reuses `{colors.outline}`; both already exist for the chip and the outlined button |
| Two variants, `subtle` and `strong` | A quiet line is the common case, but a divider that alone separates groups must stay visible (WCAG 1.4.11). Material 3 also has a single quiet divider; the second variant covers the informative case it leaves open |
| `decorative` true by default | Most dividers repeat a separation that spacing and structure already give; announcing each one would add noise for screen reader users |
| No label, no icon | A divider with text is a heading in disguise; Material 3 and Spectrum keep the divider content-free |
| One thickness, `{spacing.border-width}` | The theme already has a hairline token; a thickness scale has no use |
| No `components` entry | The line carries no text, so it is not a contrast pair (see Contrast pairs in `docs/conventions.md`) |
