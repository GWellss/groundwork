# Tooltip

A tooltip shows a short text description of an element when the element is hovered or focused. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `text`, `arrow` |
| Configurations | text only, text + arrow |
| Variants | `plain` |
| Sizes | none; one maximum width |
| Interactive states | none (never interactive); visibility states `closed`, `open` |
| State properties | none |
| Behavior options | `placement`, `arrow` |
| Behavior constants | open delay, skip delay (invariant, in this spec) |
| Elevation | `level-2` when `open` (not a token, see Token contract) |
| Tokens required | 2 colors, 1 typography, 1 rounded, 3 spacing; 4 reused, 3 new (see Token contract) |
| Contrast entries | 1 `components` entry, `backgroundColor` and `textColor` only (see Token contract) |

## Purpose

- Use a tooltip to name or briefly describe an element whose purpose is not obvious, typically an icon-only button.
- Use it for supplementary information only: the interface must stay usable without it, including on touch screens where hover does not exist.
- Do not use a tooltip for interactive content (links, buttons, inputs): use a popover or a dialog.
- Do not use a tooltip for errors, validation messages, or anything the user must read: show it inline.
- Do not use a tooltip on a disabled element: a disabled element cannot be focused, so keyboard users never see it.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | Holds the text, carries the fill and the radius | yes | Always present |
| `text` | Plain text description | yes | No formatting, no interactive content |
| `arrow` | Triangle pointing to the trigger | no | Same fill as `container`; shown only when `arrow` is true |

The trigger is the element the tooltip describes. It is not a part of the tooltip.

### Configurations

| Configuration | `text` | `arrow` | Allowed |
|---|---|---|---|
| text-only | yes | no | yes |
| text-arrow | yes | yes | yes |
| arrow-only | no | yes | no |
| empty | no | no | no |
| interactive-content | links or controls | any | no |

Combination rules:

- A tooltip always has text. An empty tooltip is never rendered.
- `text` is plain text only: no link, no button, no input, no image.
- One trigger has at most one tooltip, and at most one tooltip is open on the page at a time.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `text` | text | none, required | The description; short, one sentence at most |
| `placement` | `top`, `right`, `bottom`, `left` | `top` | Preferred side of the trigger; the tooltip flips if space runs out |
| `arrow` | `true`, `false` | `false` | Shows `arrow` pointing to the trigger |

## Variants

| Variant | Container | Content | Typical use |
|---|---|---|---|
| `plain` | dark solid fill | light | Short label or description of a trigger |

Rich tooltips (title, body, actions) are out of scope.

## Sizes

### Decision

The tooltip has no named sizes: its size follows its text. It declares one maximum width, a theme token, so that long text wraps onto several lines instead of growing across the screen. Padding, offset, and arrow reuse spacing tokens of the theme, so density applies to tooltips.

### Size table

| Dimension | Token |
|---|---|
| `max-width` | `{spacing.tooltip-max-width}` |
| `padding-inline` | `{spacing.sm}` |
| `padding-block` | `{spacing.xs}` |
| `offset` | `{spacing.xs}` |
| `arrow-width` | `{spacing.sm}` |

| Dimension | Token |
|---|---|
| `viewport-padding` | `{spacing.sm}` |
| `typography` | `{typography.label-sm}` |
| `radius` | `{rounded.overlay}` |

Geometry rules:

- Width fits the text, up to `max-width`. Beyond it, the text wraps; it is never truncated.
- Height follows the text: padding block, then the lines of text.
- `offset` is the distance between the trigger and the tooltip; with `arrow`, it is measured to the tip of the arrow.
- `arrow` is an isosceles triangle, `arrow-width` wide at its base and half as high, centered on the trigger along the placement side while the tooltip is aligned center.
- `viewport-padding` is the minimum distance kept between the tooltip and the edge of the viewport.
- The tooltip is aligned center on the trigger along its placement side, and shifts along that side when needed to respect `viewport-padding`; `arrow` keeps pointing to the trigger.

## States

### Interactive states

None: the tooltip is never interactive. It only has visibility states.

| State | Trigger | Visual effect |
|---|---|---|
| `closed` | Default; after dismissal, or when hover and focus have left | Not rendered |
| `open` | Trigger hovered for the open delay, or focused | `plain` tokens |

### State properties

None: a tooltip has no `disabled` or `loading` property. Its trigger may be disabled, which is discouraged (see Purpose).

Precedence: dismissal with `Escape` overrides hover and focus until both have left the trigger.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border).

### `plain`

| State | Container | Content | Border | Arrow |
|---|---|---|---|---|
| `open` | `{colors.inverse-surface}` | `{colors.on-inverse-surface}` | `none` | `{colors.inverse-surface}` |

### Elevation

The tooltip is at `level-2` when `open`; `closed` is not rendered. `open` is a resting level: the tooltip is never interactive, so it never uses `level-4` or `level-5`. The shadow applies to the container and the arrow as one shape.

## Token contract

The theme must define every token below. The questionnaire asks for them; the generator fails if one is missing.

### Palette scales

`colors.inverse-surface` points to a `solid` step of the neutral scale, following the "Dark background with light content" case of the Contrast pairs rule in `docs/conventions.md`. The declared background step is `900`, the last step of the neutral scale. `colors.on-inverse-surface` is white by default, or step `50` of the neutral scale.

### Colors

| Token | Role | New |
|---|---|---|
| `colors.inverse-surface` | `plain` container and arrow; neutral step `900` | yes |
| `colors.on-inverse-surface` | `plain` text | yes |

### Typography

| Token | Role | New |
|---|---|---|
| `typography.label-sm` | Tooltip text | no |

### Rounded

| Token | Role | New |
|---|---|---|
| `rounded.overlay` | Container radius; a moderate radius in every corner style, never a stadium shape | yes |

### Spacing

| Token | Role | New |
|---|---|---|
| `spacing.xs` | Padding block; offset | no |
| `spacing.sm` | Padding inline; arrow width; viewport padding | no |
| `spacing.tooltip-max-width` | Maximum width of the container | yes |

### Components entries (contrast checks)

One entry for the single variant and its single visible state, using only the standard `backgroundColor` and `textColor` properties. The tooltip has no `hover` or `pressed` state, so the entry has no state suffix. The pair follows the "Dark background with light content" case of `docs/conventions.md`: a `solid` background and an `on-*` content token.

| Entry | backgroundColor | textColor |
|---|---|---|
| `tooltip-plain` | `{colors.inverse-surface}` | `{colors.on-inverse-surface}` |

### Totals

| Category | Count | Reused | New |
|---|---|---|---|
| Colors | 2 | 0 | 2 |
| Typography | 1 | 1 | 0 |
| Rounded | 1 | 0 | 1 |
| Spacing | 3 | 2 | 1 |
| Components entries | 1 | 0 | 1 |

### Non-token requirement

Elevation is not a token. The tooltip uses `level-2` of the elevation table in the `## Elevation & Depth` section of DESIGN.md (see Elevation in `docs/conventions.md`); it is not counted in the totals. The tooltip has no icon. Its timing values are behavior constants, not tokens (see Behavior).

## Accessibility

| Topic | Requirement |
|---|---|
| Role | The container has the `tooltip` role. |
| Relation | The trigger references the tooltip with `aria-describedby` while it is open. The tooltip is a description, not a name. |
| Accessible name | The tooltip never replaces the accessible name of the trigger. An icon-only button keeps its own name; when the tooltip only repeats that name, do not also reference it with `aria-describedby`, to avoid a double announcement. |
| Triggers | Opens on pointer hover and on keyboard focus of the trigger. Hover alone is not enough. |
| Dismissible | `Escape` closes the tooltip without moving focus (WCAG 1.4.13). |
| Hoverable | The pointer can move from the trigger onto the tooltip, across the offset, without the tooltip closing (WCAG 1.4.13). |
| Persistent | The tooltip stays open while the trigger is hovered or focused, or the tooltip is hovered, until dismissed (WCAG 1.4.13). It never closes on a timer. |
| Interactive content | Never. The tooltip is not focusable and contains no focusable element. |
| Target size | Not applicable: the tooltip is not interactive. The trigger follows its own spec. |
| Contrast | Text reaches at least 4.5:1 against the container. Delegated to the DESIGN.md lint through the `tooltip-plain` entry. |

## Behavior

Behavior constants. They are invariant, they are not theme tokens, and the theme never overrides them.

| Constant | Value | Meaning |
|---|---|---|
| `open-delay` | 700 ms | Time the pointer rests on the trigger before the tooltip opens |
| `skip-delay` | 300 ms | Window after a tooltip closes during which hovering another trigger opens its tooltip with no delay |
| `focus-delay` | 0 ms | Keyboard focus opens the tooltip at once |

- Closing: the tooltip closes as soon as neither the trigger nor the tooltip is hovered and the trigger is not focused. The gap of the offset counts as part of the hover area, so moving the pointer onto the tooltip does not close it.
- Activation: pressing or activating the trigger closes the tooltip.
- Placement: the tooltip opens on `placement`. If it does not fit there, it flips to the opposite side; if it fits on neither, it keeps `placement` and shifts to stay inside the viewport.
- Single tooltip: opening a tooltip closes any other open tooltip.
- Text: wraps at `max-width`, never truncated.

## Do and don't

| Do | Don't |
|---|---|
| Name icon-only buttons in one or two words: "Edit", "Share" | Repeat the visible label of a text button |
| Keep the text to one short sentence | Write paragraphs |
| Give the trigger its own accessible name | Rely on the tooltip as the only name |
| Open on hover and on focus | Open on hover only |
| Show essential information inline | Hide required information in a tooltip |
| Put the tooltip on a focusable trigger | Attach it to a disabled element or to plain text |

## Out of scope

Rich tooltips (title, body, actions), animations, dark mode, touch-specific triggers such as long press, and tooltips that follow the pointer are not covered by this spec; contrast is checked only against `{colors.surface}`, so on an image or a dark background the user retouches the tooltip colors after generation.

## Rationale

| Decision | Reason |
|---|---|
| `plain` only | Material 3 separates plain and rich tooltips; a rich tooltip holds actions, which a tooltip must never hold (Carbon), so it belongs to a popover spec |
| Dark solid container, light text | "Dark background with light content" case of the Contrast pairs rule; Material 3 plain tooltips use an inverse surface |
| Neutral step `900` | The step farthest from `{colors.surface}`, so the tooltip separates from light screens; white on it has the highest margin above 4.5:1 |
| New `inverse-surface` and `on-inverse-surface` tokens | No existing token is a dark neutral; reusing `{colors.on-primary}` for the text would tie the tooltip to the brand color by name |
| No sizes, one maximum width | A tooltip follows its text; Spectrum (160) and Radix Themes (360) both cap the width |
| Maximum width as a theme token | It depends on font size and density, which are theme choices |
| New `rounded.overlay` | A tooltip can wrap onto several lines; with a pill theme, `{rounded.control}` would turn a multi-line tooltip into a stadium shape |
| Padding and offset reuse `{spacing.sm}` and `{spacing.xs}` | Spectrum uses an offset of 4 and a container padding of 8; the theme's small spacing steps match without new tokens |
| Elevation `level-2` | The tooltip is an overlay tied to a trigger and shown briefly, the role of `level-2`; Material 3 menus use level 2. `level-3` is kept for elements that stay above content while it scrolls. `level-4` and `level-5` are interaction levels, and the tooltip is never interactive |
| Arrow optional, off by default | Radix makes the arrow optional; Material 3 plain tooltips have none |
| Default placement `top`, aligned center, flip when space runs out | Radix and Spectrum default to `top`; Radix aligns center by default |
| Delays are behavior constants in the spec | DESIGN.md has no duration token type, and adding a non-standard key breaks the kit's rule of standard-only tokens. Delays serve accessibility and usability, not brand identity, so they are invariant |
| Open delay 700 ms, skip delay 300 ms | Radix defaults (`delayDuration`, `skipDelayDuration`) |
| Opens at once on focus | Keyboard focus is a deliberate action; a delay would slow keyboard users |
| Hover and focus, `Escape`, hoverable, persistent | WCAG 1.4.13 Content on Hover or Focus; Carbon requires hover and focus and `Escape` to close |
| Description, not name | Carbon allows one or two words for an icon-only button; the button must still carry its own accessible name, so the tooltip never becomes the only source of it |
