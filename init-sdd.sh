#!/usr/bin/env bash
set -euo pipefail

# init-sdd.sh — Initialize an installed SDD instance under docs/sdd/.
# Run from anywhere inside the product repository; paths are resolved from this script location.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG="$SCRIPT_DIR/sdd.config.json"
TEMPLATE_CONFIG="$SCRIPT_DIR/templates/sdd.config.json"
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
    if [[ -f "$TEMPLATE_CONFIG" ]]; then
        cp "$TEMPLATE_CONFIG" "$CONFIG"
    else
        DEFAULT_NAME="${PROJECT_NAME:-My Project}"
        cat > "$CONFIG" <<EOF
{
  "project_name": "$DEFAULT_NAME",
  "project_description": "Project using sdd-framework",
  "sdd_root": "docs/sdd",
  "project_root": ".",
  "paths": {
    "core": "docs/sdd/00_core",
    "execution": "docs/sdd/01_execution",
    "policies": "docs/sdd/02_policies",
    "operations": "docs/sdd/03_operations",
    "project_governance": "docs/sdd/04_project_governance",
    "templates": "docs/sdd/templates",
    "pre_sdd": "docs/sdd/03_operations/pre_sdd",
    "artifacts": {
      "design": "docs/sdd/artifacts/design",
      "specs": "docs/sdd/artifacts/specs",
      "tasks": "docs/sdd/artifacts/tasks",
      "audit_reports": "docs/sdd/artifacts/audit_reports",
      "features_for_specs": "docs/sdd/artifacts/features_for_specs",
      "adr": "docs/sdd/artifacts/adr"
    }
  },
  "stack": {
    "languages": [],
    "frameworks": [],
    "hardware": null
  },
  "surfaces": ["browser", "os_fs", "wiring", "network", "env_proxy"],
  "skills_registry": "docs/sdd/03_operations/skills/skills_registry.json",
  "migration": {
    "enabled": false,
    "source_stack": null,
    "target_stack": null,
    "legacy_path": null,
    "parity_required": true,
    "rollback_strategy": null
  }
}
EOF
    fi
    echo "[OK] Created $CONFIG"
fi

# --- Helper to extract paths from config ---
get_path() {
    jq -r "$1" "$CONFIG" 2>/dev/null || echo ""
}

resolve_repo_path() {
    local p="$1"
    if [[ -z "$p" || "$p" == "null" ]]; then
        return 1
    fi
    if [[ "$p" = /* ]]; then
        printf '%s\n' "$p"
    else
        printf '%s/%s\n' "$PROJECT_ROOT" "$p"
    fi
}

# --- Create artifact directories ---
DESIGN_DIR=$(get_path '.paths.artifacts.design // "docs/sdd/artifacts/design"')
SPECS_DIR=$(get_path '.paths.artifacts.specs // "docs/sdd/artifacts/specs"')
TASKS_DIR=$(get_path '.paths.artifacts.tasks // "docs/sdd/artifacts/tasks"')
AUDIT_DIR=$(get_path '.paths.artifacts.audit_reports // "docs/sdd/artifacts/audit_reports"')
FEATURES_DIR=$(get_path '.paths.artifacts.features_for_specs // "docs/sdd/artifacts/features_for_specs"')
ADR_DIR=$(get_path '.paths.artifacts.adr // "docs/sdd/artifacts/adr"')

for d in "$DESIGN_DIR" "$SPECS_DIR" "$TASKS_DIR" "$AUDIT_DIR" "$FEATURES_DIR" "$ADR_DIR"; do
    ABS_DIR=$(resolve_repo_path "$d")
    if [[ ! -d "$ABS_DIR" ]]; then
        mkdir -p "$ABS_DIR"
        echo "[OK] Created directory: $d"
    else
        echo "[SKIP] Directory already exists: $d"
    fi
done

# --- Create skills registry directory if referenced ---
SKILLS_REGISTRY=$(get_path '.skills_registry // empty')
if [[ -n "$SKILLS_REGISTRY" ]]; then
    SKILLS_DIR=$(dirname "$SKILLS_REGISTRY")
    ABS_SKILLS_DIR=$(resolve_repo_path "$SKILLS_DIR")
    if [[ ! -d "$ABS_SKILLS_DIR" ]]; then
        mkdir -p "$ABS_SKILLS_DIR"
        echo "[OK] Created directory: $SKILLS_DIR"
    fi
fi

# --- Optional sample feature ---
if [[ "$CREATE_SAMPLE" == "--sample" ]]; then
    FEATURES_ABS=$(resolve_repo_path "$FEATURES_DIR")
    SAMPLE_PATH="$FEATURES_ABS/feat-001-example.json"
    SAMPLE_DISPLAY="$FEATURES_DIR/feat-001-example.json"
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
        echo "[OK] Created sample feature: $SAMPLE_DISPLAY"
    fi
fi

echo ""
echo "SDD initialization complete."
echo "Next steps:"
echo "  1. Review and customize docs/sdd/sdd.config.json"
echo "  2. Read docs/sdd/AGENTS.md and docs/sdd/00_core/SDD_RUNTIME.md"
echo "  3. Create your first feature record in $FEATURES_DIR/"
