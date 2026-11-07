# Button rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Five sizes `xs` to `xl` | Matches Material 3; Spectrum and Radix use four |
| Two optional icons | Explicit need; Spectrum only offers a leading icon |
| Icon-only as a property | Same approach as Spectrum `isLabelHidden`: variants, states, and tokens stay shared; only geometry changes. Material 3 and Radix use a separate component |
| `loading` as a state property | Present in Spectrum (pending) and Radix (loading) |
| Emphasis variants | Material 3 naming (filled, tonal, outlined, text); Radix uses solid, soft, outline, ghost |
| Explicit state color tokens | Every cell is a real color the lint can check, no opacity rule hidden in the kit |
| `danger` variant | Destructive actions need a distinct, recognizable signal; it has its own tokens and matrix |
| State colors from palette scales | Hover and pressed come from a rule on a primitive scale, so the user only gives a base color |
| Content darkens on `outlined` and `text` hover and pressed | The tinted hover and pressed backgrounds are `light` steps, which carry only steps `700` to `900`; keeping `{colors.primary}` would fail 4.5:1 or force the pressed background back to the hover one, hiding the press feedback |
| Content adjusts to the background, also on `tonal` | The rule "the content adjusts to the background, never the reverse" applies to `tonal` as well, not only to `outlined` and `text`: `{colors.on-primary-container}` is searched in steps `700`, `800`, then `900` against the `50`, `100`, and `200` backgrounds, and the backgrounds stay fixed |
| One shared `{colors.on-primary-subtle}` | One token is computed against the darker of the two subtle backgrounds, so it is valid for both; a token per state would add a color for no visible gain |
| Standard-only `components` entries | The lint checks contrast only there; standard properties keep the theme valid and the kit non-intrusive |
| Floating as a property, not a component | User decision, same approach as icon-only: variants, states, and tokens stay shared; only elevation, allowed variants, and allowed sizes change. Material 3 uses a separate FAB component |
| Floating icon-only and extended | Material 3 offers both the FAB and the extended FAB; both map to existing configurations of the button |
| Floating `filled` and `tonal` only | A floating button covers content, so it needs its own fill; Material 3 FAB colors are filled containers. `danger` is excluded so a destructive action is never the one always at hand |
| Floating sizes `l` and `xl` only | A floating button is the main action and is often used on touch; Material 3 FAB is 56dp by default, larger than a standard button, and `l` and `xl` are the closest control heights |
| Floating at `level-3` at rest, `level-4` on hover | Material 3 FAB: resting level 3, raised one level on hover; `level-3` is the highest resting level of the scale |
| Floating `pressed` at `level-3` | Material 3 FAB pressed returns to its resting level (unverified against the current Material 3 spec); `level-5` stays reserved for drag |
| Floating `disabled` and `loading` at `level-3` | Neither state has hover, so both keep the resting level; the button keeps floating above the content. Material 3 FAB has no disabled state, so this is a kit decision |
| No new `components` entry for floating | The floating colors are the `filled` and `tonal` pairs, already declared |
| Spinner size and stroke from existing tokens | The icon size keeps the spinner in proportion with the content it replaces; `{spacing.focus-ring-width}` gives a visible stroke at icon sizes, where `{spacing.border-width}` is too thin, without a new token |
| Spinner slowed, not stopped, under reduced motion | Same rule as the progress indicator: a static arc is indistinguishable from a stuck button, and WCAG 2.2.2 exempts essential activity. The turn takes about 2.5 to 3 times longer, which lowers the discomfort while the spinner still shows that loading goes on |
| `spinner-turn` as a behavior constant | Same reason as the tooltip delays: DESIGN.md has no duration token type, and the speed serves usability, not brand identity |
| `aria-busy` instead of native disabled for `loading` | Native disabled removes focus, which the Loading requirement keeps; the style reads the same attribute, so there is one source of truth |
