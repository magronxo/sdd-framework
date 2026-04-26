package doctor

import (
	"encoding/json"
	"os"
	"path/filepath"
)

var (
	ErrGovernanceRead     = &GovernanceError{Code: "G001", Message: "feature record JSON parse error"}
	ErrMissingRequired    = &GovernanceError{Code: "G002", Message: "missing required field"}
	ErrValidationGate     = &GovernanceError{Code: "G003", Message: "validation gate violation: state requires validation_result=PASS"}
	ErrInvalidState       = &GovernanceError{Code: "G004", Message: "invalid or unknown state"}
	ErrInvalidType        = &GovernanceError{Code: "G005", Message: "invalid field type: must be non-empty string"}
)

type GovernanceError struct {
	Code    string
	Message string
}

func (e *GovernanceError) Error() string {
	return e.Message
}

type FeatureRecord struct {
	ID                string `json:"id"`
	Type              string `json:"type"`
	State             string `json:"state"`
	Title             string `json:"title"`
	CreatedAt         string `json:"created_at"`
	UpdatedAt         string `json:"updated_at"`
	ValidationResult  string `json:"validation_result,omitempty"`
}

var allowedStates = map[string]bool{
	"DESIGN":     true,
	"SPEC":       true,
	"VALIDATION": true,
	"TASKS":      true,
	"IMPLEMENT":  true,
	"VERIFY":     true,
	"AUDIT":     true,
	"ARCHIVE":    true,
}

var statesRequiringValidationGate = map[string]bool{
	"TASKS":     true,
	"IMPLEMENT": true,
	"VERIFY":    true,
	"AUDIT":     true,
	"ARCHIVE":   true,
}

func (d *Doctor) checkGovernance() {
	recordsPath := filepath.Join(d.targetPath, "artifacts", "features_for_specs")

	entries, err := os.ReadDir(recordsPath)
	if err != nil {
		if os.IsNotExist(err) {
			d.addFinding("governance", SeverityPASS, "OK", "no feature records found")
			return
		}
		d.addFinding("governance", SeverityFAIL, ErrGovernanceRead.Code, ErrGovernanceRead.Error())
		return
	}

	foundRecords := false
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if filepath.Ext(entry.Name()) != ".json" {
			continue
		}
		foundRecords = true
		d.checkFeatureRecord(filepath.Join(recordsPath, entry.Name()))
	}

	if !foundRecords {
		d.addFinding("governance", SeverityPASS, "OK", "no feature records found")
	}
}

func (d *Doctor) checkFeatureRecord(filePath string) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		d.addFinding("governance:"+filepath.Base(filePath), SeverityFAIL, ErrGovernanceRead.Code, ErrGovernanceRead.Error())
		return
	}

	var record FeatureRecord
	if err := json.Unmarshal(data, &record); err != nil {
		d.addFinding("governance:"+filepath.Base(filePath), SeverityFAIL, ErrGovernanceRead.Code, ErrGovernanceRead.Error())
		return
	}

	relPath, _ := filepath.Rel(d.targetPath, filePath)

	if record.ID == "" {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrMissingRequired.Code, "missing required field: id")
	}
	if record.Type == "" {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrMissingRequired.Code, "missing required field: type")
	}
	if record.State == "" {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrMissingRequired.Code, "missing required field: state")
	} else if !allowedStates[record.State] {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrInvalidState.Code, "invalid state: "+record.State)
	}
	if record.Title == "" {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrMissingRequired.Code, "missing required field: title")
	}
	if record.CreatedAt == "" {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrMissingRequired.Code, "missing required field: created_at")
	}
	if record.UpdatedAt == "" {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrMissingRequired.Code, "missing required field: updated_at")
	}

	if record.Type != "" && record.Type == "" {
		d.addFinding("governance:"+relPath, SeverityFAIL, ErrInvalidType.Code, ErrInvalidType.Error())
	}

	if record.State != "" && statesRequiringValidationGate[record.State] {
		if record.ValidationResult != "PASS" {
			d.addFinding("governance:"+relPath, SeverityFAIL, ErrValidationGate.Code, "validation gate violation: state "+record.State+" requires validation_result=PASS")
		}
	}

	if record.ID != "" && record.Type != "" && record.State != "" && record.Title != "" && record.CreatedAt != "" && record.UpdatedAt != "" {
		if record.State == "" || !statesRequiringValidationGate[record.State] || record.ValidationResult == "PASS" {
			d.addFinding("governance:"+relPath, SeverityPASS, "OK", "governance valid")
		}
	}
}