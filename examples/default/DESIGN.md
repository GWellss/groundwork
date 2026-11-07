---
name: "Design System"
colors:
  blue-50: "#F0F5FF"
  blue-100: "#DCE8FF"
  blue-200: "#BED5FF"
  blue-300: "#96BAFF"
  blue-400: "#699BFF"
  blue-500: "#3F7DFF"
  blue-600: "#2563EB"
  blue-700: "#0946CD"
  blue-800: "#0032A4"
  blue-900: "#002177"
  red-50: "#FFF2F0"
  red-100: "#FFE0DB"
  red-200: "#FFC4BC"
  red-300: "#FF9B90"
  red-400: "#FF6459"
  red-500: "#EC3934"
  red-600: "#DC2626"
  red-700: "#A8000D"
  red-800: "#810008"
  red-900: "#5D0004"
  neutral-50: "#FCFCFC"
  neutral-100: "#E8E8E8"
  neutral-200: "#D4D4D4"
  neutral-300: "#BABABA"
  neutral-400: "#9E9E9E"
  neutral-500: "#868686"
  neutral-600: "#6F6F6F"
  neutral-700: "#585858"
  neutral-800: "#424242"
  neutral-900: "#2E2E2E"
  surface: "{colors.neutral-50}"
  primary: "{colors.blue-600}"
  on-primary: "#FFFFFF"
  primary-hover: "{colors.blue-800}"
  primary-pressed: "{colors.blue-900}"
  primary-container: "{colors.blue-50}"
  on-primary-container: "{colors.blue-700}"
  primary-container-hover: "{colors.blue-100}"
  primary-container-pressed: "{colors.blue-200}"
  primary-subtle-hover: "{colors.blue-50}"
  primary-subtle-pressed: "{colors.blue-100}"
  on-primary-subtle: "{colors.blue-700}"
  danger: "{colors.red-600}"
  on-danger: "#FFFFFF"
  danger-hover: "{colors.red-800}"
  danger-pressed: "{colors.red-900}"
  outline: "{colors.neutral-500}"
  disabled-container: "{colors.neutral-100}"
  on-disabled: "{colors.neutral-500}"
  focus-ring: "{colors.blue-600}"
  on-surface: "{colors.neutral-700}"
  neutral-subtle-hover: "{colors.neutral-100}"
  neutral-subtle-pressed: "{colors.neutral-200}"
  inverse-surface: "{colors.neutral-900}"
  on-inverse-surface: "#FFFFFF"
  link-visited: "#7D56B8"
typography:
  label-sm:
    fontFamily: "system-ui"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 15px
    letterSpacing: 0px
  label-md:
    fontFamily: "system-ui"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 18px
    letterSpacing: 0px
  label-lg:
    fontFamily: "system-ui"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 20px
    letterSpacing: 0px
  label-xl:
    fontFamily: "system-ui"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 23px
    letterSpacing: 0px
rounded:
  control: 4px
  overlay: 4px
  avatar: 9999px
spacing:
  control-xs: 28px
  control-sm: 32px
  control-md: 40px
  control-lg: 48px
  control-xl: 56px
  icon-sm: 16px
  icon-md: 20px
  icon-lg: 24px
  icon-xl: 28px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 20px
  2xl: 24px
  tooltip-max-width: 240px
  border-width: 1px
  focus-ring-width: 2px
  focus-ring-offset: 2px
components:
  button-filled:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  button-filled-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  button-filled-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
  button-tonal:
    backgroundColor: "{colors.primary-container}"
    textColor: "{colors.on-primary-container}"
  button-tonal-hover:
    backgroundColor: "{colors.primary-container-hover}"
    textColor: "{colors.on-primary-container}"
  button-tonal-pressed:
    backgroundColor: "{colors.primary-container-pressed}"
    textColor: "{colors.on-primary-container}"
  button-outlined:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
  button-outlined-hover:
    backgroundColor: "{colors.primary-subtle-hover}"
    textColor: "{colors.on-primary-subtle}"
  button-outlined-pressed:
    backgroundColor: "{colors.primary-subtle-pressed}"
    textColor: "{colors.on-primary-subtle}"
  button-text:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
  button-text-hover:
    backgroundColor: "{colors.primary-subtle-hover}"
    textColor: "{colors.on-primary-subtle}"
  button-text-pressed:
    backgroundColor: "{colors.primary-subtle-pressed}"
    textColor: "{colors.on-primary-subtle}"
  button-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-danger}"
  button-danger-hover:
    backgroundColor: "{colors.danger-hover}"
    textColor: "{colors.on-danger}"
  button-danger-pressed:
    backgroundColor: "{colors.danger-pressed}"
    textColor: "{colors.on-danger}"
  button-focus-ring:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.focus-ring}"
  chip-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
  chip-default-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  chip-default-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  chip-selected:
    backgroundColor: "{colors.primary-container}"
    textColor: "{colors.on-primary-container}"
  chip-selected-hover:
    backgroundColor: "{colors.primary-container-hover}"
    textColor: "{colors.on-primary-container}"
  chip-selected-pressed:
    backgroundColor: "{colors.primary-container-pressed}"
    textColor: "{colors.on-primary-container}"
  chip-remove:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
  chip-remove-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  chip-remove-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  chip-focus-ring:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.focus-ring}"
  tooltip-plain:
    backgroundColor: "{colors.inverse-surface}"
    textColor: "{colors.on-inverse-surface}"
  link:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
  link-hover:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary-hover}"
  link-pressed:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary-pressed}"
  link-visited:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.link-visited}"
  link-focus-ring:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.focus-ring}"
  badge-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  badge-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-danger}"
  badge-neutral:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  avatar-default:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  progress-primary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
  progress-danger:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.danger}"
---

## Overview

Design System is a design system theme for buttons, chips, tooltips, dividers, links, badges, avatars, progress indicators and the components built on them. It uses a blue brand color (#2563EB), a red danger color (#DC2626), neutral grays, the system-ui font, soft corners and default density. Every value lives in this file; component specs only reference tokens.

## Colors

The theme has three primitive scales: `blue-50` to `blue-900` for the brand, `red-50` to `red-900` for destructive actions, and `neutral-50` to `neutral-900` for grays and backgrounds. State colors are semantic tokens that point to scale steps. The `default` step is the first step from 600 to 900 reaching 4.5:1 in the worse case between white and `{colors.surface}`; `hover` is `default` plus 2 steps and `pressed` is `default` plus 4 steps, stopped at 900. Here the brand `default` is `blue-600` and the danger `default` is `red-600`. Content on a filled brand or danger color (`on-primary`, `on-danger`) is always white. Tonal containers use steps 50, 100 and 200 (enabled, hover, pressed); `on-primary-container` and `on-primary-subtle` are the first step from 700 to 900 reaching 4.5:1 on every background they serve. The neutral chip uses `surface`, `neutral-subtle-hover` and `neutral-subtle-pressed` (neutral 50, 100, 200) with `on-surface`, found by the same search on the neutral scale. The tooltip is `inverse-surface` (neutral 900) with white `on-inverse-surface`. Links, badges, avatars and progress indicators reuse these tokens: the link moves its content color (`primary`, `primary-hover`, `primary-pressed`, then its own violet `link-visited` when visited) on the surface, the avatar and the neutral badge use `neutral-subtle-pressed` with `on-surface`, and the progress indicator is `primary` or `danger` on the surface. The divider has no text and declares no pair.

## Typography

The interface font is system-ui. Four label sizes serve the button sizes: sm 12px, md 14px, lg 16px, xl 18px. Weight is 500 and line height is 1.25 times the font size.

## Layout

Density is default. Control heights: xs 28px, sm 32px, md 40px, lg 48px, xl 56px. Spacing scale: xs 4px, sm 8px, md 12px, lg 16px, xl 20px, 2xl 24px. Borders are 1px and the focus ring is 2px wide with a 2px offset.

## Elevation & Depth

This theme defines no shadow token: the elevation scale is this table.

| Level | Role | Shadow |
|---|---|---|
| `level-0` | At rest, flat on the surface | none |
| `level-1` | At rest, slightly raised | `0 1px 2px rgba(0, 0, 0, 0.30), 0 1px 3px 1px rgba(0, 0, 0, 0.15)` |
| `level-2` | At rest, overlay tied to a trigger | `0 1px 2px rgba(0, 0, 0, 0.30), 0 2px 6px 2px rgba(0, 0, 0, 0.15)` |
| `level-3` | At rest, floating above scrolling content | `0 1px 3px rgba(0, 0, 0, 0.30), 0 4px 8px 3px rgba(0, 0, 0, 0.15)` |
| `level-4` | Interaction only, one step above a resting level | `0 2px 3px rgba(0, 0, 0, 0.30), 0 6px 10px 4px rgba(0, 0, 0, 0.15)` |
| `level-5` | Interaction only, highest | `0 4px 4px rgba(0, 0, 0, 0.30), 0 8px 12px 6px rgba(0, 0, 0, 0.15)` |

## Shapes

Corners are soft: `rounded.control` is 4px and `rounded.overlay` (tooltip) is 4px. `rounded.avatar` is 9999px (a circle) whatever the corners; edit it to change the avatar shape.

## Icons

Icon style: outlined. Icon library: Material Symbols.

## Components

The `components` entries declare one `backgroundColor` and `textColor` pair per button variant, per chip group and per `enabled`, `hover` and `pressed` state, plus the focus rings against the surface, the tooltip pair, the link states against the surface, the badge variants, the avatar and the progress indicators, so the lint checks contrast. Disabled pairs are exempt (WCAG 1.4.3) and are not declared. See the component specs in the kit: `button.md`, `chip.md`, `tooltip.md`, `divider.md`, `link.md`, `badge.md`, `avatar.md`, `progress.md`.

## Do's and Don'ts

- Do use semantic tokens such as `{colors.primary}`, never raw hex values.
- Do keep the state rule: `default`, then plus 2 steps for hover, then plus 4 steps for pressed.
- Don't add non-standard properties to `components`.
- Don't declare disabled pairs in `components`.
