---
name: "Design System (dark)"
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
  green-50: "#ECF9EE"
  green-100: "#D5F0DA"
  green-200: "#B5E2BD"
  green-300: "#89CD98"
  green-400: "#60B475"
  green-500: "#3B9D58"
  green-600: "#15803D"
  green-700: "#006B2E"
  green-800: "#005122"
  green-900: "#003915"
  orange-50: "#FFF2EC"
  orange-100: "#FFE1D1"
  orange-200: "#FDC7AB"
  orange-300: "#F4A57B"
  orange-400: "#DF8450"
  orange-500: "#CA6728"
  orange-600: "#B45309"
  orange-700: "#8C3E00"
  orange-800: "#6C2E00"
  orange-900: "#4C1E00"
  neutral-50: "#FCFCFC"
  neutral-100: "#E8E8E8"
  neutral-200: "#D4D4D4"
  neutral-300: "#BABABA"
  neutral-400: "#9E9E9E"
  neutral-500: "#868686"
  neutral-600: "#6F6F6F"
  neutral-700: "#585858"
  neutral-800: "#424242"
  neutral-900: "#030303"
  surface: "#0F1216"
  primary: "{colors.blue-400}"
  on-primary: "{colors.blue-900}"
  primary-hover: "{colors.blue-300}"
  primary-pressed: "{colors.blue-200}"
  primary-container: "{colors.blue-900}"
  on-primary-container: "{colors.blue-200}"
  primary-container-hover: "{colors.blue-800}"
  primary-container-pressed: "{colors.blue-700}"
  primary-subtle-hover: "{colors.blue-900}"
  primary-subtle-pressed: "{colors.blue-800}"
  on-primary-subtle: "{colors.blue-200}"
  danger: "{colors.red-300}"
  on-danger: "{colors.red-900}"
  success: "{colors.green-300}"
  on-success: "{colors.green-900}"
  warning: "{colors.orange-300}"
  on-warning: "{colors.orange-900}"
  danger-hover: "{colors.red-200}"
  danger-pressed: "{colors.red-100}"
  danger-container: "{colors.red-900}"
  danger-container-hover: "{colors.red-800}"
  danger-container-pressed: "{colors.red-700}"
  on-danger-container: "{colors.red-200}"
  success-container: "{colors.green-900}"
  success-container-hover: "{colors.green-800}"
  success-container-pressed: "{colors.green-700}"
  on-success-container: "{colors.green-200}"
  warning-container: "{colors.orange-900}"
  warning-container-hover: "{colors.orange-800}"
  warning-container-pressed: "{colors.orange-700}"
  on-warning-container: "{colors.orange-200}"
  outline: "{colors.neutral-500}"
  disabled-container: "{colors.neutral-800}"
  on-disabled: "{colors.neutral-500}"
  focus-ring: "{colors.blue-300}"
  on-surface: "{colors.neutral-200}"
  on-surface-muted: "{colors.neutral-400}"
  neutral-subtle-hover: "{colors.neutral-800}"
  neutral-subtle-pressed: "{colors.neutral-700}"
  inverse-surface: "{colors.neutral-100}"
  on-inverse-surface: "{colors.neutral-900}"
  link-visited: "#859FD0"
  surface-level-1: "#15171C"
  surface-level-2: "#1A1D22"
  surface-level-3: "#202328"
  surface-level-4: "#26292E"
  surface-level-5: "#2C2F34"
  scrim: "{colors.neutral-900}"
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
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary}"
  button-outlined-hover:
    backgroundColor: "{colors.primary-subtle-hover}"
    textColor: "{colors.on-primary-subtle}"
  button-outlined-pressed:
    backgroundColor: "{colors.primary-subtle-pressed}"
    textColor: "{colors.on-primary-subtle}"
  button-text:
    backgroundColor: "{colors.surface-level-5}"
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
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  chip-default:
    backgroundColor: "{colors.surface-level-5}"
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
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  chip-remove-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  chip-remove-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  chip-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  tooltip-plain:
    backgroundColor: "{colors.inverse-surface}"
    textColor: "{colors.on-inverse-surface}"
  link:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary}"
  link-hover:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary-hover}"
  link-pressed:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary-pressed}"
  link-visited:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.link-visited}"
  link-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  badge-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  badge-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-danger}"
  badge-success:
    backgroundColor: "{colors.success}"
    textColor: "{colors.on-success}"
  badge-warning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.on-warning}"
  badge-neutral:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  avatar-default:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  progress-primary:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary}"
  progress-danger:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.danger}"
  text-field:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  text-field-muted:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface-muted}"
  text-field-error:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.danger}"
  text-field-read-only:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  text-field-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  search-field-clear:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  search-field-clear-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  search-field-clear-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  checkbox:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  checkbox-muted:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface-muted}"
  checkbox-error:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.danger}"
  checkbox-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  checkbox-selected:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  checkbox-selected-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  checkbox-selected-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
  radio-selected:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  radio-selected-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  radio-selected-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
  switch-on:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  switch-on-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  switch-on-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
  slider:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary}"
  slider-hover:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary-hover}"
  slider-pressed:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.primary-pressed}"
  tab:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface-muted}"
  tab-selected:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  tab-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  tab-selected-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  tab-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  tab-selected-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  tab-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  accordion:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  accordion-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  accordion-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  accordion-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  menu-item:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  menu-item-danger:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.danger}"
  menu-item-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  menu-item-danger-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.danger-hover}"
  menu-item-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  menu-item-danger-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.danger-pressed}"
  menu-muted:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface-muted}"
  menu-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  popover:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  alert-danger:
    backgroundColor: "{colors.danger-container}"
    textColor: "{colors.on-danger-container}"
  alert-danger-hover:
    backgroundColor: "{colors.danger-container-hover}"
    textColor: "{colors.on-danger-container}"
  alert-danger-pressed:
    backgroundColor: "{colors.danger-container-pressed}"
    textColor: "{colors.on-danger-container}"
  alert-success:
    backgroundColor: "{colors.success-container}"
    textColor: "{colors.on-success-container}"
  alert-success-hover:
    backgroundColor: "{colors.success-container-hover}"
    textColor: "{colors.on-success-container}"
  alert-success-pressed:
    backgroundColor: "{colors.success-container-pressed}"
    textColor: "{colors.on-success-container}"
  alert-warning:
    backgroundColor: "{colors.warning-container}"
    textColor: "{colors.on-warning-container}"
  alert-warning-hover:
    backgroundColor: "{colors.warning-container-hover}"
    textColor: "{colors.on-warning-container}"
  alert-warning-pressed:
    backgroundColor: "{colors.warning-container-pressed}"
    textColor: "{colors.on-warning-container}"
  card:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  card-hover:
    backgroundColor: "{colors.neutral-subtle-hover}"
    textColor: "{colors.on-surface}"
  card-pressed:
    backgroundColor: "{colors.neutral-subtle-pressed}"
    textColor: "{colors.on-surface}"
  card-focus-ring:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.focus-ring}"
  dialog:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  toast:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.on-surface}"
  toast-success:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.success}"
  toast-danger:
    backgroundColor: "{colors.surface-level-5}"
    textColor: "{colors.danger}"
  text-on-level-1:
    backgroundColor: "{colors.surface-level-1}"
    textColor: "{colors.on-surface}"
  text-on-level-2:
    backgroundColor: "{colors.surface-level-2}"
    textColor: "{colors.on-surface}"
  text-on-level-3:
    backgroundColor: "{colors.surface-level-3}"
    textColor: "{colors.on-surface}"
  text-on-level-4:
    backgroundColor: "{colors.surface-level-4}"
    textColor: "{colors.on-surface}"
---

## Overview

Dark mode of Design System, applied under `data-theme="dark"`. It has the same role names as DESIGN.md and other values; spacing, rounded and icons stay in DESIGN.md; typography is repeated because the lint warns on a file without it. Each pair of `components` is checked against `surface-level-5`, the lightest surface.

## Colors

The five primitive scales are the same as in DESIGN.md, except `neutral-900`, darker here so that `scrim` (`neutral-900`, as in DESIGN.md) dims the dark page; each role takes the step that suits the dark mode. Surfaces are gray with a weak, constant tint of the theme color: `surface` is #0F1216 and each level is a notch lighter, up to `surface-level-5` (#2C2F34). The accent `default` step is the first step from 300 to 600 searched from the lightest, reaching 4.5:1 on `surface-level-5` and against its content: here `blue-400` (brand), `red-300` (danger), `green-300` (success) and `orange-300` (warning). Hover is `default` minus 1 step and pressed is `default` minus 2 steps, stopped at 50: each state is lighter than the previous one. Content on an accent fill (`on-primary`, `on-danger`, `on-success`, `on-warning`) is step 900 of the same scale. Tonal containers use steps 900, 800 and 700 (enabled, hover, pressed), with content searched among steps 200, 100 and 50. Text is `on-surface`, a neutral step 200, 100 or 50; `on-surface-muted` and `outline` (3:1) are checked on `surface-level-5`. The tooltip is inverted: `inverse-surface` is a light neutral step with a dark `on-inverse-surface`. `scrim` is the veil behind the dialog.

Brand note: brand #2563EB: proposed step blue-400 accepted.

## Elevation & Depth

This theme has no shadow in dark mode: each elevation level has its own surface, a notch lighter than the previous level.

| Level | Surface role |
|---|---|
| `level-0` | `surface` |
| `level-1` | `surface-level-1` |
| `level-2` | `surface-level-2` |
| `level-3` | `surface-level-3` |
| `level-4` | `surface-level-4` |
| `level-5` | `surface-level-5` |

## Components

The `components` entries are the same as in DESIGN.md, with `surface-level-5` in place of `surface` as background, so the lint checks the most unfavorable surface; four `text-on-level-<n>` entries add the text pair on `surface-level-1` to `surface-level-4`. Disabled pairs are exempt (WCAG 1.4.3) and are not declared.
