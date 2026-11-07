# Menu rationale

For human contributors: why the spec is the way it is. Agents do not need this file.

| Decision | Reason |
|---|---|
| Floating surface defined once in `docs/conventions.md` | Menu, select list, popover and tooltip share placement, flipping, offset, radius, elevation, and dismissal; stating them four times would let them drift |
| Fill is `{colors.surface}`, not a new "container" color | A new surface color would force a new muted-text rule and new contrast pairs. The surface keeps `on-surface-muted` valid and adds no token; the border and the `level-2` shadow separate it from the page |
| Quiet border `neutral-subtle-pressed` | The shadow can be lost (forced colors, retouched theme); a hairline keeps the edge. It carries no information, so no 3:1 check is needed |
| Elevation `level-2` | The existing role of `level-2` is an overlay tied to a trigger; Material 3 menus sit at level 2. The words "shown for a short time" were dropped from that role because a menu stays open as long as the user needs |
| Two new spacing tokens, `menu-min-width` and `floating-max-width` | Widths depend on font size and density, which are theme choices. One maximum serves menu, select list, and popover |
| Roles `menu`, `menuitem`, `menuitemcheckbox`, `menuitemradio` | The WAI-ARIA menu pattern; the select uses `listbox` instead because it picks a value rather than running a command |
| Roving focus, `Escape` returns to the trigger, `Tab` closes | WAI-ARIA menu button pattern |
| Disabled items stay reachable | WAI-ARIA recommends it so that a screen reader user learns the command exists; `aria-disabled` rather than the native attribute |
| Arrow keys wrap, letter jumps to the next match | WAI-ARIA example behavior; `Home` and `End` cover the ends |
| Pointer hover does not move keyboard focus | One rule for the ring (focus visible only); no hidden focus jumps under a resting pointer |
| Danger item darkens from `danger` to `danger-hover` to `danger-pressed` | `danger` reaches 4.5:1 on the surface only; on the grayed hover fills a lighter step may fall below 4.5:1. The darker steps of the State colors rule always pass there. The alternatives were a red or solid fill on hover (the focus ring would then fail 3:1 on it) or new danger-tinted tokens |
| Convention extended for that pairing only | `danger-hover` serves `neutral-subtle-hover` and `danger-pressed` serves `neutral-subtle-pressed`; the theme script refuses any other pairing |
| Shortcut quiet at rest, `on-surface` on hover | `on-surface-muted` is allowed on the surface only; the same pattern as the unselected tab |
| Activation closes the menu, checkable items included | Predictable; Radix and Material 3 close by default. Keeping a menu open is an explicit project choice |
| Labels wrap, never truncated | The kit rule for text; a truncated command is an unsafe command |
| No submenu | A submenu needs a pointer-direction safety area (so moving to it does not close it) and left and right keys; that is not simple, so it is left out |
| `dot` and `check-icon` as in radio and checkbox | Same marks as the controls users already know, without a new glyph |
| Icon with a checkable mark `out-of-scope`, empty menu and interactive content `forbidden` | Two leading elements would break the shared leading space of the items. The `menu` role needs items, and the items are its only focus targets: a control inside the container is not reachable as a menu item |
