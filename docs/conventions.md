# Conventions

## Language

All content is in English: text, headings, file names, examples.

## DESIGN.md version

The theme follows DESIGN.md as checked by `@google/design.md` pinned to 0.4.0. Upgrade the pin deliberately, never implicitly.

## Token references

- Reference tokens by path, in DESIGN.md format: `{colors.primary}`.
- Never copy a token value into a component file. A value lives in the theme only.

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
| `solid` | State colors rule | State colors rule | State colors rule |

A variant with fewer states uses the first columns of its row.

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

## Lint and contrast

- The DESIGN.md contrast rule (`contrast-ratio`) checks only the entries of the `components` key.
- The kit never adds non-standard properties to `components`. It only declares standard `backgroundColor` and `textColor` entries, one per variant and active state, so the DESIGN.md lint checks contrast.
- Disabled-state pairs are never declared in `components`, because WCAG 1.4.3 exempts inactive components and the lint would otherwise flag them. The disabled token mapping stays described in the component spec, and the `on-disabled` and `disabled-container` tokens stay in the colors token contract.
- Theme validation criterion: 0 errors and 0 `contrast-ratio` warnings. `orphaned-tokens` warnings on unused primitive palette steps are expected and tolerated; no other warning is.

## CLI facts (`@google/design.md` 0.4.0)

- Free token names are accepted in `spacing` and `rounded` (for example `control-xs`, `icon-sm`, `border-width`, `rounded.control`).
- The `css-vars` export exists, with an optional `--prefix`, but it does not export `typography`. The kit generates the typography variables itself.
- Icon style is not a token. It lives in a free `## Icons` Markdown section of DESIGN.md (position free, accepted without warning), stating the style and the icon library. A top-level `icons` YAML key is rejected because exports ignore it.

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
| 9 | Token mapping | One table per variant: rows are states, columns are parts or properties | Short tables, at most five columns |
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
