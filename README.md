# design-system-conf

A reference kit that lets an AI agent bootstrap a design system without starting from scratch.

Status: early work in progress. Nothing here is stable yet.

## What and why

All design systems share invariants: component anatomy, named sizes, states, variants. They differ by a theme: colors, radius, typography, icon style.

This kit captures the invariants as detailed component specifications, and isolates the theme in a single file. An agent asks the user a few questions, fills in the theme, then generates web code from the specs and the theme.

## Relation to DESIGN.md

This kit complements [Google's DESIGN.md](https://github.com/google-labs-code/design.md) (alpha format, Apache-2.0). It is an independent project and is not affiliated with or endorsed by Google.

- The theme is a valid DESIGN.md file: YAML tokens (`colors`, `typography`, `rounded`, `spacing`), checked with its lint, contrast included.
- The kit never duplicates DESIGN.md. It never adds non-standard properties to `components`; it only declares standard `backgroundColor` and `textColor` entries so the DESIGN.md lint checks contrast.
- The kit adds what DESIGN.md does not cover: component specs (anatomy, sizes, variant by state matrix, accessibility, behavior), a questionnaire to fill the theme, and web code generation.
- The pinned DESIGN.md CLI version is `@google/design.md` 0.4.0.
- W3C DTCG 2025.10 JSON is only an optional export format.
- Icon style is recorded in a free `## Icons` section of DESIGN.md, not as a token.
- The `css-vars` export does not cover `typography`: the kit generates the typography variables itself.
- Theme validation: 0 errors and 0 `contrast-ratio` warnings; `orphaned-tokens` warnings on unused palette steps are tolerated.

## How an agent uses the kit

1. Ask the user the questionnaire to collect theme choices.
2. Write the theme as a DESIGN.md file.
3. Run the DESIGN.md lint and fix any error.
4. Read the component specs.
5. Generate CSS custom properties and HTML/CSS from the token tree.

## Planned structure

```
theme/        DESIGN.md theme and questionnaire
components/   one spec per component (button, chip, tooltip first)
docs/         glossary and conventions
examples/     generated output samples
```

Only `docs/` exists today. A web interface to set the theme may come later.

## License

To be decided. The repository is private for now and is intended to become open source.
