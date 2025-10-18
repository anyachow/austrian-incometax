# Austrian Income Tax Filing Ontology (Resident Individuals)

## Overview
This repository contains the **Austrian Income Tax Filing Ontology for Austrian Resident Individuals**, developed to represent and reason about **income tax filing obligations** in Austria.  
It models the conditions under which an Austrian resident taxpayer must file a **tax return (Form L1 or E1)**—either mandatory or voluntary—based on income sources, employment situations, and specific tax conditions.

---

## Repository Contents

### Ontology Files
The main ontology is provided in two formats:
- **`austrian-tax-ontology.ttl`** – Turtle format 
- **`austrian-tax-ontology.owl`** – OWL/RDF-XML format 

### Test Cases
A comprehensive set of test cases to validate the ontology's reasoning capabilities:
- **`test-cases.ttl`** – Test cases in Turtle format
- **`test-cases.owl`** – Test cases in OWL/RDF-XML format
- Includes 15 test cases covering:
  - 5 Mandatory L1 filing scenarios
  - 1 Mandatory E1 filing scenario  
  - 1 Combined Mandatory E1 + L1 scenario
  - 7 Voluntary L1 filing scenarios
  - 2 Tax books use cases

### Documentation
- **`COMPETENCY_QUESTIONS.md`** – Detailed competency questions that guide the ontology design

---

## Purpose
The ontology formalizes Austrian income tax rules to:
- Enable **automated reasoning** about filing obligations.  
- Support future **expert systems** that assist taxpayers or developers in determining correct tax return requirements.  
- Demonstrate the application of **Semantic Web technologies** in e-government and taxation domains.

---

## Ontology Vocabulary Description

The ontology namespace is `http://example.org/austrian-tax-resident#` and it builds upon standard vocabularies including **OWL**, **RDF**, and **RDFS**.

| Property | Value |
|-----------|--------|
| `rdfs:label` | Austrian Tax Residents Income Tax Ontology |
| `owl:versionInfo` | 2.1 |

---

### Annotation Properties
Annotation properties provide metadata about ontology elements.

| Property | Description | Prefix |
|-----------|--------------|---------|
| `:legalBasis` | Reference to specific Austrian tax law provisions. | `:` |
| `:taxYearApplicable` | Tax year(s) for which this rule applies. | `:` |
| `:thresholdAmount` | Specific monetary threshold in EUR for 2025. | `:` |
| `dc:creator` | Standard Dublin Core creator. | `dc:` |
| `dcterms:license` | Standard Dublin Core license. | `dcterms:` |

---

## Classes and Properties

### Classes

| Class | Description |
|-------|--------------|
| **`:AustrianResident`** | A person subject to unlimited tax liability in Austria under §1 EStG. |
| **`:MandatoryL1Filer`** | Taxpayers legally required to file L1 return when annual wage > €14,517 **and** at least one condition applies (e.g., multiple employments, incorrect tax credits, incorrect commuter allowance, Family Bonus errors, or special payment situations). |
| **`:VoluntaryL1Filer`** | Taxpayers eligible for voluntary filing (e.g., single employer, correct withholding, varying income without roll-up, unclaimed deductions/credits, or low income SV repayment eligibility). |
| **`:MandatoryE1Filer`** | Taxpayers required to file E1 return when non-employment income (self-employment, rent, etc.) exceeds €730 (excluding fully taxed capital yields). |

---

### Data Properties

Each `:AustrianResident` individual is described through the following key data properties:

| Property | Type | Description |
|-----------|------|-------------|
| `:hasAnnualWageIncome` | decimal | Total annual wage/pension income under §25 EStG. |
| `:hasNonWageIncome` | decimal | Total annual non-wage income (e.g., self-employment, rental). |
| `:hasFiledEmploymentTax` | boolean | Indicates if wage tax was properly filed. |
| `:hasMultipleEmploymentsWithoutJointTax` | boolean | Multiple employments without joint assessment. |
| `:hasIncorrectTaxCredits` | boolean | True if tax credits were incorrectly applied. |
| `:hasIncorrectCommuterAllowance` | boolean | Indicates incorrect commuter allowance. |
| `:hasIncorrectFamilyBonus` | boolean | Indicates Family Bonus Plus conditions not met. |
| `:hasSpecialPaymentSituations` | boolean | Receipt of sick pay, military pay, or service vouchers. |
| `:hasDiscretionaryAssessment` | boolean | Indicates discretionary assessment applied. |
| `:hasEmployerChange` | boolean | Indicates employer change or partial-year employment. |
| `:hasVaryingIncomeNoRollup` | boolean | Indicates varying income without annual roll-up. |
| `:hasUnclaimedTaxCredits` | boolean | Indicates unclaimed tax credits (e.g., commuter, family). |
| `:hasUnclaimedDeductions` | boolean | Indicates unclaimed deductible expenses. |
| `:hasSVRepaymentEligibility` | boolean | Indicates eligibility for social security refund. |
| `:hasSingleEmployer` | boolean | Indicates sole income source from one employer. |
| `:hasCorrectWageTax` | boolean | Indicates correct wage tax withholding. |

---

## Axiomatic Rules (Equivalent Class Definitions)

### Mandatory E1 Filing Rule
An `:AustrianResident` is a **`:MandatoryE1Filer`** if `hasNonWageIncome > 730`

This covers income beyond employment wages such as self-employment, freelance, or rental income (excluding fully taxed capital yields).

---

### Mandatory L1 Filing Rule
An `:AustrianResident` is a **`:MandatoryL1Filer`** if any of the following apply:

1. `:hasAnnualWageIncome > 14,517` **AND** one of:
   - `:hasMultipleEmploymentsWithoutJointTax = true`
   - `:hasIncorrectCommuterAllowance = true`
   - `:hasIncorrectFamilyBonus = true`
2. `:hasAnnualWageIncome > 13,308` **AND** `:hasFiledEmploymentTax = false`
3. `:hasSpecialPaymentSituations = true`
4. `:hasDiscretionaryAssessment = true`
5. `:hasIncorrectTaxCredits = true`

---

### Voluntary L1 Filing Rule
An `:AustrianResident` is a **`:VoluntaryL1Filer`** if any of the following apply:

- `:hasSingleEmployer = true` **AND** `:hasCorrectWageTax = true`
- `:hasVaryingIncomeNoRollup = true`
- `:hasEmployerChange = true`
- `:hasSVRepaymentEligibility = true`
- `:hasUnclaimedTaxCredits = true`
- `:hasUnclaimedDeductions = true`

These typically indicate eligibility for a refund rather than a mandatory filing.

---

## Ontology Reuse and Alignments

The ontology links to external academic tax ontologies using **SKOS** and **RDFS** mappings to ensure interoperability:

| Austrian Tax Ontology Term | SKOS/RDFS Relation | Linked Ontology | External Term |
|-----------------------------|--------------------|----------------|----------------|
| `AustrianResident` | `skos:closeMatch` | Bhatta et al. (2021) | Residence |
|  | `rdfs:seeAlso` | Sharipbaev et al. (2014) | Subjects of taxation |
|  | `skos:narrowMatch` | Elsayed (2023) | income_tax_payer |
|  | `skos:narrowMatch` | Gao et al. (2015) | tax payer |
|  | `skos:narrowMatch` | Cheng et al. (2010) | Taxpayer |
| `hasAnnualWageIncome` | `rdfs:seeAlso` | Elsayed (2023) | transaction |
|  | `rdfs:seeAlso` | Elsayed (2023) | taxpayment |
| `hasNonWageIncome` | `skos:broadMatch` | Elsayed (2023) | income_from_real_estate_possessions |
|  | `skos:broadMatch` | Elsayed (2023) | income_from_the_commercial_and_professional_activity |
| `hasUnclaimedDeductions` | `skos:narrowMatch` | Elsayed (2023) | TaxDeduction |
| `hasUnclaimedTaxCredits` | `skos:narrowMatch` | Elsayed (2023) | TaxRefund |
|  | `skos:narrowMatch` | Bhatta (2021) | TaxReturns |

---

## Test Cases and Validation

The ontology has been validated with **12 test cases and 2 tax-book use cases.**

### Test Results Summary

| Total Test Cases | Passed | Failed | Success Rate |
|------------------|--------|--------|--------------|
| 15 | 14 | 1 | 93.3% |

**Combined E1 + L1 filing (Test Case 6)**
- **Description:** Taxpayer with €20,000 wage income, €1,000 non-wage income, multiple employments, and incorrect tax credits
- **Expected:** Mandatory E1 Filer
- **Actual:** Classified as both Mandatory E1 Filer AND Mandatory L1 Filer
- **Explanation:** The ontology is designed in such that classes are not mutually exclusive due to the nature of taxation. However, the ontology lacks prioritisation rules, resulting failed.

---

## Compliance Note
This ontology follows the **Austrian Income Tax Act (EStG 1988)** and relevant BMF interpretations as of **Tax Year 2025**.  
It is designed for **academic and non-commercial use** and aims to support transparent, legally grounded decision automation in e-government contexts.  
The ontology does **not replace professional tax advice** and is provided solely for research and educational purposes.

---

## Implementation Details
- **Ontology Language:** OWL 2 DL  
- **Syntax:** RDF/XML and Turtle  
- **Tool:** Protégé 5.6.1  
- **Reasoner:** HermiT 1.4.3.456  
- **Evaluation:** 14 test cases (13 passed) and 2 legal textbook use cases validated the reasoning outcomes.

---

## Usage
1. Open the ontology in **Protégé**.  
2. Load test cases file.  
3. Use the **HermiT** reasoner to infer classification results.  
4. Optionally query with **SPARQL** to retrieve taxpayer filing obligations.  

---

## Repository Structure

```
austrian-tax-ontology/
├── README.md                           # This file
├── COMPETENCY_QUESTIONS.md             # Detailed competency questions
├── austrian-tax-ontology.ttl           # Main ontology (Turtle)
├── austrian-tax-ontology.owl           # Main ontology (OWL/XML)
├── test-cases.ttl                      # Test cases (Turtle)
└── test-cases.owl                      # Test cases (OWL/XML)
```

---

## License and Citation
This ontology is released for **academic and non-commercial use**.  
When using or referencing, please cite as:

> Chowsombat, A. (2025). *Ontology-based Expert System for Income Tax Filing Obligations in Austria*. Vienna University of Economics and Business (WU Vienna).