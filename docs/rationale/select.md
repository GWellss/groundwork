# Select rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Native `select` is the default | The platform gives a picker on touch screens, the whole keyboard, type-ahead, and screen reader announcements for free; a custom list must rebuild all of it. The closed field can still follow the tokens. The custom listbox is for options with icons or a themed list |
| Closed field reuses the text field | Same label, help, error, sizes, border, and ring; the spec states only the differences, so the two cannot drift |
| Role `combobox` (select-only) with a `listbox`, never `menu` | A select sets a value, a menu runs commands; assistive technologies announce them differently. The select-only combobox is the WAI-ARIA pattern for a custom select, and keeps focus on the field with `aria-activedescendant` |
| Option rows reuse the menu item | One row size, one hover and pressed fill, one ring inside; no new entry or token |
| Selected option shown by a `check-icon` at the end, space reserved | WCAG 1.4.1: not by color alone. At the end, labels stay aligned with the field text; reserved space keeps rows from jumping |
| Selected option has no fill | A fill would add a state to the contrast matrix; the mark and `aria-selected` are enough |
| No `read-only`, no clear | The native select has no read-only; clearing is an explicit "None" option, which also reads aloud |
| `Tab` chooses the active option | WAI-ARIA select-only example |
| Option labels wrap, the field value truncates | The field is one line high like the text field; the list can grow, so the full text stays readable |
| Multiple selection and filterable select left out | Multiple selection needs a list that stays open, a summary in the field, and checkable rows; a combobox needs filtering and live result announcements. Neither is simple. The listbox and options are written so a later combobox spec can reuse them |
| Suggestions of the search field attach to the listbox | A search field with suggestions is a combobox: a text input driving this list. That is why the search field spec now points here |
| No new token or entry | Everything is reused from the text field and the menu |
