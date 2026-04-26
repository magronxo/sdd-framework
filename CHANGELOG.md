# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-beta] - 2026-04-23

### Added

- Core SDD framework with canonical 8-phase pipeline (DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE)
- Project governance layer (PROJECT_MANIFEST.md, GLOSSARY.md, PROJECT_MAP.md)
- Pre-SDD intake system (seed capture, classification, triage)
- Onboarding documentation (GETTING_STARTED.md, SDD_PIPELINE_VISUAL.md, PROJECT_TOUR.md)
- Enterprise policies (EXTERNAL_FRAMEWORK_POLICY.md, VALIDATION_BOUNDARIES_POLICY.md, ROADMAP_TEMPLATE.md)
- Migration playbook for adopting SDD in existing projects
- Role prompts (Designer, Specifier, Validator, Planner, Implementer, Verifier, Auditor, Migration Auditor)
- Templates (design, specs, ADR, migration plan)
- Init scripts (PowerShell and Bash)
- Competitive analysis (BDD, TLA+, Clean Architecture, Diátaxis, Rust RFC, Python PEP)
- Diátaxis mode tags across all documentation
- Invariants section in spec template (inspired by TLA+)

### Notes

This is a **beta release**. The framework core is solid but awaits practical validation in real projects.

### Future Evaluation

- Executable SDT bridge (Gherkin → automated tests)
- Optional DISCUSSION phase before DESIGN
- Seed type `process` for methodology changes
- Architecture layer mapping (surfaces → Clean Architecture)

[0.1.0-beta]: https://github.com/oriolcoll/sdd-framework/releases/tag/v0.1.0-beta
