"""读取集合仓库维护的简化 YAML 来源清单。"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


EXPECTED_SCHEMA_VERSION = 1
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]*(.*))?$")


class ManifestError(ValueError):
    """来源清单格式或内容无效。"""


@dataclass(frozen=True)
class SkillSource:
    name: str
    repository: str
    source_path: str
    submodule_path: str
    local_path: str


@dataclass(frozen=True)
class CollectionManifest:
    version: int
    skills: tuple[SkillSource, ...]
    pending: tuple[str, ...]


def normalize_repository_url(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.endswith(".git"):
        value = value[:-4]
    return value.lower()


def _scalar(value: str, line_number: int) -> str:
    value = re.sub(r"[ \t]+#.*$", "", value).strip()
    if not value:
        raise ManifestError(f"第 {line_number} 行缺少字段值")
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ManifestError(f"第 {line_number} 行不是有效的双引号字符串") from exc
        if not isinstance(decoded, str):
            raise ManifestError(f"第 {line_number} 行的字段值必须是字符串")
        return decoded
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ManifestError(f"第 {line_number} 行不是有效的单引号字符串")
        return value[1:-1].replace("''", "'")
    return value


def _key_value(value: str, line_number: int) -> tuple[str, str]:
    key, separator, raw_value = value.partition(":")
    if not separator or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key.strip()):
        raise ManifestError(f"第 {line_number} 行不是有效的键值字段")
    return key.strip(), _scalar(raw_value, line_number)


def _validate_relative_path(field: str, value: str, name: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ManifestError(f"{name} 的 {field} 必须是仓库内的相对 POSIX 路径")
    return value


def load_manifest(path: str | Path) -> CollectionManifest:
    manifest_path = Path(path)
    try:
        lines = manifest_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ManifestError(f"无法读取来源清单：{manifest_path}") from exc

    schema_version: int | None = None
    in_skills = False
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))

        if indent == 0:
            if current is not None:
                entries.append(current)
                current = None
            top_match = TOP_LEVEL_KEY_RE.match(line)
            if not top_match:
                raise ManifestError(f"第 {line_number} 行不是有效的顶层字段")
            key = top_match.group(1)
            raw_value = (top_match.group(2) or "").strip()
            if key == "version":
                try:
                    schema_version = int(_scalar(raw_value, line_number))
                except ValueError as exc:
                    raise ManifestError("来源清单 version 必须是整数") from exc
            elif key == "skills" and not raw_value:
                in_skills = True
            else:
                raise ManifestError(f"第 {line_number} 行有不支持的顶层字段：{key}")
            continue

        if not in_skills:
            raise ManifestError(f"第 {line_number} 行出现在 skills 清单之前")
        if indent == 2 and stripped.startswith("- "):
            if current is not None:
                entries.append(current)
            current = {}
            key, value = _key_value(stripped[2:], line_number)
            current[key] = value
            continue
        if indent == 4 and current is not None:
            key, value = _key_value(stripped, line_number)
            if key in current:
                raise ManifestError(f"第 {line_number} 行重复定义字段：{key}")
            current[key] = value
            continue
        raise ManifestError(f"第 {line_number} 行缩进或列表结构无效")

    if current is not None:
        entries.append(current)
    if schema_version != EXPECTED_SCHEMA_VERSION:
        raise ManifestError(
            f"不支持的来源清单版本：{schema_version!r}；"
            f"当前只支持 {EXPECTED_SCHEMA_VERSION}"
        )

    skills: list[SkillSource] = []
    pending: list[str] = []
    names: set[str] = set()
    allowed_fields = {
        "name",
        "repository",
        "source_path",
        "submodule_path",
        "local_path",
        "status",
        "reason",
    }
    required_fields = {"name", "repository", "source_path", "submodule_path", "local_path"}

    for entry in entries:
        unknown = sorted(set(entry) - allowed_fields)
        if unknown:
            raise ManifestError("来源条目包含不支持的字段：" + ", ".join(unknown))
        name = entry.get("name", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ManifestError(f"Skill 名称无效：{name!r}")
        if name in names:
            raise ManifestError(f"Skill 名称重复：{name}")
        names.add(name)

        if entry.get("status") == "pending":
            if not entry.get("reason"):
                raise ManifestError(f"待接入的 Skill {name} 缺少 reason")
            pending.append(name)
            continue
        missing = sorted(required_fields - set(entry))
        if missing:
            raise ManifestError(f"Skill {name} 缺少字段：" + ", ".join(missing))
        if "status" in entry or "reason" in entry:
            raise ManifestError(f"已接入的 Skill {name} 不应设置 pending 字段")
        if not entry["repository"].startswith(("https://", "ssh://", "git@")):
            raise ManifestError(f"Skill {name} 的 repository 必须是 Git URL")

        for field in ("source_path", "submodule_path", "local_path"):
            _validate_relative_path(field, entry[field], name)

        skills.append(
            SkillSource(
                name=name,
                repository=entry["repository"],
                source_path=entry["source_path"],
                submodule_path=entry["submodule_path"],
                local_path=entry["local_path"],
            )
        )

    return CollectionManifest(
        version=schema_version,
        skills=tuple(skills),
        pending=tuple(pending),
    )
