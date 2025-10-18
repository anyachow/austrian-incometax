# Competency Questions for Austrian Tax Residents Income Tax Ontology

## Overview

Competency Questions (CQs) are a set of natural language questions that an ontology must be able to address [1]. They are widely used in ontology engineering as a way to define the scope and purpose of the ontology and to ensure that the ontology captures the essential domain knowledge [2]. They also guide the concepts and relationships that the ontology should contain [3]. 

This document presents the competency questions for the Austrian Tax Residents Income Tax Ontology, which models income tax filing obligations for Austrian tax residents under the Austrian Income Tax Act (Einkommensteuergesetz - EStG) for tax year 2025.

---

## Core Competency Questions

### CQ1: What income thresholds and type determine filing obligations?

**Purpose:** Identify the specific monetary thresholds and income types that trigger different tax filing requirements.

**For Example:**
- EUR 730 threshold for non-wage income (triggers Mandatory E1 filing)
- EUR 13,308 threshold for wage income (when employment tax not filed, triggers Mandatory L1)
- EUR 14,517 threshold for wage income (with specific conditions, triggers Mandatory L1)
- Income types: wage income (§25 EStG), non-wage income (self-employment, rental, investment, etc.)
- Exclusion: fully taxed capital yields

**Ontology Coverage:**
- Properties: `hasAnnualWageIncome`, `hasNonWageIncome`
- Classes: `MandatoryE1Filer`, `MandatoryL1Filer`

---

### CQ2: What are the tax filing obligation types of taxpayer?

**Purpose:** Determine all possible filing obligation categories a taxpayer can be classified into.

**Expected Answer Elements:**
- Mandatory E1 Filing (Form E1 required by law)
- Mandatory L1 Filing (Form L1 required by law)
- Voluntary L1 Filing (Form L1 beneficial but not required)

**Ontology Coverage:**
- Classes: `MandatoryE1Filer`, `MandatoryL1Filer`, `VoluntaryL1Filer`
- Base class: `AustrianResident`

---

### CQ3: Which tax form does the taxpayer need?

**Purpose:** Identify the specific tax form(s) a taxpayer must file or may benefit from filing.

**Ontology Coverage:**
- Implicit in class names: `MandatoryE1Filer` → Form E1, `MandatoryL1Filer` / `VoluntaryL1Filer` → Form L1
- Classification through reasoning determines form requirements

---

### CQ4: What are the properties that trigger the mandatory filing obligation?

**Purpose:** Identify all conditions/properties that legally require a taxpayer to file a tax return.

**For Mandatory E1:**
- `hasNonWageIncome` > EUR 730

**For Mandatory L1:**
- `hasAnnualWageIncome` > EUR 14,517 AND any of:
  - `hasMultipleEmploymentsWithoutJointTax` = true
  - `hasIncorrectCommuterAllowance` = true
  - `hasIncorrectFamilyBonus` = true
- `hasAnnualWageIncome` ≥ EUR 13,308 AND `hasFiledEmploymentTax` = false
- `hasSpecialPaymentSituations` = true (regardless of income)
- `hasDiscretionaryAssessment` = true (regardless of income)
- `hasIncorrectTaxCredits` = true (regardless of income)

**Ontology Coverage:**
- Data properties: All boolean flags and income amounts
- Defined classes: `MandatoryE1Filer`, `MandatoryL1Filer` with `owl:equivalentClass` axioms
- Reasoning: Automatic classification based on property assertions

---

### CQ5: What are the properties that trigger different tax filing forms (L1 form or E1 form)?

**Purpose:** Distinguish the specific conditions that determine whether a taxpayer needs Form E1 or Form L1.

**Form E1 Triggers:**
- `hasNonWageIncome` > EUR 730
- This is the ONLY trigger for E1 form

**Form L1 Triggers:**

*Mandatory L1:*
- High wage income (> EUR 14,517) with incorrect credits/allowances
- No employment tax filed with wage ≥ EUR 13,308
- Special payment situations
- Discretionary assessment
- Incorrect tax credits

*Voluntary L1:*
- `hasSingleEmployer` = true AND `hasCorrectWageTax` = true
- `hasVaryingIncomeNoRollup` = true
- `hasEmployerChange` = true
- `hasSVRepaymentEligibility` = true
- `hasUnclaimedTaxCredits` = true
- `hasUnclaimedDeductions` = true

---

## References

[1] Alfaifi, A., et al. (2022). Competency questions in ontology engineering.

[2] Grüninger, M., & Fox, M. S. (1995). Methodology for the design and evaluation of ontologies.

[3] Monfardini, G., et al. (2023). Use of competency questions in ontology engineering.

