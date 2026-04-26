# Contributing to SDD Framework

Thank you for your interest in contributing! This is a young project and all feedback is valuable.

## How to Contribute

### Reporting Issues

If you find a bug, inconsistency, or something unclear:

1. Check if the issue already exists
2. If not, open a new issue with:
   - What you expected
   - What actually happened
   - Which document or file is affected
   - Your context (project type, team size, etc.)

### Proposing Changes

If you want to improve the framework:

1. Fork the repository
2. Create a branch: `git checkout -b feat/description`
3. Make your changes
4. Open a pull request with:
   - Clear description of the change
   - Why it improves the framework
   - Any breaking changes

### What We Need

- **Validation reports**: How does SDD work in your project? What frictions did you find?
- **Stack-specific adaptations**: How did you adapt the framework for your language/framework?
- **Documentation improvements**: What was unclear? What examples are missing?
- **Translations**: The framework is currently in English and Catalan. Translations welcome.

## Development Workflow

This project uses its own SDD framework for changes. If you are adding a feature to the framework itself:

1. Capture a seed in `03_operations/pre_sdd/seeds/`
2. Run it through the pipeline
3. Include the feature record, design, spec, and tasks in your PR

## Code of Conduct

- Be respectful and constructive
- Focus on the problem, not the person
- Prefer questions over assumptions

## Questions?

Open an issue with the label `question` or start a discussion.

---

**License**: Apache-2.0 (see LICENSE file)
