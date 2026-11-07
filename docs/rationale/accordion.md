# Accordion rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| `multiple` mode by default | Closing a section the user opened, because they opened another, loses content they were reading and surprises screen reader users whose focus is in it. `single` is an explicit choice for long, unrelated sections |
| All sections may be closed in `single` mode | A user who closes the only open item expects it to close; forcing one open would make the header do nothing |
| Heading wrapping a native button | The heading puts every section in the page outline and in the headings list of assistive technologies; the button gives keyboard and `aria-expanded` for free (WAI-ARIA accordion pattern) |
| `heading-level` is a property, default 3 | The right level depends on the page; hard-coding one breaks the outline. 3 is the common case below a page title and a section heading |
| `role="region"` up to six items | The WAI-ARIA guidance: panels as landmarks help with a few items and flood the landmark list with many |
| Chevron turns, colors do not change | WCAG 1.4.1: the open state is shape and content, not color; the fill is left to hover and pressed, as everywhere else |
| `strong` dividers, none at the ends | The line is the only cue between two items, so it must reach 3:1; the divider spec forbids a first or last line |
| No leading icon, no badge in the header | Each adds an alignment and a color rule; the header is a title and a chevron, and can grow later |
| Single item allowed | It is the disclosure pattern, which needs no separate component |
| Panel typography left to the project | The kit's typography tokens are labels; a body font would be a new theme choice outside this lot |
| Transition removed, not slowed, under reduced motion | The kit slows only essential motion (loading, WCAG 2.2.2). An expansion carries no information beyond its end state, so removing it costs nothing. The rule now lives in `docs/conventions.md` (Motion) |
| Arrow keys between headers not defined | Optional in the WAI-ARIA pattern; Tab already reaches every header |
