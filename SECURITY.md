# Security policy

## Reporting a vulnerability

Please do **not** open a public issue for security problems. Use GitHub's
[private vulnerability reporting](https://github.com/agrvasu05/DevCrew/security/advisories/new)
instead. You'll get a response within 7 days.

## Things to know

- DevCrew **does not execute** the code its Developer agent generates; it only writes it to
  `output/02_code.py`. Review generated code before running it.
- Your API key is read from the environment or a local `.env` file, which is git-ignored.
  Never commit `.env`.
