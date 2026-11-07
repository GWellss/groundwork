# Link

A link is a text element that takes the user to another place: another page, another section, a file, or an external site. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `label`, `trailing-icon` |
| Configurations | label only, label + trailing icon (`standalone` only) |
| Variants | `inline`, `standalone` |
| Sizes | `inline` follows the surrounding text; `standalone` has `s`, `m`, `l` |
| Interactive states | `enabled`, `hover`, `focus`, `pressed` |
| State properties | `visited`, `disabled` |

## Purpose

- Use an `inline` link inside a sentence or a paragraph, to point to related content.
- Use a `standalone` link on its own line or in a list of links (footer, "Learn more", breadcrumb), where the text is not part of a sentence.
- Use a link to navigate. Use a button for an action that changes data or state, even when it looks like a link.
- Do not use a link as a button, and do not use a button to navigate.
- Do not use vague labels ("click here", "more"): the label says where the link goes.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `label` | Text that names the destination; carries the underline | yes | Always visible; provides the accessible name |
| `trailing-icon` | Icon after the label, for example an external-link icon | no | Decorative; only `standalone` |

### Configurations

| Configuration | Variant | Trailing slot | Status |
|---|---|---|---|
| inline-label | `inline` | none | allowed |
| standalone-label | `standalone` | none | allowed |
| standalone-label-icon | `standalone` | `trailing-icon` | allowed |
| inline-icon | `inline` | `trailing-icon` | out-of-scope |
| no-label | any | any | forbidden |

Combination rules:

- A link always has a visible label. An icon-only link is `forbidden`: use an icon-only button, or give the link a visible label.
- `inline` has no icon, so that the line height of the paragraph never changes. An icon in an `inline` link is `out-of-scope`: the inline link has no icon size.
- A link that opens a new window or tab says so in its label or through the external-link `trailing-icon` and its accessible text.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `label` | text | none, required | Text of the link; accessible name |
| `destination` | URL or route | none, required unless `disabled` | Where the link goes |
| `variant` | `inline`, `standalone` | `inline` | Appearance group |
| `size` | `s`, `m`, `l` | `m` | Named dimension set; only `standalone` |
| `trailing-icon` | icon reference | none | Optional icon after the label; only `standalone` |
| `disabled` | `true`, `false` | `false` | The link cannot be activated |

## Variants

| Variant | Used by | Underline | Intent |
|---|---|---|---|
| `inline` | Inside running text | always | Distinguished from the text by the underline, never by color alone (WCAG 1.4.1) |
| `standalone` | Alone on a line, in a list or a footer | on `hover`, `focus`, and `pressed` only | Clean look where the context already shows that the text is a link |

## Sizes

### Decision

The `inline` link has no size: it inherits the typography of the surrounding text, so it always matches its sentence. The `standalone` link has three sizes that reuse the label typography. Padding, gap, and icon size reuse tokens of the theme.

### Size table

| Size | Typography | Icon size | Gap |
|---|---|---|---|
| `s` | `{typography.label-sm}` | `{spacing.icon-sm}` | `{spacing.xs}` |
| `m` | `{typography.label-md}` | `{spacing.icon-md}` | `{spacing.xs}` |
| `l` | `{typography.label-lg}` | `{spacing.icon-lg}` | `{spacing.sm}` |

Geometry rules:

- A link has no fill, no border, and no padding of its own: its box is the text, plus the icon for `standalone`.
- Gap separates the label from `trailing-icon`.
- The underline is drawn under the label only, with the thickness of `{spacing.border-width}`; it never runs under `trailing-icon`.
- The icon inherits the content color of the current state.
- The focus ring radius is `{rounded.overlay}`.

## States

### Interactive states

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default, no interaction | Base tokens |
| `hover` | Pointer over the link | Hover color; the `standalone` underline appears |
| `focus` | Keyboard focus (focus visible) | Adds the focus ring; never changes color or underline; `standalone` shows its underline |
| `pressed` | Pointer down or key held | Pressed color |

`focus` combines with `hover` and `pressed`: the ring is drawn on top of their tokens.

### State properties

| Property | Effect on interaction | Visual effect |
|---|---|---|
| `visited` | None; the link stays interactive | `visited` color. Set by the platform from the browsing history; it applies only to links with a destination |
| `disabled` | No hover, no pressed, not activatable, not a navigation | Disabled color, no underline for `standalone` |

Precedence: `disabled` overrides `visited`. Interactive states (`hover`, `pressed`) override `visited`: while the pointer is on the link, it shows the `hover` or `pressed` color, then returns to `visited`.

## Token mapping

Cell vocabulary: a token reference, or `none`. A link has no container and no border: only the content (label, underline, icon) has a color. Every color is checked against `{colors.surface}`.

### Content color

| State | Content |
|---|---|
| `enabled` | `{colors.primary}` |
| `hover` | `{colors.primary-hover}` |
| `pressed` | `{colors.primary-pressed}` |
| `visited` | `{colors.link-visited}` |
| `disabled` | `{colors.on-disabled}` |

The state moves the content color, because there is no fill to move. `enabled`, `hover`, and `pressed` are each darker than the previous one. `visited` has its own color, `{colors.link-visited}`, the step of the `primary` scale right after the `primary` step. It is different from `{colors.primary}`, `{colors.primary-hover}` and `{colors.primary-pressed}`, so a visited link is recognizable by color in running text without a second hue.

### Focus ring

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

## Token contract

The theme must define every token below. The link adds one token, `colors.link-visited`; every other color is reused from the button and the chip.

### Colors

| Token | Role |
|---|---|
| `colors.surface` | Background of every contrast check |
| `colors.primary` | `enabled` content |
| `colors.primary-hover` | `hover` content |
| `colors.primary-pressed` | `pressed` content |
| `colors.link-visited` | `visited` content. Default: the `primary` scale step right after the `primary` step, reaching 4.5:1 against `colors.surface`, different from `colors.primary`, `colors.primary-hover` and `colors.primary-pressed` |
| `colors.on-disabled` | `disabled` content |
| `colors.focus-ring` | Focus ring |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | `standalone`, size `s` |
| `typography.label-md` | `standalone`, size `m` |
| `typography.label-lg` | `standalone`, size `l` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | Focus ring radius |

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-sm` | Icon size for `s` |
| `spacing.icon-md` | Icon size for `m` |
| `spacing.icon-lg` | Icon size for `l` |
| `spacing.xs` | Gap for `s` and `m` |
| `spacing.sm` | Gap for `l` |
| `spacing.border-width` | Underline thickness |
| `spacing.focus-ring-width` | Focus ring width |
| `spacing.focus-ring-offset` | Gap between the link and its focus ring |

### Components entries (contrast checks)

One entry per state that changes the content color, using only the standard `backgroundColor` and `textColor` properties. The link has no fill: `backgroundColor` is `{colors.surface}` for every entry. `disabled` is never declared (WCAG 1.4.3 exemption, see `docs/conventions.md`).

| Entry | backgroundColor | textColor |
|---|---|---|
| `link` | `{colors.surface}` | `{colors.primary}` |
| `link-hover` | `{colors.surface}` | `{colors.primary-hover}` |
| `link-pressed` | `{colors.surface}` | `{colors.primary-pressed}` |
| `link-visited` | `{colors.surface}` | `{colors.link-visited}` |
| `link-focus-ring` | `{colors.surface}` | `{colors.focus-ring}` |

### Non-token requirement

Icon style and library come from the `## Icons` section of DESIGN.md. The external-link icon is the library's "open in new" glyph. The link has no elevation.

## Accessibility

| Topic | Requirement |
|---|---|
| Role | Native link semantics (an anchor with a destination). Never a non-link element with a click handler. |
| Accessible name | The `label` text, meaningful out of context. An external-link `trailing-icon` is hidden from assistive technologies, so the label or a visually hidden text says that the link opens elsewhere. |
| Not by color alone | `inline` is always underlined (WCAG 1.4.1). `visited` differs from `enabled` by color, which is an extra cue, never the only one. |
| Focus visible | The focus ring appears on keyboard focus. It must never be removed. |
| Keyboard | `Enter` activates the link. `Tab` moves focus to it. |
| Disabled | The link has no destination and is exposed as disabled (`aria-disabled="true"`); it stays readable. It is removed from the tab order. |
| Target size | `standalone`: hit area at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8); extend it invisibly without overlapping a neighbor. `inline`: exempt, because the target is in a sentence. |
| Contrast | Content reaches at least 4.5:1 against `{colors.surface}`. Delegated to the DESIGN.md lint through the `components` entries of the Token contract. `disabled` is exempt (WCAG 1.4.3). |

## Behavior

- Activation navigates to `destination`. A link that opens in a new context states it (see Anatomy).
- `visited` is read from the platform. A platform that does not expose it never shows `visited`: the link keeps its `enabled` look.
- Label: `inline` wraps with the text. `standalone` is single line; if space runs out, it is truncated with an ellipsis and the accessible name keeps the full text.
- `trailing-icon` stays on the same line as the last word of the label and does not wrap alone.

## Do and don't

| Do | Don't |
|---|---|
| Name the destination: "Read the privacy policy" | Write "click here" or "more" |
| Underline inline links | Rely on color alone to show a link |
| Use a link to navigate and a button to act | Style a button as a link to navigate |
| Say when a link opens a new tab | Open a new tab with no warning |
| Keep the label meaningful out of context | Repeat the same label for different destinations |

## Out of scope

Animations, dark mode, an icon in an inline link, link on a colored or image background (contrast is checked only against `{colors.surface}`, so the user retouches the link colors after generation), links that look like buttons, breadcrumbs, and semantic color variants (danger, success) are not covered by this spec.
