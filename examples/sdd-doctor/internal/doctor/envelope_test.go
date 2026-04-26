package doctor

import (
	"testing"
)

func TestCheckSpecEnvelope_AllSectionsPresent(t *testing.T) {
	content := `
# Specification: Test Feature

## 1. Introduction

### Context
This is a test spec.

### Goals
1. Goal one
2. Goal two

## 2. Requirements

RF-01: Test requirement

## 3. Inputs and Outputs

Input: test input
Output: test output

## 4. Error Codes

E001: Test error

## 5. Acceptance Criteria

Scenario: Test
  Given a test
  When I run
  Then result is

## 6. Integration Surfaces

| Surface | Active |
|---------|--------|
| os_fs | Yes |
`
	valid, missing := CheckSpecEnvelope(content)
	if !valid {
		t.Errorf("expected valid spec, got missing sections: %v", missing)
	}
	if len(missing) != 0 {
		t.Errorf("expected no missing sections, got: %v", missing)
	}
}

func TestCheckSpecEnvelope_MissingSection(t *testing.T) {
	content := `
# Specification: Test Feature

## 1. Introduction

### Context
This is a test spec.

### Goals
1. Goal one

## 2. Requirements

RF-01: Test requirement

## 3. Inputs and Outputs

Input: test input
Output: test output

## 4. Error Codes

E001: Test error

## 6. Integration Surfaces

| Surface | Active |
|---------|--------|
| os_fs | Yes |
`
	valid, missing := CheckSpecEnvelope(content)
	if valid {
		t.Error("expected invalid spec, got valid")
	}
	if len(missing) == 0 {
		t.Error("expected missing sections, got none")
	}
	foundAcceptanceCriteria := false
	for _, m := range missing {
		if m == "Acceptance Criteria" {
			foundAcceptanceCriteria = true
			break
		}
	}
	if !foundAcceptanceCriteria {
		t.Errorf("expected 'Acceptance Criteria' in missing sections, got: %v", missing)
	}
}

func TestCheckValidationReportEnvelope_AllSectionsPresent(t *testing.T) {
	content := `
# Validation Report: Test

## 1. Completeness Checklist
- All requirements defined

## 2. Determinism Checklist
- No undefined behavior

## 3. Traceability Checklist
- RFs map to acceptance criteria

## 4. Implementability Checklist
- Implementation feasible

## 5. Validation Decision

PASS

## 6. Feature Record Update

{"state": "PASS"}
`
	valid, missing := CheckValidationReportEnvelope(content)
	if !valid {
		t.Errorf("expected valid report, got missing sections: %v", missing)
	}
	if len(missing) != 0 {
		t.Errorf("expected no missing sections, got: %v", missing)
	}
}

func TestCheckValidationReportEnvelope_MissingSection(t *testing.T) {
	content := `
# Validation Report: Test

## 1. Determinism Checklist
- No undefined behavior

## 2. Traceability Checklist
- RFs map to acceptance criteria

## 3. Implementability Checklist
- Implementation feasible

## 4. Validation Decision

PASS
`
	valid, missing := CheckValidationReportEnvelope(content)
	if valid {
		t.Error("expected invalid report, got valid")
	}
	if len(missing) == 0 {
		t.Error("expected missing sections, got none")
	}
	foundCompleteness := false
	for _, m := range missing {
		if m == "Completeness" {
			foundCompleteness = true
			break
		}
	}
	if !foundCompleteness {
		t.Errorf("expected 'Completeness' in missing sections, got: %v", missing)
	}
}

func TestCheckAuditReportEnvelope_AllSectionsPresent(t *testing.T) {
	content := `
# Audit Report: Test

## 1. Spec-Code Alignment

All RFs implemented as specified.

## 2. Implementation Scope Check

Scope not exceeded.

## 3. Test Coverage Analysis

All tests pass.

## 4. Final Assessment

Implementation correct.

## 5. Audit Decision

PASS
`
	valid, missing := CheckAuditReportEnvelope(content)
	if !valid {
		t.Errorf("expected valid report, got missing sections: %v", missing)
	}
	if len(missing) != 0 {
		t.Errorf("expected no missing sections, got: %v", missing)
	}
}

func TestCheckAuditReportEnvelope_MissingSection(t *testing.T) {
	content := `
# Audit Report: Test

## 1. Spec-Code Alignment

All RFs implemented as specified.

## 2. Implementation Scope Check

Scope not exceeded.

## 3. Test Coverage Analysis

All tests pass.
`
	valid, missing := CheckAuditReportEnvelope(content)
	if valid {
		t.Error("expected invalid report, got valid")
	}
	if len(missing) == 0 {
		t.Error("expected missing sections, got none")
	}
	foundAuditDecision := false
	for _, m := range missing {
		if m == "Audit Decision" {
			foundAuditDecision = true
			break
		}
	}
	if !foundAuditDecision {
		t.Errorf("expected 'Audit Decision' in missing sections, got: %v", missing)
	}
}

func TestCheckCrossReferences_ValidReference(t *testing.T) {
	result := CheckCrossReference("spec.md", "doctor.go")
	if !result {
		t.Error("expected valid cross-reference, got false")
	}
}

func TestCheckCrossReferences_BrokenReference(t *testing.T) {
	result := CheckCrossReference("spec.md", "artifacts/design/nonexistent.md")
	if result {
		t.Error("expected broken cross-reference to return false, got true")
	}
}