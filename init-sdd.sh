#!/usr/bin/env bash
set -euo pipefail

# init-sdd.sh — Initialize SDD artifact directories and configuration

CONFIG="sdd.config.json"
PROJECT_NAME="${1:-}"
CREATE_SAMPLE="${2:-}"

# --- Validate or create config ---
if [[ -f "$CONFIG" ]]; then
    echo "[OK] Found $CONFIG"
    if ! jq empty "$CONFIG" 2>/dev/null; then
        echo "[ERROR] Invalid JSON in $CONFIG" >&2
        exit 1
    fi
else
    echo "[INFO] $CONFIG not found. Creating default..."
    DEFAULT_NAME="${PROJECT_NAME:-My Project}"
    cat > "$CONFIG" <<EOF
{
  "project_name": "$DEFAULT_NAME",
  "project_description": "Project using sdd-framework",
  "sdd_root": ".",
  "paths": {
    "core": "00_core",
    "execution": "01_execution",
    "policies": "02_policies",
    "operations": "03_operations",
    "templates": "templates",
    "artifacts": {
      "design": "artifacts/design",
      "specs": "artifacts/specs",
      "tasks": "artifacts/tasks",
      "audit_reports": "artifacts/audit_reports",
      "features_for_specs": "artifacts/features_for_specs"
    }
  },
  "stack": {
    "languages": [],
    "frameworks": [],
    "hardware": null
  },
  "surfaces": ["browser", "os_fs", "wiring", "network", "env_proxy"],
  "skills_registry": "03_operations/skills/skills_registry.json"
}
EOF
    echo "[OK] Created $CONFIG"
fi

# --- Helper to extract paths from config ---
get_path() {
    jq -r "$1" "$CONFIG" 2>/dev/null || echo ""
}

# --- Create artifact directories ---
DESIGN_DIR=$(get_path '.paths.artifacts.design // "artifacts/design"')
SPECS_DIR=$(get_path '.paths.artifacts.specs // "artifacts/specs"')
TASKS_DIR=$(get_path '.paths.artifacts.tasks // "artifacts/tasks"')
AUDIT_DIR=$(get_path '.paths.artifacts.audit_reports // "artifacts/audit_reports"')
FEATURES_DIR=$(get_path '.paths.artifacts.features_for_specs // "artifacts/features_for_specs"')

for d in "$DESIGN_DIR" "$SPECS_DIR" "$TASKS_DIR" "$AUDIT_DIR" "$FEATURES_DIR"; do
    if [[ ! -d "$d" ]]; then
        mkdir -p "$d"
        echo "[OK] Created directory: $d"
    else
        echo "[SKIP] Directory already exists: $d"
    fi
done

# --- Create skills registry directory if referenced ---
SKILLS_REGISTRY=$(get_path '.skills_registry // empty')
if [[ -n "$SKILLS_REGISTRY" ]]; then
    SKILLS_DIR=$(dirname "$SKILLS_REGISTRY")
    if [[ ! -d "$SKILLS_DIR" ]]; then
        mkdir -p "$SKILLS_DIR"
        echo "[OK] Created directory: $SKILLS_DIR"
    fi
fi

# --- Optional sample feature ---
if [[ "$CREATE_SAMPLE" == "--sample" ]]; then
    SAMPLE_PATH="$FEATURES_DIR/feat-001-example.json"
    if [[ ! -f "$SAMPLE_PATH" ]]; then
        TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        cat > "$SAMPLE_PATH" <<EOF
{
  "id": "feat-001",
  "type": "SYSTEM_SPEC",
  "state": "DESIGN",
  "title": "Example feature",
  "created_at": "$TIMESTAMP",
  "updated_at": "$TIMESTAMP",
  "design_path": "$DESIGN_DIR/feat-001-example.md"
}
EOF
        echo "[OK] Created sample feature: $SAMPLE_PATH"
    fi
fi

echo ""
echo "SDD initialization complete."
echo "Next steps:"
echo "  1. Review and customize $CONFIG"
echo "  2. Read AGENTS.md and 00_core/SDD_RUNTIME.md"
echo "  3. Create your first feature record in $FEATURES_DIR/"
