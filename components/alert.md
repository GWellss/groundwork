# Alert

An alert is a message that stays in the page and tells the user something about the state of the page or of a task: information, a success, a warning, an error. This spec is theme independent: every visual value is a token reference to the DESIGN.md theme.

## At a glance

| Aspect | Summary |
|---|---|
| Parts | `container`, `icon`, `title`, `message`, `action`, `close-button` |
| Configurations | message only; with title; with action; with close button; any combination |
| Variants | `info`, `success`, `warning`, `danger` (severity) |
| Layouts | `inline` (in the content), `banner` (full width, top of the page) |
| Sizes | none; one size, padding and gaps from spacing tokens |
| Interactive states | none for the alert itself; `action` and `close-button` have `enabled`, `hover`, `focus`, `pressed` |
| State properties | none |
| Elevation | `level-0` |

## Purpose

- Use an alert for a message the user must be able to read at their own pace and that stays until it is no longer true or until the user dismisses it: a form-level error summary, a service notice, a warning before a risky step, a success that explains what comes next.
- Use `inline` when the message belongs to a part of the page, and `banner` when it concerns the whole page or the whole product (maintenance, an expired session, an offline state).
- Use a toast for a brief confirmation that needs no reading and no answer (see `components/toast.md`). A message the user must not miss is an alert, not a toast.
- Use a dialog when the user must answer before going on (see `components/dialog.md`).
- Use the error message of a field for a problem with one field (see `components/text-field.md`); an alert may summarize several of them.
- Do not use an alert for decoration, for marketing, or for a message that is always there: it loses its meaning.
- Do not stack many alerts: one or two per area. A long list of problems is a list in the page, with one alert on top.

## Anatomy

### Parts

| Part | Role | Required | Notes |
|---|---|---|---|
| `container` | The tonal panel; carries fill, border, radius | yes | Always present |
| `icon` | Glyph of the severity | yes | Never omitted: it carries the severity beside the color |
| `title` | Short heading of the message | no | One line, a few words |
| `message` | The text | yes | Plain text, no link inside (use `action`) |
| `action` | One action about the message | no | A link (navigates) or a button (acts); one only |
| `close-button` | Dismisses the alert | no | A button with the library close icon, at the end of the first row |

### Configurations

| Configuration | Parts | Status |
|---|---|---|
| message-only | `icon`, `message` | allowed |
| titled | `icon`, `title`, `message` | allowed |
| with-action | `action` with any of the above | allowed |
| with-close | `close-button` with any of the above | allowed |
| no-icon | no `icon` | forbidden |
| no-message | no `message` | out-of-scope |
| two-actions | two `action` parts | out-of-scope |
| link-in-message | a link inside `message` | out-of-scope |

Combination rules:

- An alert with no `icon` is `forbidden`: the icon carries the severity besides the color (WCAG 1.4.1).
- `message` states what is happening and, when it can, what to do. The `title` must not repeat it.
- `action` is a single, optional way to go on ("Review", "Try again", "Sign in"). Two choices are a dialog.
- `action` is rendered as a link when it navigates and as a button when it acts; both look the same here (see Token mapping).
- A `banner` has at most one per page, above the page content.

## Properties

| Property | Values | Default | Description |
|---|---|---|---|
| `severity` | `info`, `success`, `warning`, `danger` | `info` | Meaning and color group |
| `layout` | `inline`, `banner` | `inline` | In the content, or full width at the top of the page |
| `title` | text | none | Heading of the alert |
| `message` | text | none, required | The text |
| `action` | label and destination or handler | none | The single action |
| `closable` | `true`, `false` | `false` | Shows `close-button` |

## Variants

| Variant | Meaning | Tone | Icon glyph |
|---|---|---|---|
| `info` | Neutral information, a tip | brand tonal | the library information glyph |
| `success` | A task is done, a state is good | success tonal | the library check-in-circle glyph |
| `warning` | Something may go wrong, attention needed soon | warning tonal | the library warning glyph |
| `danger` | Something failed or blocks the user | danger tonal | the library error glyph |

`info` reuses the brand tonal container (the same colors as the `tonal` button), so it adds no color. `closable` is off by default: an alert that tells the user what is true should not vanish without their will.

## Sizes

### Decision

The alert has no named sizes. `inline` and `banner` are one component with two layouts, not two components: the parts, the tokens and the behavior are the same, only the container geometry changes. Padding, gaps, and the size of the icon reuse spacing tokens, so density applies.

### Size table

| Dimension | Token |
|---|---|
| `padding` | `{spacing.md}` |
| `padding-inline`, `banner` | `{spacing.xl}` |
| `icon-title-gap` | `{spacing.sm}` |
| `title-message-gap` | `{spacing.xs}` |
| `message-action-gap` | `{spacing.sm}` |
| `icon-size` | `{spacing.icon-md}` |
| `title-typography` | `{typography.label-lg}` |
| `message-typography` | `{typography.label-md}` |
| `action-typography` | `{typography.label-md}` |
| `control-size` | `{spacing.control-xs}` |
| `radius`, `inline` | `{rounded.overlay}` |

Geometry rules:

- `inline`: the container fills the width of its parent. Its radius is `radius`, and the border is drawn on every side. It never overlays other content.
- `banner`: the container fills the full width of the page, has no radius, and the border is drawn on its bottom edge only. It sits in the page flow, above the content; it is not sticky.
- `padding` is measured inside the border, which is reserved (`{spacing.border-width}`).
- `icon` is at the start, aligned with the first line of the text. `title` and `message` form one column that takes the free width. `message` wraps; it is never truncated.
- `action` sits under `message`, aligned to the start of the column. In `banner`, it sits at the end of the row, before `close-button`, and moves under `message` when the width does not allow it.
- `close-button` sits at the end of the first row, level with `title` (or the first line of `message`).
- `action` and `close-button` have a square or rectangular hit shape of height `control-size`, a radius of `{rounded.control}`, and inline padding `{spacing.sm}` for `action`. Their focus ring is drawn outside, inside the padding of the alert, which is larger than the ring and its offset.

## States

### Interactive states

None for the alert itself. `action` and `close-button` are controls:

| State | Trigger | Visual effect |
|---|---|---|
| `enabled` | Default | No fill, content color of the severity |
| `hover` | Pointer over the control | Hover fill of the severity |
| `focus` | Keyboard focus (focus visible) | Adds the focus ring; never changes fill or content |
| `pressed` | Pointer down or key held | Pressed fill of the severity |

`focus` combines with `hover` and `pressed`.

### State properties

None: an alert has no `disabled` or `loading` property.

## Token mapping

Cell vocabulary: a token reference, or `none` (no fill, no border). The content covers `icon`, `title`, `message`, and the label or glyph of the controls. The four severities have the same structure; only the tokens change.

### `info`

| Part or state | Fill | Content | Border |
|---|---|---|---|
| `container` | `{colors.primary-container}` | `{colors.on-primary-container}` | `{colors.primary-container-pressed}` |
| `action`, `close-button`, `enabled` | `none` | `{colors.on-primary-container}` | `none` |
| `action`, `close-button`, `hover` | `{colors.primary-container-hover}` | `{colors.on-primary-container}` | `none` |
| `action`, `close-button`, `pressed` | `{colors.primary-container-pressed}` | `{colors.on-primary-container}` | `none` |

### `success`

| Part or state | Fill | Content | Border |
|---|---|---|---|
| `container` | `{colors.success-container}` | `{colors.on-success-container}` | `{colors.success-container-pressed}` |
| `action`, `close-button`, `enabled` | `none` | `{colors.on-success-container}` | `none` |
| `action`, `close-button`, `hover` | `{colors.success-container-hover}` | `{colors.on-success-container}` | `none` |
| `action`, `close-button`, `pressed` | `{colors.success-container-pressed}` | `{colors.on-success-container}` | `none` |

### `warning`

| Part or state | Fill | Content | Border |
|---|---|---|---|
| `container` | `{colors.warning-container}` | `{colors.on-warning-container}` | `{colors.warning-container-pressed}` |
| `action`, `close-button`, `enabled` | `none` | `{colors.on-warning-container}` | `none` |
| `action`, `close-button`, `hover` | `{colors.warning-container-hover}` | `{colors.on-warning-container}` | `none` |
| `action`, `close-button`, `pressed` | `{colors.warning-container-pressed}` | `{colors.on-warning-container}` | `none` |

### `danger`

| Part or state | Fill | Content | Border |
|---|---|---|---|
| `container` | `{colors.danger-container}` | `{colors.on-danger-container}` | `{colors.danger-container-pressed}` |
| `action`, `close-button`, `enabled` | `none` | `{colors.on-danger-container}` | `none` |
| `action`, `close-button`, `hover` | `{colors.danger-container-hover}` | `{colors.on-danger-container}` | `none` |
| `action`, `close-button`, `pressed` | `{colors.danger-container-pressed}` | `{colors.on-danger-container}` | `none` |

Border width is `{spacing.border-width}`. The border carries no information, so it needs no 3:1 check.

### Control content and focus ring

- `action` and `close-button` are not `button` or `link` components: they are parts of the alert, so they take the colors above and not those of the button spec, whose `primary` content is checked on the surface only. `action` is underlined (the label is in the same color as the text, so the underline tells it apart).
- Focus ring, all severities:

| Property | Token |
|---|---|
| Color | `{colors.focus-ring}` |
| Width | `{spacing.focus-ring-width}` |
| Offset | `{spacing.focus-ring-offset}` |

The ring is the one `{colors.focus-ring}` of the whole kit, not a color of the alert. The theme script checks it at 3:1 on the container and on the hover and pressed fills of every severity (WCAG 1.4.11), as on the surface and the neutral fills, and picks a darker brand step for the single global ring when one of them fails. The alert declares no ring color of its own.

### Elevation

The alert is at `level-0` in every state: it is part of the page flow.

## Token contract

The theme must define every token below. The alert adds the tonal containers of `danger`, `success` and `warning`: twelve semantic colors that follow the model of `primary-container`. The `info` severity adds nothing.

### Colors

| Token | Role |
|---|---|
| `colors.primary-container`, `-hover`, `-pressed` | `info` container; hover and pressed fills of its controls |
| `colors.on-primary-container` | `info` content |
| `colors.success-container`, `-hover`, `-pressed` | `success` container and control fills. Default: success steps `50`, `100`, `200` |
| `colors.on-success-container` | `success` content: first step from `700` to `900` reaching 4.5:1 on all three fills |
| `colors.warning-container`, `-hover`, `-pressed` | `warning` container and control fills. Default: warning steps `50`, `100`, `200` |
| `colors.on-warning-container` | `warning` content, same search |
| `colors.danger-container`, `-hover`, `-pressed` | `danger` container and control fills. Default: danger steps `50`, `100`, `200` |
| `colors.on-danger-container` | `danger` content, same search |
| `colors.focus-ring` | Focus ring of `action` and `close-button`, shared with the rest of the kit; the script checks it at 3:1 on the nine tonal fills above and on `primary-container*` |

### Typography

| Token | Role |
|---|---|
| `typography.label-lg` | `title` |
| `typography.label-md` | `message`, `action` |

### Rounded

| Token | Role |
|---|---|
| `rounded.overlay` | `inline` container radius |
| `rounded.control` | `action` and `close-button` radius |

### Spacing

| Token | Role |
|---|---|
| `spacing.xs` | Title to message gap |
| `spacing.sm` | Icon to text gap; message to action gap; `action` padding inline |
| `spacing.md` | Container padding |
| `spacing.xl` | `banner` padding inline |
| `spacing.icon-md` | Icon size |
| `spacing.control-xs` | Height of `action` and `close-button` |
| `spacing.border-width` | Border width |
| `spacing.focus-ring-width` | Focus ring width |
| `spacing.focus-ring-offset` | Gap between control and focus ring |

### Components entries (contrast checks)

One entry per severity and per `enabled`, `hover`, `pressed` fill, using only the standard `backgroundColor` and `textColor` properties. The enabled entry is the container itself (its text and icon); the hover and pressed entries are the fills of `action` and `close-button`. The `info` severity declares nothing: it reuses `button-tonal`, `button-tonal-hover` and `button-tonal-pressed`, which are the same pairs. Every pair follows the contrast pair rule of `docs/conventions.md`: step `50`, `100`, `200` backgrounds, content step `700` to `900` of the same scale.

| Entry | backgroundColor | textColor |
|---|---|---|
| `alert-success` | `{colors.success-container}` | `{colors.on-success-container}` |
| `alert-success-hover` | `{colors.success-container-hover}` | `{colors.on-success-container}` |
| `alert-success-pressed` | `{colors.success-container-pressed}` | `{colors.on-success-container}` |
| `alert-warning` | `{colors.warning-container}` | `{colors.on-warning-container}` |
| `alert-warning-hover` | `{colors.warning-container-hover}` | `{colors.on-warning-container}` |
| `alert-warning-pressed` | `{colors.warning-container-pressed}` | `{colors.on-warning-container}` |
| `alert-danger` | `{colors.danger-container}` | `{colors.on-danger-container}` |
| `alert-danger-hover` | `{colors.danger-container-hover}` | `{colors.on-danger-container}` |
| `alert-danger-pressed` | `{colors.danger-container-pressed}` | `{colors.on-danger-container}` |

### Non-token requirement

- Icon style and library come from the `## Icons` section of DESIGN.md. `icon` shows the glyph of its severity; `close-button` shows the library close icon.
- The alert has no elevation (`level-0`).

## Accessibility

| Topic | Requirement |
|---|---|
| Not by color alone | `icon` carries the severity beside the color (WCAG 1.4.1), and the text says what is wrong. `icon` is not decorative: it has an image role and an accessible name that states the severity ("Information", "Success", "Warning", "Error"), given by the project in its language. |
| Role, urgent | `danger`, inserted into the page after it loaded: `role="alert"` (assertive), because the user must know now (a failed save, a blocking error). |
| Role, not urgent | `info`, `success`, `warning`, inserted after load: `role="status"` (polite), read when the user is idle. |
| Role, present at load | An alert rendered with the page takes no live role: it is read in reading order, and a live role there would be announced twice or not at all. |
| `banner` and landmarks | A `banner` layout never takes the `banner` landmark role (that is the page header) and is not a landmark. |
| Updates | Changing `message` of a live alert is announced by its role; the project does not change it more often than the user can follow. |
| Focus | The alert itself is not focusable and never takes focus when it appears. `action` and `close-button` are in the tab order, after the text, at the place of the alert in reading order. |
| Keyboard | `Enter` and `Space` activate `action` (a link activates on `Enter` only) and `close-button`. |
| Accessible name | `close-button` has a label ("Dismiss"), given by the project. `action` is named by its label. |
| Target size | `action` and `close-button` are at least `{spacing.control-xs}` high, and at least 24 by 24 CSS pixels (WCAG 2.2 criterion 2.5.8). |
| Contrast | Text, icon and control content reach 4.5:1 against the fill of their state. Delegated to the DESIGN.md lint through the `alert-*` entries and, for `info`, the `button-tonal*` entries. |

## Behavior

- Dismissing: `close-button` removes the alert from the layout; the content below moves up. Focus goes to the next focusable element in reading order, or, when there is none, to the heading of the page region, never to the top of the page and never lost.
- An alert stays until the project removes it (the condition is no longer true) or the user dismisses it. It never disappears by itself: use a toast for a message that does.
- Stacking: alerts of one area are separated by `{spacing.md}`. At most one `banner` is shown at a time.
- The project decides whether a dismissed alert returns on the next visit.
- Transitions: appearance and removal, if any, are the project's choice and are removed under reduced motion (see Motion in `docs/conventions.md`).

## Do and don't

| Do | Don't |
|---|---|
| Say what happened and what to do in the `message` | Write "Error" alone |
| Keep the `icon`: it carries the severity beside the color | Remove the icon because the color is clear |
| Use `danger` for a failure, `warning` for a risk, `info` for the rest | Use `danger` for plain information |
| Use one `action` at most, with a clear label | Put two buttons or a link inside the message |
| Put a `banner` above the page content, one at a time | Stack several banners, or make the banner sticky |
| Use a toast for a brief confirmation | Let an alert disappear on a timer |
| Use the field error for one field | Use an alert for a single invalid field |

## Out of scope

Alerts on a dark or tinted background, a sticky or floating banner, an alert with several actions or a form, links inside the message, light and outlined variants, a solid (filled) alert, a collapsible alert, a title-only alert, a countdown or auto-dismiss, a `banner` that follows the scroll, animations, and dark mode are not covered by this spec. The `info` severity uses the brand color: a theme whose brand hue is close to the danger or warning hue may blur the two, so the user checks it after generation.
