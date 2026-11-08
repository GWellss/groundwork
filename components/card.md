# Card

A card is a container that groups the content of one subject: an optional image, a heading, some text, and actions. It is either static, or entirely clickable. This spec defines the minimum and nothing more: a card is not a place to put anything. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `media`, `header`, `body`, `actions` |
| Configurations | any non-empty mix of `media`, `header`, `body`; `actions` on a static card (on a clickable card: avoid, see Combination rules) |
| Variants | `outlined`, `elevated` |
| Types | static (default), clickable (`interactive` is `link` or `button`) |
| Sizes | none; the width comes from the parent, padding and gaps from spacing tokens |
| Interactive states | static: none; clickable: `enabled`, `hover`, `focus`, `pressed` |
| State properties | `disabled`, clickable only |
| Elevation | `outlined`: `level-0`; `elevated`: `level-1` at rest, `level-4` on hover when clickable (not a token, see Token contract) |

## Purpose

- Use a card to present one self-contained item among others: a product, an article, a project, a person, a summary. The user reads it as one unit.
- Use a static card when the user reads it and may act through buttons inside it. Use a clickable card when the whole card goes somewhere or does one thing.
- Do not use a card to wrap a whole page or a form, or to style a section: use spacing and a divider (see `components/divider.md`). A card around everything groups nothing.
- Do not use a card for a list of rows or a table: use a list or a table.
- Do not use a card for a message (see `components/alert.md`), nor for a panel that floats (see `components/popover.md` and `components/dialog.md`).
- Avoid making a card clickable and giving it buttons or links too: prefer a static card, see the rule below.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | The box; carries fill, border, radius, elevation | yes | Always present |
| `media` | An image or an illustration | no | At the top, edge to edge; never carries text |
| `header` | The heading of the card | no | A heading; one or two lines |
| `body` | The text and content | no | Free content; every element follows its own spec |
| `actions` | Row of buttons at the end of the card | no | Static card (on a clickable card: avoid); at most two buttons |

At least one of `media`, `header`, `body` is present.

### Configurations

| Configuration | Parts | Status |
|---|---|---|
| content | any non-empty mix of `media`, `header`, `body` | allowed |
| with-actions | `actions`, static card | allowed |
| clickable | any content, `interactive` is `link` or `button` | allowed |
| clickable-with-actions | a clickable card with `actions` | avoid |
| clickable-with-controls | a clickable card holding a link or a button | avoid |
| clickable-with-field | a clickable card holding a text field or any input | forbidden |
| empty | none of `media`, `header`, `body` | avoid |
| text-over-media | text drawn over `media` | forbidden |

Combination rules:

- A clickable card with `actions` or with other controls is `avoid`, and only exists in the form described below. A text field or any input in a clickable card is `forbidden`: an input inside a link or a button is invalid HTML.
- Text drawn over `media` is `forbidden`: its contrast cannot be checked, since the kit checks contrast against the surface only.
- An empty card is `avoid`: it groups nothing. Add a `header` or a `body`, or drop the card.

- One card, one way to act is the rule to prefer. Avoid a clickable card that also holds other links or buttons: a link or a button inside a link or a button is invalid HTML, and two hit areas on one surface are easy to confuse by keyboard, touch and screen reader. Several actions, or a secondary action next to the main one, are better served by a static card with `actions`, or by placing the second action outside the card, next to it.
- If the project still wants a whole-card click with other controls, do it in this form only:
  1. The main link is the link inside `header` (the heading), stretched by layout to cover the whole card. The `container` is not itself a link or a button, so no interactive element is nested in another.
  2. The other buttons and links are siblings of that link, stacked above the stretched area, each with its own distinct hit area, reached by `Tab` after the heading link, in reading order. Keep them apart by at least `{spacing.sm}`.
  3. Each target is at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8), and has its own accessible name; the card is named by the heading link.
  4. The hover fill shows only when the pointer is over the main area, not over a secondary control; the focus ring of the main link is drawn around the card, and the secondary controls draw their own.
  5. Never put a text field or any input in it, and never more than one stretched link.
- A static card whose main action is a link may make its `header` a link; the card itself is then still static.
- `media` is always first. It fills the width of the card with no padding and follows the card radius.
- `actions` holds at most two buttons: the main one at the end, the secondary one before it. More choices belong in a menu.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `variant` | `outlined`, `elevated` | `outlined` | Border, or raised |
| `interactive` | `none`, `link`, `button` | `none` | Static, or the whole card is a link or a button |
| `destination` | URL or route | none, required for `link` | Where a clickable link card goes |
| `label` | text | none, required if there is no `header` and `interactive` is not `none` | Accessible name of a clickable card with no heading |
| `heading-level` | 2 to 6 | 3 | Level of `header`; the project sets the one that fits the page outline |
| `disabled` | `true`, `false` | `false` | Clickable card cannot be activated; not for a static card |

## Variants

| Variant | Container | Border | Depth | Typical use |
|---|---|---|---|---|
| `outlined` | `{colors.surface}` | yes | none | Default; many cards side by side, flat pages |
| `elevated` | `{colors.surface}` | none | raised | A card that should stand out from the page |

The two variants differ in depth only. The clickable card changes its fill on hover and pressed in both, so that the shadow is never the only feedback.

## Sizes

### Decision

The card has no named sizes: its width is given by its parent (a column, a grid), and its height follows its content. Padding and gaps reuse spacing tokens, so density applies. Heading and text reuse the existing label typography.

### Size table

| Dimension | Token |
|---|---|
| `padding` | `{spacing.lg}` |
| `header-body-gap` | `{spacing.sm}` |
| `body-actions-gap` | `{spacing.lg}` |
| `actions-gap` | `{spacing.sm}` |
| `header-typography` | `{typography.label-lg}` |
| `body-typography` | `{typography.label-md}` |
| `radius` | `{rounded.overlay}` |

Geometry rules:

- `container` has the width of its parent. It has no minimum or maximum width of its own.
- `padding` is measured inside the border, which is reserved (`{spacing.border-width}`), and applies to `header`, `body` and `actions`, not to `media`.
- Order from the top: `media`, `header`, `body`, `actions`. `header-body-gap` and `body-actions-gap` separate the parts that are present. When `media` is present, `padding` still applies above `header` or `body`.
- `media` is clipped by `radius` at the top corners. It keeps its aspect ratio, which the project sets.
- `actions` is a row aligned to the end, with `actions-gap`; the buttons are size `s` (see `components/button.md`).
- `header` and `body` wrap; they are never truncated by the card.
- The border is reserved on `elevated` too, transparent, so that the two variants share the same geometry.

## States

### Interactive states

For a static card: none. `container` is not a control; its content follows its own specs.

For a clickable card:

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default | Base tokens |
| `hover` | Pointer over the card | Hover fill; `elevated` rises to `level-4` |
| `focus` | Keyboard focus (focus visible) | Adds the focus ring around the card; never changes fill, content, or border |
| `pressed` | Pointer down or key held | Pressed fill; `elevated` returns to its resting level |

`focus` combines with `hover` and `pressed`.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `disabled` | No hover, no pressed, not focusable, not activatable | Disabled tokens; the card keeps its resting elevation |

Precedence: `disabled` overrides the interactive states.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). Content covers `header` and `body`.

### `outlined`, static

| State | Fill | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.surface}` | `{colors.on-surface}` | `{colors.neutral-subtle-pressed}` |

A static card may use `{colors.on-surface-muted}` for quiet text of the `body`: its fill is the surface.

### `outlined`, clickable

| State | Fill | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.surface}` | `{colors.on-surface}` | `{colors.outline}` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `{colors.outline}` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` | `{colors.outline}` |
| `disabled` | `none` | `{colors.on-disabled}` | `{colors.disabled-container}` |

### `elevated`, static

| State | Fill | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.surface}` | `{colors.on-surface}` | `none` |

### `elevated`, clickable

| State | Fill | Content | Border |
|---|---|---|---|
| `enabled` | `{colors.surface}` | `{colors.on-surface}` | `none` |
| `hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` | `none` |
| `pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` | `none` |
| `disabled` | `{colors.disabled-container}` | `{colors.on-disabled}` | `none` |

A clickable card takes `{colors.on-surface}` for all its text, never `{colors.on-surface-muted}`: its fill turns gray on hover and pressed, where the muted color falls below 4.5:1. Border width is `{spacing.border-width}`. The border `outline` of a clickable `outlined` card keeps 3:1 on the surface (non-text check of the script) and tells it apart from a static card next to it.

### Focus ring (clickable)

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

### Elevation

Cell vocabulary: a level name.

| Variant and state | Elevation |
|---|---|
| `outlined`, every state | `level-0` |
| `elevated`, `enabled` | `level-1` |
| `elevated`, `hover` (clickable) | `level-4` |
| `elevated`, `pressed` | `level-1` |
| `elevated`, `disabled` | `level-1` |

- `level-4` is an interaction level, used on hover only. `pressed` returns to the resting level, as the floating button does: the press reads as pushing the card back.
- Elevation never carries state feedback alone: the hover and pressed fills do.
- In dark mode there is no shadow: the `elevated` card takes the surface role of its level as fill (see Dark mode in `docs/conventions.md`).

## Token contract

The theme must define every token below. The card adds no color and no token.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Fill at rest |
| `colors.on-surface` | `header`, `body` |
| `colors.on-surface-muted` | Quiet text of a static card, on the surface only |
| `colors.neutral-subtle-pressed` | Static `outlined` border; clickable pressed fill |
| `colors.neutral-subtle-hover` | Clickable hover fill |
| `colors.outline` | Clickable `outlined` border |
| `colors.disabled-container` | Disabled `elevated` fill; disabled `outlined` border |
| `colors.on-disabled` | Disabled content |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-lg` | `header` |
| `typography.label-md` | `body` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | `container` radius |

### Spacing

| Token | Role |
|---|---|
| `spacing.sm` | Header to body gap; gap between buttons of `actions` |
| `spacing.lg` | Padding; body to actions gap |
| `spacing.border-width` | Border width, reserved on every variant |
| `spacing.focus-ring-width` | Focus ring width |
| `spacing.focus-ring-offset` | Gap between card and focus ring |

### Components entries (contrast checks)

One entry per state of the clickable card and one for the focus ring, using only the standard `backgroundColor` and `textColor` properties. The static card is the `enabled` entry. The pairs follow the surface scale rule of `docs/conventions.md`: surface, then neutral `100`, then `200`.

| Entry | backgroundColor | textColor |
|---|---|---|
| `card` | `{colors.surface}` | `{colors.on-surface}` |
| `card-hover` | `{colors.neutral-subtle-hover}` | `{colors.on-surface}` |
| `card-pressed` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `card-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

`disabled` pairs are never declared. The buttons inside a static card declare their own entries.

### Non-token requirement

Elevation is not a token. The `elevated` card uses `level-1` and `level-4` of the elevation table in the `## Elevation & Depth` section of DESIGN.md. The card has no icon.

## Accessibility

| Topic | Requirement |
|---|---|
| Role, static | No role of its own. A card that is one item of a list or a grid is an `article` or a list item, so that the group is announced. |
| Role, clickable | The whole container is one native link (`interactive` is `link`) or one native button (`button`). Nothing interactive is inside it. In the discouraged form (Combination rules), the heading link is the one control that covers the card, and the other controls are its siblings, never nested. |
| Accessible name | Static: `header` is the heading, at `heading-level`. Clickable: `header` names the control (`aria-labelledby`), `body` describes it (`aria-describedby`); with no `header`, `label` names it. The heading stays inside the link or button, so the card remains in the outline. |
| Media | `media` of a clickable card is decorative (empty alternative text). In a static card it has an alternative text when it carries information. |
| Focus | Only a clickable card is focusable; the ring is drawn around the container. A static card is not in the tab order: only the buttons inside it are. |
| Keyboard | Link: `Enter`. Button: `Enter` and `Space`. `Tab` moves focus to and from a clickable card. |
| Disabled | Removed from the tab order, not activatable. |
| Not by color alone | The hover and pressed states change the fill, and an `elevated` card does not rely on its shadow. |
| Target size | A clickable card is far above 24 by 24 CSS pixels. The buttons of `actions` follow their own spec. |
| Contrast | Text reaches 4.5:1 against the fill of its state. Delegated to the DESIGN.md lint through the `card*` entries; the `outline` border is checked by the theme script. |

## Behavior

- A clickable card fires once per activation, as a button or a link does. The pointer cursor and the hover fill appear only when the card is clickable.
- Cards of a row or a grid share their layout and the height of their row, which belongs to the page; the card only stretches to it.
- A static card never changes its look on hover, so the user never takes it for a control.
- Transitions of fill and elevation, if any, are the project's choice and are removed under reduced motion (see Motion in `docs/conventions.md`).

## Do and don't

| Do | Don't |
|---|---|
| Give the card a heading that names the subject | Leave a card with only decoration |
| Make the card clickable only when it has one destination or one action | Nest a button or a link inside the link or button of a clickable card |
| Use a static card with `actions` when there are several actions | Stack a clickable card and a hidden button on it; if you need both, follow the stretched heading link form |
| Keep `media` first, edge to edge, with no text over it | Write text over an image: contrast is not controlled |
| Use `outlined` by default, `elevated` for one that stands out | Mix both variants in one row |
| Use `on-surface` for all text of a clickable card | Use `on-surface-muted` in a clickable card |
| Use spacing or a divider to group a section | Wrap a whole section in a card |

## Out of scope

Horizontal cards, expandable or collapsible cards, selectable cards (a checkbox or radio drawn as a card), draggable cards, an action menu in the header (put the trigger button in `actions`), a card with a title bar of its own, a card on an image or a tinted fill, a row or grid layout, a card with a `status` badge or avatar built in (the project places them in `body`), and animations are not covered by this spec; contrast is checked only against `{colors.surface}`.
