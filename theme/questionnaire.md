# Theme questionnaire

This file is for an AI agent. Follow it to produce a valid DESIGN.md theme from the fewest possible answers from the user. Token names come from the Token contract of every component spec in `components/` (`button.md`, `chip.md`, `tooltip.md`); conventions come from `docs/conventions.md`. Both take precedence over this file if they differ. The contrast rule is defined once, in the "State colors" and "Contrast pairs" sections of `docs/conventions.md`; this file applies it and does not restate it.

## Step 0: identify your level

Before asking anything, find out which tools you have. Pick the highest level that applies. The level decides how you derive colors and how you validate the result; the questions stay the same, except the color questions at Level 3.

| Level | Name | You can | Derivation | Validation |
|---|---|---|---|---|
| 1 | terminal | Run commands | Script `theme/theme.py` | Script contrast report, then the lint `npx @google/design.md@0.4.0 lint` |
| 2 | code execution | Run Python in a sandbox, without a terminal (for example Claude.ai, ChatGPT) | Script `theme/theme.py`, pasted into the sandbox | Script contrast report only (no lint CLI) |
| 3 | no tools | Converse only | Copy from `theme/palettes.md`; never compute | Online contrast checker, run by the user |

### Level 1: terminal

- You do: ask the questions, run `python3 theme/theme.py` with one option per answer (for example `python3 theme/theme.py --name Acme --brand "#7C3AED" --corners pill --out DESIGN.md`; run it with `--help` to list the options), read the contrast report, run the lint, and fix what they report. The script also writes `tokens.css` next to DESIGN.md; `--css <path>` chooses another path.
- You delegate: the color math and the contrast checks, to the script. Do not compute colors by hand.
- Script exit codes: `0` all pairs pass; `1` at least one pair fails; `2` a color is unusable and the script proposes an alternative (follow "When a color cannot reach AA").
- Done when: exit code `0`, and the lint reports 0 errors and 0 `contrast-ratio` warnings (see the Output procedure).

### Level 2: code execution

- You do: ask the questions, paste the content of `theme/theme.py` into the sandbox, call its `main([...])` function with the same options as Level 1, read the contrast report, and give the resulting DESIGN.md and `tokens.css` to the user.
- You delegate: the color math and the contrast checks, to the script. The lint CLI is not available, so the script report is the validation.
- Same exit codes as Level 1.
- Done when: exit code `0` and the report shows every pair passing. Tell the user that the lint was not run, and that they can run it later with a terminal.

### Level 3: no tools

- Never compute a color, a contrast ratio, or a scale yourself, even approximately. Every color value comes from `theme/palettes.md`.
- You do: ask the questions. Replace the `brand` and `danger` questions with "Choose the range closest to your brand color" among the 14 ranges of `theme/palettes.md`. If the user gives a hex code, propose the closest range and say that the match is approximate. For the `neutral` question, map the answer to a range of `theme/palettes.md`: neutral → `gray`, warm → `warm-gray`, cool → `cool-gray`. Do not offer the "tinted with the brand color" option at this level, because no precomputed range exists for it: propose only the other three, and if the user wants a tinted gray, say that it requires Level 1 or Level 2. Take density, corners, and typography from the default tables below. Copy the precomputed steps (`default`, `hover`, `pressed`, and the other steps of the range) into the DESIGN.md. For the neutral-derived colors, use the range chosen for `neutral` (`gray`, `warm-gray`, or `cool-gray`): `on-surface` is the `on-container` row of that range (step `700`, searched against steps `50`, `100`, `200`, which are `surface`, `neutral-subtle-hover`, and `neutral-subtle-pressed`); `neutral-subtle-hover` is step `100`, `neutral-subtle-pressed` is step `200`, `inverse-surface` is step `900`, and `on-inverse-surface` is white. Name the copied scale `neutral` in the DESIGN.md. If a value needed here is missing from `theme/palettes.md`, say so to the user instead of computing it.
- Elevation: copy the default table of "Elevation" below; it needs no computation.
- `tokens.css`: no script writes it at this level. If code is to be generated, write it by copying the values of the DESIGN.md under the variable names of `docs/implementation.md`, semantic colors resolved to the hex of their step, and the font family followed by the fallback stack of "Typography" below. Copy only; never compute.
- You delegate: the final check, to the user, with an online contrast checker such as WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/). List the key pairs to check, each with its two hex values: every `components` entry that pairs a background with a text color (including the 10 `chip-*` entries and `tooltip-plain`), and at least the `primary` on `surface` pair. Neutral-derived values (`on-surface`, `neutral-subtle-hover`, `neutral-subtle-pressed`, `inverse-surface`) come from the range chosen for `neutral`, as described in "Semantic color tokens".
- Done when: the DESIGN.md is delivered, the list of pairs to check is given, and you have said that the contrast was copied from precomputed values and not verified in this conversation.

## Principle

- Ask one question at a time, in the order of the list below.
- Every question comes with a default value. Show it, and let the user accept it with a single word ("ok", "default").
- Skip a question when the user already answered it, or when the answer can be deduced (for example a brand color given in the first message).
- If the user says "use defaults for the rest", stop asking and apply the remaining defaults.
- Never ask about anything that the derivation rules below settle. Ask 8 questions at most.
- Do not mention token names to the user. Speak in design terms (color, corners, density).

## Questions

| Id | Question to ask |
|---|---|
| `name` | What is the name of your design system? (default: the product name if known, otherwise "Design System") |
| `brand` | What is your main brand color? Give a hex code or a color name. (default: `#2563EB`, a blue) |
| `danger` | Which color should signal destructive actions such as delete? (default: `#DC2626`, a red) |
| `neutral` | Which tint should grays and backgrounds have: neutral, warm, cool, or tinted with your brand color? (default: neutral) |
| `font` | Which font should the interface use? (default: the system UI font) |
| `corners` | How rounded should corners be: sharp, soft, rounded, or pill? (default: soft) |
| `density` | How dense should controls be: compact, default, or comfortable? (default: default) |
| `icons` | Which icon style and library? For example outlined, filled, or rounded, from Material Symbols or Lucide. (default: outlined, Material Symbols) |

| Id | Default | Feeds |
|---|---|---|
| `name` | product name, else "Design System" | DESIGN.md `name`, Overview section |
| `brand` | `#2563EB` | primary scale and every `primary-*` and `on-primary*` color; `focus-ring` |
| `danger` | `#DC2626` | danger scale; `danger`, `on-danger`, `danger-hover`, `danger-pressed` |
| `neutral` | neutral | neutral scale; `surface`, `on-surface`, `neutral-subtle-hover`, `neutral-subtle-pressed`, `inverse-surface`, `outline`, `disabled-container`, `on-disabled` |
| `font` | system UI font | `fontFamily` of the 4 typography tokens |
| `corners` | soft | `rounded.control`, `rounded.overlay` |
| `density` | default | `spacing` sizes (control, icon, gaps, paddings, `tooltip-max-width`), `fontSize` of the 4 typography tokens |
| `icons` | outlined, Material Symbols | `## Icons` section (no token) |

## Derivation rules

Everything below is deduced. Do not ask the user about it.

### Palette scales

Build three primitive scales in `colors`: one for `brand`, one for `danger`, one for the neutral tint. Each has 10 steps named `<name>-50`, `-100`, `-200`, `-300`, `-400`, `-500`, `-600`, `-700`, `-800`, `-900`, from lightest to darkest.

- Name a scale after the common English color name of its hue (blue, red, green, orange). If the brand and danger colors share the same name, call the brand scale `brand`. Call the neutral scale `neutral`.
- Method: convert the base color to the OKLCH model (perceptual lightness, chroma, hue). Keep the hue constant across the scale. Set the lightness of each step to a fixed target, then set its chroma to a share of the base chroma, then reduce the chroma if needed until the color fits the sRGB gamut. Output hex values.
- Replace the step whose lightness is closest to the base color with the exact base color, so the brand color appears unchanged in the scale.
- For the neutral scale, use the same lightness targets, but chroma is fixed by the answer to `neutral`, and the hue follows it.

| Step | Target lightness | Share of base chroma |
|---|---|---|
| 50 | 0.97 | 15% |
| 100 | 0.93 | 30% |
| 200 | 0.87 | 50% |
| 300 | 0.79 | 75% |
| 400 | 0.70 | 90% |
| 500 | 0.62 | 100% |
| 600 | 0.54 | 100% |
| 700 | 0.46 | 100% |
| 800 | 0.38 | 90% |
| 900 | 0.30 | 75% |

For the neutral scale, set `neutral-50` to lightness 0.99, so that the surface is nearly white.

| Answer to `neutral` | Chroma | Hue |
|---|---|---|
| neutral | 0 | none |
| warm | 0.010 | 70 |
| cool | 0.010 | 250 |
| tinted | 0.010 | hue of the brand color |

### Content colors

`on-primary`, `on-danger`, and `on-inverse-surface` are white (`#FFFFFF`). The other three content colors depend on the light backgrounds they serve:

- `on-primary-container`: content of the `tonal` variant and of the `selected` chip, on the backgrounds `primary-container`, `primary-container-hover`, and `primary-container-pressed` (brand steps `50`, `100`, `200`).
- `on-primary-subtle`: content of the `outlined` and `text` variants on hover and pressed, on the backgrounds `primary-subtle-hover` and `primary-subtle-pressed` (brand steps `50` and `100`).
- `on-surface`: content of the `default` chip and of the chip remove button, on the backgrounds `surface`, `neutral-subtle-hover`, and `neutral-subtle-pressed` (neutral steps `50`, `100`, `200`: the "Surface scale" sequence of `docs/conventions.md`).

For each of them, apply the content step search of `docs/conventions.md`: test steps `700`, `800`, then `900` of the scale of its backgrounds (brand scale for the first two, neutral scale for `on-surface`), and keep the first one that reaches 4.5:1 against every background it serves. Never change a background to make a content color pass. If no step passes for `on-surface`, report the pair to the user instead of forcing it.

### State colors

Apply the State colors rule of `docs/conventions.md` to the brand scale and to the danger scale separately: `default` is searched from `600` to `900` against the `on-*` color and against `surface`; `hover` is `default` plus 2 steps; `pressed` is `default` plus 4 steps, stopping at `900`. Compute contrast with the WCAG 2.x relative luminance formula.

### Semantic color tokens

Write the 25 colors of the token contracts of the button (20), the chip (3 new), and the tooltip (2 new) as references to scale steps. `<brand>` and `<danger>` are the scale names; `d` is the `default` step of the corresponding scale; `c` is the step found by the content step search above; `n` is the step found by the same search on the neutral scale for `on-surface`.

| Token | Value |
|---|---|
| `surface` | `{colors.neutral-50}` |
| `primary` | `{colors.<brand>-d}` |
| `on-primary` | `#FFFFFF` |
| `primary-hover` | brand scale, `default` + 2 steps |
| `primary-pressed` | brand scale, `default` + 4 steps |
| `primary-container` | `{colors.<brand>-50}` |
| `on-primary-container` | `{colors.<brand>-c}`, searched against `50`, `100`, `200` |
| `primary-container-hover` | `{colors.<brand>-100}` |
| `primary-container-pressed` | `{colors.<brand>-200}` |
| `primary-subtle-hover` | `{colors.<brand>-50}` |
| `primary-subtle-pressed` | `{colors.<brand>-100}` |
| `on-primary-subtle` | `{colors.<brand>-c}`, searched against `50`, `100` |
| `danger` | `{colors.<danger>-d}` |
| `on-danger` | `#FFFFFF` |
| `danger-hover` | danger scale, `default` + 2 steps |
| `danger-pressed` | danger scale, `default` + 4 steps |
| `outline` | `{colors.neutral-500}` |
| `disabled-container` | `{colors.neutral-100}` |
| `on-disabled` | `{colors.neutral-500}` |
| `focus-ring` | same step as `primary` |
| `on-surface` | `{colors.neutral-n}`, searched against `surface`, `neutral-100`, `neutral-200` |
| `neutral-subtle-hover` | `{colors.neutral-100}` |
| `neutral-subtle-pressed` | `{colors.neutral-200}` |
| `inverse-surface` | `{colors.neutral-900}` |
| `on-inverse-surface` | `#FFFFFF` |

If a pair fails, never make two states identical, never move a background back to an earlier step, and never lower the 4.5:1 threshold (see "Contrast pairs" in `docs/conventions.md`). Only the content step can change, within its search. If no step passes, report the pair to the user instead of forcing it, following "When a color cannot reach AA".

### Typography

Write 4 tokens: `label-sm`, `label-md`, `label-lg`, `label-xl`. Each carries `fontFamily` (the answer to `font`; for the system UI font, use `system-ui`), `fontSize`, `fontWeight` 500, `lineHeight`, and `letterSpacing` 0px. Line height is 1.25 times the font size, rounded to the nearest whole pixel and written in px. Font size follows density.

Fallback stack: in `tokens.css`, the font family is followed by generic fallbacks, `system-ui` then `sans-serif` (a generic family is not repeated). DESIGN.md keeps the entered font alone. The kit does not load fonts: if the chosen font is not installed on the target devices, tell the user that the project must load it, otherwise the fallback is shown.

| Density | label-sm | label-md | label-lg | label-xl |
|---|---|---|---|---|
| compact | 12px | 13px | 14px | 16px |
| default | 12px | 14px | 16px | 18px |
| comfortable | 13px | 15px | 17px | 20px |

### Rounded

Two tokens, `rounded.control` and `rounded.overlay`. The overlay radius is moderate in every corner style, so that a multi-line overlay (the tooltip) never turns into a stadium shape.

| Answer to `corners` | `rounded.control` | `rounded.overlay` |
|---|---|---|
| sharp | 0px | 0px |
| soft | 4px | 4px |
| rounded | 8px | 8px |
| pill | 9999px | 8px |

### Spacing

The 19 spacing tokens come from the density table (16 rows) and the constant table (3 rows). Values are in px: this file is the defaults file of the theme, not a component spec. The three constant tokens do not depend on density.

| Token | compact | default | comfortable |
|---|---|---|---|
| `control-xs` | 24px | 28px | 32px |
| `control-sm` | 28px | 32px | 40px |
| `control-md` | 32px | 40px | 48px |
| `control-lg` | 40px | 48px | 56px |
| `control-xl` | 48px | 56px | 64px |
| `icon-sm` | 14px | 16px | 20px |
| `icon-md` | 16px | 20px | 24px |
| `icon-lg` | 20px | 24px | 28px |
| `icon-xl` | 24px | 28px | 32px |
| `xs` | 2px | 4px | 6px |
| `sm` | 6px | 8px | 10px |
| `md` | 8px | 12px | 16px |
| `lg` | 12px | 16px | 20px |
| `xl` | 16px | 20px | 24px |
| `2xl` | 20px | 24px | 32px |
| `tooltip-max-width` | 200px | 240px | 280px |

| Constant token | Value |
|---|---|
| `border-width` | 1px |
| `focus-ring-width` | 2px |
| `focus-ring-offset` | 2px |

### Components entries

Write every `components` entry listed in the Token contract of each component spec, with only `backgroundColor` and `textColor`. Never add another property (a shadow property included), and never declare a disabled pair. 27 entries in total:

| Spec | Entries | Count |
|---|---|---|
| `components/button.md` | `button-filled` through `button-focus-ring` | 16 |
| `components/chip.md` | `chip-default` through `chip-focus-ring` | 10 |
| `components/tooltip.md` | `tooltip-plain` | 1 |

### Elevation

No question is asked about elevation. The six levels are generated with the default values below. The user may edit them after generation; each level must stay visually higher than the previous one. The values are two layers (a key shadow and an ambient shadow), black at low opacity, inspired by the Material 3 elevation shadows.

| Level | Role | Shadow |
|---|---|---|
| `level-0` | At rest, flat on the surface | `none` |
| `level-1` | At rest, slightly raised | `0 1px 2px rgba(0, 0, 0, 0.30), 0 1px 3px 1px rgba(0, 0, 0, 0.15)` |
| `level-2` | At rest, overlay tied to a trigger | `0 1px 2px rgba(0, 0, 0, 0.30), 0 2px 6px 2px rgba(0, 0, 0, 0.15)` |
| `level-3` | At rest, floating above scrolling content | `0 1px 3px rgba(0, 0, 0, 0.30), 0 4px 8px 3px rgba(0, 0, 0, 0.15)` |
| `level-4` | Interaction only, one step above a resting level | `0 2px 3px rgba(0, 0, 0, 0.30), 0 6px 10px 4px rgba(0, 0, 0, 0.15)` |
| `level-5` | Interaction only, highest | `0 4px 4px rgba(0, 0, 0, 0.30), 0 8px 12px 6px rgba(0, 0, 0, 0.15)` |

Elevation is never a YAML key and never a `components` property (see "Elevation" in `docs/conventions.md`).

### Icons

Write a `## Icons` section stating the icon style and the icon library from the answer to `icons`. Do not create an `icons` key in the YAML.

## Output procedure

1. Identify your level (Step 0), then ask the questions (skip those already answered).
2. Derive everything. Levels 1 and 2: the script applies the rules above; use its output instead of computing by hand. Level 3: copy from `theme/palettes.md`. If a brand or danger color triggers the case in "When a color cannot reach AA" (script exit code `2` at Levels 1 and 2), stop and handle it before writing.
3. Write DESIGN.md at the path given by the task. At Levels 1 and 2, check that the file produced by the script has the sections below and add any that is missing. If none is given, write `DESIGN.md` in the working directory. The YAML front matter holds `name`, `colors`, `typography`, `rounded`, `spacing`, and `components`. Below it, write the sections in this exact order:

| Order | Section | Content |
|---|---|---|
| 1 | Overview | Name, purpose of the theme, the choices made (two to four sentences) |
| 2 | Colors | The three scales, how state colors are derived, the `on-*` rule |
| 3 | Typography | Font choice and the four label sizes |
| 4 | Layout | Density, control heights, spacing scale |
| 5 | Elevation & Depth | One short sentence (the theme defines no shadow token; the scale is this table), then the table `Level` / `Role` / `Shadow` with the six rows of "Elevation" above |
| 6 | Shapes | Corner style and its radius |
| 7 | Components | The contrast entries and a pointer to the component specs |
| 8 | Do's and Don'ts | Short list: use semantic tokens, never raw hex; keep the state rule; do not add non-standard properties to `components` |

The `## Icons` section may sit anywhere; place it right after Shapes.

4. Validate, by level:
   - Level 1: read the script contrast report, then run `npx @google/design.md@0.4.0 lint <path to DESIGN.md>`.
   - Level 2: read the script contrast report. The lint is not available.
   - Level 3: give the user the list of pairs to check with an online contrast checker (see Level 3).
5. Fix every error and every failed pair, then validate again. Repeat until the criterion is met: Level 1, 0 lint errors and 0 `contrast-ratio` warnings; Level 2, script exit code `0`; Level 3, no iteration possible, deliver and state that the check is left to the user. `orphaned-tokens` warnings on unused palette steps are tolerated; any other warning must be fixed. Fixes follow the contrast rule of `docs/conventions.md`. After 5 runs without success, stop and give the user the remaining findings as they are.
6. Reply to the user with a short summary of the choices, as in the template below. Mention any deviation from the defaults and any color you adjusted.
7. Button color different from the entered color: when the `default` step of the brand or danger scale is not the exact entered color, tell the user in plain words, with both hex codes. For example (illustrative values): "Your blue #3B82F6 stays in the palette, but buttons use the darker #2563EB so that white text stays readable." At Levels 1 and 2, the script prints a `Warning:` line for this case; relay it, never drop it. At Level 3, compare the entered hex with the `default` step of the chosen range.

Summary template:

| Choice | Result |
|---|---|
| Name | the name |
| Brand color | base hex, and the step used for buttons |
| Danger color | base hex, and the step used for buttons |
| Grays | the tint |
| Font | the font |
| Corners | the style |
| Density | the density |
| Icons | style and library |
| Chip | neutral outlined chip, brand-tinted when selected |
| Tooltip | dark neutral background, white text, maximum width |
| Elevation | six levels generated by default, editable afterwards |

Add one line on the validation: Level 1, the lint passed (0 errors, 0 contrast warnings); Level 2, the script report passed and the lint was not run; Level 3, the contrast was not verified and the pairs to check are listed.

## When a color cannot reach AA

A brand or danger color is unusable as it stands in any of these cases:

- No step from `600` to `900` of its scale reaches 4.5:1 against the `on-*` color and `surface`.
- For the brand color, no step from `700` to `900` reaches 4.5:1 against every background of `on-primary-container` or `on-primary-subtle`.
- The `default` step is `700` or later: hover and pressed would collapse onto the same step.
- At the `default` step, the chroma is below half of the base chroma: the color has turned muddy and no longer looks like the brand.

Do this:

1. Tell the user, in plain words, that this color cannot give accessible buttons, and why in one sentence. For example: "This yellow is too light: buttons would need a dark olive to be readable."
2. Propose one alternative: the same hue, at lightness 0.54, with the highest chroma that fits the sRGB gamut. Give its hex code.
3. Offer two choices: accept the alternative, or give another color. Wait for the answer.
4. Never force: do not shift the color silently, do not lower the threshold, do not skip the contrast entries.
