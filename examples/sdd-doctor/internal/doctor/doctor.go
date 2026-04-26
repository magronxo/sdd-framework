package doctor

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

const (
	ExitCodeOK        = 0
	ExitCodeFindings  = 1
	ExitCodeRuntime   = 2
)

type Config struct {
	Version         string `json:"version"`
	Name            string `json:"name"`
	Paths           Paths  `json:"paths"`
	FrameworkVersion string `json:"framework_version"`
}

type Paths struct {
	Root      string `json:"root"`
	Core      string `json:"core"`
	Artifacts string `json:"artifacts"`
	Policies  string `json:"policies"`
	Governance string `json:"governance"`
}

type Finding struct {
	Location string
	Severity Severity
	Code     string
	Message  string
}

type Severity string

const (
	SeverityPASS     Severity = "PASS"
	SeverityWARN     Severity = "WARN"
	SeverityFAIL     Severity = "FAIL"
	SeverityBLOCKED  Severity = "BLOCKED"
)

var (
	ErrPathNotExist     = &RuntimeError{Code: "E001", Message: "target path does not exist"}
	ErrPathNotReadable  = &RuntimeError{Code: "E003", Message: "target path is not readable"}
	ErrConfigNotFound   = &RuntimeError{Code: "E004", Message: "sdd.config.json not found"}
	ErrConfigParse      = &RuntimeError{Code: "E002", Message: "sdd.config.json parse error"}
)

type RuntimeError struct {
	Code    string
	Message string
}

func (e *RuntimeError) Error() string {
	return fmt.Sprintf("[%s] %s", e.Code, e.Message)
}

type Doctor struct {
	targetPath string
	findings   []Finding
	errors     []*RuntimeError
}

func New(targetPath string) *Doctor {
	return &Doctor{targetPath: targetPath}
}

func Run(args []string) int {
	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "Usage: sdd-doctor check <path>")
		return ExitCodeRuntime
	}

	if args[0] != "check" {
		fmt.Fprintf(os.Stderr, "Usage: sdd-doctor check <path>\n")
		return ExitCodeRuntime
	}

	if len(args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: sdd-doctor check <path>")
		return ExitCodeRuntime
	}

	targetPath := args[1]

	absPath, err := filepath.Abs(targetPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: cannot resolve path: %v\n", err)
		return ExitCodeRuntime
	}

	info, err := os.Stat(absPath)
	if err != nil {
		if os.IsNotExist(err) {
			fmt.Fprintf(os.Stderr, "Error: %s\n", ErrPathNotExist)
		} else {
			fmt.Fprintf(os.Stderr, "Error: %s\n", ErrPathNotReadable)
		}
		return ExitCodeRuntime
	}

	if !info.IsDir() {
		fmt.Fprintf(os.Stderr, "Error: target must be a directory\n")
		return ExitCodeRuntime
	}

	doctor := New(absPath)
	doctor.Run()

	doctor.Report(os.Stdout)

	if doctor.HasBlockingFindings() {
		return ExitCodeFindings
	}

	return ExitCodeOK
}

func (d *Doctor) Run() {
	d.checkConfig()
	d.checkCoreDirectories()
	d.checkArtifactDirectories()
	d.checkGovernance()
	d.checkEnvelopes()
}

func (d *Doctor) checkConfig() {
	configPath := filepath.Join(d.targetPath, "sdd.config.json")

	data, err := os.ReadFile(configPath)
	if err != nil {
		if os.IsNotExist(err) {
			d.addFinding("sdd.config.json", SeverityFAIL, "E004", "sdd.config.json not found")
			return
		}
		d.errors = append(d.errors, ErrConfigParse)
		d.addFinding("sdd.config.json", SeverityFAIL, "E002", "sdd.config.json parse error")
		return
	}

	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		d.errors = append(d.errors, ErrConfigParse)
		d.addFinding("sdd.config.json", SeverityFAIL, "E002", "sdd.config.json parse error")
		return
	}

	if cfg.Paths.Root == "" {
		d.addFinding("sdd.config.json/paths/root", SeverityFAIL, "E005", "paths.root field missing or empty")
	}

	if cfg.FrameworkVersion == "" {
		d.addFinding("sdd.config.json/framework_version", SeverityFAIL, "E006", "framework_version field missing or empty")
	}

	if len(d.errors) == 0 {
		d.addFinding("sdd.config.json", SeverityPASS, "OK", "sdd.config.json valid")
	}
}

func (d *Doctor) checkCoreDirectories() {
	requiredDirs := []string{
		"00_core",
		"02_policies",
		"03_projects",
		"04_project_governance",
		"05_workflows",
	}

	optional := map[string]bool{
		"01_docs":          false,
		"examples":         false,
		".github":          false,
	}

	allRequired := append(requiredDirs, "artifacts")
	for _, dir := range allRequired {
		fullPath := filepath.Join(d.targetPath, dir)
		if _, err := os.Stat(fullPath); os.IsNotExist(err) {
			d.addFinding("core:"+dir, SeverityFAIL, "E007", "required directory missing: "+dir)
		} else {
			d.addFinding("core:"+dir, SeverityPASS, "OK", "directory exists: "+dir)
		}
	}

	for dir, warnIfMissing := range optional {
		fullPath := filepath.Join(d.targetPath, dir)
		if _, err := os.Stat(fullPath); os.IsNotExist(err) {
			if warnIfMissing {
				d.addFinding("core:"+dir, SeverityWARN, "W001", "optional directory missing: "+dir)
			}
		} else {
			d.addFinding("core:"+dir, SeverityPASS, "OK", "directory exists: "+dir)
		}
	}
}

func (d *Doctor) checkArtifactDirectories() {
	required := []string{
		"design",
		"specs",
		"validation_reports",
		"tasks",
	}

	optional := map[string]bool{
		"features_for_specs": true,
		"deltas":             true,
	}

	artifactsPath := filepath.Join(d.targetPath, "artifacts")
	if _, err := os.Stat(artifactsPath); os.IsNotExist(err) {
		d.addFinding("artifacts", SeverityFAIL, "E008", "artifacts directory missing")
		return
	}

	d.addFinding("artifacts", SeverityPASS, "OK", "artifacts directory exists")

	for _, dir := range required {
		fullPath := filepath.Join(artifactsPath, dir)
		if _, err := os.Stat(fullPath); os.IsNotExist(err) {
			d.addFinding("artifacts/"+dir, SeverityFAIL, "E009", "required artifacts subdirectory missing: "+dir)
		} else {
			d.addFinding("artifacts/"+dir, SeverityPASS, "OK", "artifacts/"+dir+" exists")
		}
	}

	for dir, warnIfMissing := range optional {
		fullPath := filepath.Join(artifactsPath, dir)
		if _, err := os.Stat(fullPath); os.IsNotExist(err) {
			if warnIfMissing {
				d.addFinding("artifacts/"+dir, SeverityWARN, "W002", "optional artifacts subdirectory missing: "+dir)
			}
		} else {
			d.addFinding("artifacts/"+dir, SeverityPASS, "OK", "artifacts/"+dir+" exists")
		}
	}
}

func (d *Doctor) addFinding(location string, severity Severity, code string, message string) {
	d.findings = append(d.findings, Finding{
		Location: location,
		Severity: severity,
		Code:     code,
		Message:  message,
	})
}

func (d *Doctor) Report(output *os.File) {
	fmt.Fprintln(output, "")
	fmt.Fprintln(output, "=== SDD Doctor Report ===")
	fmt.Fprintln(output, "")

	if len(d.errors) > 0 {
		fmt.Fprintln(output, "Runtime Errors:")
		for _, err := range d.errors {
			fmt.Fprintf(output, "  [%s] %s\n", err.Code, err.Message)
		}
		fmt.Fprintln(output, "")
	}

	if len(d.findings) == 0 {
		fmt.Fprintln(output, "No findings.")
		return
	}

	fmt.Fprintln(output, "Findings:")
	fmt.Fprintln(output, "")
	for _, f := range d.findings {
		icon := iconForSeverity(f.Severity)
		fmt.Fprintf(output, "  %s [%s] %s: %s\n", icon, f.Severity, f.Location, f.Message)
	}

	fmt.Fprintln(output, "")
	counts := d.countBySeverity()
	fmt.Fprintf(output, "Summary: %d PASS, %d WARN, %d FAIL, %d BLOCKED\n",
		counts[SeverityPASS], counts[SeverityWARN], counts[SeverityFAIL], counts[SeverityBLOCKED])
}

func iconForSeverity(s Severity) string {
	switch s {
	case SeverityPASS:
		return "✓"
	case SeverityWARN:
		return "⚠"
	case SeverityFAIL:
		return "✗"
	case SeverityBLOCKED:
		return "⊗"
	default:
		return "?"
	}
}

func (d *Doctor) countBySeverity() map[Severity]int {
	counts := map[Severity]int{
		SeverityPASS:     0,
		SeverityWARN:     0,
		SeverityFAIL:     0,
		SeverityBLOCKED:  0,
	}
	for _, f := range d.findings {
		counts[f.Severity]++
	}
	return counts
}

func (d *Doctor) HasBlockingFindings() bool {
	for _, f := range d.findings {
		if f.Severity == SeverityFAIL || f.Severity == SeverityBLOCKED {
			return true
		}
	}
	return false
}