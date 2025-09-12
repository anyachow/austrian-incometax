# Austrian Tax Filing Requirements Knowledge Graph

A semantic knowledge graph system using OWL 2 reasoning to determine Austrian tax filing obligations for individuals and organizations.

## Overview

This system uses an OWL 2 ontology combined with a Python reasoning engine to automatically determine whether a person or entity must file Austrian income tax returns. It leverages semantic web technologies and automated reasoning to provide accurate, rule-based decisions.

## Architecture

### Components

1. **OWL 2 Ontology** (`austrian_tax_ontology.ttl`)
   - Defines tax concepts, entities, and filing rules in Turtle format
   - Uses OWL 2 constructs for automated inference
   - Captures Austrian tax law requirements

2. **Python Reasoning Engine** (`tax_reasoning_engine.py`)
   - Loads and processes the ontology
   - Applies OWL 2 RL reasoning using `owlrl` library
   - Provides query interface and interactive system

3. **Knowledge Base**
   - Stores information about individuals and organizations
   - Maintains personal/entity data for tax decisions

### Key Concepts

#### Entity Types
- **Person**: Individual taxpayers
- **Organization**: Corporate entities (Corporation, Partnership, Sole Proprietorship)

#### Residency Status
- **ResidentEntity**: Austrian tax residents
- **NonResidentEntity**: Non-residents with potential Austrian obligations

#### Filing Classifications
- **MustFileReturn**: Entities required to file
- **OptionalFiling**: Entities that may benefit from filing
- **NoFilingRequired**: Entities with no filing obligation

#### Income Types
- Employment Income
- Business Income
- Investment Income
- Rental Income
- Austrian Source Income

## Tax Filing Rules

The system implements these key Austrian tax filing rules:

1. **High Income Residents**: Austrian residents with annual income ≥ €12,000 must file
2. **Self-Employment**: Individuals with self-employment income must file regardless of amount
3. **Non-Resident Austrian Income**: Non-residents with Austrian source income must file
4. **Multiple Income Streams**: Entities with multiple income sources typically must file
5. **Low Income Simple**: Residents below €12,000 with simple employment may file optionally

## Installation

1. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

2. Ensure you have the following files:
   - `austrian_tax_ontology.ttl` - The OWL ontology in Turtle format
   - `tax_reasoning_engine.py` - Main Python script
   - `requirements.txt` - Dependencies

## Usage

### Basic Usage

Run the system:
```bash
python3 tax_reasoning_engine.py
```

The system will:
1. Load the OWL ontology from Turtle format
2. Apply OWL 2 reasoning
3. Add example entities
4. Show filing requirements for examples
5. Start interactive mode

### Interactive Commands

Once in interactive mode, you can use these commands:

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
Annual income (EUR, or press Enter to skip): 10000
Austrian resident? (y/n/skip): y
Has self-employment income? (y/n): n
Has multiple income streams? (y/n): n
Has Austrian source income? (y/n): y

=== Filing Requirements for person_005 ===
📄 Optional filing (may be beneficial)

Reasons:
  • Matches rule: Low income resident with simple employment (optional filing)
  • Matches rule: Austrian tax resident

> check person_005
=== Filing Requirements for person_005 ===
📄 Optional filing (may be beneficial)

Reasons:
  • Matches rule: Low income resident with simple employment (optional filing)
  • Matches rule: Austrian tax resident

> list optional
Entities with status 'optional': ['person_004', 'person_005']
```

## System Features

### Automated Reasoning
- Uses OWL 2 RL reasoning for automatic classification
- Infers filing requirements based on entity properties
- Provides explanations for decisions

### Turtle Format Benefits
- More readable and concise than XML
- Easier to edit and maintain
- Better for version control
- Human-friendly syntax

### Extensible Ontology
- Easy to add new rules and concepts
- Supports complex tax scenarios
- Maintains logical consistency

### Interactive Interface
- User-friendly command-line interface
- Real-time reasoning and feedback
- Comprehensive entity management

### Query Capabilities
- Check individual filing requirements
- Query entities by filing status
- Explore entity properties and classifications

## Technical Details

### OWL 2 Reasoning
The system uses OWL 2 RL (Rule Language) profile for reasoning, which provides:
- Efficient computation
- Decidable reasoning
- Support for complex property restrictions
- Class equivalences and disjunctions

### Knowledge Representation
Entities are represented with properties like:
- `hasAnnualIncome`: Annual income amount
- `isAustrianResident`: Residency status
- `hasSelfEmploymentIncome`: Self-employment flag
- `hasMultipleIncomeStreams`: Multiple income sources
- `hasAustrianSourceIncome`: Austrian income source

### Inference Rules in Turtle Format
The ontology includes inference rules such as:
```turtle
# High income residents must file
:HighIncomeResident rdf:type owl:Class ;
    owl:equivalentClass [
        rdf:type owl:Class ;
        owl:intersectionOf (
            :ResidentEntity
            [ rdf:type owl:Restriction ;
              owl:onProperty :hasAnnualIncome ;
              owl:someValuesFrom [ rdf:type rdfs:Datatype ;
                                   owl:onDatatype xsd:decimal ;
                                   owl:withRestrictions ( [ xsd:minInclusive "12000.0"^^xsd:decimal ] )
                                 ]
            ]
        )
    ] ;
    rdfs:subClassOf :MustFileReturn .

# Self-employed entities must file
:SelfEmployedEntity rdf:type owl:Class ;
    owl:equivalentClass [ rdf:type owl:Restriction ;
                          owl:onProperty :hasSelfEmploymentIncome ;
                          owl:hasValue "true"^^xsd:boolean
                        ] ;
    rdfs:subClassOf :MustFileReturn .
```

## Extending the System

### Adding New Rules
1. Edit `austrian_tax_ontology.ttl` to add new OWL classes and restrictions
2. The reasoning engine will automatically apply new rules

### Adding New Properties
1. Define new properties in the ontology
2. Update the `TaxEntity` dataclass in the Python script
3. Modify the `add_entity_to_kb` method to handle new properties

### Custom Queries
Create custom SPARQL queries using the `rdflib` Graph object for advanced analysis.

## Compliance Note

This system is for educational and demonstration purposes. For actual tax filing decisions, consult with qualified tax professionals and refer to official Austrian tax authority guidance.

## Dependencies

- Python 3.7+
- `rdflib`: RDF processing and SPARQL queries
- `owlrl`: OWL 2 RL reasoning engine

## License

This project is provided as-is for educational purposes. Please ensure compliance with relevant tax regulations when using for actual tax decisions. 