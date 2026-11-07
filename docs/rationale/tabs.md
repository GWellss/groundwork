# Tabs rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Automatic activation by default | Arrows that also select match the radio group and the segmented control, and the most common panels are already on the page. Manual stays available when a panel is slow or has a side effect (WAI-ARIA allows both) |
| Distinguished from navigation | Tabs keep the user on the same page and the same URL; a label that leads to another page is a link, with link semantics, history, and open-in-new-tab |
| One look, underline | A single indicator (a bar) keeps the spec short; filled or pill tabs are a different component feel and can be added later |
| Selection shown by bar and darker label | WCAG 1.4.1: the bar is a shape cue; the label also changes from `on-surface-muted` to `on-surface` |
| `on-surface-muted` for the unselected label at rest | The tab sits on the surface at rest, the only place the muted text is allowed; once hover or pressed adds a fill, the label turns `on-surface`, as the Muted text rule requires |
| New `tab*` entries, none for the segmented control | The tab labels need the muted pair of their own. The segmented control has exactly the chip pairs, so it reuses them as radio reuses the checkbox ones |
| Indicator in `primary`, thickness `spacing.xs` | The brand `default` step is already 4.5:1 on the surface, above the 3:1 of non-text contrast; `xs` is the thinnest spacing token and follows density |
| Indicator space always reserved | Selecting a tab never moves content |
| Ring drawn inside the tab | A scrolling container clips anything outside its box |
| Overflow by scrolling, no wrap, no truncation | Two rows break the reading order of the selection; a truncated label may no longer tell the tabs apart |
| Badge in the flow | A badge anchored to a corner would overlap the padding and the next tab; in the flow it is read and laid out with the label. The badge spec now names this exception |
| `status` badge refused | It is a text, a competing label inside a label |
| Icon-only tabs refused | The visible label is the accessible name and the way to tell tabs apart; an icon alone fails users who do not know the icon |
| Hidden panels keep their state | Losing a form being filled when the user peeks at another tab is the most common complaint about tabs |
| Heights one step above the matching button | Tabs are a navigation-like target; the extra height holds the bar |
