from __future__ import annotations

import re
import subprocess
from pathlib import Path

try:
    from .collection_manifest import ManifestError, load_manifest, normalize_repository_url
except ImportError:
    from collection_manifest import ManifestError, load_manifest, normalize_repository_url


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill_name(path: Path) -> str:
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"^name:\s*([^\n]+)$", text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"missing name frontmatter: {path}")
    return match.group(1).strip().strip('"\'')


def main() -> int:
    try:
        manifest = load_manifest(ROOT / "sources.yaml")
    except ManifestError as exc:
        raise RuntimeError(f"invalid sources.yaml: {exc}") from exc

    sources = {source.name: source for source in manifest.skills}
    expected = set(sources)
    actual = {item.name for item in SKILLS.iterdir() if item.is_symlink()}
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise RuntimeError(f"skill link mismatch; missing={missing}, extra={extra}")

    for item in sorted(SKILLS.iterdir(), key=lambda path: path.name):
        if not item.is_symlink():
            continue
        target = item.resolve()
        skill_file = target / "SKILL.md"
        if not skill_file.is_file():
            raise RuntimeError(f"broken Skill link: {item} -> {target}")
        source = sources[item.name]
        expected_target = (ROOT / source.submodule_path / source.source_path).resolve()
        if target != expected_target:
            raise RuntimeError(
                f"source mapping mismatch: {item.name} -> {target}; expected {expected_target}"
            )
        declared = read_skill_name(target)
        if declared != item.name:
            raise RuntimeError(f"name mismatch: {item.name} != {declared}")
        origin = subprocess.run(
            ["git", "-C", str(ROOT / source.submodule_path), "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=False,
        )
        if origin.returncode != 0:
            raise RuntimeError(f"submodule origin missing: {source.submodule_path}")
        if normalize_repository_url(origin.stdout) != normalize_repository_url(source.repository):
            raise RuntimeError(
                f"repository mismatch for {item.name}: {origin.stdout.strip()} != {source.repository}"
            )
        print(f"ok {item.name}: {target}")
    for name in manifest.pending:
        print(f"pending {name}: no independent public source yet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
