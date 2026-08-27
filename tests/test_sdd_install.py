from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = ROOT / "tools/sdd_install.py"
VALIDATOR_PATH = ROOT / "tools/sdd_validate.py"
MANIFEST_PATH = ROOT / "contract/v1/install-manifest.json"
REQUIREMENTS_PATH = ROOT / "contract/v1/requirements-validator.txt"
EXPECTED_VALIDATOR_REQUIREMENT = "jsonschema[format-nongpl]==4.25.1"

spec = importlib.util.spec_from_file_location("sdd_install", INSTALLER_PATH)
assert spec and spec.loader
sdd_install = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sdd_install
spec.loader.exec_module(sdd_install)

REQUIRED_DESTINATIONS = {
    "docs/sdd/contract/v1/install-manifest.json",
    "docs/sdd/contract/v1/feature-record.schema.json",
    "docs/sdd/contract/v1/sdd-protocol.json",
    "docs/sdd/contract/v1/README.md",
    "docs/sdd/contract/v1/requirements-validator.txt",
    "docs/sdd/tools/sdd_validate.py",
    "docs/sdd/tools/sdd.py",
    "docs/sdd/AGENTS.md",
    "docs/sdd/00_core",
    "docs/sdd/01_execution",
    "docs/sdd/02_policies",
    "docs/sdd/03_operations",
    "docs/sdd/04_project_governance",
    "docs/sdd/templates",
    "docs/sdd/init-sdd.sh",
    "docs/sdd/init-sdd.ps1",
    "docs/sdd/sdd.config.json",
}


def run_installer(target: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER_PATH), "--target", str(target), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def tree_digest(root: Path) -> dict[str, tuple[str, int]]:
    result: dict[str, tuple[str, int]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_file():
            result[relative] = (
                hashlib.sha256(path.read_bytes()).hexdigest(),
                stat.S_IMODE(path.stat().st_mode),
            )
        elif path.is_dir():
            result[relative + "/"] = ("DIR", stat.S_IMODE(path.stat().st_mode))
    return result


class InstallManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.manifest = sdd_install.load_manifest(MANIFEST_PATH, ROOT)

    def test_manifest_declares_required_distribution_and_dependency(self) -> None:
        self.assertEqual(self.manifest.version, "1.0.0")
        self.assertEqual(self.manifest.distribution, "Canonical SDD Model v1")
        self.assertEqual(self.manifest.install_root, "docs/sdd")
        destinations = {entry.destination for entry in self.manifest.entries}
        self.assertTrue(REQUIRED_DESTINATIONS.issubset(destinations))
        dependency = next(
            item for item in self.manifest.dependencies if item["name"] == "jsonschema"
        )
        self.assertEqual(dependency["requirement"], "==4.25.1")
        self.assertEqual(
            dependency["requirements_path"],
            "docs/sdd/contract/v1/requirements-validator.txt",
        )
        operator = next(
            entry for entry in self.manifest.entries if entry.source == "tools/sdd.py"
        )
        self.assertEqual(operator.destination, "docs/sdd/tools/sdd.py")
        self.assertEqual(operator.source_kind, "file")
        self.assertEqual(operator.element_type, "tool")
        self.assertTrue(operator.required)
        self.assertTrue(operator.executable)

    def test_validator_dependency_declares_date_time_format_support(self) -> None:
        self.assertEqual(
            REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines(),
            [EXPECTED_VALIDATOR_REQUIREMENT],
        )
        requirements_entry = next(
            entry
            for entry in self.manifest.entries
            if entry.source == "contract/v1/requirements-validator.txt"
        )
        self.assertEqual(
            requirements_entry.destination,
            "docs/sdd/contract/v1/requirements-validator.txt",
        )
        self.assertTrue(requirements_entry.required)

    def test_manifest_sources_exist_and_match_kind(self) -> None:
        sdd_install.validate_sources(self.manifest, ROOT)
        for entry in self.manifest.entries:
            source = ROOT / entry.source
            self.assertTrue(source.exists(), entry.source)
            self.assertEqual(source.is_dir(), entry.source_kind == "directory")

    def test_installer_has_no_second_distribution_inventory(self) -> None:
        source = INSTALLER_PATH.read_text(encoding="utf-8")
        for forbidden in (
            "feature-record.schema.json",
            "sdd-protocol.json",
            "AGENTS.md",
            "init-sdd.sh",
            "init-sdd.ps1",
            "01_execution",
            "02_policies",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def _assert_manifest_error(self, mutate) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source_root = Path(temp) / "source"
            shutil.copytree(
                ROOT,
                source_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            raw = json.loads(
                (source_root / "contract/v1/install-manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            mutate(raw)
            path = source_root / "contract/v1/install-manifest.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(sdd_install.ManifestError):
                sdd_install.load_manifest(path, source_root)

    def test_manifest_rejects_unsafe_paths_and_collisions(self) -> None:
        mutations = {
            "absolute_source": lambda raw: raw["entries"][0].update(
                source="/tmp/source"
            ),
            "windows_absolute_source": lambda raw: raw["entries"][0].update(
                source="C:/source"
            ),
            "parent_source": lambda raw: raw["entries"][0].update(
                source="../source"
            ),
            "wildcard_source": lambda raw: raw["entries"][0].update(
                source="contract/*"
            ),
            "outside_destination": lambda raw: raw["entries"][0].update(
                destination="docs/outside/file"
            ),
            "parent_destination": lambda raw: raw["entries"][0].update(
                destination="docs/sdd/../outside"
            ),
            "duplicate_destination": lambda raw: raw["entries"][1].update(
                destination=raw["entries"][0]["destination"]
            ),
            "colliding_destination": lambda raw: raw["entries"][1].update(
                destination=raw["entries"][0]["destination"] + "/nested"
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(case=name):
                self._assert_manifest_error(mutation)

    def test_required_missing_source_is_rejected_before_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source_root = Path(temp) / "source"
            shutil.copytree(
                ROOT,
                source_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            missing = source_root / "AGENTS.md"
            missing.unlink()
            manifest = sdd_install.load_manifest(
                source_root / "contract/v1/install-manifest.json", source_root
            )
            with self.assertRaises(sdd_install.SourceError):
                sdd_install.validate_sources(manifest, source_root)

    def _alternate_checkout(self) -> tuple[tempfile.TemporaryDirectory, Path, Path, Path]:
        temp = tempfile.TemporaryDirectory()
        source_root = Path(temp.name) / "source"
        shutil.copytree(
            ROOT,
            source_root,
            ignore=shutil.ignore_patterns(".git", "__pycache__"),
        )
        target = Path(temp.name) / "target"
        target.mkdir()
        manifest = source_root / "contract/v1/install-manifest.json"
        return temp, source_root, manifest, target

    def test_alternate_manifest_with_explicit_source_root_passes(self) -> None:
        temp, source_root, manifest, target = self._alternate_checkout()
        try:
            done = run_installer(
                target,
                "--manifest",
                str(manifest),
                "--source-root",
                str(source_root),
                "--dry-run",
                "--format",
                "json",
            )
            self.assertEqual(done.returncode, 0, done.stderr)
            payload = json.loads(done.stdout)
            self.assertEqual(payload["status"], "DRY_RUN")
            self.assertEqual(payload["distribution"], "Canonical SDD Model v1")
        finally:
            temp.cleanup()

    def test_alternate_manifest_outside_contract_layout_returns_4(self) -> None:
        temp, source_root, manifest, target = self._alternate_checkout()
        try:
            outside_layout = source_root / "install-manifest.json"
            shutil.copy2(manifest, outside_layout)
            done = run_installer(
                target,
                "--manifest",
                str(outside_layout),
                "--source-root",
                str(source_root),
                "--dry-run",
                "--format",
                "json",
            )
            self.assertEqual(done.returncode, sdd_install.EXIT_MANIFEST)
            self.assertNotIn("Traceback", done.stderr)
        finally:
            temp.cleanup()

    def test_shallow_manifest_path_has_stable_exit_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / "install-manifest.json"
            manifest.write_text(json.dumps(self.raw), encoding="utf-8")
            target = root / "target"
            target.mkdir()
            done = run_installer(
                target,
                "--manifest",
                str(manifest),
                "--source-root",
                str(root),
                "--dry-run",
                "--format",
                "json",
            )
            self.assertEqual(done.returncode, sdd_install.EXIT_MANIFEST)
            self.assertNotIn("Traceback", done.stderr)
            self.assertEqual(json.loads(done.stderr)["exit_code"], 4)

    def test_manifest_source_escape_is_rejected(self) -> None:
        temp, source_root, manifest, target = self._alternate_checkout()
        try:
            outside = Path(temp.name) / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            raw = json.loads(manifest.read_text(encoding="utf-8"))
            raw["entries"][0]["source"] = "../outside.txt"
            manifest.write_text(json.dumps(raw), encoding="utf-8")
            done = run_installer(
                target,
                "--manifest",
                str(manifest),
                "--source-root",
                str(source_root),
                "--dry-run",
                "--format",
                "json",
            )
            self.assertEqual(done.returncode, sdd_install.EXIT_MANIFEST)
            self.assertNotIn("Traceback", done.stderr)
        finally:
            temp.cleanup()

    def test_manifest_version_2_is_rejected_with_exit_4(self) -> None:
        temp, source_root, manifest, target = self._alternate_checkout()
        try:
            raw = json.loads(manifest.read_text(encoding="utf-8"))
            raw["manifest_version"] = "2.0.0"
            manifest.write_text(json.dumps(raw), encoding="utf-8")
            done = run_installer(
                target,
                "--manifest",
                str(manifest),
                "--source-root",
                str(source_root),
                "--dry-run",
                "--format",
                "json",
            )
            self.assertEqual(done.returncode, sdd_install.EXIT_MANIFEST)
            self.assertIn("Unsupported manifest_version", done.stderr)
        finally:
            temp.cleanup()

    def test_unknown_distribution_is_rejected_with_exit_4(self) -> None:
        temp, source_root, manifest, target = self._alternate_checkout()
        try:
            raw = json.loads(manifest.read_text(encoding="utf-8"))
            raw["distribution"] = "Unknown Distribution"
            manifest.write_text(json.dumps(raw), encoding="utf-8")
            done = run_installer(
                target,
                "--manifest",
                str(manifest),
                "--source-root",
                str(source_root),
                "--dry-run",
                "--format",
                "json",
            )
            self.assertEqual(done.returncode, sdd_install.EXIT_MANIFEST)
            self.assertIn("Unsupported distribution", done.stderr)
        finally:
            temp.cleanup()


class InstallerSmokeTests(unittest.TestCase):
    def test_dry_run_lists_paths_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "product"
            target.mkdir()
            sentinel = target / "sentinel.txt"
            sentinel.write_text("unchanged", encoding="utf-8")
            before = tree_digest(target)
            done = run_installer(target, "--dry-run", "--format", "json")
            self.assertEqual(done.returncode, 0, done.stderr)
            payload = json.loads(done.stdout)
            self.assertEqual(payload["status"], "DRY_RUN")
            self.assertTrue(payload["dry_run"])
            self.assertEqual(before, tree_digest(target))
            self.assertFalse((target / "docs/sdd").exists())
            self.assertIn(
                str(
                    target.resolve()
                    / "docs/sdd/contract/v1/feature-record.schema.json"
                ),
                payload["created"],
            )

    def test_install_smoke_self_check_record_and_reinstall_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            target = base / "product"
            target.mkdir()
            outside = base / "outside-sentinel.txt"
            outside.write_text("untouched", encoding="utf-8")

            done = run_installer(target, "--format", "json")
            self.assertEqual(done.returncode, 0, done.stderr)
            payload = json.loads(done.stdout)
            self.assertEqual(payload["status"], "INSTALLED")
            self.assertEqual({path.name for path in target.iterdir()}, {"docs"})
            self.assertEqual(outside.read_text(encoding="utf-8"), "untouched")

            for destination in REQUIRED_DESTINATIONS:
                self.assertTrue((target / destination).exists(), destination)
            for path in target.rglob("*"):
                if path != target / "docs":
                    path.resolve().relative_to((target / "docs/sdd").resolve())

            installed = target / "docs/sdd"
            validator = installed / "tools/sdd_validate.py"
            operator = installed / "tools/sdd.py"
            requirements = installed / "contract/v1/requirements-validator.txt"
            self.assertTrue(operator.stat().st_mode & stat.S_IXUSR)
            self.assertEqual(validator.read_bytes(), VALIDATOR_PATH.read_bytes())
            self.assertEqual(requirements.read_bytes(), REQUIREMENTS_PATH.read_bytes())
            self.assertEqual(
                requirements.read_text(encoding="utf-8").splitlines(),
                [EXPECTED_VALIDATOR_REQUIREMENT],
            )
            schema = installed / "contract/v1/feature-record.schema.json"
            protocol = installed / "contract/v1/sdd-protocol.json"
            self_check = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    "--schema",
                    str(schema),
                    "--protocol",
                    str(protocol),
                    "--self-check",
                    "--format",
                    "json",
                ],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(self_check.returncode, 0, self_check.stderr)
            self.assertTrue(json.loads(self_check.stdout)["contracts_ok"])

            record = installed / "synthetic-feature.json"
            record.write_text(
                json.dumps(
                    {
                        "id": "feat-900-install-smoke",
                        "type": "SYSTEM_SPEC",
                        "state": "DESIGN",
                        "title": "Synthetic install smoke",
                        "created_at": "2026-07-11T09:00:00Z",
                        "updated_at": "2026-07-11T09:00:00Z",
                        "design_path": "docs/sdd/artifacts/design/feat-900-install-smoke.md",
                        "open_questions": [],
                    }
                ),
                encoding="utf-8",
            )
            validation = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    str(record),
                    "--schema",
                    str(schema),
                    "--protocol",
                    str(protocol),
                    "--format",
                    "json",
                ],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stderr)
            self.assertTrue(json.loads(validation.stdout)["valid"])

            status = subprocess.run(
                [sys.executable, str(operator), "status", str(record), "--json"],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            status_payload = json.loads(status.stdout)
            self.assertTrue(status_payload["read_only"])
            self.assertEqual(status_payload["effective_state"], "DESIGN")

            next_route = subprocess.run(
                [sys.executable, str(operator), "next", str(record), "--json"],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(next_route.returncode, 0, next_route.stderr)
            next_payload = json.loads(next_route.stdout)
            self.assertEqual(next_payload["next_status"], "READY")
            self.assertEqual(next_payload["ready_route"]["to"], "SPEC")

            second = run_installer(target, "--format", "json")
            self.assertEqual(second.returncode, sdd_install.EXIT_TARGET)
            self.assertIn("Existing SDD installation", second.stderr)

    def test_installations_are_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first, second = root / "one", root / "two"
            first.mkdir()
            second.mkdir()
            self.assertEqual(run_installer(first).returncode, 0)
            self.assertEqual(run_installer(second).returncode, 0)
            self.assertEqual(
                tree_digest(first / "docs/sdd"), tree_digest(second / "docs/sdd")
            )

    @unittest.skipIf(os.name == "nt", "symlink behavior differs on Windows")
    def test_symlinked_docs_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "product"
            outside = root / "outside"
            target.mkdir()
            outside.mkdir()
            (target / "docs").symlink_to(outside, target_is_directory=True)
            done = run_installer(target, "--format", "json")
            self.assertEqual(done.returncode, sdd_install.EXIT_TARGET)
            self.assertFalse((outside / "sdd").exists())


if __name__ == "__main__":
    unittest.main()
