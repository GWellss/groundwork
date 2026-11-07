# Theme questionnaire

This file is for an AI agent. Follow it to produce a valid DESIGN.md theme from the fewest possible answers from the user. Token names come from the Token contract of every component spec in `components/` (24 specs: `button.md`, `chip.md`, `tooltip.md`, `divider.md`, `link.md`, `badge.md`, `avatar.md`, `progress.md`, `text-field.md`, `search-field.md`, `checkbox.md`, `radio.md`, `switch.md`, `slider.md`, `segmented-control.md`, `tabs.md`, `accordion.md`, `menu.md`, `select.md`, `popover.md`, `dialog.md`, `alert.md`, `toast.md`, `card.md`); conventions come from `docs/conventions.md`. Both take precedence over this file if they differ. The contrast rule is defined once, in the "State colors" and "Contrast pairs" sections of `docs/conventions.md`; this file applies it and does not restate it.

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
- You do: ask the questions. Replace the `brand`, `danger`, `success` and `warning` questions with "Choose the range closest to your brand color" among the 14 ranges of `theme/palettes.md`. If the user gives a hex code, propose the closest range and say that the match is approximate. For the `neutral` question, map the answer to a range of `theme/palettes.md`: neutral → `gray`, warm → `warm-gray`, cool → `cool-gray`. Do not offer the "tinted with the brand color" option at this level, because no precomputed range exists for it: propose only the other three, and if the user wants a tinted gray, say that it requires Level 1 or Level 2. Take density, corners, and typography from the default tables below. Copy the precomputed steps (`default`, `hover`, `pressed`, and the other steps of the range) into the DESIGN.md. For the neutral-derived colors, use the range chosen for `neutral` (`gray`, `warm-gray`, or `cool-gray`): `on-surface` is the `on-container` row of that range (step `700`, searched against steps `50`, `100`, `200`, which are `surface`, `neutral-subtle-hover`, and `neutral-subtle-pressed`); `neutral-subtle-hover` is step `100`, `neutral-subtle-pressed` is step `200`, `inverse-surface` is step `900`, and `on-inverse-surface` is white. Name the copied scale `neutral` in the DESIGN.md. If a value needed here is missing from `theme/palettes.md`, say so to the user instead of computing it.
- Elevation: copy the default table of "Elevation" below; it needs no computation.
- `tokens.css`: no script writes it at this level. If code is to be generated, write it by copying the values of the DESIGN.md under the variable names of `docs/implementation.md`, semantic colors resolved to the hex of their step, and the font family followed by the fallback stack of "Typography" below. Copy only; never compute.
- You delegate: the final check, to the user, with an online contrast checker such as WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/). List the key pairs to check, each with its two hex values: every `components` entry that pairs a background with a text color (including the `chip-*`, `link-*`, `badge-*`, `avatar-default`, `progress-*`, `text-field*`, `search-field-clear*`, `checkbox*`, `radio-selected*`, `switch-on*`, `slider*`, `tab*`, `accordion*`, `menu-*`, `popover`, `dialog`, `alert-*`, `toast*`, `card*` entries and `tooltip-plain`), and at least the `primary` on `surface` pair. Neutral-derived values (`on-surface`, `on-surface-muted`, `neutral-subtle-hover`, `neutral-subtle-pressed`, `inverse-surface`) come from the range chosen for `neutral`, as described in "Semantic color tokens".
- Done when: the DESIGN.md is delivered, the list of pairs to check is given, and you have said that the contrast was copied from precomputed values and not verified in this conversation.

## Principle

- Ask one question at a time, in the order of the list below.
- Every question comes with a default value. Show it, and let the user accept it with a single word ("ok", "default").
- Skip a question when the user already answered it, or when the answer can be deduced (for example a brand color given in the first message).
- If the user says "use defaults for the rest", stop asking and apply the remaining defaults.
- Never ask about anything that the derivation rules below settle. Ask 10 questions at most.
- Do not mention token names to the user. Speak in design terms (color, corners, density).

## Questions

| Id | Question to ask |
|---|---|
| `name` | What is the name of your design system? (default: the product name if known, otherwise "Design System") |
| `brand` | What is your main brand color? Give a hex code or a color name. (default: `#2563EB`, a blue) |
| `danger` | Which color should signal destructive actions such as delete? (default: `#DC2626`, a red) |
| `success` | Which color should signal success, such as a completed or paid status? (default: `#15803D`, a green) |
| `warning` | Which color should signal a warning, such as a status that needs attention soon? (default: `#B45309`, an amber-orange) |
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
| `success` | `#15803D` | success scale; `success`, `on-success` |
| `warning` | `#B45309` | warning scale; `warning`, `on-warning` |
| `neutral` | neutral | neutral scale; `surface`, `on-surface`, `neutral-subtle-hover`, `neutral-subtle-pressed`, `inverse-surface`, `outline`, `on-surface-muted`, `disabled-container`, `on-disabled` |
| `font` | system UI font | `fontFamily` of the typography tokens |
| `corners` | soft | `rounded.control`, `rounded.overlay` (`rounded.avatar` is constant, see "Rounded") |
| `density` | default | `spacing` sizes (control, icon, gaps, paddings, `tooltip-max-width`, `dialog-max-width`), `fontSize` of the typography tokens |
| `icons` | outlined, Material Symbols | `## Icons` section (no token) |

## Derivation rules

Everything below is deduced. Do not ask the user about it.

### Palette scales

Build five primitive scales in `colors`: one for `brand`, one for each of `danger`, `success` and `warning`, one for the neutral tint. Each has 10 steps named `<name>-50`, `-100`, `-200`, `-300`, `-400`, `-500`, `-600`, `-700`, `-800`, `-900`, from lightest to darkest.

- Name a scale after the common English color name of its hue (blue, red, green, orange). If the brand color shares its name with the danger, success or warning color, call the brand scale `brand`. Danger, success and warning must have different names: otherwise ask for another color. Call the neutral scale `neutral`.
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
- `on-surface`: content of the `default` chip, of the chip remove button, of the avatar, and of the neutral badge, on the backgrounds `surface`, `neutral-subtle-hover`, and `neutral-subtle-pressed` (neutral steps `50`, `100`, `200`: the "Surface scale" sequence of `docs/conventions.md`).

For each of them, apply the content step search of `docs/conventions.md`: test steps `700`, `800`, then `900` of the scale of its backgrounds (brand scale for the first two, neutral scale for `on-surface`), and keep the first one that reaches 4.5:1 against every background it serves. Never change a background to make a content color pass. If no step passes for `on-surface`, report the pair to the user instead of forcing it.

`on-danger-container`, `on-success-container` and `on-warning-container` follow the same search as `on-primary-container`, on the scale of their own role: steps `700`, `800`, then `900` of the scale, first one reaching 4.5:1 on the steps `50`, `100` and `200` of that scale (the three tonal fills of the alert). At Level 3, copy the `on-container` row of the chosen range.

Two more colors come from the neutral scale and follow their own rule:

- `on-surface-muted`: placeholder, helper text, counter, affixes, and icons of the text field, and the helper text of the choice controls and the slider, on `surface` only, never on a grayed fill (`neutral-100` and beyond). It is the first step of `600`, then `700`, reaching 4.5:1 against `surface`, and it must differ from `on-surface` (if `600` fails and `700` equals `on-surface`, report it to the user; the script stops with an explicit error).
- `outline`: the field border (and the chip border, the unselected border and off thumb of the checkbox, radio button, and switch, the slider track, and the border and dividers of the segmented control and the accordion). It is the first step of `500`, then `600`, reaching 3:1 (not 4.5:1: WCAG 1.4.11, non-text) against `surface`. The DESIGN.md lint cannot check this pair; the script does (`outline` row of its report). At Level 3, compute it by hand and list it among the pairs to check.

### State colors

Apply the State colors rule of `docs/conventions.md` to the brand, danger, success and warning scales separately: `default` is searched from `600` to `900` against the `on-*` color and against `surface`; `hover` is `default` plus 2 steps; `pressed` is `default` plus 4 steps, stopping at `900`. Compute contrast with the WCAG 2.x relative luminance formula.

### Semantic color tokens

Write the colors of the token contracts of the button, the chip (new colors), and the tooltip (new colors) as references (divider, avatar, progress, and search field add no color; the badge adds the `success` and `warning` colors; the alert adds the tonal containers of `danger`, `success` and `warning`; the link adds only `link-visited`; the text field adds only `on-surface-muted`; the checkbox, radio, switch, slider, segmented control, tabs, accordion, menu, select, popover, dialog, toast, and card add no color) to scale steps. `<brand>`, `<danger>`, `<success>` and `<warning>` are the scale names; `d` is the `default` step of the corresponding scale; `c` is the step found by the content step search above; `n` is the step found by the same search on the neutral scale for `on-surface`.

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
| `success` | `{colors.<success>-d}` |
| `on-success` | `#FFFFFF` |
| `warning` | `{colors.<warning>-d}` |
| `on-warning` | `#FFFFFF` |
| `outline` | `{colors.neutral-500}`, or `{colors.neutral-600}` if `500` is below 3:1 on `surface` |
| `on-surface-muted` | `{colors.neutral-m}`: step `600`, or `700` if `600` is below 4.5:1 on `surface` |
| `disabled-container` | `{colors.neutral-100}` |
| `on-disabled` | `{colors.neutral-500}` |
| `focus-ring` | same step as `primary` |
| `on-surface` | `{colors.neutral-n}`, searched against `surface`, `neutral-100`, `neutral-200` |
| `neutral-subtle-hover` | `{colors.neutral-100}` |
| `neutral-subtle-pressed` | `{colors.neutral-200}` |
| `inverse-surface` | `{colors.neutral-900}` |
| `on-inverse-surface` | `#FFFFFF` |
| `danger-container` | `{colors.<danger>-50}` |
| `danger-container-hover` | `{colors.<danger>-100}` |
| `danger-container-pressed` | `{colors.<danger>-200}` |
| `on-danger-container` | `{colors.<danger>-c}`, searched against `50`, `100`, `200` |
| `success-container` | `{colors.<success>-50}` |
| `success-container-hover` | `{colors.<success>-100}` |
| `success-container-pressed` | `{colors.<success>-200}` |
| `on-success-container` | `{colors.<success>-c}`, searched against `50`, `100`, `200` |
| `warning-container` | `{colors.<warning>-50}` |
| `warning-container-hover` | `{colors.<warning>-100}` |
| `warning-container-pressed` | `{colors.<warning>-200}` |
| `on-warning-container` | `{colors.<warning>-c}`, searched against `50`, `100`, `200` |
| `link-visited` | `{colors.<brand>-v}`, where `v` is the step right after `d` (`default` is always `600`, so `700`): a step of the same scale as `primary`, distinct from `default`, `hover` (`800`) and `pressed` (`900`), reaching 4.5:1 on `surface` |

If a pair fails, never make two states identical, never move a background back to an earlier step, and never lower the 4.5:1 threshold (see "Contrast pairs" in `docs/conventions.md`). Only the content step can change, within its search. If no step passes, report the pair to the user instead of forcing it, following "When a color cannot reach AA".

### Typography

Write the tokens `label-sm`, `label-md`, `label-lg`, `label-xl`. Each carries `fontFamily` (the answer to `font`; for the system UI font, use `system-ui`), `fontSize`, `fontWeight` 500, `lineHeight`, and `letterSpacing` 0px. Line height is 1.25 times the font size, rounded to the nearest whole pixel and written in px. Font size follows density.

Fallback stack: in `tokens.css`, the font family is followed by generic fallbacks, `system-ui` then `sans-serif` (a generic family is not repeated). DESIGN.md keeps the entered font alone. The kit does not load fonts: if the chosen font is not installed on the target devices, tell the user that the project must load it, otherwise the fallback is shown.

| Density | label-sm | label-md | label-lg | label-xl |
|---|---|---|---|---|
| compact | 12px | 13px | 14px | 16px |
| default | 12px | 14px | 16px | 18px |
| comfortable | 13px | 15px | 17px | 20px |

### Rounded

Write `rounded.control`, `rounded.overlay`, and `rounded.avatar`. The overlay radius is moderate in every corner style, so that a multi-line overlay (the tooltip, the menu, the select list, the popover, the dialog, the alert, the toast, the card) never turns into a stadium shape. `rounded.avatar` is `9999px` (a circle) in every corner style and is not asked: the user edits it after generation to change the avatar shape.

| Answer to `corners` | `rounded.control` | `rounded.overlay` |
|---|---|---|
| sharp | 0px | 0px |
| soft | 4px | 4px |
| rounded | 8px | 8px |
| pill | 9999px | 8px |

### Spacing

The spacing tokens come from the density table and the constant table. Values are in px: this file is the defaults file of the theme, not a component spec. The three constant tokens do not depend on density.

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
| `menu-min-width` | 128px | 160px | 192px |
| `floating-max-width` | 280px | 320px | 360px |
| `dialog-max-width` | 400px | 480px | 560px |

| Constant token | Value |
|---|---|
| `border-width` | 1px |
| `focus-ring-width` | 2px |
| `focus-ring-offset` | 2px |

### Components entries

Write every `components` entry listed in the Token contract of each component spec, with only `backgroundColor` and `textColor`. Never add another property (a shadow property included), and never declare a disabled pair. Entries by spec:

| Spec | Entries |
|---|---|
| `components/button.md` | `button-filled` through `button-focus-ring` |
| `components/chip.md` | `chip-default` through `chip-focus-ring` |
| `components/tooltip.md` | `tooltip-plain` |
| `components/divider.md` | none |
| `components/link.md` | `link` through `link-focus-ring` |
| `components/badge.md` | `badge-primary`, `badge-danger`, `badge-success`, `badge-warning`, `badge-neutral` |
| `components/avatar.md` | `avatar-default` |
| `components/progress.md` | `progress-primary`, `progress-danger` |
| `components/text-field.md` | `text-field`, `text-field-muted`, `text-field-error`, `text-field-read-only`, `text-field-focus-ring` |
| `components/search-field.md` | `search-field-clear`, `search-field-clear-hover`, `search-field-clear-pressed` |
| `components/checkbox.md` | `checkbox`, `checkbox-muted`, `checkbox-error`, `checkbox-focus-ring`, `checkbox-selected`, `checkbox-selected-hover`, `checkbox-selected-pressed` (the first four also serve radio, switch, and slider) |
| `components/radio.md` | `radio-selected`, `radio-selected-hover`, `radio-selected-pressed` |
| `components/switch.md` | `switch-on`, `switch-on-hover`, `switch-on-pressed` |
| `components/slider.md` | `slider`, `slider-hover`, `slider-pressed` |
| `components/segmented-control.md` | none (reuses the `chip-default*`, `chip-selected*`, and `chip-focus-ring` entries) |
| `components/tabs.md` | `tab`, `tab-hover`, `tab-pressed`, `tab-selected`, `tab-selected-hover`, `tab-selected-pressed`, `tab-focus-ring` |
| `components/accordion.md` | `accordion`, `accordion-hover`, `accordion-pressed`, `accordion-focus-ring` |
| `components/menu.md` | `menu-item`, `menu-item-hover`, `menu-item-pressed`, `menu-item-danger`, `menu-item-danger-hover`, `menu-item-danger-pressed`, `menu-muted`, `menu-focus-ring` |
| `components/select.md` | none (reuses `text-field*` and `menu-item*`) |
| `components/popover.md` | `popover` |
| `components/dialog.md` | `dialog` |
| `components/alert.md` | `alert-success`, `alert-success-hover`, `alert-success-pressed`, `alert-warning`, `alert-warning-hover`, `alert-warning-pressed`, `alert-danger`, `alert-danger-hover`, `alert-danger-pressed` (the information severity reuses `button-tonal*`) |
| `components/toast.md` | `toast`, `toast-success`, `toast-danger` |
| `components/card.md` | `card`, `card-hover`, `card-pressed`, `card-focus-ring` |

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
2. Derive everything. Levels 1 and 2: the script applies the rules above; use its output instead of computing by hand. Level 3: copy from `theme/palettes.md`. If a brand, danger, success or warning color triggers the case in "When a color cannot reach AA" (script exit code `2` at Levels 1 and 2), stop and handle it before writing.
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
7. Button color different from the entered color: when the `default` step of the brand, danger, success or warning scale is not the exact entered color, tell the user in plain words, with both hex codes. For example (illustrative values): "Your blue #3B82F6 stays in the palette, but buttons use the darker #2563EB so that white text stays readable." At Levels 1 and 2, the script prints a `Warning:` line for this case; relay it, never drop it. At Level 3, compare the entered hex with the `default` step of the chosen range.

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
| Menu, select list, popover | surface fill, quiet border, level-2 shadow; two widths |
| Dialog, toast | same surface and border, level-3 shadow; the dialog has a veil and two widths |
| Alert | tonal fill (50-200) with dark content, by severity; information uses the brand tonal fill |
| Card | outlined or elevated, on the surface; clickable cards gray on hover |
| Elevation | six levels generated by default, editable afterwards |

Add one line on the validation: Level 1, the lint passed (0 errors, 0 contrast warnings); Level 2, the script report passed and the lint was not run; Level 3, the contrast was not verified and the pairs to check are listed.

## When a color cannot reach AA

A brand, danger, success or warning color is unusable as it stands in any of these cases:

- No step from `600` to `900` of its scale reaches 4.5:1 against the `on-*` color and `surface`.
- For the brand color, no step from `700` to `900` reaches 4.5:1 against every background of `on-primary-container` or `on-primary-subtle`.
- For the brand and danger colors (the only ones with solid hover and pressed), the `default` step is `700` or later: hover and pressed would collapse onto the same step.
- At the `default` step, the chroma is below half of the base chroma: the color has turned muddy and no longer looks like the brand.

Do this:

1. Tell the user, in plain words, that this color cannot give accessible buttons, and why in one sentence. For example: "This yellow is too light: buttons would need a dark olive to be readable."
2. Propose one alternative: the same hue, at lightness 0.54, with the highest chroma that fits the sRGB gamut. Give its hex code.
3. Offer two choices: accept the alternative, or give another color. Wait for the answer.
4. Never force: do not shift the color silently, do not lower the threshold, do not skip the contrast entries.
