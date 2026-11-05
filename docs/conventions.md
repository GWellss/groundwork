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

The user gives only the base color. The agent that fills the theme builds the scale and applies this rule for each base color (`primary`, `danger`):

| State | Rule |
|---|---|
| default | First step of the scale reaching WCAG AA 4.5:1 with the content color (`on-*`) |
| hover | default plus 2 steps |
| pressed | default plus 4 steps |
| scale end | If a step goes past the end of the scale, stop at the last step |

Example (illustrative): white on `blue-500` gives 3.68:1, which fails. Default is therefore `blue-600`, hover `blue-800`, and pressed `blue-900` (capped at the last step).

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
