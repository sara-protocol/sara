# Publishing Rules (v1)

## Publishing Surface
- Pages only publishes `site/`.
- `site/index.html` must exist; otherwise CI fails.
- `site/` is generated output and MUST NOT be committed.

## CI Triggers
- `push` to `main`: build + readiness gate + deploy Pages.
- `pull_request`: build + readiness gate (no deploy).

## Build Requirements
CI must run:
- `make LANG=zh all`
- `make LANG=en all`
- `make readiness-gate`
- `make site`

## Quality Gate (Hard)
- Readiness score MUST be `100`.
- QA Fail MUST be `0`.
- QA Warn may exist, but must be visible in dashboard.

## Git Discipline
- `main` is always deployable.
- Never hand-edit `site/`; always generate via `make site`.
- CI/workflow changes should be separate commits prefixed with `ci:`.
