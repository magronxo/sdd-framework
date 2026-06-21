#requires -Version 5.1
<#
.SYNOPSIS
    Initialize an installed SDD instance under docs/sdd/.

.DESCRIPTION
    Creates the artifact directory structure and validates docs/sdd/sdd.config.json.
    Optionally creates a sample feature record.

.EXAMPLE
    .\docs\sdd\init-sdd.ps1
    .\docs\sdd\init-sdd.ps1 -ProjectName "MyProject" -CreateSampleFeature
#>
[CmdletBinding()]
param(
    [string]$ProjectName = "",
    [switch]$CreateSampleFeature
)

$ScriptDir = Split-Path -Parent $PSCommandPath
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$ConfigPath = Join-Path $ScriptDir "sdd.config.json"
$TemplateConfigPath = Join-Path $ScriptDir "templates\sdd.config.json"

function Resolve-RepoPath {
    param([string]$PathValue)
    if (-not $PathValue) { return $null }
    if ([System.IO.Path]::IsPathRooted($PathValue)) { return $PathValue }
    return (Join-Path $ProjectRoot $PathValue)
}

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
    if (Test-Path $TemplateConfigPath) {
        Copy-Item $TemplateConfigPath $ConfigPath
        $Config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
    } else {
        $DefaultName = if ($ProjectName) { $ProjectName } else { "My Project" }
        $Config = @{
            project_name = $DefaultName
            project_description = "Project using sdd-framework"
            sdd_root = "docs/sdd"
            project_root = "."
            paths = @{
                core = "docs/sdd/00_core"
                execution = "docs/sdd/01_execution"
                policies = "docs/sdd/02_policies"
                operations = "docs/sdd/03_operations"
                project_governance = "docs/sdd/04_project_governance"
                templates = "docs/sdd/templates"
                pre_sdd = "docs/sdd/03_operations/pre_sdd"
                artifacts = @{
                    design = "docs/sdd/artifacts/design"
                    specs = "docs/sdd/artifacts/specs"
                    tasks = "docs/sdd/artifacts/tasks"
                    audit_reports = "docs/sdd/artifacts/audit_reports"
                    features_for_specs = "docs/sdd/artifacts/features_for_specs"
                    adr = "docs/sdd/artifacts/adr"
                }
            }
            stack = @{
                languages = @()
                frameworks = @()
                hardware = $null
            }
            surfaces = @("browser", "os_fs", "wiring", "network", "env_proxy")
            skills_registry = "docs/sdd/03_operations/skills/skills_registry.json"
            migration = @{
                enabled = $false
                source_stack = $null
                target_stack = $null
                legacy_path = $null
                parity_required = $true
                rollback_strategy = $null
            }
        }
        $Config | ConvertTo-Json -Depth 8 | Set-Content $ConfigPath -Encoding UTF8
    }
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
if ($ArtifactRoot.adr) { $Dirs += $ArtifactRoot.adr }

foreach ($d in $Dirs) {
    $AbsDir = Resolve-RepoPath $d
    if (-not (Test-Path $AbsDir)) {
        New-Item -ItemType Directory -Path $AbsDir -Force | Out-Null
        Write-Host "[OK] Created directory: $d" -ForegroundColor Green
    } else {
        Write-Host "[SKIP] Directory already exists: $d" -ForegroundColor DarkGray
    }
}

# --- Create skills registry directory if referenced ---
if ($Config.skills_registry) {
    $SkillsDir = Split-Path $Config.skills_registry -Parent
    $AbsSkillsDir = Resolve-RepoPath $SkillsDir
    if ($SkillsDir -and -not (Test-Path $AbsSkillsDir)) {
        New-Item -ItemType Directory -Path $AbsSkillsDir -Force | Out-Null
        Write-Host "[OK] Created directory: $SkillsDir" -ForegroundColor Green
    }
}

# --- Optional sample feature ---
if ($CreateSampleFeature) {
    $FeaturesDir = if ($ArtifactRoot.features_for_specs) { $ArtifactRoot.features_for_specs } else { "docs/sdd/artifacts/features_for_specs" }
    $FeaturesAbs = Resolve-RepoPath $FeaturesDir
    $SamplePath = Join-Path $FeaturesAbs "feat-001-example.json"
    if (-not (Test-Path $SamplePath)) {
        $Sample = @{
            id = "feat-001"
            type = "SYSTEM_SPEC"
            state = "DESIGN"
            title = "Example feature"
            created_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            updated_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            design_path = if ($ArtifactRoot.design) { "$($ArtifactRoot.design)/feat-001-example.md" } else { "docs/sdd/artifacts/design/feat-001-example.md" }
        }
        $Sample | ConvertTo-Json -Depth 3 | Set-Content $SamplePath -Encoding UTF8
        Write-Host "[OK] Created sample feature: $FeaturesDir/feat-001-example.json" -ForegroundColor Green
    }
}

Write-Host "`nSDD initialization complete." -ForegroundColor Cyan
Write-Host "Next steps:"
Write-Host "  1. Review and customize docs/sdd/sdd.config.json"
Write-Host "  2. Read docs/sdd/AGENTS.md and docs/sdd/00_core/SDD_RUNTIME.md"
Write-Host "  3. Create your first feature record in $($ArtifactRoot.features_for_specs)/"
