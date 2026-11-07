# Avatar

An avatar is a small circular visual that identifies a person or an entity, with an image, initials, or a generic icon. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `image`, `initials`, `fallback-icon` |
| Content types | `image`, `initials`, `fallback-icon`; one at a time, with an automatic fallback order |
| Variants | none; one neutral look |
| Sizes | `xs`, `s`, `m`, `l` |
| Interactive states | none (never interactive) |
| State properties | none |

## Purpose

- Use an avatar to identify a person, a team, or an organization next to its name or its content (a comment, a list row, a profile).
- Use `initials` when no image exists, and `fallback-icon` when not even a name exists.
- Do not use an avatar for an arbitrary picture or an illustration: use an image.
- Do not use an avatar as a button on its own: wrap it in a button or a link, which carries the states and the focus ring.
- Do not use an avatar to show a count: use a badge on the avatar.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | Circular clip and fill | yes | Always present |
| `image` | Picture of the person or entity | no | Covers the container fully |
| `initials` | First letters of the name | no | Shown when no image is available |
| `fallback-icon` | Generic person icon | no | Shown when neither image nor initials are available |

### Configurations

| Configuration | Content | Allowed |
|---|---|---|
| image | `image` | yes |
| initials | `initials` | yes |
| icon | `fallback-icon` | yes |
| image-and-initials | `image` and `initials` shown together | no |
| empty | none | no |

Combination rules:

- One content is shown at a time. The fallback order is `image`, then `initials`, then `fallback-icon`.
- A badge may sit on the avatar; it is a separate component (see `components/badge.md`) and is not a part of the avatar.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `image` | image reference | none | Picture; when it is missing or fails to load, the next content is shown |
| `name` | text | none | Full name of the person or entity; source of `initials` |
| `size` | `xs`, `s`, `m`, `l` | `m` | Named dimension set |
| `label` | text | `name` | Accessible name. An empty `label` makes the avatar decorative |

## Variants

The avatar has no variants: one neutral look serves every person or entity. Its color comes from the single `default` group, used as the variant name in the `components` entry.

## Sizes

### Decision

Four sizes, each with its own tokens. `xs` fits dense rows and stacked lists, `l` fits a profile header. Dimensions reuse the control and icon sizes of the theme, so density applies to avatars without new tokens.

### Size table

| Size | Diameter | Initials typography | Fallback icon size |
|---|---|---|---|
| `xs` | `{spacing.icon-lg}` | `{typography.label-sm}` | `{spacing.icon-sm}` |
| `s` | `{spacing.control-sm}` | `{typography.label-sm}` | `{spacing.icon-md}` |
| `m` | `{spacing.control-md}` | `{typography.label-md}` | `{spacing.icon-lg}` |
| `l` | `{spacing.control-xl}` | `{typography.label-xl}` | `{spacing.icon-xl}` |

Geometry rules:

- The avatar is a square box of the diameter, always clipped to a circle. This is a fixed geometry, not a theme value: an avatar never follows `{rounded.control}`.
- `image` covers the container fully and is cropped to fill it, never stretched.
- `initials` and `fallback-icon` are centered.
- Initials: up to two letters, the first letter of the first and of the last word of `name`, in uppercase. Size `xs` shows only the first letter. Two letters that do not fit in the circle are replaced by the first one.
- The avatar has no border and no padding.
- Icons inherit the content color.

## States

### Interactive states

None: an avatar is never interactive and never focusable. A clickable avatar is wrapped in a button or a link, which owns its states and its focus ring.

### State properties

None. An avatar has no `disabled` state; a disabled wrapper follows its own spec.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). Content covers the initials and the fallback icon.

### `default`

| Content type | Fill | Content |
|---|---|---|
| `image` | `none` | `none` |
| `initials` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |
| `fallback-icon` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

An image covers the fill. The fill and the content are those of the chip avatar, so a chip and a standalone avatar of the same person look the same.

The avatar is at `level-0`.

## Token contract

The theme must define every token below. The avatar adds no token: every color is reused from the chip.

### Colors

| Token | Role |
|---|---|
| `colors.neutral-subtle-pressed` | Fill of `initials` and `fallback-icon`. Default: neutral step `200` |
| `colors.on-surface` | Content of `initials` and `fallback-icon` |

### Typography

| Token | Role |
|---|---|
| `typography.label-sm` | Initials for `xs` and `s` |
| `typography.label-md` | Initials for `m` |
| `typography.label-xl` | Initials for `l` |

### Spacing

| Token | Role |
|---|---|
| `spacing.icon-sm` | Fallback icon for `xs` |
| `spacing.icon-md` | Fallback icon for `s` |
| `spacing.icon-lg` | Diameter for `xs`; fallback icon for `m` |
| `spacing.icon-xl` | Fallback icon for `l` |
| `spacing.control-sm` | Diameter for `s` |
| `spacing.control-md` | Diameter for `m` |
| `spacing.control-xl` | Diameter for `l` |

### Components entries (contrast checks)

One entry for the single group, using only the standard `backgroundColor` and `textColor` properties. The avatar has no interactive state, so the entry has no state suffix. The pair equals `chip-default-pressed`; the avatar still declares its own entry so that the contrast report names the avatar and a theme stays valid whatever components it includes.

| Entry | backgroundColor | textColor |
|---|---|---|
| `avatar-default` | `{colors.neutral-subtle-pressed}` | `{colors.on-surface}` |

### Non-token requirement

Icon style and library come from the `## Icons` section of DESIGN.md. `fallback-icon` uses the library's person glyph. The avatar has no elevation.

## Accessibility

| Topic | Requirement |
|---|---|
| Role, informative | The avatar is an image: `image` content has the `img` role with `alt` set to `label`. `initials` and `fallback-icon` use a container with the `img` role and the same text as its accessible name; the letters and the icon are hidden from assistive technologies. |
| Role, decorative | When the name of the person or entity is already written next to the avatar, `label` is empty: `image` has an empty `alt`, and the container is hidden from assistive technologies. |
| Accessible name | `label`, by default `name` ("Ada Lovelace"). Never a file name, never "avatar". |
| Fallback | When `image` fails to load, the fallback keeps the same accessible name as the image. |
| Focus | Never focusable. A wrapper (button or link) owns the focus and the focus ring. |
| Target size | Not applicable: not interactive. A wrapper follows its own spec. |
| Contrast | Initials and icon reach at least 4.5:1 against the fill. Delegated to the DESIGN.md lint through the `avatar-default` entry. An `image` has no contrast requirement. |

## Behavior

- Fallback: if `image` is missing or fails to load, `initials` is shown; if `name` is missing, `fallback-icon` is shown. The avatar never shows a broken image icon, and its size never changes during loading.
- Initials come from `name` only; they are never typed by hand.
- Stacked or grouped avatars (an overlapping row with a "+3" counter) are not part of this spec.

## Do and don't

| Do | Don't |
|---|---|
| Give the avatar the name of the person: "Ada Lovelace" | Name it "avatar" or leave an informative avatar unnamed |
| Leave `label` empty when the name is written next to it | Announce the same name twice |
| Let the fallback chain run: image, initials, icon | Show a broken image |
| Wrap a clickable avatar in a button or a link | Make the avatar itself the control |
| Use a badge for a count on an avatar | Draw a counter inside the avatar |

## Out of scope

Square or rounded avatars, avatar groups, presence or status indicators, upload or edit overlays, colored fills chosen from the name, animations, dark mode, and avatars on colored or image backgrounds (contrast is checked only against `{colors.surface}`) are not covered by this spec.
