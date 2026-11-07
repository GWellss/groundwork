# Text field rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Outlined field only, no filled appearance | One appearance keeps the spec small; the outlined box gives the clearest boundary, and the fill is kept for the read-only state, where it carries meaning |
| Visible label always, never floating or inside | A label that disappears on focus (placeholder as label) fails users with memory or attention issues and breaks the accessible name; the label stays above the field |
| Border is `{colors.outline}` at 3:1 | WCAG 1.4.11 asks 3:1 for the boundary of an input. The lint only checks `backgroundColor`/`textColor` pairs at 4.5:1, so it cannot see a border. A `components` pair would impose 4.5:1, stricter than the rule, and `neutral-500` (about 3.5:1) would fail it; a non-standard property is forbidden. The theme script checks the one border pair at 3:1 outside the lint |
| `outline` falls back to neutral step `600` | Some neutral tints may give less than 3:1 at step `500`; the script then takes step `600` rather than reporting a theme the user cannot fix |
| New token `on-surface-muted` | The placeholder and the helper text must be visibly quieter than the typed value, yet reach 4.5:1 (placeholder is text for WCAG 1.4.3). The Contrast pairs rule allows only steps `700`-`900` as content, and `on-surface` is already `700` in the default theme, so no existing token could be quieter. Step `600` is about 4.9:1 on the surface; the family rule lists it as an accent on the surface only |
| `hover` moves the border, not the content | The field has no fill. For a text input, changing the typed text color on hover would be odd; the border is the part that changes. Fill-less exception of the conventions, applied to a border. Text pairs stay unchanged |
| Focus adds only the ring | Same rule as button, chip, and link: focus never changes tokens. The ring is enough for WCAG 2.4.7 and avoids a second border color to keep at 3:1 |
| Error: danger border + icon + text | WCAG 1.4.1: never color alone. The message replaces the helper text in the same slot so the layout does not jump twice |
| No `error` with `disabled` or `read-only` | The user cannot fix such a field, so an error there is a dead end; the project resolves the cause elsewhere |
| `error` derived from `error-message` | Same pattern as progress mode from `value`: one property, no way to be in error without saying why |
| Read-only is filled; disabled is filled differently | Read-only stays readable and focusable, so it keeps the standard text pair on a quiet fill; disabled uses the exempt disabled tokens |
| Counter outside `aria-describedby` | Reading the count at every keystroke is noise; the project announces thresholds |
| Single line has no vertical padding | Same as the chip: height is fixed by the control token, content centered. Multiline needs padding and a minimum height by rows |
| Vertical resize only | Horizontal resize breaks layouts and the full-width rule |
| Affixes and icons single line only | In several lines their alignment is ambiguous (first line or centered) |
| `type` limited to four values | Those change keyboard and validation on touch screens; password and number add reveal and stepper controls, out of scope |
| Affixes and icons of a read-only field use `on-surface` | `on-surface-muted` is checked on the surface only; on the read-only fill (neutral 100) it falls below 4.5:1. The rule is general (see `docs/conventions.md`, Muted text): muted text never sits on a grayed fill |
| `error` with `read-only` is `avoid`, with `disabled` `forbidden` | In both cases the user cannot fix the value, a dead end. A read-only field is focusable, so its message can be read and the kit only discourages it. A disabled field leaves the tab order, so its error cannot be reached by keyboard. A field without a label is `forbidden`; an icon with an affix on one side, and elements on a multiline field, are `out-of-scope` |
