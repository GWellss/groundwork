# Groundwork

A reference kit that lets an AI agent bootstrap a design system without starting from scratch.

Status: version 0.1.0 (see [CHANGELOG.md](CHANGELOG.md)). The kit is usable, but the specs and the format may still change before 1.0.

## What and why

All design systems share invariants: component anatomy, named sizes, states, variants. They differ by a theme: colors, radius, typography, icon style.

This kit captures the invariants as detailed component specifications, and isolates the theme in a single file. An agent asks the user a few questions, fills in the theme, then generates component code from the specs and the theme, in the stack chosen by the user.

## Relation to DESIGN.md

This kit complements [Google's DESIGN.md](https://github.com/google-labs-code/design.md) (alpha format, Apache-2.0). It is an independent project and is not affiliated with or endorsed by Google.

- The theme is a valid DESIGN.md file: YAML tokens (`colors`, `typography`, `rounded`, `spacing`), checked with its lint, contrast included.
- The kit never duplicates DESIGN.md. It never adds non-standard properties to `components`; it only declares standard `backgroundColor` and `textColor` entries so the DESIGN.md lint checks contrast.
- The kit adds what DESIGN.md does not cover: component specs (anatomy, sizes, variant by state matrix, accessibility, behavior), a questionnaire to fill the theme, and implementation conventions for code generation.
- The pinned DESIGN.md CLI version is `@google/design.md` 0.4.0.
- W3C DTCG 2025.10 JSON is only an optional export format.
- Icon style is recorded in a free `## Icons` section of DESIGN.md, not as a token.
- The kit does not use the `css-vars` export (it does not cover `typography`): the theme script generates `tokens.css` itself, with fixed variable names (see `docs/implementation.md`).
- Optional dark mode: a second theme file, `DESIGN.dark.md`, and a `[data-theme="dark"]` block in `tokens.css`; the application decides when to apply it (see "Dark mode" in `docs/conventions.md`).
- Theme validation: 0 errors and 0 `contrast-ratio` warnings; `orphaned-tokens` warnings on unused palette steps are tolerated.

## Requirements

- Python 3, standard library only (no package to install), to run the theme script.
- Node.js only for the optional DESIGN.md lint (`npx @google/design.md@0.4.0 lint <file>`).

## Quick start

### With an AI agent

The kit is designed to be used by an agent. Give it the repository: the URL `https://github.com/GWellss/groundwork`, or a cloned folder that the agent can read. Then send it a prompt such as:

```
Read theme/questionnaire.md in this repository and follow it to create the theme of my design system.
Then write the component code from the specs in components/ and docs/implementation.md, for the web.
```

The agent then:

1. Asks you a few questions (name, brand color, corners, density, font, icons, optional dark mode), each with a default you can accept.
2. Generates the theme and checks the color contrast.
3. Writes the component code in your stack, reading every value from `tokens.css`.

You get a `DESIGN.md` theme, a `tokens.css` file (plus `DESIGN.dark.md` if you asked for dark mode), and the component code. The steps are detailed in "How an agent uses the kit" below.

What the agent can do depends on its tools. With a terminal it runs the theme script and the lint; with code execution only, it runs the script without the lint; with no tools, it copies precomputed colors from [theme/palettes.md](theme/palettes.md) and you check the contrast yourself. See the three levels in [theme/questionnaire.md](theme/questionnaire.md).

### Without an agent

You can generate a theme yourself with the script (Python 3, no package to install):

```
git clone https://github.com/GWellss/groundwork.git
cd groundwork
python3 theme/theme.py --help
```

Then generate your theme in a folder of your own. For example, a violet theme with rounded corners and a dark mode:

```
mkdir -p my-theme
python3 theme/theme.py --name Acme --brand "#7C3AED" --corners rounded --dark --dark-brand accept --out my-theme/DESIGN.md
```

The script does not create the output folder, hence the `mkdir`. It prints the contrast report, and writes `my-theme/DESIGN.md`, `my-theme/tokens.css` and, because of `--dark`, `my-theme/DESIGN.dark.md`. `--dark-brand accept` accepts the nearest palette step if your brand color is too dark for a dark background (usual brand colors are); use `keep` to refuse it and have the failing pairs reported. Writing the component code is up to you, from the specs in `components/`.

The options that apply the questionnaire choices are described in [theme/questionnaire.md](theme/questionnaire.md). To regenerate the examples of this repository, see [CONTRIBUTING.md](CONTRIBUTING.md).

## How an agent uses the kit

1. Ask the user the questionnaire to collect theme choices. The questionnaire first asks the agent to identify its level (terminal, code execution, or no tools), which decides how colors are derived and checked.
2. Write the theme as a DESIGN.md file.
3. Run the DESIGN.md lint and fix any error.
4. Read the component specs and `docs/implementation.md`. Each configuration of a spec has a status (`allowed`, `forbidden`, `avoid`, `out-of-scope`), defined in `docs/conventions.md`; the agent handles it as `docs/implementation.md` states.
5. Generate the component code in the stack chosen by the user, reading every value from `tokens.css`. The theme script writes `tokens.css` next to DESIGN.md in step 2; without the script (Level 3 of the questionnaire), the agent copies it from DESIGN.md. The script's `--css <path>` option chooses another path for `tokens.css` (see `theme/questionnaire.md`).

## Structure

```
theme/        questionnaire, theme script (DESIGN.md and tokens.css), palettes
components/   one spec per component (24): button, chip, tooltip, divider, link, badge, avatar, progress, text-field, search-field, checkbox, radio, switch, slider, segmented-control, tabs, accordion, menu, select, popover, dialog, alert, toast, card
docs/         glossary, conventions, implementation
docs/rationale/  explanations of the decisions, for human contributors; not needed by agents
examples/     generated example themes
  default/        light theme: DESIGN.md, tokens.css
  default-dark/   light and dark theme: DESIGN.md, DESIGN.dark.md, tokens.css
```

Other files at the root: [LICENSE](LICENSE), [CREDITS.md](CREDITS.md), [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [SECURITY.md](SECURITY.md), [CHANGELOG.md](CHANGELOG.md). Continuous integration is in `.github/`: it runs the script self-test and checks that the examples are up to date (both blocking), and runs the DESIGN.md lint (not blocking).

## What's ready and what's planned

| Ready (0.1.0) | Planned |
|---|---|
| 24 component specs | Other technologies than the web |
| Questionnaire and theme script (DESIGN.md, `tokens.css`) | Target technologies asked in the questionnaire |
| Optional dark mode | Multi-format output (iOS, Android) |
| Example themes, CI | A web interface to set the theme |

## Scope

For now, the kit targets the web only. The theme script produces `tokens.css` (CSS custom properties), and the agent writes component code that reads those variables. Other technologies are not yet supported by the script; opening the kit to them is a planned evolution (see Roadmap).

## Roadmap

Planned, not yet available:

- Multi-format output: the theme script computes the theme once, then writes it in several formats. For example `tokens.css` for the web, a Swift file plus a light/dark `.xcassets` asset catalog for iOS, and Android later.
- Target technologies in the questionnaire: it will ask at the start which technology or technologies are targeted (several choices allowed).
- Component code stays written by the agent from the specs, whatever the target.
- A web interface to set the theme may come later.

## License

MIT, see [LICENSE](LICENSE). Third-party credits are in [CREDITS.md](CREDITS.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md). To report a vulnerability, see [SECURITY.md](SECURITY.md).
