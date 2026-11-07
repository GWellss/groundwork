# Segmented control rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Separate component, built on chip colors and radio behavior | The look is the chip's selected and neutral fills, the semantics are a radio group's; a third copy of the colors would drift, so the spec points to the chip and declares no entry |
| Distinguished by immediate effect and by "same content, other view" | Radio is a form answer sent on submit, tabs reveal different content, selectable chips are independent toggles. Each rule gives a one-line test to settle an ambiguous case |
| Two to five segments | Beyond five the labels no longer fit on a phone and the options are better in a select; a single segment is not a choice |
| Always one selected, no deselect | A view or a mode always has a current value; an empty state would show nothing selected and nothing applied |
| Multiple selection left out | The simple version is selectable chips, which already exist; a multi-select segmented control would need its own pressed semantics (checkbox group) for little gain |
| `check-icon` on the selected segment | WCAG 1.4.1: the two fills (brand 50 and surface) differ by hue only. Material 3 does the same |
| No icon-only segments | The check replaces the icon when selected, so an icon alone would vanish at the moment it should be clearest. Chip and tabs refuse icon-only for the same reason of meaning |
| Equal widths measured as if selected | A segment that grows by the check width when selected would shift its neighbors on every click |
| Native radios, arrows select | Same expectations and same code path as the radio group; a `radiogroup` role is supported by every assistive technology, unlike a custom toolbar |
| Ring drawn inside | The group clips its content to its rounded border, so an outside ring would be cut off |
| Border and dividers in `outline` | Already checked at 3:1 by the script; the divider reuses the existing `strong` variant, no new token |
| Sizes of the `s` and `m` buttons | The control is often next to a button; the same heights avoid a visible mismatch |
| Statuses of the "no" cases | A mix of icons, fewer than two segments, and no selection are `avoid`: they break the look or the meaning, not accessibility. Icon-only, more than five segments, and multiple selection are `out-of-scope`: the kit has no rule for them |
