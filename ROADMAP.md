# Roadmap

Maturity: maintenance

Planned cadence: every 2-4 weeks, plus urgent fixes for broken registry checks,
README truthfulness regressions, or CI failures.

`install-truth-guard` is intentionally narrow: it protects README install
instructions from promising unpublished packages or images. The current CLI is
useful and stable, so future work should focus on higher-confidence registry
coverage and CI ergonomics rather than broad feature growth.

## Now

- Add a repository-level roadmap and cadence notes so the project can be rotated
  responsibly with the rest of the `codecat-ai` portfolio.
- Keep the source-checkout usage documentation truthful until a package registry
  release is explicitly approved and verified.

## Next

- Add a documented configuration file for repeated allow/ignore policies across
  multiple README files in a repository.
- Add GitHub Actions annotation output for CI runs so install-claim failures can
  point to the Markdown line that needs attention.
- Expand offline examples with representative npm, PyPI, Cargo, and Docker
  snippets that demonstrate default versus strict unsupported-ecosystem results.

## Later

- Evaluate read-only Cargo crate and Docker image existence checks after the
  supported semantics are clear and safely testable.
- Add a multi-file project scan mode for repositories with translated README
  variants and documentation subdirectories.
- Consider a small release checklist before any package-manager publication,
  including verified install commands and synchronized README updates.

## Maintenance triggers

- A supported registry changes response shape, timeout behavior, or package-name
  normalization rules.
- A user reports a false positive, false negative, or confusing diagnostic.
- CI, dependency metadata, README language switchers, or MIT license detection
  drift from the portfolio standard.
- Documentation starts suggesting an install path that has not been published and
  verified.

## Cadence-review notes

Review cadence after two consecutive maintenance runs with no issues, no CI
failures, and no roadmap item that materially improves user safety. If that
happens, keep the project on `mature-low-frequency` maintenance and reserve
routine effort for higher-value active or growth projects.

## Completion-review rule

Before adding a new phase, confirm that it improves real user outcomes for README
truthfulness, CI diagnostics, registry coverage, or team policy reuse. If the
remaining ideas are only nice-to-have checker options, lower the cadence instead
of extending the roadmap.
