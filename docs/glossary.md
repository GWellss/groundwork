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
