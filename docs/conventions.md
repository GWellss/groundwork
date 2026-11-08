# Conventions

## Language

All content is in English: text, headings, file names, examples.

## DESIGN.md version

The theme follows DESIGN.md as checked by `@google/design.md` pinned to 0.4.0. Upgrade the pin deliberately, never implicitly.

## Token references

- Reference tokens by path, in DESIGN.md format: `{colors.primary}`.
- Never copy a token value into a component file. A value lives in the theme only.
- In code, a token reference becomes a variable of the generated `tokens.css` (for example `{colors.primary}` becomes `--color-primary`). See `docs/implementation.md`.
- Free token names are accepted in `spacing` and `rounded` (for example `control-xs`, `icon-sm`, `border-width`, `rounded.control`).
- The `css-vars` export of `@google/design.md` 0.4.0 exists, with an optional `--prefix`, but it does not export `typography`. The kit does not use it: the theme script generates `tokens.css`, with every group (colors, spacing, rounded, typography, elevation) under fixed variable names.
- Icon style is not a token. It lives in a free `## Icons` Markdown section of DESIGN.md (position free, accepted without warning), stating the style and the icon library. A top-level `icons` YAML key is rejected because exports ignore it.

## State colors

State colors (default, hover, pressed) are semantic tokens that reference steps of a primitive palette scale defined in `colors`, for example `{colors.blue-600}`. A scale runs from the lightest step to the darkest (for example `blue-50` to `blue-900`).

The user gives only the base color. The agent that fills the theme builds the scale and applies this rule for each base color (`primary`, `danger`, `success`, `warning`). It is the solid-family case of the contrast pair rule below.

This section and the next ones describe the light mode, which is the reference. The dark mode has its own derivation and its own direction of state changes (see Dark mode).

| State | Rule |
|---|---|
| default | First step from `600` to `900` reaching WCAG AA 4.5:1 against both the content color (`on-*`) and `colors.surface` |
| hover | default plus 2 steps |
| pressed | default plus 4 steps |
| scale end | If a step goes past the end of the scale, stop at the last step |
| distinct states | For brand and danger (success and warning have no solid hover or pressed): if hover and pressed land on the same step after the stop, the color is unusable: report it, never merge two states |

Consequence of the scale end: for brand and danger, if default is step `700` or later, hover (+2) and pressed (+4) both land on `900` and become identical. The color is then declared unusable, the theme script exits with code 2 and proposes an alternative color, and the theme agent follows "When a color cannot reach AA" in `theme/questionnaire.md`.

Example (illustrative): white on `blue-500` gives 3.68:1, which fails, and `500` is not a solid step anyway. Default is therefore `blue-600`, hover `blue-800`, and pressed `blue-900` (capped at the last step).

## Contrast pairs

This rule applies to every pair declared in `components` by every component, present and future (button, chip, tooltip, and others). A pair is one `backgroundColor` and one `textColor`. A component without fill uses `{colors.surface}` as the background of its pair. Borders and fills that carry no text or icon are not pairs.

### Background families

Steps are those of a 10-step scale, `50` (lightest) to `900` (darkest). The families apply to every scale, the neutral scale included. `{colors.surface}` is a light background.

This classification is that of the light mode. A background is light or dark according to the mode, never by its step number alone: in dark mode `{colors.surface}` is a dark background and the families are set again (see Dark mode).

| Family | Background steps | Allowed content |
|---|---|---|
| `light` | `50`, `100`, `200` | Step `700`, `800`, or `900` of the same scale |
| `light`, surface only | `{colors.surface}` | Same as `light`, or an accent token whose step comes from the State colors rule (`primary`, `primary-hover`, `primary-pressed`, `danger`, `success`, `focus-ring`), `link-visited`, the brand step right after `primary`, or `on-surface-muted`, neutral step `600` (or `700`), the quieter text of the text field |
| `intermediate` | `300`, `400`, `500` | none: never a background behind text or icons |
| `solid` | `600` to `900` | An `on-*` token: white by default; a theme may choose step `50` of the same scale instead |

One extension covers the destructive menu item (see `components/menu.md`): `danger-hover` is allowed on `neutral-subtle-hover`, and `danger-pressed` on `neutral-subtle-pressed`, and no other accent content is allowed on a grayed fill. They are the darker steps of the State colors rule, chosen because `danger` itself reaches 4.5:1 on `{colors.surface}` only. The script checks the pairing and the 4.5:1 ratio.

Tonal containers exist for every status role, not only for the brand: `primary-container`, `danger-container`, `success-container` and `warning-container` are steps `50`, `100` and `200` of their scale (enabled, hover, pressed), with a content token (`on-primary-container`, `on-danger-container`, and so on) found by the content step search below. This is the plain `light` family rule, with no exception: the content is step `700` to `900` of the same scale as its background. The `success` accent on the surface is the only addition to the accent list above; it serves the status icon of the toast (see `components/toast.md`).

Every focus ring is `focus-ring`, with no exception. The script checks it at 3:1 (WCAG 1.4.11) on every fill it can meet: the surface, the neutral hover and pressed fills, and the container, hover and pressed fills of the brand, danger, success and warning tonal containers (the controls of the alert). If the brand step fails on one of them, the script takes a darker brand step: the adjustment is global, never a color per component.

### State changes

The background moves first, the content follows.

1. Background. Each interactive state of a variant (`enabled`, `hover`, `pressed`) has its own background, distinct from the other states, each state darker than the previous one (light mode; in dark mode each state is lighter, see Dark mode), and staying in its family.

| Case | enabled | hover | pressed |
|---|---|---|---|
| `light`, enabled with fill | step `50` | step `100` | step `200` |
| `light`, enabled without fill | `{colors.surface}` | step `50` | step `100` |
| `light`, enabled without fill, scale of `{colors.surface}` (neutral) | `{colors.surface}` | step `100` | step `200` |
| `solid` | State colors rule | State colors rule | State colors rule |

A variant with fewer states uses the first columns of its row.

Fill-less exception: a component with no fill at all (the link, the text field, the slider) keeps `{colors.surface}` as the background of every state. Its content color moves instead, each state darker than the previous one (State colors rule: `primary`, `primary-hover`, `primary-pressed`), and the script checks the content order for these entries. The text field has no fill and no text that should change on hover, so its border moves instead (a non-text part, not a pair); its text entries are unchanged between states. The slider moves the color of its fill and thumb, as the link moves its text. An unselected checkbox, radio button, or switch has no fill either, and no text inside it: its border moves on hover and a quiet fill appears on pressed, none of them a pair.

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

A component with a dark background and light content (for example a tooltip) uses a `solid` step of a scale, usually the neutral scale, as its background, and an `on-*` content token: white by default, or step `50` of the same scale. The component token contract declares the background step, within `600` to `900`. The pair is checked like any other. Dark-background components with interactive states are not covered yet: a spec that needs them must extend this rule first. This paragraph describes the light mode. In dark mode the tooltip is inverted (light background, dark content): see "Tooltip and scrim" in Dark mode.

### Automatic check

- Every `components` entry is checked against 4.5:1 by the theme script and by the DESIGN.md lint. A new component is covered as soon as it declares its pairs as `components` entries; no other list needs updating.
- Entry names: `<component>-<variant>` for `enabled`, `<component>-<variant>-<state>` for `hover` and `pressed`. The script groups entries by removing the `-hover` or `-pressed` suffix, and checks that the backgrounds of a group resolve to distinct colors. The lint does not check this; the script does.
- The script also checks the families: no pair has an `intermediate` background, and every content step is allowed for the family of its background.
- An entry that is not a variant state (for example `button-focus-ring`) is only checked for contrast.
- Disabled-state pairs stay excluded (see below).

### Muted text

`on-surface-muted` (placeholder, helper text, counter, affixes, quiet icons) is quieter than `on-surface` but is only checked against `{colors.surface}`.

- Use it on `{colors.surface}` only. Never use it on a grayed fill: `neutral-subtle-hover`, `neutral-subtle-pressed`, `disabled-container`, or any neutral step `100` and beyond. On those fills it falls below 4.5:1. A part that sits on a grayed fill (for example the affixes of a `read-only` text field) takes `on-surface`.
- In dark mode the rule holds with the surface levels: it is allowed on any surface level and is checked against the most unfavorable one (see Dark mode).
- It must not resolve to the same color as `on-surface`. `theme/theme.py` stops with an explicit error (exit code 2, nothing written) when both fall on the same neutral step, instead of silently accepting a muted text that is not quieter.

### Known limit

The script checks each `components` entry against its own declared background (for example `chip-default-hover` on a gray fill), and accent or content colors without an entry only against `{colors.surface}`; on an image or a dark background (for example under a floating button), the user retouches the theme after generation.

Point of vigilance. Two treatments sit outside the surface, and each is handled by a dedicated rule, not by a general check:

- `on-surface-muted` is forbidden on a grayed fill (see Muted text). A part on a grayed fill takes `on-surface`.
- The destructive menu item is the only exception that puts an accent color on a grayed fill: `danger-hover` on `neutral-subtle-hover`, and `danger-pressed` on `neutral-subtle-pressed` (see Background families and `components/menu.md`).

If such exceptions multiply, stop adding rules. Check every content color against all the backgrounds where it really sits.

## Lint and contrast

- The DESIGN.md contrast rule (`contrast-ratio`) checks only the entries of the `components` key.
- The kit never adds non-standard properties to `components`. It only declares standard `backgroundColor` and `textColor` entries, one per variant and active state, so the DESIGN.md lint checks contrast.
- Non-text contrast (WCAG 1.4.11, 3:1) cannot be declared in `components`: a pair would be checked at 4.5:1, and a border property would be non-standard. The one such pair of the kit, `colors.outline` against `colors.surface` (see `components/text-field.md`), is checked by `theme/theme.py` and listed in its report; without the script, compute it by hand. It covers every part drawn in `outline`: the field border, the border of a clickable outlined card, the border of an unselected checkbox, radio button, and switch (and the off thumb), the slider track, the border and dividers of the segmented control, and the dividers of the accordion.
- Disabled-state pairs are never declared in `components`, because WCAG 1.4.3 exempts inactive components and the lint would otherwise flag them. The disabled token mapping stays described in the component spec, and the `on-disabled` and `disabled-container` tokens stay in the colors token contract.
- Theme validation criterion: 0 errors and 0 `contrast-ratio` warnings. `orphaned-tokens` warnings on unused primitive palette steps are expected and tolerated; no other warning is. When the theme has a dark mode, the criterion applies to each of the two theme files, validated separately (see Dark mode).

## Dark mode

The dark mode is an option of the questionnaire, never a default. The light mode stays the reference: every rule of this file that does not mention the dark mode is a light mode rule. A theme without the option has one theme file and no dark rule applies.

Rules marked "to confirm by the trial of lot D4" are proposals, not measured results: the exact steps are fixed only once the trial has been run on real palettes.

### Activation

- The kit does not switch modes. It provides two sets of values and one documented activation point: the dark mode applies under the attribute `data-theme="dark"`.
- The consuming application decides when to set the attribute (system preference, user setting, or anything else) and on which element (the root element for the whole page, or any ancestor to scope it). Without the attribute, the light values apply.
- Component code does not change between modes: it reads the same variables, and only their values differ (see `docs/implementation.md`).

### Two theme files

- The light theme is the existing DESIGN.md. The dark theme is a second file in the DESIGN.md format, specific to the project, named `DESIGN.dark.md`.
- Both files use the same role names, with different values. A role exists in both, or in neither.
- Each file is validated separately by the lint, with the criterion of "Lint and contrast". The dark file declares its own `components` entries, because the lint checks only these entries.
- The dark file carries what depends on the mode: `colors`, the `components` pairs, and `## Elevation & Depth`. Spacing, rounded, typography and `## Icons` stay in the light file. To confirm in lot D2: the dark file must remain valid on its own, so it may only reference tokens it defines.
- The Google DESIGN.md spec is never modified. If DESIGN.md adds `modes` (see issue 13 of `google-labs-code/design.md`), the two files are merged into one; the roles and values do not change.

### Color derivation

- Dark colors are derived by role correspondence, each role taking the step that suits the dark mode (the Material 3 and Radix models). They are never derived by arithmetic inversion of the light steps (step `600` becoming `300`).
- A scale keeps its direction, `50` the lightest to `900` the darkest, in both modes. What changes is the step each role takes.
- Whether a background is light or dark depends on the mode, not on its step number. The families below replace those of "Background families" in dark mode.

### Families in dark mode

Provisional, to confirm by the trial of lot D4.

| Family | Background | Allowed content |
|---|---|---|
| `dark` | The surface roles (see below), and steps `800` and `900` of a scale | Step `50`, `100`, or `200` of the same scale, or `on-surface` |
| `bright` | The accent fills of the State colors rule in dark mode | An `on-*` token: step `900` of the same scale by default |
| `intermediate` | The steps between the two families above | none: never a background behind text or icons |

The ban on an `intermediate` background and on content on it holds in both modes.

### State changes in dark mode

- Each state is lighter than the previous one: the background moves first and the content follows, as in "State changes". The four forbidden cases of that section hold, with the direction reversed: two states with the same background, darkening a background or moving it back to an earlier step to pass contrast, lowering the 4.5:1 threshold, content on an `intermediate` background.
- State colors: default is the first step, searched from the lightest side of the accent range, reaching 4.5:1 against its content color and against the most unfavorable surface (see below). Hover is default minus 2 steps and pressed default minus 4 steps, stopping at step `50` if the scale starts there. Distinct states still hold: if two states land on the same step, the color is unusable and is reported. The search range and the offsets are to confirm by the trial of lot D4.
- Fill-less components keep their surface as the background of every state, and their content color lightens from one state to the next.
- Content step search: test the content steps from the darkest to the lightest of the allowed set (`200`, then `100`, then `50`), keep the first reaching 4.5:1 against every background of the set. The lightest background of the set decides. At the scale end there is no further step: the pair fails and is reported, as in "Content step search".

### Brand color

The brand color is never modified without the user's agreement.

1. If the brand color reaches the contrast required in dark mode on `{colors.surface-level-5}`, it is kept as is.
2. Otherwise the kit proposes the nearest step of the brand palette that passes, with its measured ratio.
3. The user accepts or refuses. On refusal, the pair is reported as failing (see "When a color cannot reach AA" in `theme/questionnaire.md`). The kit never substitutes silently.

### Surfaces and elevation

In dark mode there is no shadow. Each elevation level has its own surface, a notch lighter than the previous level.

| Level | Surface role |
|---|---|
| `level-0` | `{colors.surface}` |
| `level-1` | `{colors.surface-level-1}` |
| `level-2` | `{colors.surface-level-2}` |
| `level-3` | `{colors.surface-level-3}` |
| `level-4` | `{colors.surface-level-4}` |
| `level-5` | `{colors.surface-level-5}` |

- Each surface is strictly lighter than the previous one, from `{colors.surface}` to `{colors.surface-level-5}`.
- Tint option, asked by the questionnaire:
  - `slightly tinted` (default): gray with a weak tint of the theme color. The tint is constant at every level, and never grows with the elevation (the Material 3 approach that was dropped).
  - `neutral`: pure gray, as in Carbon and Atlassian.
- A component at `level-n` takes the surface role of its level as fill in dark mode, in place of the `{colors.surface}` that its spec names for the light mode. The specs keep naming `{colors.surface}` and the level; the correspondence is stated once, here. To confirm in lot D5: the Token mapping of the specs may be aligned later.
- Contrast on a surface is checked on the lightest level, `{colors.surface-level-5}`, the most unfavorable one for light text. A pair that passes there passes on every lower level. This applies to text, to the accent colors listed with the surface in "Background families", to `on-surface-muted`, to the 3:1 non-text pairs (`colors.outline`) and to the focus ring.
- Elevation never carries state feedback alone, as in light mode. Hover and pressed keep their color tokens.

### Tooltip and scrim

- The tooltip is inverted in dark mode: a light background and a dark content. It is the one component that reverses with the mode: `{colors.inverse-surface}` resolves to a light step in the dark file, and its content token to a dark step of the same scale. The pair is checked at 4.5:1 like any other.
- The scrim of the dialog is its own role, `{colors.scrim}`, in both files, so that it no longer depends on the tooltip. Its opacity remains a behavior constant of the dialog spec. Its dark mode value is to confirm by the trial of lot D4.

### Floating surface and overlay panel

- The menu, the select list and the popover, and the dialog and the toast, take the surface role of their level (`level-2` for the first three, `level-3` for the other two) as fill, with the border of their common look and no shadow. The border and the surface step carry the depth.
- The toast follows the active mode, as in "Overlay panel".

### New color roles

| Role | Mode | Use |
|---|---|---|
| `surface-level-1` to `surface-level-5` | Dark; light value to confirm in lot D2 | Fill of a component at that elevation level. `level-0` keeps `{colors.surface}` |
| `scrim` | Both | Color of the veil behind the dialog |

Open for lot D2: in the light file, `surface-level-1` to `surface-level-5` may resolve to `{colors.surface}` so that both files hold the same roles, or exist only in the dark file. The choice depends on the `orphaned-tokens` tolerance of the lint, which covers primitive palette steps only. `inverse-surface` and its content token keep their names and exist in both files.

### Automatic check

The theme script checks the dark file the same way as the light file, with the dark families and directions above: every `components` pair at 4.5:1, the distinct and lighter states, the families, the `outline` and focus ring pairs at 3:1, and the strict order of the surface roles. This is the work of lot D2.

## Motion

- Essential motion, which tells the user that work is going on (the button spinner, the indeterminate progress), is kept under `prefers-reduced-motion` but slowed down by about 2.5 to 3 times (WCAG 2.2.2). It is never turned into a static shape.
- Every other transition (the height of an accordion panel, the turn of its chevron, the move of a tab indicator, the change of fill of a segmented control, a thumb or a determinate progress change) carries no information that the final state does not give. It is optional, it is the project's choice, and it is removed under reduced motion: the final state appears at once. It is removed, not slowed.
- A duration named by a spec is a behavior constant, not a theme token.

## Elevation

Elevation (shadow) is not a token, like the icon style. DESIGN.md has no shadow or elevation token type and no YAML key for it: it defines `Elevation & Depth` as a prose section describing the required styling (spread, blur, color). The scale lives in the `## Elevation & Depth` Markdown section of DESIGN.md, as a table. Component specs designate a level by its name; they never hold a shadow value.

### Levels

The scale follows the Material 3 model: six levels, named after their relative distance above the surface. The level names are stable: they never change from one theme to another, and a theme never adds, removes, or renames a level.

| Level | Role | Typical use |
|---|---|---|
| `level-0` | At rest, in the page flow, flat on the surface, no shadow | Every component that declares no level |
| `level-1` | At rest, slightly raised, still in the page flow | Elevated card |
| `level-2` | At rest, overlay tied to a trigger | Tooltip, menu, select list, popover |
| `level-3` | At rest, floating above the content while it scrolls | Floating button, dialog, toast |
| `level-4` | Interaction only, one step above a resting level | Hover of the floating button and of the clickable elevated card |
| `level-5` | Interaction only, highest | Dragged element (no kit component yet) |

- Resting state: a component at rest (no user interaction, for example `enabled`, `open`, `disabled`, `loading`) uses `level-0` to `level-3`.
- Interaction states: `level-4` and `level-5` are reserved for user interaction states, such as hover and drag. A spec states which state uses which level; a state may also keep its resting level.
- Each level reads as higher than the previous one. In light mode only `level-0` has no shadow. In dark mode no level has a shadow and each level reads higher by its surface (see Dark mode).
- A level is a visual depth cue, not a stacking order. Which element is drawn on top (for example a tooltip over a floating button) belongs to the page layout.
- Elevation never carries state feedback alone. Hover and pressed keep their color tokens, so a component stays fully usable without its shadow.
- Dark mode: there is no shadow. Depth is carried by the surface: each level has its own surface color, a notch lighter than the previous level (see Dark mode, "Surfaces and elevation"). The level names and their uses do not change.

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
- In the dark theme file the table keeps the same six rows, and every `Shadow` cell is `none`: the depth is carried by the surface roles, not by this table.
- The default values are given by `theme/questionnaire.md`, never by this file or by a component spec. No question is asked about shadows.

### Forbidden

- An `elevation`, `shadow`, or similar key in the YAML front matter. The CLI tolerates a custom key but ignores it in every export.
- A reference such as `{elevation.level-2}`, in the theme or in a spec. The lint reports it as a broken reference.
- Any shadow property in a `components` entry. The lint warns, which breaks the validation criterion; `components` entries stay `backgroundColor` and `textColor` only.

### Reference from a spec

- A spec designates a level by its name in backticks, for example `level-2`. Never a shadow value, never a token reference.
- In Token mapping, elevation has its own short table, one row per state, when the level changes with the state; otherwise one line stating the level.
- In Token contract, elevation is listed under "Non-token requirement", next to the icon style.
- A spec that declares no level is at `level-0` in every state.

## Floating surface

A floating surface is a panel that opens next to a trigger and floats above the page: the tooltip, the menu, the select list, and the popover. It is defined once, here. Each spec states only what it adds or changes and never repeats this section.

### Common look

| Aspect | Rule |
|---|---|
| Fill | `{colors.surface}`; the tooltip alone is inverted (`{colors.inverse-surface}`, dark in light mode and light in dark mode, see `components/tooltip.md`). In dark mode the fill is the surface role of the elevation level below |
| Border | `{spacing.border-width}` in `{colors.neutral-subtle-pressed}`; the tooltip has none |
| Radius | `{rounded.overlay}` |
| Elevation | `level-2` while open; never `level-4` or `level-5` (the surface itself is never an interaction state). In dark mode: no shadow, the depth is the surface of `level-2` plus the border |
| Offset | `{spacing.xs}` between the trigger and the surface; with an arrow, to the tip of the arrow |
| Viewport padding | `{spacing.sm}`, the minimum distance kept to the edge of the viewport |

The fill of the menu, the select list, and the popover is `{colors.surface}`, so every rule that is bound to the surface still holds on them: `on-surface-muted` is allowed on it, and contrast is checked against it (see Muted text). Items that sit on a grayed fill (hover, pressed) take `on-surface`, as everywhere else. The border and the shadow set the surface apart from the page for sighted users; no information depends on them, so the 3:1 non-text rule does not apply to the border.

### Placement

- `placement` is the preferred side of the trigger: `top`, `right`, `bottom`, or `left`. `align` is the alignment along that side: `start`, `center`, or `end`. The tooltip is always `center`.
- If the surface does not fit on the preferred side, it flips to the opposite side. If it fits on neither, it keeps the preferred side and shifts along the side to respect the viewport padding.
- A surface taller or wider than the viewport minus twice the viewport padding does not grow beyond it: it scrolls inside. The scroll never closes it.
- Width comes from the content, between the minimum and the maximum of the component. Tokens: `{spacing.menu-min-width}` (menu), `{spacing.floating-max-width}` (menu, select list, popover), `{spacing.tooltip-max-width}` (tooltip).
- The surface sits above the page content. Which element is drawn on top of what stays a layout choice (see Elevation); the platform top layer is preferred to a stacking number.

### Opening and closing

- An interactive surface (menu, select list, popover) opens on activation of its trigger, never on hover alone. The trigger exposes `aria-expanded` and `aria-controls`, and `aria-haspopup` with the role of the surface.
- It closes on `Escape`, on a pointer press outside the surface and its trigger, and on activation of the trigger again. Each spec adds its own closes (activating an item, leaving by `Tab`).
- `Escape` returns focus to the trigger when focus was inside the surface. A press outside closes the surface without moving focus: it stays where the user pressed.
- At most one interactive surface is open at a time: opening one closes the other. A tooltip closes when its trigger is activated.
- Motion: the opening and closing transitions, if any, are the project's choice and are removed under reduced motion (see Motion).

### With a dialog

A dialog is modal and may hold floating surfaces: a select list, a menu, a popover, or a tooltip opened from inside it belongs to the dialog and sits above it. The "one interactive surface at a time" rule applies between those surfaces, not between a surface and the dialog that contains it. `Escape` closes the innermost surface first, and the dialog on the next press. Opening a dialog closes every floating surface that was open outside it.

## Overlay panel

An overlay panel is a panel that floats above the page and is not tied to a trigger by position: the dialog (modal, centered) and the toast (not modal, at an edge of the viewport). It is defined once, here. Each spec states only what it adds or changes.

| Aspect | Rule |
|---|---|
| Fill | `{colors.surface}`: the toast follows the active theme mode (light surface in light mode, dark surface in dark mode). In dark mode the fill is the surface role of the elevation level below |
| Border | `{spacing.border-width}` in `{colors.neutral-subtle-pressed}` |
| Radius | `{rounded.overlay}` |
| Elevation | `level-3` while open: it floats above the content, higher than a surface tied to a trigger (`level-2`); never `level-4` or `level-5`. In dark mode: no shadow, the depth is the surface of `level-3` plus the border |
| Placement | By the spec (centered for the dialog, an edge for the toast), never by a trigger: no offset, no flipping |

- Text on the surface follows the same rules as for a floating surface: `on-surface-muted` is allowed (the toast does not use it), contrast is checked against the surface, and the border and the shadow need no 3:1 check since no information depends on them.
- The page behind a dialog is inert and veiled by the scrim, which is `{colors.scrim}` at a fixed opacity (a behavior constant of the dialog spec, not a theme token). `scrim` is its own role: it does not depend on the tooltip color (see Dark mode, "Tooltip and scrim"). A toast does not veil or block anything.
- A toast waits while a dialog is open, because the page behind a dialog is inert and a message shown there would not be announced.

## Sizes

Each component declares its own sizes. There is no shared scale imposed on all components.

Sizes are declared in an explicit table, one row per size, and each cell is one token reference. A computed rule (base unit times a coefficient) is not used: real systems do not scale linearly, and an explicit table is readable by a human and convertible by an agent without arithmetic.

Structural dimensions (height, padding, gap, icon size) live in the theme, not in the spec: density is a theme choice, and keeping the values in the theme keeps every value in one file, as the token reference convention requires. A spec holds only what is specific to its component.

## Naming

Use kebab-case for file names, token names, variants, states, and parts. Example: `leading-icon`.

## Component spec format

The reference spec is `components/button.md`. Every component spec uses the sections below, in this order. A section that does not apply is kept with one line saying why.

| Order | Section | Content | Form |
|---|---|---|---|
| 1 | Title and intro | Component name, one sentence on what it does | Prose |
| 2 | At a glance | Summary of parts, configurations, variants, sizes, states | Table: aspect, summary |
| 3 | Purpose | When to use it, when not to | Short list |
| 4 | Anatomy | Parts, then configurations with their status, then combination rules | Tables: part, role, required, notes; configuration by part, status |
| 5 | Properties | Every input of the component | Table: property, values, default, description |
| 6 | Variants | Each variant and its intent | Table |
| 7 | Sizes | Optional short note on what is specific to this component's sizes, then one row per size, then geometry rules | Table: size, then one column per dimension |
| 8 | States | Interactive states, then state properties (such as `disabled`, `loading`), then precedence | Two tables, one precedence line |
| 9 | Token mapping | One table per variant: rows are states, columns are parts or properties; elevation by level name (see Elevation) | Short tables, at most five columns |
| 10 | Token contract | Every token the theme must define, grouped by DESIGN.md group | One table per group: token, role |
| 11 | Accessibility | Role, accessible name, focus, keyboard, target size, contrast | Table: topic, requirement |
| 12 | Behavior | Runtime behavior not covered by states | Short list |
| 13 | Do and don't | Usage guidance | Table: do, don't |
| 14 | Out of scope | What the spec deliberately ignores, including every configuration with the status `out-of-scope` | One line |

The justification of a spec's decisions is not part of the spec: it goes in `docs/rationale/<component>.md`, for human contributors.

Table rules, so that a machine-readable block can be derived without ambiguity:

- The first column is the key of the row. Keys use kebab-case and the exact names declared in the spec.
- A cell holds one value: a token reference such as `{colors.primary}`, a name in backticks, `none`, `yes`, `no`, short text, or, in a Status column, one status (see Configuration status).
- `none` means no fill, no border, or no value. Never leave a cell empty, never write "same as above".
- No values copied from the theme. No code blocks in a spec.
- Keep tables narrow: split a wide table into several short ones rather than adding columns.

### Configuration status

Each configuration of the Anatomy table has one status, in a `Status` column. The four statuses are defined here once; a spec never redefines them.

| Status | Meaning | Use it when |
|---|---|---|
| `allowed` | The kit specifies the case in full | The spec has the rules, tokens, and geometry for it |
| `forbidden` | The case is never generated | Accessibility or valid markup is at stake: no accessible name, interactive content where the role forbids it, invalid nesting of HTML or ARIA, a contrast that cannot be checked |
| `avoid` | The case can exist, but is discouraged | A design reason applies and no accessibility failure follows. The spec says why to avoid it and, when it is simple, how to do it correctly (model: the clickable card with controls, `components/card.md`) |
| `out-of-scope` | The case is not specified yet | The kit has no rule, token, or geometry for it. The spec also lists it in its Out of scope section |

Rules:

- `forbidden` is reserved for accessibility and for invalid HTML or ARIA. A reason of taste, density, or economy never makes a case `forbidden`.
- A `forbidden` case never moves to `avoid` when accessibility is at stake. In doubt, keep `forbidden`.
- The reason and the correct form of an `avoid` case sit in the Combination rules of the spec, in one or two sentences. The full justification sits in `docs/rationale/<component>.md`.
- A Status cell holds one status. A condition on an `allowed` case goes in the configuration cell or in the Combination rules.
- Row keys are kebab-case, like every other key of a spec.
- What an agent does with each status: see Component API in `docs/implementation.md`.
