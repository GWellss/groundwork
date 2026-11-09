# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | yes |
| earlier than 0.1.0 | no |

## Reporting a vulnerability

Please do not report a vulnerability in a public issue.

Use the private reporting feature of GitHub: open the Security tab of this repository, then choose "Report a vulnerability". Describe the problem, the files concerned, and the steps to reproduce it.

You will get an answer as soon as the maintainer can review the report. If the report is confirmed, a fix is released and the change is recorded in [CHANGELOG.md](CHANGELOG.md).

## Scope

The repository holds Markdown specifications and one Python script, `theme/theme.py`, which uses the standard library only. A relevant report is, for example, a flaw in how the script reads its input or writes its output files.
