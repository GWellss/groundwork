# Field notes: first trial on a real project

Feedback collected while using the kit on a real project. Notes are not decisions: each one is a finding to triage.

## Context

- Target: a desktop app (Tauri) written in TypeScript without a UI framework, with an existing design system to carry over.
- Path: the questionnaire was redone from scratch at the `terminal` tool level, then 8 components were coded (4 with a Groundwork spec, 4 specific to the app).

## Priority legend

- `bug`: the kit produces a wrong or misleading result.
- `gap`: something the kit does not cover and the implementer must work around.
- `nice-to-have`: an improvement that is not blocking.

## Summary

| Id | Zone | Topic | Priority |
|---|---|---|---|
| F1 | theme.py | Font stack mangled into one family name | bug |
| F2 | theme.py | Fallback is always `system-ui, sans-serif` | gap |
| F3 | theme.py | Single `brand` color drives fills and focus | gap |
| F4 | theme.py | Exit code 2 writes no file at all | gap |
| F5 | theme.py | `white/other` in the dark contrast report | nice-to-have |
| F6 | conventions | Light `on-surface` convention not fixed | gap |
| F7 | conventions | No extension convention for app-specific tokens | gap |
| F8 | docs (README, implementation) | No adoption guide for an existing design system | gap |
| F9 | implementation | `data-demo-state` forces duplicated rules | gap |
| F10 | implementation | No visually-hidden (sr-only) recipe | nice-to-have |
| F11 | implementation | No composite typography variable | nice-to-have |
| F12 | components/dialog | Header and footer separators while the body scrolls | gap |

Totals: 1 bug, 8 gap, 3 nice-to-have (12 findings).

## theme.py

### F1. Font stack mangled into one family name (bug)

- Finding: `--font "Roboto Mono, ui-monospace, monospace"` is accepted without error but written as one quoted family, `"Roboto Mono, ui-monospace, monospace", system-ui, sans-serif`.
- Impact: the font is broken in `tokens.css` and in the text of `DESIGN.md`, silently.
- Lead: split on commas and quote only names that contain spaces, or reject a stack with a clear error and document that `--font` takes a single family.

### F2. Fallback is always `system-ui, sans-serif` (gap)

- Finding: the fallback appended after the chosen font is fixed.
- Impact: a monospace font cannot get a monospace fallback.
- Lead: add a fallback option (or infer it from a generic family given by the user). Closely tied to F1.

### F3. Single `brand` color drives fills and focus (gap)

- Finding: one `brand` color feeds both solid buttons and the focus / active state.
- Impact: neutral solid buttons (dark gray) with a colored focus ring cannot be expressed, a common pattern.
- Lead: allow a separate accent for focus and active state, or a neutral-fill option for primary actions; ask it in the questionnaire.

### F4. Exit code 2 writes no file at all (gap)

- Finding: when the main color needs an adjustment in dark mode (exit code 2), nothing is written, not even the light theme.
- Impact: the user must rerun to see anything, with no partial result to inspect.
- Lead: write the light outputs before stopping, and say which files were written.

### F5. `white/other` in the dark contrast report (nice-to-have)

- Finding: some rows of the dark contrast report show `white/other` instead of the name of the background step.
- Impact: hard to read which pair failed.
- Lead: print the actual step name in every row.

## conventions.md

### F6. Light `on-surface` convention not fixed (gap)

- Finding: `on-surface` on `neutral-700` (`#585858` with neutral grays) passes (6.9:1) but is much lighter than common practice and barely distinct from `on-surface-muted` (`#6F6F6F`, 4.9:1). The dark convention is stated (around line 203); the light one is not.
- Impact: primary and secondary text look almost the same in light mode.
- Lead: state the light convention explicitly, and consider a darker step for `on-surface`.

### F7. No extension convention for app-specific tokens (gap)

- Finding: there is no place for tokens that belong to the application (bubble width, mascot size, tile size, navigation item height).
- Impact: implementers repurpose tokens with another meaning, for example `--spacing-focus-ring-width` for a 2 px stripe, or `--color-neutral-subtle-hover` for a resting background.
- Lead: document an extension convention (a prefix or a separate file, and what is allowed) so app tokens never reuse kit tokens.

## README and docs/implementation.md

### F8. No adoption guide for an existing design system (gap)

- Finding: the README and `implementation.md` assume a theme created from scratch.
- Impact: nothing says how to compare the kit output with the existing system, what to archive, or where to put the generated files.
- Lead: add a short guide: comparison steps, what to keep or archive, output locations.

### F9. `data-demo-state` forces duplicated rules (gap)

- Finding: the `data-demo-state` approach proposed in `implementation.md` requires duplicating every `:hover` / `:active` rule.
- Impact: more CSS to maintain, and drift risk between real and demo states.
- Lead: add a CSS recipe that forces states on a demo page without duplication (for example a shared selector list or a nesting pattern).

### F10. No visually-hidden (sr-only) recipe (nice-to-have)

- Finding: `1px` literals are allowed for accessibility, but no example or constant is provided.
- Impact: each implementer rewrites the pattern.
- Lead: ship a standard sr-only snippet and note that it is an allowed literal use.

### F11. No composite typography variable (nice-to-have)

- Finding: every component repeats the `font` declaration as 5 variables.
- Impact: verbose CSS and easy to get out of sync.
- Lead: offer a composite variable or a documented shorthand per text style.

## components/dialog.md

### F12. Separators while the body scrolls (gap)

- Finding: header and footer separators that appear only while the body scrolls have no CSS-only solution, and the spec does not address it.
- Impact: implementers improvise (scripted observers or always-visible separators).
- Lead: state the expected behavior in the spec and give a recommended technique, or say that always-visible separators are acceptable.
