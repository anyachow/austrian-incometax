# Austrian Tax Return Filing Ontology

A semantic ontology using OWL 2 reasoning to determine Austrian tax filing obligations for individuals and organizations based on Austrian income tax law.

## Overview

This system uses an OWL 2 ontology combined with a Python reasoning engine to automatically determine whether a person or entity must file Austrian income tax returns. It leverages semantic web technologies and automated reasoning to provide accurate, rule-based decisions for both L1 (employee assessment) and E1 (supplementary assessment) tax returns.

## Architecture

### Components

1. **OWL 2 Ontology** (`austrian_tax_ontology_resident_only.owl` / `.ttl`)
   - Defines tax concepts, entities, and filing rules
   - Uses OWL 2 constructs for automated inference
   - Captures Austrian tax law requirements for residents with only domestic employee income

2. **Python Reasoning Engine** (`tax_reasoning_engine.py`)
   - Loads and processes the ontology
   - Applies basic RDF inference with custom tax classification rules
   - Provides query interface and interactive system

3. **Test Suite** (`test_austrian_tax_rules.py`)
   - Comprehensive test cases covering all filing scenarios
   - Validates system accuracy across different tax situations

4. **Conversion Utilities** (`convert_ttl_to_owl.py`)
   - Converts Turtle format ontology to OWL/XML for better compatibility
   - Automated conversion as part of the test pipeline

### Key Concepts

#### Entity Types
- **Austrian Resident**: Tax residents subject to Austrian tax law

#### Filing Classifications

**L1 Filing (Employee Assessment)**
- **MandatoryL1Filer**: Required due to specific conditions
- **VoluntaryL1Filer**: Optional filing that may be beneficial

**E1 Filing (Supplementary Assessment)**
- **MandatoryE1Filer**: Required when other income exceeds €730

#### Income Types
- **Annual Wage Income**: Employment income subject to wage tax
- **Other Income**: Self-employment, rental, investment income, etc.

## Tax Filing Rules

The system implements these Austrian tax filing rules:

### Mandatory L1 Filing (Employee Assessment)
1. **High Income with Conditions**: Annual wage income > €14,517 AND one of:
   - Incorrect tax credits applied
   - Multiple employments
   - Incorrect commuter allowance
   - Incorrect Family Bonus Plus

### Additional Mandatory L1 Filing
2. **No Wage Tax**: Annual wage income ≥ €13,308 with no wage tax withheld
3. **Special Payment Situations**: Sick pay, service vouchers, etc.
4. **Discretionary Assessment**: Discretionary assessment included in salary

### Voluntary L1 Filing
5. **Single Employer**: Income > €14,517 with single employer and correct wage tax
6. **Beneficial Circumstances**: Income > €14,517 with:
   - Varying income levels without rollup
   - Employer change during year
   - Social insurance repayment eligibility
   - Unclaimed tax credits or deductions

### Mandatory E1 Filing (Supplementary Assessment)
7. **Other Income Threshold**: Other income (self-employment, rental, etc.) > €730

## Installation

1. **Clone the repository** and navigate to the project directory

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Required files**:
   - `austrian_tax_ontology_resident_only.owl` - The OWL ontology
   - `austrian_tax_ontology_resident_only.ttl` - Turtle format (optional)
   - `tax_reasoning_engine.py` - Main Python script
   - `test_austrian_tax_rules.py` - Test suite
   - `requirements.txt` - Dependencies

## Usage

### Quick Start

```bash
python3 tax_reasoning_engine.py
```

The system will:
1. Load the OWL ontology
2. Apply reasoning rules
3. Add example entities
4. Show filing requirements for examples
5. Start interactive mode

### Running Tests

Execute the comprehensive test suite:

```bash
# Using the test runner script
./run_tests.sh

# Or run directly
python3 test_austrian_tax_rules.py
```

The test suite includes 18 test cases covering all major filing scenarios.

### Interactive Commands

Once in interactive mode, use these commands:

- `add <entity_id>` - Add a new entity interactively
- `check <entity_id>` - Check filing requirements for an entity
- `list <status>` - List entities by status (must_file/optional/no_filing)
- `rules` - Show explanation of filing rules
- `entities` - List all entities in the system
- `help` - Show help message
- `quit` - Exit the system

### Example Session

```
> add person_005
Adding entity: person_005
Name: Klaus Fischer
Type (Person/Organization): Person
Annual income (EUR, or press Enter to skip): 35000
Austrian resident? (y/n/skip): y
Has self-employment income? (y/n): n
Has multiple income streams? (y/n): n

=== Filing Requirements for person_005 ===
📋 MUST FILE tax return

Reasons:
  • Entity classified as 'Mandatory Filing L1'

> check person_005
=== Filing Requirements for person_005 ===
📋 MUST FILE tax return

Classifications: MandatoryL1Filer
Filing Requirement: MandatoryFilingL1

> list must_file
Entities with status 'must_file': ['person_001', 'person_005']
```

## System Features

### Automated Reasoning
- Uses basic RDF inference with custom tax classification rules
- Infers filing requirements based on entity properties
- Provides detailed explanations for decisions

### Comprehensive Test Coverage
- 18 test cases covering all filing scenarios
- Validates both mandatory and voluntary filing conditions
- Tests edge cases and multiple trigger conditions

### Format Flexibility
- Supports both OWL/XML and Turtle formats
- Automatic conversion between formats
- Human-friendly Turtle syntax for editing

### Interactive Interface
- User-friendly command-line interface
- Real-time reasoning and feedback
- Comprehensive entity management

### Query Capabilities
- Check individual filing requirements
- Query entities by filing status
- Explore entity properties and classifications

## Technical Details

### Reasoning Implementation
The system uses basic RDF inference combined with custom tax classification logic:

```python
# Example: Mandatory L1 classification
if annual_wage > 14517.0:
    has_mandatory_condition = any([
        has_incorrect_tax_credits,
        has_multiple_employments,
        has_incorrect_commuter_allowance,
        has_incorrect_family_bonus
    ])
    if has_mandatory_condition:
        self.graph.add((entity_uri, RDF.type, TAX.MandatoryL1Filer))
```

### Entity Properties
Entities are represented with comprehensive properties:

**Income Properties:**
- `hasAnnualWageIncome`: Employment income subject to wage tax
- `hasOtherIncome`: Self-employment, rental, investment income, etc.

**L1 Mandatory Conditions:**
- `hasIncorrectTaxCredits`: Incorrect tax credits applied
- `hasMultipleEmployments`: Multiple employment relationships
- `hasIncorrectCommuterAllowance`: Incorrect commuter allowance
- `hasIncorrectFamilyBonus`: Incorrect Family Bonus Plus

**L1 Additional Mandatory Conditions:**
- `hasNoWageTax`: No wage tax withheld despite income threshold
- `hasSpecialPaymentSituations`: Special payment circumstances
- `hasDiscretionaryAssessment`: Discretionary assessment in salary

**L1 Voluntary Conditions:**
- `hasSingleEmployer`: Single employer relationship
- `hasCorrectWageTax`: Correct wage tax withholding
- `hasVaryingIncomeNoRollup`: Varying income without rollup
- `hasEmployerChange`: Employer change during tax year
- `hasSVRepaymentEligibility`: Social insurance repayment eligibility
- `hasUnclaimedTaxCredits`: Unclaimed tax credits available
- `hasUnclaimedDeductions`: Unclaimed special expenses/deductions

## Test Cases

The system includes comprehensive test coverage:

1. **Mandatory L1 Cases**: High income with various mandatory conditions
2. **Additional Mandatory L1 Cases**: Special circumstances requiring filing
3. **Voluntary L1 Cases**: Beneficial filing scenarios
4. **Mandatory E1 Cases**: Other income above threshold
5. **Combined Cases**: Multiple filing requirements (E1 takes priority)
6. **Edge Cases**: Complex scenarios with multiple triggers

### Sample Test Results

```
Test Case: TestCase_MandatoryL1_HighIncome
Input Parameters:
- Annual Income: €35,000.00
- Has incorrect tax credits: True

Results:
- Classifications: MandatoryL1Filer
- Filing Requirement: MandatoryFilingL1
- Must File: True
✅ MATCH
```

## File Conversion

Convert between ontology formats:

```python
# Convert Turtle to OWL/XML
python3 convert_ttl_to_owl.py
```

## Dependencies

- **Python 3.7+**
- **owlready2**: OWL ontology processing
- **rdflib**: RDF processing and SPARQL queries
- **colorama**: Terminal color output

```
owlready2>=0.46
rdflib>=7.0.0
colorama>=0.4.6
```

## Project Structure

```
austrian-tax-ontology/
├── README.md
├── requirements.txt
├── tax_reasoning_engine.py          # Main reasoning engine
├── test_austrian_tax_rules.py       # Comprehensive test suite
├── convert_ttl_to_owl.py            # Format conversion utility
├── run_tests.sh                     # Test runner script
├── austrian_tax_ontology_resident_only.owl   # OWL ontology
└── austrian_tax_ontology_resident_only.ttl   # Turtle format (optional)
```

## Extending the System

### Adding New Rules
1. Edit the ontology file to add new OWL classes and restrictions
2. Update the reasoning engine's classification logic if needed
3. Add corresponding test cases

### Adding New Properties
1. Define new properties in the ontology
2. Update the `TaxEntity` dataclass
3. Modify the `add_entity_to_kb` method
4. Add test coverage for new properties

### Custom Queries
Create custom SPARQL queries using the `rdflib` Graph object for advanced analysis.

## Validation

The system has been validated against Austrian tax law requirements and includes:
- ✅ 18 comprehensive test cases
- ✅ Coverage of all major filing scenarios  
- ✅ Edge case handling
- ✅ Automated test pipeline
- ✅ Format conversion utilities

## Compliance Note

This system is designed for educational and demonstration purposes based on Austrian income tax law. For actual tax filing decisions, always consult with qualified tax professionals and refer to official Austrian tax authority guidance.

## License

This project is provided as-is for educational purposes. Please ensure compliance with relevant tax regulations when using for actual tax decisions.

---

**Austrian Tax Authority Resources:**
- [BMF - Federal Ministry of Finance](https://www.bmf.gv.at/)
- [FinanzOnline](https://finanzonline.bmf.gv.at/)
- Official tax law documentation and current regulations