package doctor

import (
	"os"
	"path/filepath"
	"strings"
)

const (
	ErrSpecMissingSection     = "E010"
	ErrValidationReportMissing = "E011"
	ErrAuditReportMissing     = "E012"
	ErrCrossRefMismatch      = "E013"
	WarnOptionalMissing       = "W003"
	WarnNoFilesFound          = "W004"
)

var (
	specRequiredSections = []string{
		"Introduction",
		"Context",
		"Requirements",
		"Inputs",
		"Outputs",
		"Error Codes",
		"Acceptance Criteria",
		"Integration Surfaces",
	}

	specSectionEither = []string{
		"Goals",
		"Objectives",
	}

	validationReportRequiredSections = []string{
		"Completeness",
		"Determinism",
		"Traceability",
		"Implementability",
		"Validation Decision",
		"Feature Record",
	}

	auditReportRequiredSections = []string{
		"Spec-Code Alignment",
		"Implementation Scope",
		"Test Coverage",
		"Final Assessment",
		"Audit Decision",
	}
)

func (d *Doctor) checkEnvelopes() {
	d.checkSpecEnvelopes()
	d.checkValidationReportEnvelopes()
	d.checkAuditReportEnvelopes()
}

func (d *Doctor) checkSpecEnvelopes() {
	specsPath := filepath.Join(d.targetPath, "artifacts", "specs")

	entries, err := os.ReadDir(specsPath)
	if err != nil {
		if os.IsNotExist(err) {
			d.addFinding("envelope:specs", SeverityWARN, WarnNoFilesFound, "no matching artifact files: artifacts/specs")
			return
		}
		d.addFinding("envelope:specs", SeverityFAIL, ErrSpecMissingSection, "cannot read artifacts/specs directory")
		return
	}

	foundFiles := false
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if filepath.Ext(entry.Name()) != ".md" {
			continue
		}
		foundFiles = true
		d.checkSpecEnvelope(filepath.Join(specsPath, entry.Name()))
	}

	if !foundFiles {
		d.addFinding("envelope:specs", SeverityWARN, WarnNoFilesFound, "no matching artifact files: artifacts/specs")
	}
}

func (d *Doctor) checkSpecEnvelope(filePath string) {
	content, err := os.ReadFile(filePath)
	if err != nil {
		d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityFAIL, ErrSpecMissingSection, "cannot read spec file")
		return
	}

	missing := findMissingSpecSections(string(content))
	if len(missing) > 0 {
		for _, m := range missing {
			d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityFAIL, ErrSpecMissingSection, "spec missing required section: "+m)
		}
		return
	}

	d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityPASS, "OK", "spec envelope valid")
}

func (d *Doctor) checkValidationReportEnvelopes() {
	reportsPath := filepath.Join(d.targetPath, "artifacts", "validation_reports")

	entries, err := os.ReadDir(reportsPath)
	if err != nil {
		if os.IsNotExist(err) {
			d.addFinding("envelope:validation_reports", SeverityWARN, WarnNoFilesFound, "no matching artifact files: artifacts/validation_reports")
			return
		}
		d.addFinding("envelope:validation_reports", SeverityFAIL, ErrValidationReportMissing, "cannot read artifacts/validation_reports directory")
		return
	}

	foundFiles := false
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if filepath.Ext(entry.Name()) != ".md" {
			continue
		}
		foundFiles = true
		d.checkValidationReportEnvelope(filepath.Join(reportsPath, entry.Name()))
	}

	if !foundFiles {
		d.addFinding("envelope:validation_reports", SeverityWARN, WarnNoFilesFound, "no matching artifact files: artifacts/validation_reports")
	}
}

func (d *Doctor) checkValidationReportEnvelope(filePath string) {
	content, err := os.ReadFile(filePath)
	if err != nil {
		d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityFAIL, ErrValidationReportMissing, "cannot read validation report file")
		return
	}

	missing := findMissingSections(string(content), validationReportRequiredSections)
	if len(missing) > 0 {
		for _, m := range missing {
			d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityFAIL, ErrValidationReportMissing, "validation report missing required section: "+m)
		}
		return
	}

	d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityPASS, "OK", "validation report envelope valid")
}

func (d *Doctor) checkAuditReportEnvelopes() {
	reportsPath := filepath.Join(d.targetPath, "artifacts", "audit_reports")

	entries, err := os.ReadDir(reportsPath)
	if err != nil {
		if os.IsNotExist(err) {
			d.addFinding("envelope:audit_reports", SeverityWARN, WarnNoFilesFound, "no matching artifact files: artifacts/audit_reports")
			return
		}
		d.addFinding("envelope:audit_reports", SeverityFAIL, ErrAuditReportMissing, "cannot read artifacts/audit_reports directory")
		return
	}

	foundFiles := false
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if filepath.Ext(entry.Name()) != ".md" {
			continue
		}
		foundFiles = true
		d.checkAuditReportEnvelope(filepath.Join(reportsPath, entry.Name()))
	}

	if !foundFiles {
		d.addFinding("envelope:audit_reports", SeverityWARN, WarnNoFilesFound, "no matching artifact files: artifacts/audit_reports")
	}
}

func (d *Doctor) checkAuditReportEnvelope(filePath string) {
	content, err := os.ReadFile(filePath)
	if err != nil {
		d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityFAIL, ErrAuditReportMissing, "cannot read audit report file")
		return
	}

	missing := findMissingSections(string(content), auditReportRequiredSections)
	if len(missing) > 0 {
		for _, m := range missing {
			d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityFAIL, ErrAuditReportMissing, "audit report missing required section: "+m)
		}
		return
	}

	d.addFinding("envelope:"+relPath(d.targetPath, filePath), SeverityPASS, "OK", "audit report envelope valid")
}

func findMissingSections(content string, required []string) []string {
	var missing []string
	upperContent := strings.ToUpper(content)
	for _, section := range required {
		if !strings.Contains(upperContent, strings.ToUpper(section)) {
			missing = append(missing, section)
		}
	}
	return missing
}

func findMissingSpecSections(content string) []string {
	var missing []string
	upperContent := strings.ToUpper(content)

	for _, section := range specRequiredSections {
		if !strings.Contains(upperContent, strings.ToUpper(section)) {
			missing = append(missing, section)
		}
	}

	hasGoalsOrObjectives := false
	for _, section := range specSectionEither {
		if strings.Contains(upperContent, strings.ToUpper(section)) {
			hasGoalsOrObjectives = true
			break
		}
	}
	if !hasGoalsOrObjectives {
		missing = append(missing, "Goals or Objectives")
	}

	return missing
}

func relPath(targetPath, filePath string) string {
	rel, err := filepath.Rel(targetPath, filePath)
	if err != nil {
		return filePath
	}
	return rel
}

func CheckSpecEnvelope(content string) (bool, []string) {
	missing := findMissingSpecSections(content)
	return len(missing) == 0, missing
}

func CheckValidationReportEnvelope(content string) (bool, []string) {
	missing := findMissingSections(content, validationReportRequiredSections)
	return len(missing) == 0, missing
}

func CheckAuditReportEnvelope(content string) (bool, []string) {
	missing := findMissingSections(content, auditReportRequiredSections)
	return len(missing) == 0, missing
}

func CheckCrossReference(specPath string, designPath string) bool {
	_, err := os.Stat(designPath)
	return err == nil
}