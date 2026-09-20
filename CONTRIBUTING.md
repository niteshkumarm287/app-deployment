# Contributing to app-deployment

## Project scope

GKE deployment example. Review the target project, namespace, RBAC, and cleanup instructions before applying manifests. Static checks do not provision or validate a live cluster.

## Development workflow

1. Create a focused branch from the repository's default branch.
2. Follow the existing setup instructions for the component being changed.
3. Use `.editorconfig` for new and edited files; avoid unrelated formatting changes.
4. Run the relevant checks and include the results in the pull request.
5. Request review from `@niteshkumarm287` before merging.

## Checks

The shared source check requires Python 3.11 or newer and PyYAML 6.0.3.
Run from the repository root:

```bash
python3 -m pip install PyYAML==6.0.3
python3 .github/scripts/check_repository.py
```

CI runs the syntax check on tracked Python, JSON, notebook JSON, TOML, and plain YAML files. Helm templates and VS Code JSONC
are excluded from generic parsing.
It does not execute application imports, interactive exercises, cloud commands,
or deployment scripts. A green syntax check alone does not prove runtime correctness.
Use project-specific tests and integration checks for behavior changes.

## Configuration and data

Keep credentials in local environment variables or your secret manager. Commit
sanitized `.env.example` templates when documenting required settings. Do not add
virtual environments, bytecode, Terraform state, saved plans, or local caches.
Preserve existing licenses, upstream attribution, and dataset usage restrictions.

## Review expectations

Describe the concrete problem, resulting behavior, validation, and any operational
impact. Keep changes small enough to review and include a rollback approach for
infrastructure or data changes. Existing deployment workflows may require cloud
credentials; do not run them as a substitute for offline validation.
