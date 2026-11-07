# Glossary

**Anatomy**: the list of parts that make up a component. Example: a button has a container, a label, and optional leading and trailing icons.

**Part**: one named element of an anatomy. Example: `label`.

**Slot**: a part where content can be inserted. Example: the `leading-icon` slot of a button.

**Variant**: a visual or semantic flavor of a component. Example: `primary`, `secondary`, `ghost`.

**Size**: a named dimension set, declared per component. Example: a button may have five sizes, a tooltip only a maximum width.

**State**: a condition of a component driven by interaction or data. Example: `hover`, `focus`, `disabled`.

**Token**: a named design value. Example: `colors.primary`.

**Primitive token**: a raw value with no meaning attached. Example: a hex color or a pixel length.

**Semantic token**: a token named by its role, usually pointing to a primitive. Example: `colors.primary`.

**Palette scale**: an ordered set of primitive color steps from lightest to darkest. Example: `blue-50` to `blue-900`.

**Token reference**: a pointer to a token by path, written `{colors.primary}`.

**Theme**: the DESIGN.md file holding the token values of one design system: colors, typography, rounded, spacing.

**Questionnaire**: the list of questions an agent asks the user to fill the theme.

**Component spec**: the document describing a component independently of any theme: anatomy, sizes, variant by state matrix, accessibility, behavior.

**Floating surface**: a panel that opens next to a trigger and floats above the page. Example: a tooltip, a menu, a select list, a popover.

**Trigger**: the element that opens a floating surface. Example: the button of a menu.

**Overlay panel**: a panel that floats above the page without being placed by a trigger. Example: a dialog, a toast.

**Modal**: said of a panel that blocks the page behind it until it is closed. Example: a dialog.

**Scrim**: the veil drawn over the page behind a modal panel. Example: the dark layer behind a dialog.

**Tonal container**: a pale fill, steps 50 to 200 of a color scale, with dark content of the same scale. Example: the fill of an alert.

**Live region**: an area of the page whose changes assistive technologies announce. Example: the region that holds the toasts.

**Landmark**: a named region of the page that assistive technologies list and jump to. Example: the search landmark around a search field, or the "Notifications" region of the toasts.

**Container**: the part of a component that holds the other parts and carries its fill, border, radius, and elevation. Example: the `container` of a card. Not to be mixed with a tonal container, which is a fill.

**Host**: the element a count or dot badge is attached to. Example: the icon that carries an unread count.

**Status badge**: the text form of the badge, a short static text that states a status. It is never interactive. Example: "Paid". Not to be mixed with a chip.

**Focus ring**: the outline drawn around the element that holds keyboard focus. Example: the ring of a button.

**Elevation level**: a named step of the shadow scale, from `level-0` (flat) to `level-5`. Example: a menu is at `level-2`.

**Muted text**: the quieter text color `on-surface-muted`, allowed on the surface only, never on a grayed fill. Example: a placeholder.

**Grayed fill**: a neutral fill of step 100 or beyond, used for hover, pressed, and read-only. Example: the hover fill of a menu item.

**Contrast pair**: one background color and one content color declared together in `components`, checked at 4.5:1. Example: `button-filled`.

**Behavior constant**: a fixed value stated by a spec, such as a delay or a duration. It is not a theme token. Example: the 700 ms open delay of the tooltip.

**Reduced motion**: the user setting that asks the platform to limit animation. Essential motion is slowed, other transitions are removed. Example: the spinner turns slower, the accordion panel appears at once.

**Target size**: the minimum hit area of an interactive element, 24 by 24 CSS pixels. Example: the remove button of a chip.

**Configuration status**: the status of one configuration in a spec: `allowed`, `forbidden` (accessibility or invalid HTML), `avoid` (possible but discouraged), or `out-of-scope` (not specified yet). Example: a switch in a group is out of scope.
