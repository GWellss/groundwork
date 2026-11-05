# Conventions

## Language

All content is in English: text, headings, file names, examples.

## DESIGN.md version

The theme follows DESIGN.md as checked by `@google/design.md` pinned to 0.4.0. Upgrade the pin deliberately, never implicitly.

## Token references

- Reference tokens by path, in DESIGN.md format: `{colors.primary}`.
- Never copy a token value into a component file. A value lives in the theme only.

## Sizes

Each component declares its own sizes. There is no shared scale imposed on all components.

## Naming

Use kebab-case for file names, token names, variants, states, and parts. Example: `leading-icon`.

## Component spec format

The internal format of a component spec is not fixed yet. It will be defined together with the button spec.
