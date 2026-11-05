# Conventions

## Language

All content is in English: text, headings, file names, examples.

## DESIGN.md version

The theme follows DESIGN.md as checked by `@google/design.md` pinned to 0.4.0. Upgrade the pin deliberately, never implicitly.

## Token references

- Reference tokens by path, in DESIGN.md format: `{colors.primary}`.
- Never copy a token value into a component file. A value lives in the theme only.
- In code, a token reference becomes a variable of the generated `tokens.css` (for example `{colors.primary}` becomes `--color-primary`). See `docs/implementation.md`.

## State colors

State colors (default, hover, pressed) are semantic tokens that reference steps of a primitive palette scale defined in `colors`, for example `{colors.blue-600}`. A scale runs from the lightest step to the darkest (for example `blue-50` to `blue-900`).

The user gives only the base color. The agent that fills the theme builds the scale and applies this rule for each base color (`primary`, `danger`). It is the solid-family case of the contrast pair rule below.

| State | Rule |
|---|---|
| default | First step from `600` to `900` reaching WCAG AA 4.5:1 against both the content color (`on-*`) and `colors.surface` |
| hover | default plus 2 steps |
| pressed | default plus 4 steps |
| scale end | If a step goes past the end of the scale, stop at the last step |
| distinct states | If hover and pressed land on the same step after the stop, the color is unusable: report it, never merge two states |

Consequence of the scale end: if default is step `700` or later, hover (+2) and pressed (+4) both land on `900` and become identical. The color is then declared unusable, the theme script exits with code 2 and proposes an alternative color, and the theme agent follows "When a color cannot reach AA" in `theme/questionnaire.md`.

Example (illustrative): white on `blue-500` gives 3.68:1, which fails, and `500` is not a solid step anyway. Default is therefore `blue-600`, hover `blue-800`, and pressed `blue-900` (capped at the last step).

## Contrast pairs

This rule applies to every pair declared in `components` by every component, present and future (button, chip, tooltip, and others). A pair is one `backgroundColor` and one `textColor`. A component without fill uses `{colors.surface}` as the background of its pair. Borders and fills that carry no text or icon are not pairs.

### Background families

Steps are those of a 10-step scale, `50` (lightest) to `900` (darkest). The families apply to every scale, the neutral scale included. `{colors.surface}` is a light background.

| Family | Background steps | Allowed content |
|---|---|---|
| `light` | `50`, `100`, `200` | Step `700`, `800`, or `900` of the same scale |
| `light`, surface only | `{colors.surface}` | Same as `light`, or an accent token whose step comes from the State colors rule (`primary`, `danger`, `focus-ring`) |
| `intermediate` | `300`, `400`, `500` | none: never a background behind text or icons |
| `solid` | `600` to `900` | An `on-*` token: white by default; a theme may choose step `50` of the same scale instead |

### State changes

The background moves first, the content follows.

1. Background. Each interactive state of a variant (`enabled`, `hover`, `pressed`) has its own background, distinct from the other states, each state darker than the previous one, and staying in its family.

| Case | enabled | hover | pressed |
|---|---|---|---|
| `light`, enabled with fill | step `50` | step `100` | step `200` |
| `light`, enabled without fill | `{colors.surface}` | step `50` | step `100` |
| `light`, enabled without fill, scale of `{colors.surface}` (neutral) | `{colors.surface}` | step `100` | step `200` |
| `solid` | State colors rule | State colors rule | State colors rule |

A variant with fewer states uses the first columns of its row.

Surface scale: `{colors.surface}` is step `50` of the neutral scale. When the variant without fill takes its hover and pressed backgrounds from the scale of `{colors.surface}`, step `50` would equal the enabled background, so the sequence shifts by one step: surface, `100`, `200`. It stays in the `light` family, and the three backgrounds are distinct and each darker than the previous one.

2. Content. The content color is then computed for the new backgrounds, with the search below. It may change from one state to the next; the background never does the adjusting.

3. Forbidden: two states of a variant with the same background color; lightening a background or moving it back to an earlier step to pass contrast; lowering the 4.5:1 threshold; content on an `intermediate` background.

### Content step search

For each content token on a `light` background:

1. Collect every `components` entry that uses the token as `textColor`. Their `backgroundColor` values form the background set of the token.
2. Test steps `700`, `800`, then `900` of the background scale, in this order.
3. Keep the first step reaching 4.5:1 against every background of the set. The darkest background of the set therefore decides.
4. Scale end: if `900` fails, there is no further step. Do not wrap, do not pick a lighter step, do not change a background. The pair fails and is reported (the theme agent follows "When a color cannot reach AA" in `theme/questionnaire.md`).

For a content token on a `solid` background (`on-*`): white is used. Solid backgrounds only darken from state to state, so white passing on `enabled` passes on later states; every pair is still checked. If the theme chooses step `50` instead, it is checked the same way.

A component spec decides whether a state has its own content token or shares one with other states. Prefer sharing: the search above makes a shared token valid for all its backgrounds, and the token count stays low.

Example (illustrative): `blue-600` text on a `blue-100` pressed background gives 4.19:1. The pair is forbidden anyway, because `600` is not a content step for a `light` background. The content token of that state takes `blue-700` if it reaches 4.5:1 against every background it serves, otherwise `blue-800`, then `blue-900`. The pressed background stays `blue-100`.

### Dark background with light content

A component with a dark background and light content (for example a tooltip) uses a `solid` step of a scale, usually the neutral scale, as its background, and an `on-*` content token: white by default, or step `50` of the same scale. The component token contract declares the background step, within `600` to `900`. The pair is checked like any other. Dark-background components with interactive states are not covered yet: a spec that needs them must extend this rule first.

### Automatic check

- Every `components` entry is checked against 4.5:1 by the theme script and by the DESIGN.md lint. A new component is covered as soon as it declares its pairs as `components` entries; no other list needs updating.
- Entry names: `<component>-<variant>` for `enabled`, `<component>-<variant>-<state>` for `hover` and `pressed`. The script groups entries by removing the `-hover` or `-pressed` suffix, and checks that the backgrounds of a group resolve to distinct colors. The lint does not check this; the script does.
- The script also checks the families: no pair has an `intermediate` background, and every content step is allowed for the family of its background.
- An entry that is not a variant state (for example `button-focus-ring`) is only checked for contrast.
- Disabled-state pairs stay excluded (see below).

### Known limit

Contrast is checked only against `{colors.surface}`; on an image or a dark background (for example under a floating button), the user retouches the theme after generation.

## Lint and contrast

- The DESIGN.md contrast rule (`contrast-ratio`) checks only the entries of the `components` key.
- The kit never adds non-standard properties to `components`. It only declares standard `backgroundColor` and `textColor` entries, one per variant and active state, so the DESIGN.md lint checks contrast.
- Disabled-state pairs are never declared in `components`, because WCAG 1.4.3 exempts inactive components and the lint would otherwise flag them. The disabled token mapping stays described in the component spec, and the `on-disabled` and `disabled-container` tokens stay in the colors token contract.
- Theme validation criterion: 0 errors and 0 `contrast-ratio` warnings. `orphaned-tokens` warnings on unused primitive palette steps are expected and tolerated; no other warning is.

## Elevation

Elevation (shadow) is not a token, like the icon style. The scale lives in the `## Elevation & Depth` Markdown section of DESIGN.md, as a table. Component specs designate a level by its name; they never hold a shadow value.

### Levels

The scale follows the Material 3 model: six levels, named after their relative distance above the surface. The level names are stable: they never change from one theme to another, and a theme never adds, removes, or renames a level.

| Level | Role | Typical use |
|---|---|---|
| `level-0` | At rest, in the page flow, flat on the surface, no shadow | Every component that declares no level |
| `level-1` | At rest, slightly raised, still in the page flow | Raised containers (no kit component yet) |
| `level-2` | At rest, overlay tied to a trigger, shown for a short time | Tooltip; later menu, popover |
| `level-3` | At rest, floating above the content while it scrolls | Floating button |
| `level-4` | Interaction only, one step above a resting level | Hover of the floating button |
| `level-5` | Interaction only, highest | Dragged element (no kit component yet) |

- Resting state: a component at rest (no user interaction, for example `enabled`, `open`, `disabled`, `loading`) uses `level-0` to `level-3`.
- Interaction states: `level-4` and `level-5` are reserved for user interaction states, such as hover and drag. A spec states which state uses which level; a state may also keep its resting level.
- Each level reads as higher than the previous one. Only `level-0` has no shadow.
- A level is a visual depth cue, not a stacking order. Which element is drawn on top (for example a tooltip over a floating button) belongs to the page layout.
- Elevation never carries state feedback alone. Hover and pressed keep their color tokens, so a component stays fully usable without its shadow.
- Future rule (dark mode is out of scope): in dark mode there is no shadow; depth is carried another way, for example by the surface tint.

### Table in `## Elevation & Depth`

The section may open with one short sentence, followed by exactly this table. The theme script generates this table automatically with default values for the six levels; the user may retouch the values afterwards. The script then writes one shadow variable per level in `tokens.css` (`--elevation-level-0` to `--elevation-level-5`, see `docs/implementation.md`); this table is the only source of shadow values.

| Column | Content |
|---|---|
| `Level` | The level name in backticks: `level-0` to `level-5` |
| `Role` | The role of the level, short text |
| `Shadow` | One complete CSS `box-shadow` value in backticks, or `none` |

- One row per level, all six rows, in the order `level-0`, `level-1`, `level-2`, `level-3`, `level-4`, `level-5`. No other row.
- The `level-0` row is always `none`.
- One cell holds one complete value: no token reference, no partial value, no "same as above".
- A retouched value still follows the rules above: each level reads as higher than the previous one.
- The default values are given by `theme/questionnaire.md`, never by this file or by a component spec. No question is asked about shadows.

### Forbidden

- An `elevation`, `shadow`, or similar key in the YAML front matter. The CLI tolerates a custom key but ignores it in every export.
- A reference such as `{elevation.level-2}`, in the theme or in a spec. The lint reports it as a broken reference.
- Any shadow property in a `components` entry. The lint warns, which breaks the validation criterion; `components` entries stay `backgroundColor` and `textColor` only.

### Reference from a spec

- A spec designates a level by its name in backticks, for example `level-2`. Never a shadow value, never a token reference.
- In Token mapping, elevation has its own short table, one row per state, when the level changes with the state; otherwise one line stating the level.
- In Token contract, elevation is listed under "Non-token requirement", next to the icon style. It is not counted in the token totals.
- A spec that declares no level is at `level-0` in every state.

## CLI facts (`@google/design.md` 0.4.0)

- Free token names are accepted in `spacing` and `rounded` (for example `control-xs`, `icon-sm`, `border-width`, `rounded.control`).
- The `css-vars` export exists, with an optional `--prefix`, but it does not export `typography`. The kit does not use it: the theme script generates `tokens.css`, with every group (colors, spacing, rounded, typography, elevation) under fixed variable names. The name contract and its use by component code are in `docs/implementation.md`.
- Icon style is not a token. It lives in a free `## Icons` Markdown section of DESIGN.md (position free, accepted without warning), stating the style and the icon library. A top-level `icons` YAML key is rejected because exports ignore it.
- There is no shadow or elevation token type and no YAML key for it. The DESIGN.md spec defines `Elevation & Depth` as a prose section describing the required styling (spread, blur, color). A custom `elevation` key is tolerated but ignored by exports; a `{elevation.*}` reference is a broken-ref error; any shadow property in `components` triggers a warning. The kit therefore keeps the scale as a table in `## Elevation & Depth`, and the theme script writes the shadow variables in `tokens.css` (see Elevation).

## Sizes

Each component declares its own sizes. There is no shared scale imposed on all components.

## Naming

Use kebab-case for file names, token names, variants, states, and parts. Example: `leading-icon`.

## Component spec format

The reference spec is `components/button.md`. Every component spec uses the sections below, in this order. A section that does not apply is kept with one line saying why.

| Order | Section | Content | Form |
|---|---|---|---|
| 1 | Title and intro | Component name, one sentence on what it does | Prose |
| 2 | At a glance | Summary of parts, configurations, variants, sizes, states, token count | Table: aspect, summary |
| 3 | Purpose | When to use it, when not to | Short list |
| 4 | Anatomy | Parts, then allowed and forbidden configurations, then combination rules | Tables: part, role, required, notes; configuration by part, allowed |
| 5 | Properties | Every input of the component | Table: property, values, default, description |
| 6 | Variants | Each variant and its intent | Table |
| 7 | Sizes | Decision on how sizes are expressed, then one row per size, then geometry rules | Table: size, then one column per dimension |
| 8 | States | Interactive states, then state properties (such as `disabled`, `loading`), then precedence | Two tables, one precedence line |
| 9 | Token mapping | One table per variant: rows are states, columns are parts or properties; elevation by level name (see Elevation) | Short tables, at most five columns |
| 10 | Token contract | Every token the theme must define, grouped by DESIGN.md group | One table per group: token, role |
| 11 | Accessibility | Role, accessible name, focus, keyboard, target size, contrast | Table: topic, requirement |
| 12 | Behavior | Runtime behavior not covered by states | Short list |
| 13 | Do and don't | Usage guidance | Table: do, don't |
| 14 | Out of scope | What the spec deliberately ignores | One line |
| 15 | Rationale | Main decisions and their reasons | Table: decision, reason |

Table rules, so that a machine-readable block can be derived without ambiguity:

- The first column is the key of the row. Keys use kebab-case and the exact names declared in the spec.
- A cell holds one value: a token reference such as `{colors.primary}`, a name in backticks, `none`, `yes`, `no`, or short text.
- `none` means no fill, no border, or no value. Never leave a cell empty, never write "same as above".
- No values copied from the theme. No code blocks in a spec.
- Keep tables narrow: split a wide table into several short ones rather than adding columns.
