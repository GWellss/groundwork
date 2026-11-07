# Tabs

Tabs are a row of labels that each reveal one panel of content, one panel visible at a time, on the same page. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `tablist`, `tab`, `label`, `leading-icon`, `badge`, `indicator`, `divider`, `tabpanel` |
| Configurations | label only, with `leading-icon`, with `badge`, or both; two or more tabs |
| Selection | single, always one tab selected; `activation` `automatic` (default) or `manual` |
| Variants | none by emphasis; two appearance groups: `default` and `selected` |
| Sizes | `s`, `m` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `selected` (derived from the group `value`), `disabled` (tab) |

## Purpose

- Use tabs to split a page area into two or more peer sections of different content, where the user looks at one at a time and wants every section label visible ("Overview", "Activity", "Settings").
- Use a segmented control when the options show the same content in another way: a view, a period, a filter (see `components/segmented-control.md`).
- Use an accordion when the sections are long, stacked, and the user may want several open at once (see `components/accordion.md`).
- Do not use tabs to navigate between pages: when a label leads to another page or URL, use links (see `components/link.md`). Tabs never reload the page; the content of every panel belongs to the same page.
- Do not use tabs for a single section, for a step-by-step sequence the user must follow in order, or nested inside another set of tabs.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `tablist` | Holds the tabs in one row | yes | Scrolls horizontally when the tabs do not fit |
| `tab` | One control that shows its panel | yes | Two or more; a native button |
| `label` | Text of the tab | yes | Always visible; accessible name of the tab |
| `leading-icon` | Icon before the label | no | Decorative |
| `badge` | A `count` or `dot` badge after the label (see `components/badge.md`) | no | At most one per tab |
| `indicator` | Bar at the bottom edge of the selected tab | when selected | The shape cue of the selection |
| `divider` | Horizontal line under the whole `tablist`, separating it from the panels | yes | A `subtle` horizontal divider (see `components/divider.md`); the `indicator` is drawn over it |
| `tabpanel` | The content area of one tab | yes | One per tab; only the selected one is shown |

### Configurations

| Configuration | Elements of a tab | Allowed |
|---|---|---|
| label-only | `label` | yes |
| leading-icon-label | `leading-icon`, `label` | yes |
| label-badge | `label`, `badge` | yes |
| leading-icon-label-badge | `leading-icon`, `label`, `badge` | yes |
| icon-only | `leading-icon` | no |
| status-badge | a `status` badge | no |
| fewer than two tabs | any | no |
| no-selection | no tab selected | no |

Combination rules:

- A tab always has a visible `label`. Icon-only tabs are not allowed: use a labeled tab, or a toolbar of icon buttons for non-tab uses.
- Exactly one tab is selected at any time. The group always has a `value`.
- Every tab has exactly one `tabpanel`, and every `tabpanel` belongs to exactly one tab.
- The `badge` is a `count` or `dot` badge: a `status` badge is a text and is not allowed in a tab.
- The tabs share one size, and either all have a `leading-icon` or none does.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` (group) | text, or a reference to a visible heading | none, required | Accessible name of the `tablist` |
| `value` (group) | the `value` of a tab | the first enabled tab | The selected tab; never empty |
| `size` | `s`, `m` | `m` | Named dimension set, shared by the group |
| `activation` | `automatic`, `manual` | `automatic` | `automatic`: moving the focus with the arrow keys also selects the tab. `manual`: the arrow keys only move the focus; `Enter` or `Space` selects |
| `value` (tab) | text | none, required | Identity of the tab; unique |
| `label` (tab) | text | none, required | Text of the tab; accessible name |
| `leading-icon` (tab) | icon reference | none | Optional icon before the label; all or none |
| `badge` (tab) | a `count` or `dot` badge, with its own `label` | none | Optional counter or dot; see `components/badge.md` |
| `disabled` (tab) | `true`, `false` | `false` | The tab cannot be selected or focused |

Use `manual` when showing a panel is slow or has a side effect (a network request, a heavy rendering): the user can then move across the tabs without triggering each one. Use `automatic` otherwise.

## Variants

The tabs have no emphasis variants. One look: a text row over a baseline, with a bar under the selected tab. Two appearance groups serve as variant names.

| Variant | Used by | Container | Indicator | Intent |
|---|---|---|---|---|
| `default` | a tab that is not selected | none | none | Quiet label; neutral fill on hover and pressed |
| `selected` | the selected tab | none | brand color | Darker label plus the bar |

## Sizes

### Decision

Two sizes. Heights reuse the control tokens one step above the button of the same text size, so that a tab is easy to hit and the bar has room. Icons, gaps, and typography reuse existing tokens.

### Size table

| Size | Height | Padding inline | Gap | Icon size | Label typography | Badge size |
|---|---|---|---|---|---|---|
| `s` | `{spacing.control-md}` | `{spacing.lg}` | `{spacing.sm}` | `{spacing.icon-md}` | `{typography.label-md}` | `s` |
| `m` | `{spacing.control-lg}` | `{spacing.xl}` | `{spacing.sm}` | `{spacing.icon-lg}` | `{typography.label-lg}` | `m` |

| Dimension | Token |
|---|---|
| `indicator` thickness | `{spacing.xs}` |
| `divider` thickness | `{spacing.border-width}` |

Geometry rules:

- Height is fixed per size. Content is centered vertically in the height above the `indicator`, with no vertical padding.
- The `indicator` sits inside the tab height, along its bottom edge, over the whole width of the tab. Its space is always reserved, so selecting a tab never moves its content or the neighbors. It has square corners.
- A tab has no radius and no border. The hover and pressed fill covers the whole tab.
- Tabs are as wide as their content plus the padding, aligned to the start of the `tablist`; they are not stretched.
- The `label` is on a single line and never truncated. When the tabs exceed the width, the `tablist` scrolls horizontally instead.
- The `badge` follows the `label` after the gap, in the flow, at the badge size of the table. This is the one case where a `count` or `dot` badge takes part in the layout of its host (see `components/badge.md`).
- Icons inherit the content color of the current group and state.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens of the variant |
| `hover` | Pointer over the tab | Hover container token; content token of the state |
| `focus` | Keyboard focus (focus visible) on the tab | Adds the focus ring inside the tab; never changes container or content |
| `pressed` | Pointer down or key held on the tab | Pressed container token; content token of the state |

`focus` combines with `hover` and `pressed`. The ring is drawn inside the tab, not outside, because a scrolling `tablist` clips what lies beyond its box. On the selected tab, the `indicator` stays at the bottom edge under the ring.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `selected` (derived from the group `value`) | None; the selected tab stays focusable | `selected` tokens; `indicator` shown |
| `disabled` | No hover, no pressed, not focusable, not selectable | Disabled tokens; a selected tab keeps its `indicator` |

Precedence: `disabled` overrides `selected`, which overrides `default`; interactive states apply on top of the resulting variant.

## Token mapping

Cell vocabulary: a token reference, or `none`. Content covers the label and the icon.

### `default`

| State | Container | Content |
|---|---|---|
| `enabled` | `none` | `{colors.on-surface-muted}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `disabled` | `none` | `{colors.on-disabled}` |

`{colors.on-surface-muted}` is used here only because an enabled tab sits on `{colors.surface}`; as soon as a fill appears (hover, pressed), the content becomes `{colors.on-surface}`, in line with the Muted text rule of `docs/conventions.md`.

### `selected`

| State | Container | Content | Indicator |
|---|---|---|---|
| `enabled` | `none` | `{colors.on-surface}` | `{colors.primary}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.primary}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` | `{colors.primary}` |
| `disabled` | `none` | `{colors.on-disabled}` | `{colors.on-disabled}` |

### Baseline

| Part | Color |
|---|---|
| `divider` | `{colors.neutral-subtle-pressed}` (the `subtle` variant of the divider) |

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `none` (drawn inside the tab) |

## Token contract

The tabs add no token.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of the contrast checks where the container is `none` |
| `colors.on-surface` | Content of a selected tab, and of any tab on hover and pressed |
| `colors.on-surface-muted` | Content of an unselected tab at rest, on the surface only |
| `colors.neutral-subtle-hover` | Hover fill |
| `colors.neutral-subtle-pressed` | Pressed fill; `divider` |
| `colors.primary` | `indicator` |
| `colors.on-disabled` | Disabled content and indicator |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-md` | Label for `s` |
| `typography.label-lg` | Label for `m` |

### Spacing

| Token | Role |
|---|---|
| `spacing.control-md` | Height for `s` |
| `spacing.control-lg` | Height for `m` |
| `spacing.icon-md` | Icon size for `s` |
| `spacing.icon-lg` | Icon size for `m` |
| `spacing.lg` | Padding inline for `s` |
| `spacing.xl` | Padding inline for `m` |
| `spacing.sm` | Gap, both sizes |
| `spacing.xs` | `indicator` thickness |
| `spacing.border-width` | `divider` thickness |
| `spacing.focus-ring-width` | Focus ring width |

### Components entries (contrast checks)

One entry per group and per `enabled`, `hover`, and `pressed` state, plus the focus ring, using only the standard `backgroundColor` and `textColor` properties. `disabled` pairs are never declared. When the container is `none`, `backgroundColor` is `{colors.surface}`. `tab-selected-hover` and `tab-selected-pressed` equal `tab-hover` and `tab-pressed`; they are still declared so that the contrast report names each state.

| Entry | backgroundColor | textColor |
|---|---|---|
| `tab` | `{colors.surface}` | `{colors.on-surface-muted}` |
| `tab-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `tab-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `tab-selected` | `{colors.surface}` | `{colors.on-surface}` |
| `tab-selected-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `tab-selected-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `tab-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

### Non-token requirement

The `indicator` and the focus ring are `{colors.primary}`, at 4.5:1 or more against the surface by the State colors rule, hence above the 3:1 of WCAG 1.4.11; no new check is needed. `divider` is decorative and carries no pair. The tabs have no elevation (`level-0`).

## Accessibility

| Topic | Requirement |
|---|---|
| Roles | `tablist` has `role="tablist"`, named by `label`. Each `tab` is a native button with `role="tab"`. Each `tabpanel` has `role="tabpanel"`. |
| Relations | Each `tab` has `aria-controls` pointing to its `tabpanel`; each `tabpanel` has `aria-labelledby` pointing to its `tab`. |
| Selection | `aria-selected="true"` on the selected tab, `"false"` on the others. |
| Panels | Only the selected `tabpanel` is shown; the others are hidden from assistive technologies and from the tab order. A `tabpanel` whose content has no focusable element at its start is itself focusable (`tabindex="0"`). |
| Accessible name | Tab: its `label`, followed by the text of its `badge` (for example "Inbox, 3 unread messages"). The badge text is part of the tab content, never a separate focus stop. |
| Icons | `leading-icon` is hidden from assistive technologies. |
| Not by color alone | The selection is shown by the `indicator` (a shape) and by a darker label (WCAG 1.4.1). |
| Keyboard | `Tab` moves focus into the `tablist`, to the selected tab only (the other tabs have `tabindex="-1"`); the next `Tab` moves into the selected `tabpanel`. `ArrowRight` and `ArrowLeft` move focus to the next and previous enabled tab, wrapping from the last to the first and the reverse; `Home` and `End` move to the first and last enabled tab. With `activation` `automatic`, the focused tab is also selected. With `manual`, `Enter` or `Space` selects the focused tab. |
| Focus visible | The focus ring appears on keyboard focus, inside the tab. It must never be removed. |
| Disabled | Native `disabled`: out of the tab order, skipped by the arrow keys. |
| Target size | Each tab is at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8); at `{spacing.control-md}` high or more, it holds at every density. |
| Contrast | Text reaches 4.5:1 against its container, delegated to the `tab*` entries. `disabled` is exempt (WCAG 1.4.3). |
| Reduced motion | Moving the `indicator` between tabs is instant when the user asks for reduced motion (see Motion in `docs/conventions.md`). |

## Behavior

- Selection: activating a tab selects it, shows its panel, and hides the previous one. The `indicator` moves to it.
- The tabs never change the page, the URL, or the scroll position of the page. A tab that leads elsewhere is a link, not a tab.
- Hidden panels keep their state: the user's input, scroll position, and open items are not lost when the user switches tabs and comes back. Loading a panel on its first display is the project's choice.
- Overflow: when the tabs exceed the width, the `tablist` scrolls horizontally, by touch, wheel, or keyboard focus. Tabs never wrap onto a second row. The selected tab is scrolled into view on first display, and a tab that takes focus is scrolled into view. The kit defines no scroll buttons.
- Tabs keep the order given by the project; the component never reorders them.
- The `indicator` follows the selection; a transition between tabs is the project's choice and is removed under reduced motion.

## Do and don't

| Do | Don't |
|---|---|
| Use two to about seven tabs with short labels | Hide an important action in a tab the user may not open |
| Make each tab reveal different content of the same page | Use tabs to go to other pages: use links |
| Keep one tab always selected | Leave the tabs with no selection |
| Use `manual` activation for heavy or slow panels | Trigger a slow load on every arrow key press |
| Use a `count` or `dot` badge for a number or a change | Put long text or a status badge in a tab |
| Let the `tablist` scroll when tabs do not fit | Wrap the tabs onto a second row or truncate their labels |

## Out of scope

Animations (a sliding indicator), dark mode, vertical tabs, closable and draggable tabs, an overflow menu or scroll buttons, tabs that stretch to fill the width, filled or pill-shaped tabs, a secondary emphasis, nested tabs, tabs that mirror the URL, and icon-only tabs are not covered by this spec.
