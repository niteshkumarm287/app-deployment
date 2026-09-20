"""Validate tracked source and configuration without executing project code."""
import ast
import json
import subprocess
import sys
import tomllib

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    files = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode().split("\0")
    errors = []
    checked = 0
    for name in filter(None, files):
        path = ROOT / name
        generated = (
            "__pycache__" in path.parts
            or path.name in {".DS_Store", "tfplan", ".env"}
            or path.suffix in {".pyc", ".pyo", ".tfplan", ".tfstate"}
            or (path.name.startswith(".env.") and path.name != ".env.example" and not path.name.endswith(".example"))
        )
        if generated:
            errors.append(f"{name}: local configuration or generated artifact must not be tracked")
            continue
        if not path.is_file() or path.is_symlink():
            continue
        # VS Code uses JSON with comments; Helm templates are not plain YAML.
        if ".vscode" in path.parts or ("templates" in path.parts and path.suffix in {".yaml", ".yml"}):
            continue
        if path.suffix not in {".py", ".json", ".ipynb", ".toml", ".yaml", ".yml"}:
            continue
        try:
            source = path.read_text(encoding="utf-8-sig")
            if path.suffix == ".py":
                ast.parse(source, filename=name)
            elif path.suffix == ".toml":
                tomllib.loads(source)
            elif path.suffix in {".yaml", ".yml"}:
                list(yaml.safe_load_all(source))
            else:
                json.loads(source)
            checked += 1
        except (UnicodeError, SyntaxError, ValueError, yaml.YAMLError) as error:
            # Only print locations: parser messages may contain credential values.
            errors.append(f"{name}: invalid syntax at line {getattr(error, 'lineno', '?')}")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {checked} tracked Python/JSON/TOML/YAML files; {len(errors)} error(s).")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
