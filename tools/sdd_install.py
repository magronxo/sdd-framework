#!/usr/bin/env python3
"""Deterministic, manifest-driven installer for Canonical SDD Model v1."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_RELATIVE_PATH = PurePosixPath("contract/v1/install-manifest.json")
DEFAULT_MANIFEST = ROOT / Path(*MANIFEST_RELATIVE_PATH.parts)
EXPECTED_MANIFEST_VERSION = "1.0.0"
EXPECTED_DISTRIBUTION = "Canonical SDD Model v1"
EXPECTED_INSTALL_ROOT = "docs/sdd"
EXIT_OK = 0
EXIT_TARGET = 3
EXIT_MANIFEST = 4
EXIT_SOURCE = 5
EXIT_INSTALL = 6
ALLOWED_TYPES = {"contract", "runtime", "prompt", "policy", "template", "tool", "config"}
WILDCARDS = set("*?[]")


class InstallError(Exception):
    """Base installer error carrying a stable exit code."""

    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class ManifestError(InstallError):
    def __init__(self, message: str) -> None:
        super().__init__(message, EXIT_MANIFEST)


class SourceError(InstallError):
    def __init__(self, message: str) -> None:
        super().__init__(message, EXIT_SOURCE)


class TargetError(InstallError):
    def __init__(self, message: str) -> None:
        super().__init__(message, EXIT_TARGET)


@dataclass(frozen=True)
class Entry:
    source: str
    destination: str
    source_kind: str
    element_type: str
    required: bool
    executable: bool


@dataclass(frozen=True)
class Manifest:
    version: str
    distribution: str
    install_root: str
    dependencies: tuple[dict[str, Any], ...]
    entries: tuple[Entry, ...]


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ManifestError(f"Cannot read manifest {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"Manifest is not valid JSON: {exc}") from exc


def _safe_relative_path(value: Any, field: str) -> PurePosixPath:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{field} must be a non-empty string")
    if "\\" in value:
        raise ManifestError(f"{field} must use POSIX separators: {value}")
    if re.match(r"^[A-Za-z]:", value):
        raise ManifestError(f"{field} must not be an absolute drive path: {value}")
    if any(char in value for char in WILDCARDS):
        raise ManifestError(f"{field} must not contain wildcards: {value}")
    path = PurePosixPath(value)
    if path.is_absolute() or value.startswith("/"):
        raise ManifestError(f"{field} must be relative: {value}")
    if any(segment in {"", ".", ".."} for segment in path.parts):
        raise ManifestError(f"{field} contains a forbidden path segment: {value}")
    if str(path) != value:
        raise ManifestError(f"{field} is not normalized: {value}")
    return path


def _is_parent(parent: PurePosixPath, child: PurePosixPath) -> bool:
    return len(parent.parts) < len(child.parts) and child.parts[: len(parent.parts)] == parent.parts


def _validated_source_root(path: Path) -> Path:
    try:
        if path.is_symlink():
            raise ManifestError(f"Source root must not be a symlink: {path}")
        resolved = path.resolve(strict=True)
    except ManifestError:
        raise
    except (OSError, RuntimeError) as exc:
        raise ManifestError(f"Cannot resolve source root {path}: {exc}") from exc
    if not resolved.is_dir():
        raise ManifestError(f"Source root must be an existing directory: {path}")
    return resolved


def resolve_manifest_context(manifest_arg: Path | None, source_root_arg: Path | None) -> tuple[Path, Path]:
    """Resolve the only supported source layout without inferring arbitrary depth."""
    if manifest_arg is None:
        if source_root_arg is not None:
            raise ManifestError("--source-root is only valid together with --manifest")
        source_root = _validated_source_root(ROOT)
        manifest_path = source_root / Path(*MANIFEST_RELATIVE_PATH.parts)
        return manifest_path, source_root

    if source_root_arg is None:
        raise ManifestError("--source-root is required when --manifest is provided")

    source_root = _validated_source_root(source_root_arg)
    try:
        if manifest_arg.is_symlink():
            raise ManifestError(f"Manifest must not be a symlink: {manifest_arg}")
        manifest_path = manifest_arg.resolve(strict=False)
        relative = manifest_path.relative_to(source_root)
    except ManifestError:
        raise
    except (OSError, RuntimeError, ValueError) as exc:
        raise ManifestError(f"Manifest must be contained within source root: {manifest_arg}") from exc

    expected = Path(*MANIFEST_RELATIVE_PATH.parts)
    if relative != expected:
        raise ManifestError(
            "Alternate manifest must be located exactly at "
            f"{MANIFEST_RELATIVE_PATH.as_posix()} below --source-root"
        )
    return manifest_path, source_root


def load_manifest(path: Path = DEFAULT_MANIFEST, source_root: Path = ROOT) -> Manifest:
    source_root_resolved = _validated_source_root(source_root)
    try:
        path_resolved = path.resolve(strict=False)
        relative_manifest = path_resolved.relative_to(source_root_resolved)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ManifestError(f"Manifest escapes source root: {path}") from exc
    expected_manifest = Path(*MANIFEST_RELATIVE_PATH.parts)
    if relative_manifest != expected_manifest:
        raise ManifestError(
            "Manifest must be located exactly at "
            f"{MANIFEST_RELATIVE_PATH.as_posix()} below source root"
        )

    raw = _load_json(path_resolved)
    if not isinstance(raw, dict):
        raise ManifestError("Manifest root must be an object")

    version = raw.get("manifest_version")
    if version != EXPECTED_MANIFEST_VERSION:
        raise ManifestError(
            f"Unsupported manifest_version {version!r}; expected {EXPECTED_MANIFEST_VERSION!r}"
        )
    distribution = raw.get("distribution")
    if distribution != EXPECTED_DISTRIBUTION:
        raise ManifestError(
            f"Unsupported distribution {distribution!r}; expected {EXPECTED_DISTRIBUTION!r}"
        )
    install_root = _safe_relative_path(raw.get("install_root"), "install_root")
    if str(install_root) != EXPECTED_INSTALL_ROOT:
        raise ManifestError(f"install_root must be exactly {EXPECTED_INSTALL_ROOT}")

    dependencies = raw.get("runtime_dependencies")
    if not isinstance(dependencies, list) or not dependencies:
        raise ManifestError("runtime_dependencies must be a non-empty list")
    for index, dependency in enumerate(dependencies):
        if not isinstance(dependency, dict):
            raise ManifestError(f"runtime_dependencies[{index}] must be an object")
        for key in ("kind", "name", "requirement", "purpose"):
            if not isinstance(dependency.get(key), str) or not dependency[key].strip():
                raise ManifestError(f"runtime_dependencies[{index}].{key} is required")

    raw_entries = raw.get("entries")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise ManifestError("entries must be a non-empty list")

    entries: list[Entry] = []
    destinations: list[PurePosixPath] = []
    for index, item in enumerate(raw_entries):
        if not isinstance(item, dict):
            raise ManifestError(f"entries[{index}] must be an object")
        source = _safe_relative_path(item.get("source"), f"entries[{index}].source")
        destination = _safe_relative_path(item.get("destination"), f"entries[{index}].destination")
        if not _is_parent(install_root, destination):
            raise ManifestError(f"destination must be below docs/sdd/: {destination}")
        source_kind = item.get("source_kind")
        if source_kind not in {"file", "directory"}:
            raise ManifestError(f"entries[{index}].source_kind must be file or directory")
        element_type = item.get("type")
        if element_type not in ALLOWED_TYPES:
            raise ManifestError(f"entries[{index}].type is invalid: {element_type}")
        if not isinstance(item.get("required"), bool) or not isinstance(item.get("executable"), bool):
            raise ManifestError(f"entries[{index}] required and executable must be booleans")
        if item["executable"] and (source_kind != "file" or element_type != "tool"):
            raise ManifestError(f"entries[{index}] executable entries must be tool files")

        source_path = source_root_resolved / Path(*source.parts)
        try:
            resolved_source = source_path.resolve(strict=False)
            resolved_source.relative_to(source_root_resolved)
        except (OSError, RuntimeError, ValueError) as exc:
            raise ManifestError(f"source escapes source root: {source}") from exc
        if source_path.is_symlink():
            raise ManifestError(f"source symlinks are not allowed: {source}")

        for previous in destinations:
            if destination == previous:
                raise ManifestError(f"duplicate destination: {destination}")
            if _is_parent(previous, destination) or _is_parent(destination, previous):
                raise ManifestError(f"colliding destinations: {previous} and {destination}")
        destinations.append(destination)
        entries.append(
            Entry(
                source=str(source),
                destination=str(destination),
                source_kind=source_kind,
                element_type=element_type,
                required=item["required"],
                executable=item["executable"],
            )
        )

    destination_values = {entry.destination for entry in entries}
    for index, dependency in enumerate(dependencies):
        requirements_path = dependency.get("requirements_path")
        if requirements_path is None:
            continue
        dependency_path = _safe_relative_path(
            requirements_path, f"runtime_dependencies[{index}].requirements_path"
        )
        if not _is_parent(install_root, dependency_path):
            raise ManifestError(
                f"runtime dependency requirements_path must be below docs/sdd/: {dependency_path}"
            )
        if str(dependency_path) not in destination_values:
            raise ManifestError(
                f"runtime dependency requirements_path is not installed: {dependency_path}"
            )

    return Manifest(
        version,
        distribution,
        str(install_root),
        tuple(dependencies),
        tuple(entries),
    )


def _assert_source_tree_safe(path: Path, display: str) -> None:
    if path.is_symlink():
        raise SourceError(f"Source symlink is not allowed: {display}")
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_symlink():
                raise SourceError(
                    f"Source tree contains a symlink: {display}/{child.relative_to(path)}"
                )


def validate_sources(manifest: Manifest, source_root: Path = ROOT) -> None:
    source_root_resolved = _validated_source_root(source_root)
    for entry in manifest.entries:
        source = source_root_resolved / entry.source
        try:
            source.resolve(strict=False).relative_to(source_root_resolved)
        except (OSError, RuntimeError, ValueError) as exc:
            raise SourceError(f"Source escapes source root: {entry.source}") from exc
        if not source.exists():
            if entry.required:
                raise SourceError(f"Required source does not exist: {entry.source}")
            continue
        if entry.source_kind == "file" and not source.is_file():
            raise SourceError(f"Manifest source_kind mismatch, expected file: {entry.source}")
        if entry.source_kind == "directory" and not source.is_dir():
            raise SourceError(f"Manifest source_kind mismatch, expected directory: {entry.source}")
        _assert_source_tree_safe(source, entry.source)


def _resolve_install_root(target: Path, install_root: str) -> tuple[Path, Path]:
    if not target.exists() or not target.is_dir():
        raise TargetError(f"Target must be an existing directory: {target}")
    if target.is_symlink():
        raise TargetError(f"Target must not be a symlink: {target}")
    target_resolved = target.resolve()
    candidate = target_resolved / Path(*PurePosixPath(install_root).parts)
    try:
        candidate.resolve(strict=False).relative_to(target_resolved)
    except ValueError as exc:
        raise TargetError("Resolved install root escapes target") from exc
    current = target_resolved
    for segment in PurePosixPath(install_root).parts:
        current = current / segment
        if current.exists() and current.is_symlink():
            raise TargetError(f"Install path contains a symlink: {current}")
        if current.exists() and not current.is_dir():
            raise TargetError(f"Install path component is not a directory: {current}")
    if candidate.exists() or candidate.is_symlink():
        raise TargetError(f"Existing SDD installation is not overwritten: {candidate}")
    return target_resolved, candidate


def _destination_path(base: Path, destination: str, install_root: str) -> Path:
    destination_posix = PurePosixPath(destination)
    root_posix = PurePosixPath(install_root)
    relative = destination_posix.relative_to(root_posix)
    candidate = base / Path(*relative.parts)
    try:
        candidate.resolve(strict=False).relative_to(base.resolve(strict=False))
    except ValueError as exc:
        raise ManifestError(f"destination escapes staged install root: {destination}") from exc
    return candidate


def plan_install(manifest: Manifest, target: Path, source_root: Path = ROOT) -> dict[str, Any]:
    source_root_resolved = _validated_source_root(source_root)
    validate_sources(manifest, source_root_resolved)
    target_resolved, install_root = _resolve_install_root(target, manifest.install_root)
    return {
        "manifest_version": manifest.version,
        "distribution": manifest.distribution,
        "target": str(target_resolved),
        "install_root": str(install_root),
        "created": [
            str(target_resolved / entry.destination)
            for entry in manifest.entries
            if (source_root_resolved / entry.source).exists()
        ],
        "runtime_dependencies": list(manifest.dependencies),
    }


def _copy_entry(source: Path, destination: Path, executable: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination, copy_function=shutil.copy2)
    else:
        shutil.copy2(source, destination)
    if executable and destination.is_file():
        destination.chmod(
            destination.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )


def install(
    manifest: Manifest,
    target: Path,
    *,
    source_root: Path = ROOT,
    dry_run: bool = False,
) -> dict[str, Any]:
    result = plan_install(manifest, target, source_root)
    result["dry_run"] = dry_run
    result["status"] = "DRY_RUN" if dry_run else "INSTALLED"
    if dry_run:
        return result

    source_root_resolved = _validated_source_root(source_root)
    target_resolved = Path(result["target"])
    install_root = Path(result["install_root"])
    docs_dir = target_resolved / "docs"
    docs_existed = docs_dir.exists()
    docs_dir.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".sdd-install-", dir=docs_dir))
    stage.chmod(0o755)
    try:
        for entry in manifest.entries:
            source = source_root_resolved / entry.source
            if not source.exists():
                continue
            staged_destination = _destination_path(
                stage, entry.destination, manifest.install_root
            )
            _copy_entry(source, staged_destination, entry.executable)
        os.replace(stage, install_root)
    except Exception as exc:
        shutil.rmtree(stage, ignore_errors=True)
        if not docs_existed:
            try:
                docs_dir.rmdir()
            except OSError:
                pass
        if isinstance(exc, InstallError):
            raise
        raise InstallError(f"Installation failed: {exc}", EXIT_INSTALL) from exc
    return result


def _format_text(result: dict[str, Any]) -> str:
    lines = [
        f"STATUS: {result['status']}",
        f"DISTRIBUTION: {result['distribution']}",
        f"MANIFEST_VERSION: {result['manifest_version']}",
        f"TARGET: {result['target']}",
        f"INSTALL_ROOT: {result['install_root']}",
        "PATHS:",
    ]
    lines.extend(f"  {path}" for path in result["created"])
    lines.append("DEPENDENCIES:")
    for dependency in result["runtime_dependencies"]:
        lines.append(f"  {dependency['name']} {dependency['requirement']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target", required=True, type=Path, help="Existing product repository root"
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Alternate manifest at <source-root>/contract/v1/install-manifest.json",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=None,
        help="Explicit source checkout root; required with --manifest",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Validate and print planned paths without writing"
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest_path, source_root = resolve_manifest_context(
            args.manifest, args.source_root
        )
        manifest = load_manifest(manifest_path, source_root)
        result = install(
            manifest,
            args.target,
            source_root=source_root,
            dry_run=args.dry_run,
        )
    except InstallError as exc:
        payload = {"status": "ERROR", "error": str(exc), "exit_code": exc.exit_code}
        print(
            json.dumps(payload, indent=2, sort_keys=True)
            if args.format == "json"
            else f"ERROR: {exc}",
            file=sys.stderr,
        )
        return exc.exit_code
    print(
        json.dumps(result, indent=2, sort_keys=True)
        if args.format == "json"
        else _format_text(result)
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
