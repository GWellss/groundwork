# Accordion

An accordion is a vertical stack of sections, each with a header that shows or hides its panel of content. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `accordion`, `item`, `heading`, `header`, `title`, `chevron`, `panel`, `divider` |
| Configurations | one or more items, each collapsed or expanded |
| Modes | `multiple` (default), `single` |
| Variants | none |
| Sizes | `s`, `m` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `expanded` (item), `disabled` (item) |

## Purpose

- Use an accordion to let the user open the sections they care about in a page with many long sections: an FAQ, grouped settings, a product's details.
- Use `tabs` when the sections are peers the user switches between and wants all labels visible in one row (see `components/tabs.md`).
- Use a single-item accordion for one optional block of detail ("Show shipping details"): it is the disclosure pattern.
- Do not use an accordion to hide content the user must read to continue, or an error message.
- Do not use an accordion to navigate between pages: use links.
- Do not nest an accordion in an accordion.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `accordion` | Holds the items | yes | One or more `item` |
| `item` | One section: a `heading` and its `panel` | yes | |
| `heading` | A heading element of the level `heading-level`, wrapping the `header` | yes | Puts the section in the page outline |
| `header` | The button that expands and collapses the item; carries the fill and the focus ring | yes | A native button filling the width of the accordion |
| `title` | Text that names the section | yes | Inside `header`; accessible name of the button |
| `chevron` | Chevron icon at the end of `header` | yes | Points down when collapsed, up when expanded; decorative |
| `panel` | The content of the section | yes | Shown only when the item is expanded |
| `divider` | Line between two neighboring items | between items | A `strong` horizontal divider (see `components/divider.md`); never at the ends |

### Configurations

| Configuration | Elements | Status |
|---|---|---|
| single-item | one `item`, used as a disclosure | allowed |
| several-items | two or more `item` | allowed |
| leading-icon | an icon before `title` | out-of-scope |
| nested | an `accordion` inside a `panel` | out-of-scope |
| header-without-title | `header` with an icon only | forbidden |
| expanded-by-default | one or more items with `expanded` true | allowed |

Combination rules:

- Every `item` has a `title`, a `header`, and a `panel`. The `header` is always the button of the `heading`. A `header` with no `title` is `forbidden`: the button has no accessible name.
- In `single` mode, at most one item is expanded. The initial state may have none or one. In `multiple` mode, any number of items may start expanded.
- The component never reorders the items.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `mode` | `multiple`, `single` | `multiple` | `multiple`: items open and close independently. `single`: opening an item closes the one that was open |
| `heading-level` | 2 to 6 | 3 | Level of the `heading` of every item; the project sets the one that fits the page outline |
| `size` | `s`, `m` | `m` | Named dimension set, shared by the items |
| `title` (item) | text | none, required | Name of the section |
| `expanded` (item) | `true`, `false` | `false` | The item starts open; the user can change it afterwards |
| `disabled` (item) | `true`, `false` | `false` | The item cannot be expanded or collapsed |

In `single` mode the user can still close the open item: all items may be collapsed.

## Variants

None. The accordion has one look: a stack of full-width headers separated by lines.

## Sizes

### Decision

Two sizes. The header height is a minimum: a title that wraps makes the header taller. Heights, icons, and typography reuse existing tokens.

### Size table

| Size | Header minimum height | Padding inline | Gap | Chevron size | Title typography |
|---|---|---|---|---|---|
| `s` | `{spacing.control-md}` | `{spacing.lg}` | `{spacing.md}` | `{spacing.icon-md}` | `{typography.label-md}` |
| `m` | `{spacing.control-lg}` | `{spacing.xl}` | `{spacing.md}` | `{spacing.icon-lg}` | `{typography.label-lg}` |

| Dimension | Token |
|---|---|
| `divider` thickness | `{spacing.border-width}` |
| `panel` padding block | `{spacing.lg}` |

Geometry rules:

- `header` fills the width of the accordion. `title` is at the start and takes the free width; `chevron` is at the end, centered on the first line of `title`; the gap separates them.
- `title` wraps onto several lines; it is never truncated. The `header` grows, with the padding block set by the minimum height.
- `panel` has the same padding inline as `header`, and `{spacing.lg}` of padding block. Its content typography belongs to the project: the kit defines labels only.
- The `divider` separates two items, below the `panel` of the first (or its `header` when collapsed). There is no line above the first item or under the last.
- `header` has no radius and no border.
- `chevron` inherits the content color of the current state. Turned up when expanded: the rotation is a fixed geometry, not a theme value.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over `header` | Hover container token |
| `focus` | Keyboard focus (focus visible) on `header` | Adds the focus ring around `header`; never changes container or content |
| `pressed` | Pointer down or key held on `header` | Pressed container token |

`focus` combines with `hover` and `pressed`.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `expanded` | None; `header` stays interactive | `panel` shown, `chevron` turned up; the colors do not change |
| `disabled` | No hover, no pressed, not focusable, not activatable | Disabled tokens; an expanded item keeps its `panel` shown |

Precedence: `disabled` overrides the interactive states. The expanded item has the same tokens as the collapsed one: the open state is carried by the panel and by the shape of `chevron`, never by color.

## Token mapping

Cell vocabulary: a token reference, or `none`. Content covers `title` and `chevron`.

### `header`

| State | Container | Content |
|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `disabled` | `none` | `{colors.on-disabled}` |

### Lines

| Part | Color |
|---|---|
| `divider` | `{colors.outline}` (the `strong` variant of the divider) |

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

The ring may overlap the neighbor `divider`; it never covers the title.

## Token contract

The accordion adds no token.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the contrast checks where the container is `none` |
| `colors.on-surface` | `title` and `chevron` |
| `colors.neutral-subtle-hover` | Hover fill |
| `colors.neutral-subtle-pressed` | Pressed fill |
| `colors.outline` | `divider` |
| `colors.on-disabled` | Disabled content |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-md` | Title for `s` |
| `typography.label-lg` | Title for `m` |

### Spacing

| Token | Role |
|---|---|
| `spacing.control-md` | Minimum header height for `s` |
| `spacing.control-lg` | Minimum header height for `m` |
| `spacing.icon-md` | Chevron size for `s` |
| `spacing.icon-lg` | Chevron size for `m` |
| `spacing.lg` | Padding inline for `s`; `panel` padding block |
| `spacing.xl` | Padding inline for `m` |
| `spacing.md` | Gap between `title` and `chevron` |
| `spacing.border-width` | `divider` thickness |
| `spacing.focus-ring-width` | Focus ring width |
| `spacing.focus-ring-offset` | Gap between `header` and its ring |

### Components entries (contrast checks)

One entry per `enabled`, `hover`, and `pressed` state, plus the focus ring, using only the standard `backgroundColor` and `textColor` properties. `disabled` pairs are never declared. When the container is `none`, `backgroundColor` is `{colors.surface}`.

| Entry | backgroundColor | textColor |
|---|---|---|
| `accordion` | `{colors.surface}` | `{colors.on-surface}` |
| `accordion-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `accordion-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `accordion-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

### Non-token requirement

`divider` is `colors.outline`, which reaches 3:1 against `colors.surface` (WCAG 1.4.11): the theme script already checks it (row `outline`, see `docs/conventions.md`); it is the only cue between two items, hence `strong`. `chevron` is the library chevron-down glyph (see `## Icons` of DESIGN.md), in `{colors.on-surface}` at 4.5:1 or more. The accordion has no elevation (`level-0`).

### Behavior constants

| Constant | Value | Meaning |
|---|---|---|
| `toggle-duration` | 200 ms | Duration of the optional height transition of `panel` and of the turn of `chevron`; invariant, not a theme token |

## Accessibility

| Topic | Requirement |
|---|---|
| Structure | Each item is a `heading` of the level `heading-level` that contains a native button, the `header`. |
| State | `aria-expanded="true"` on `header` when the item is open, `"false"` when it is closed. |
| Relation | `aria-controls` on `header` points to its `panel`. |
| Panel | A collapsed `panel` is hidden from assistive technologies and from the tab order, with all its content. With six items or fewer, an expanded `panel` has `role="region"` and `aria-labelledby` pointing to its `header`; with more, it has no role, to avoid too many landmarks. |
| Accessible name | `header`: the `title` text. |
| Icons | `chevron` is hidden from assistive technologies; the state is announced by `aria-expanded`. |
| Not by color alone | The open state is shown by the visible `panel` and by the turned `chevron` (WCAG 1.4.1). |
| Keyboard | `Tab` moves focus between the headers and the interactive content of expanded panels, in page order. `Enter` and `Space` toggle the focused `header`. Arrow keys between headers are not defined by this spec. |
| Focus visible | The focus ring appears on keyboard focus, around `header`. It must never be removed. |
| Disabled | Native `disabled` on `header`: out of the tab order, not activatable. |
| Target size | `header` is the hit area, the full width of the accordion and at least `{spacing.control-md}` high, above 24 by 24 CSS pixels (WCAG 2.5.8). |
| Contrast | Text and chevron reach 4.5:1 against the container, delegated to the `accordion*` entries. `disabled` is exempt (WCAG 1.4.3). |
| Reduced motion | When the user asks for reduced motion, `panel` appears and disappears at once and `chevron` turns at once (see Motion in `docs/conventions.md`). |

## Behavior

- Toggle: activating `header` expands a collapsed item and collapses an expanded one. Focus stays on `header`.
- `single` mode: expanding an item collapses the one that was open. The page may move; the project keeps the expanded `header` in view.
- `multiple` mode (default): items are independent, so what the user opened stays open. Closing a section the user chose to open, because they opened another, would be a surprise, and would lose content they were reading.
- Opening: the height transition of `panel` and the turn of `chevron` last `toggle-duration` and are optional. Under reduced motion they are removed, not slowed: they carry no information the final state does not give.
- State of content: collapsing a `panel` does not reset its content; input and scroll position are kept.
- A `header` that is disabled keeps its `panel` shown or hidden as it was.

## Do and don't

| Do | Don't |
|---|---|
| Write a short, specific `title` | Write a `title` that needs the panel to be understood |
| Let several items stay open by default | Use `single` mode only to save space when users compare sections |
| Set `heading-level` to fit the page outline | Pick a heading level for its size |
| Keep content that the user must read outside the accordion | Hide required information or an error inside a panel |
| Use `tabs` to switch between peer sections | Use an accordion where all section labels should stay in one row |
| Use dividers between items only | Add a line above the first item or under the last |

## Out of scope

Animations other than the optional toggle transition, dark mode, a leading icon or a badge in the header, nested accordions, arrow-key navigation between headers, an "expand all" control, a bordered or card look, and a `chevron` placed at the start are not covered by this spec.
