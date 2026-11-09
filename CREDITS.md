# Credits

Groundwork is an independent project. It is not affiliated with, sponsored by, or endorsed by any project, company, or standards body listed below. Names are used only to say what a decision was inspired by or checked against. No code, text, or asset of these projects is copied into this repository.

## Format and tooling

| Source | What Groundwork takes from it | Link |
|---|---|---|
| Google DESIGN.md (`@google/design.md`, Apache-2.0) | The theme file format, its lint (including contrast), and the pinned CLI version 0.4.0. Groundwork complements it and never modifies it. | https://github.com/google-labs-code/design.md |
| WebAIM Contrast Checker | Suggested to users as an online contrast check when no script is available. | https://webaim.org/resources/contrastchecker/ |
| OKLCH color model | Method used to build color scales and dark surfaces (perceptual lightness, chroma, hue). | none in the repository |

## Accessibility references

| Source | What Groundwork takes from it | Link |
|---|---|---|
| WCAG 2.2 (W3C) | Contrast thresholds (1.4.3, 1.4.11), use of color (1.4.1), content on hover or focus (1.4.13), time limits (2.2.1), animation (2.2.2), status messages (4.1.3). | https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html and https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html |
| WAI-ARIA Authoring Practices (APG) | Keyboard and role patterns for accordion, dialog, menu, select-only combobox, and tabs. | none in the repository |
| Adrian Roselli, "Defining toast messages" | Reasoning on toast behavior and announcements. | https://adrianroselli.com/2020/01/defining-toast-messages.html |

## Design systems and design references

Groundwork compares its decisions with these systems in `docs/rationale/` and `docs/conventions.md`. Where a decision is aligned with one of them, the rationale file says so.

| Source | What Groundwork takes from it | Link |
|---|---|---|
| Material Design 3 (Google) | Elevation scale of six levels, naming of button emphasis variants, several component behaviors, and the shadow style of the default elevation values. Material Symbols is also the default icon library suggested by the questionnaire. | none in the repository |
| Radix (Radix UI and Radix Themes) | Tooltip delays and placement defaults, menu closing behavior, and the step-by-step state model for dark mode. | none in the repository |
| Adobe React Spectrum and React Aria | Component property naming, tooltip sizes and offsets, and toast behavior (pause on hover and focus). | https://react-aria.adobe.com/Toast |
| IBM Carbon Design System | Notification and tooltip behavior, and the neutral dark surface option. | https://carbondesignsystem.com/components/notification/usage/ |
| Atlassian Design System | The neutral dark surface option. | none in the repository |
| Smart Interface Design Patterns | Definition of the badge family (count, dot, status text). | none in the repository |
| Lucide | Named as an alternative icon library in the questionnaire. | none in the repository |

## Icon libraries

Groundwork ships no icon files. Projects that use an icon library, for example Material Symbols (Apache-2.0), must respect its license. See `docs/implementation.md`.
