#requires -Version 5.1
<#
.SYNOPSIS
    Initialize SDD artifact directories and configuration for a new project.

.DESCRIPTION
    Creates the artifact directory structure and validates sdd.config.json.
    Optionally creates a sample feature record.

.EXAMPLE
    .\init-sdd.ps1
    .\init-sdd.ps1 -ProjectName "MyProject" -CreateSampleFeature
#>
[CmdletBinding()]
param(
    [string]$ProjectName = "",
    [switch]$CreateSampleFeature
)

$ConfigPath = "sdd.config.json"

# --- Validate or create config ---
if (Test-Path $ConfigPath) {
    Write-Host "[OK] Found $ConfigPath" -ForegroundColor Green
    try {
        $Config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
    } catch {
        Write-Error "Invalid JSON in $ConfigPath"
        exit 1
    }
} else {
    Write-Host "[INFO] $ConfigPath not found. Creating default..." -ForegroundColor Yellow
    $DefaultName = if ($ProjectName) { $ProjectName } else { "My Project" }
    $Config = @{
        project_name = $DefaultName
        project_description = "Project using sdd-framework"
        sdd_root = "."
        paths = @{
            core = "00_core"
            execution = "01_execution"
            policies = "02_policies"
            operations = "03_operations"
            templates = "templates"
            artifacts = @{
                design = "artifacts/design"
                specs = "artifacts/specs"
                tasks = "artifacts/tasks"
                audit_reports = "artifacts/audit_reports"
                features_for_specs = "artifacts/features_for_specs"
            }
        }
        stack = @{
            languages = @()
            frameworks = @()
            hardware = $null
        }
        surfaces = @("browser", "os_fs", "wiring", "network", "env_proxy")
        skills_registry = "03_operations/skills/skills_registry.json"
    }
    $Config | ConvertTo-Json -Depth 5 | Set-Content $ConfigPath -Encoding UTF8
    Write-Host "[OK] Created $ConfigPath" -ForegroundColor Green
}

# --- Create artifact directories ---
$ArtifactRoot = if ($Config.paths.artifacts) { $Config.paths.artifacts } else { $Config.paths }

$Dirs = @()
if ($ArtifactRoot.design) { $Dirs += $ArtifactRoot.design }
if ($ArtifactRoot.specs) { $Dirs += $ArtifactRoot.specs }
if ($ArtifactRoot.tasks) { $Dirs += $ArtifactRoot.tasks }
if ($ArtifactRoot.audit_reports) { $Dirs += $ArtifactRoot.audit_reports }
if ($ArtifactRoot.features_for_specs) { $Dirs += $ArtifactRoot.features_for_specs }

foreach ($d in $Dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
        Write-Host "[OK] Created directory: $d" -ForegroundColor Green
    } else {
        Write-Host "[SKIP] Directory already exists: $d" -ForegroundColor DarkGray
    }
}

# --- Create skills registry directory if referenced ---
if ($Config.skills_registry) {
    $SkillsDir = Split-Path $Config.skills_registry -Parent
    if ($SkillsDir -and -not (Test-Path $SkillsDir)) {
        New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
        Write-Host "[OK] Created directory: $SkillsDir" -ForegroundColor Green
    }
}

# --- Optional sample feature ---
if ($CreateSampleFeature) {
    $FeaturesDir = if ($ArtifactRoot.features_for_specs) { $ArtifactRoot.features_for_specs } else { "artifacts/features_for_specs" }
    $SamplePath = Join-Path $FeaturesDir "feat-001-example.json"
    if (-not (Test-Path $SamplePath)) {
        $Sample = @{
            id = "feat-001"
            type = "SYSTEM_SPEC"
            state = "DESIGN"
            title = "Example feature"
            created_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            updated_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            design_path = if ($ArtifactRoot.design) { "$($ArtifactRoot.design)/feat-001-example.md" } else { "artifacts/design/feat-001-example.md" }
        }
        $Sample | ConvertTo-Json -Depth 3 | Set-Content $SamplePath -Encoding UTF8
        Write-Host "[OK] Created sample feature: $SamplePath" -ForegroundColor Green
    }
}

Write-Host "`nSDD initialization complete." -ForegroundColor Cyan
Write-Host "Next steps:"
Write-Host "  1. Review and customize sdd.config.json"
Write-Host "  2. Read AGENTS.md and 00_core/SDD_RUNTIME.md"
Write-Host "  3. Create your first feature record in $($ArtifactRoot.features_for_specs)/"
