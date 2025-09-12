#!/usr/bin/env python3
"""
Austrian Tax Filing Requirements Knowledge Graph
Uses basic RDF inference to determine filing obligations for individuals and entities.
"""

import sys
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, OWL, XSD


# Define namespaces
TAX = Namespace("http://example.org/austrian-tax-resident#")
PERSON_KB = Namespace("http://example.org/person-kb#")


@dataclass
class TaxEntity:
    """Represents a person or organization in the tax system"""
    id: str
    name: str
    entity_type: str  # "Person" or "Organization"
    annual_income: Optional[float] = None
    has_non_wage_income: float = 0.0
    is_austrian_resident: Optional[bool] = None
    
    # L1 Mandatory Filing Conditions
    has_incorrect_tax_credits: bool = False
    has_multiple_employments_without_joint_tax: bool = False
    has_incorrect_commuter_allowance: bool = False
    has_incorrect_family_bonus: bool = False
    
    # Additional L1 Mandatory Filing Conditions
    has_filed_employment_tax: bool = True
    has_special_payment_situations: bool = False
    has_discretionary_assessment: bool = False
    
    # Voluntary L1 Filing Conditions
    has_single_employer: bool = False
    has_correct_wage_tax: bool = False
    has_varying_income_no_rollup: bool = False
    has_employer_change: bool = False
    has_sv_repayment_eligibility: bool = False
    has_unclaimed_tax_credits: bool = False
    has_unclaimed_deductions: bool = False
    
    # E1 Filing Conditions
    has_self_employment_income: bool = False


class TaxReasoningEngine:
    """
    Main reasoning engine for Austrian tax filing requirements.
    Uses basic RDF inference to determine filing obligations.
    """
    
    def __init__(self, ontology_path: str = "austrian_tax_ontology.ttl"):
        """Initialize the reasoning engine with the ontology"""
        self.graph = Graph()
        self.ontology_path = ontology_path
        self.load_ontology()
        self.setup_reasoner()
    
    def load_ontology(self):
        """Load the OWL ontology from file"""
        try:
            # Detect format based on file extension
            if self.ontology_path.endswith('.ttl'):
                format_type = "turtle"
            elif self.ontology_path.endswith('.owl'):
                format_type = "xml"
            else:
                format_type = "turtle"  # default to turtle
                
            self.graph.parse(self.ontology_path, format=format_type)
            print(f"Loaded ontology from {self.ontology_path} (format: {format_type})")
            print(f"Graph contains {len(self.graph)} triples")
        except Exception as e:
            print(f"Error loading ontology: {e}")
            sys.exit(1)
    
    def setup_reasoner(self):
        """Setup basic RDF inference"""
        try:
            # Apply basic RDFS inference
            for s, p, o in self.graph.triples((None, RDFS.subClassOf, None)):
                for s2, p2, o2 in self.graph.triples((None, RDF.type, s)):
                    self.graph.add((s2, RDF.type, o))
            
            # Apply basic property inference
            for s, p, o in self.graph.triples((None, RDFS.subPropertyOf, None)):
                for s2, p2, o2 in self.graph.triples((None, s, None)):
                    self.graph.add((s2, o, o2))
            
            # Apply custom tax classification rules
            for entity_uri, _, _ in self.graph.triples((None, RDF.type, TAX.AustrianResident)):
                # Get annual wage income
                annual_wage = 0.0
                for _, _, income in self.graph.triples((entity_uri, TAX.hasAnnualWageIncome, None)):
                    annual_wage = float(income)
                    break
                # Get non-wage income
                non_wage_income = 0.0
                for _, _, income in self.graph.triples((entity_uri, TAX.hasNonWageIncome, None)):
                    non_wage_income = float(income)
                    break
                # --- MANDATORY L1 FILER LOGIC (MERGED) ---
                is_mandatory_l1 = False
                # Case 1: Wage > 14,517 AND (any of the three triggers)
                if annual_wage > 14517.0 and any([
                    (entity_uri, TAX.hasMultipleEmploymentsWithoutJointTax, Literal(True)) in self.graph,
                    (entity_uri, TAX.hasIncorrectCommuterAllowance, Literal(True)) in self.graph,
                    (entity_uri, TAX.hasIncorrectFamilyBonus, Literal(True)) in self.graph
                ]):
                    is_mandatory_l1 = True
                # Case 2: Wage >= 13308 AND employment tax NOT filed
                if annual_wage >= 13308.0 and (entity_uri, TAX.hasFiledEmploymentTax, Literal(False)) in self.graph:
                    is_mandatory_l1 = True
                # Case 3: Special payment situations
                if (entity_uri, TAX.hasSpecialPaymentSituations, Literal(True)) in self.graph:
                    is_mandatory_l1 = True
                # Case 4: Discretionary assessment
                if (entity_uri, TAX.hasDiscretionaryAssessment, Literal(True)) in self.graph:
                    is_mandatory_l1 = True
                # Case 5: Incorrect tax credits (standalone)
                if (entity_uri, TAX.hasIncorrectTaxCredits, Literal(True)) in self.graph:
                    is_mandatory_l1 = True
                if is_mandatory_l1:
                    self.graph.add((entity_uri, RDF.type, TAX.MandatoryL1Filer))
                    self.graph.add((entity_uri, RDF.type, TAX.MandatoryFilingL1))
                # --- VOLUNTARY L1 FILER LOGIC ---
                is_voluntary_l1 = False
                if (entity_uri, RDF.type, TAX.MandatoryL1Filer) not in self.graph and (entity_uri, RDF.type, TAX.MandatoryE1Filer) not in self.graph:
                    # Case 1: Single employer with correct wage tax
                    if (entity_uri, TAX.hasSingleEmployer, Literal(True)) in self.graph and (entity_uri, TAX.hasCorrectWageTax, Literal(True)) in self.graph:
                        is_voluntary_l1 = True
                    # Case 2: Any of the refund/voluntary triggers
                    if any([
                        (entity_uri, TAX.hasVaryingIncomeNoRollup, Literal(True)) in self.graph,
                        (entity_uri, TAX.hasEmployerChange, Literal(True)) in self.graph,
                        (entity_uri, TAX.hasSVRepaymentEligibility, Literal(True)) in self.graph,
                        (entity_uri, TAX.hasUnclaimedTaxCredits, Literal(True)) in self.graph,
                        (entity_uri, TAX.hasUnclaimedDeductions, Literal(True)) in self.graph
                    ]):
                        is_voluntary_l1 = True
                if is_voluntary_l1:
                    self.graph.add((entity_uri, RDF.type, TAX.VoluntaryL1Filer))
                    self.graph.add((entity_uri, RDF.type, TAX.VoluntaryFilingL1))
                # --- MANDATORY E1 FILER LOGIC ---
                if non_wage_income > 730.0:
                    self.graph.add((entity_uri, RDF.type, TAX.MandatoryE1Filer))
                    self.graph.add((entity_uri, RDF.type, TAX.MandatoryFilingE1))
                # --- NO FILING REQUIRED ---
                if not any([
                    (entity_uri, RDF.type, TAX.MandatoryL1Filer) in self.graph,
                    (entity_uri, RDF.type, TAX.VoluntaryL1Filer) in self.graph,
                    (entity_uri, RDF.type, TAX.MandatoryE1Filer) in self.graph
                ]):
                    self.graph.add((entity_uri, RDF.type, TAX.NoFilingRequired))
            
            print("Basic RDF inference applied successfully")
            print(f"Graph expanded to {len(self.graph)} triples after inference")
        except Exception as e:
            print(f"Error during inference: {e}")
    
    def add_entity_to_kb(self, entity: TaxEntity):
        """Add a tax entity to the knowledge base"""
        entity_uri = PERSON_KB[entity.id]
        
        # Add basic type information
        if entity.entity_type == "Person":
            self.graph.add((entity_uri, RDF.type, TAX.AustrianResident))
        
        # Add income properties
        if entity.annual_income is not None:
            self.graph.add((entity_uri, TAX.hasAnnualWageIncome, 
                           Literal(entity.annual_income, datatype=XSD.decimal)))
        
        if entity.has_non_wage_income is not None:
            self.graph.add((entity_uri, TAX.hasNonWageIncome,
                           Literal(entity.has_non_wage_income, datatype=XSD.decimal)))
        
        # Add L1 Mandatory Filing Conditions
        self.graph.add((entity_uri, TAX.hasIncorrectTaxCredits,
                       Literal(entity.has_incorrect_tax_credits, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasMultipleEmploymentsWithoutJointTax,
                       Literal(entity.has_multiple_employments_without_joint_tax, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasIncorrectCommuterAllowance,
                       Literal(entity.has_incorrect_commuter_allowance, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasIncorrectFamilyBonus,
                       Literal(entity.has_incorrect_family_bonus, datatype=XSD.boolean)))
        
        # Add Additional L1 Mandatory Filing Conditions
        self.graph.add((entity_uri, TAX.hasFiledEmploymentTax,
                       Literal(entity.has_filed_employment_tax, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasSpecialPaymentSituations,
                       Literal(entity.has_special_payment_situations, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasDiscretionaryAssessment,
                       Literal(entity.has_discretionary_assessment, datatype=XSD.boolean)))
        
        # Add Voluntary L1 Filing Conditions
        self.graph.add((entity_uri, TAX.hasSingleEmployer,
                       Literal(entity.has_single_employer, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasCorrectWageTax,
                       Literal(entity.has_correct_wage_tax, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasVaryingIncomeNoRollup,
                       Literal(entity.has_varying_income_no_rollup, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasEmployerChange,
                       Literal(entity.has_employer_change, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasSVRepaymentEligibility,
                       Literal(entity.has_sv_repayment_eligibility, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasUnclaimedTaxCredits,
                       Literal(entity.has_unclaimed_tax_credits, datatype=XSD.boolean)))
        self.graph.add((entity_uri, TAX.hasUnclaimedDeductions,
                       Literal(entity.has_unclaimed_deductions, datatype=XSD.boolean)))
        
        # Re-run inference after adding new data
        self.setup_reasoner()
        print(f"Added entity {entity.name} ({entity.id}) to knowledge base")
    
    def check_filing_requirement(self, entity_id: str) -> Dict[str, Any]:
        """
        Check filing requirements for a specific entity
        Returns a dictionary with filing status and reasoning
        """
        entity_uri = PERSON_KB[entity_id]
        
        # Check if entity exists
        if (entity_uri, None, None) not in self.graph:
            return {"error": f"Entity {entity_id} not found in knowledge base"}
        
        result = {
            "entity_id": entity_id,
            "must_file": False,
            "optional_filing": False,
            "no_filing_required": False,
            "reasons": [],
            "inferred_classes": []
        }
        
        # Define base classes to exclude from inferred_classes
        base_classes = {TAX.AustrianResident, TAX.NonResidentEntity, TAX.ResidentEntity}
        
        # Define filing requirement classes
        filing_classes = {
            TAX.NoFilingRequired: "NoFilingRequired",
            TAX.MandatoryFilingL1: "MandatoryFilingL1",
            TAX.MandatoryFilingE1: "MandatoryFilingE1",
            TAX.VoluntaryFilingL1: "VoluntaryFilingL1"
        }
        
        # Track filing requirement
        filing_requirement = None
        
        # Check inferred classes
        for _, _, class_uri in self.graph.triples((entity_uri, RDF.type, None)):
            if class_uri in base_classes:
                continue
            
            # Handle filing requirement classes
            if class_uri in filing_classes:
                filing_requirement = filing_classes[class_uri]
                if class_uri == TAX.MandatoryFilingL1:
                    result["must_file"] = True
                    result["reasons"].append("Entity classified as 'Mandatory Filing L1'")
                elif class_uri == TAX.VoluntaryFilingL1:
                    result["optional_filing"] = True
                    result["reasons"].append("Entity classified as 'Voluntary Filing L1'")
                elif class_uri == TAX.MandatoryFilingE1:
                    result["must_file"] = True
                    result["reasons"].append("Entity classified as 'Mandatory Filing E1'")
                elif class_uri == TAX.NoFilingRequired:
                    result["no_filing_required"] = True
                    result["reasons"].append("Entity classified as 'No Filing Required'")
                continue
            
            # Add other classes to inferred_classes
            class_name = str(class_uri).split('#')[-1] if '#' in str(class_uri) else str(class_uri)
            result["inferred_classes"].append(class_name)
        
        # Add filing requirement to result
        if filing_requirement:
            result["filing_requirement"] = filing_requirement
        
        # Check specific rule classes
        rule_classes = [
            (TAX.HighIncomeResident, "High income Austrian resident (>€12,000)"),
            (TAX.SelfEmployedEntity, "Self-employed individual"),
            (TAX.NonResidentWithAustrianIncome, "Non-resident with Austrian source income"),
            (TAX.MultipleIncomeEntity, "Has multiple income streams"),
            (TAX.LowIncomeSimpleResident, "Low income resident with simple employment (optional filing)"),
            (TAX.ResidentEntity, "Austrian tax resident"),
            (TAX.NonResidentEntity, "Non-resident entity")
        ]
        
        for rule_class, description in rule_classes:
            if (entity_uri, RDF.type, rule_class) in self.graph:
                result["reasons"].append(f"Matches rule: {description}")
        
        return result
    
    def query_entities_by_filing_status(self, status: str) -> List[str]:
        """
        Query entities by their filing status
        status can be: 'must_file', 'optional', 'no_filing'
        """
        if status == 'must_file':
            class_uri = TAX.MandatoryFilingL1
        elif status == 'optional':
            class_uri = TAX.VoluntaryFilingL1
        elif status == 'no_filing':
            class_uri = TAX.MandatoryFilingE1
        else:
            return []
        
        entities = []
        for entity_uri, _, _ in self.graph.triples((None, RDF.type, class_uri)):
            if str(entity_uri).startswith(str(PERSON_KB)):
                entity_id = str(entity_uri).split('#')[-1]
                entities.append(entity_id)
        
        return entities
    
    def get_entity_properties(self, entity_id: str) -> Dict[str, Any]:
        """Get all properties of an entity"""
        entity_uri = PERSON_KB[entity_id]
        properties = {}
        
        for _, prop, value in self.graph.triples((entity_uri, None, None)):
            prop_name = str(prop).split('#')[-1] if '#' in str(prop) else str(prop)
            if prop_name not in ['type']:  # Skip RDF type
                properties[prop_name] = str(value)
        
        return properties
    
    def explain_rules(self) -> Dict[str, str]:
        """Return explanation of all tax filing rules"""
        return {
            "High Income Resident": "Austrian residents with annual income ≥ €12,000 must file",
            "Self-Employment": "Individuals with self-employment income must file regardless of amount",
            "Non-Resident Austrian Income": "Non-residents with Austrian source income must file", 
            "Multiple Income Streams": "Entities with multiple income sources typically must file",
            "Low Income Simple": "Residents below €12,000 with single employment may file optionally",
            "Basic Threshold": "Residents below €12,000 with single employment may not need to file"
        }
    
    def interactive_query(self):
        """Interactive command-line interface for querying the system"""
        print("\n=== Austrian Tax Filing Requirements System ===")
        print("Commands:")
        print("  add <entity_id> - Add a new entity interactively")
        print("  check <entity_id> - Check filing requirements for entity")
        print("  list <status> - List entities by status (must_file/optional/no_filing)")
        print("  rules - Show explanation of filing rules")
        print("  entities - List all entities in the system")
        print("  help - Show this help message")
        print("  quit - Exit the system")
        
        while True:
            try:
                command = input("\n> ").strip().split()
                if not command:
                    continue
                
                if command[0] == "quit":
                    break
                elif command[0] == "help":
                    self.interactive_query()
                    break
                elif command[0] == "add" and len(command) > 1:
                    self._interactive_add_entity(command[1])
                elif command[0] == "check" and len(command) > 1:
                    result = self.check_filing_requirement(command[1])
                    self._print_filing_result(result)
                elif command[0] == "list" and len(command) > 1:
                    entities = self.query_entities_by_filing_status(command[1])
                    print(f"Entities with status '{command[1]}': {entities}")
                elif command[0] == "rules":
                    rules = self.explain_rules()
                    for rule, explanation in rules.items():
                        print(f"  {rule}: {explanation}")
                elif command[0] == "entities":
                    self._list_all_entities()
                else:
                    print("Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _interactive_add_entity(self, entity_id: str):
        """Interactive entity addition"""
        print(f"\nAdding entity: {entity_id}")
        name = input("Name: ")
        entity_type = input("Type (Person/Organization): ")
        
        try:
            annual_income = input("Annual income (EUR, or press Enter to skip): ")
            annual_income = float(annual_income) if annual_income else None
        except ValueError:
            annual_income = None
        
        is_resident = input("Austrian resident? (y/n/skip): ").lower()
        is_austrian_resident = True if is_resident == 'y' else False if is_resident == 'n' else None
        
        has_self_employment = input("Has self-employment income? (y/n): ").lower() == 'y'
        has_multiple_streams = input("Has multiple income streams? (y/n): ").lower() == 'y'
        has_austrian_income = input("Has Austrian source income? (y/n): ").lower() == 'y'
        
        entity = TaxEntity(
            id=entity_id,
            name=name,
            entity_type=entity_type,
            annual_income=annual_income,
            is_austrian_resident=is_austrian_resident,
            has_self_employment_income=has_self_employment,
            has_multiple_income_streams=has_multiple_streams,
            has_austrian_source_income=has_austrian_income
        )
        
        self.add_entity_to_kb(entity)
        
        # Automatically check filing requirements
        result = self.check_filing_requirement(entity_id)
        self._print_filing_result(result)
    
    def _print_filing_result(self, result: Dict[str, Any]):
        """Pretty print filing requirement results"""
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        
        print(f"\n=== Filing Requirements for {result['entity_id']} ===")
        
        if result["must_file"]:
            print("📋 MUST FILE tax return")
        elif result["optional_filing"]:
            print("📄 Optional filing (may be beneficial)")
        elif result["no_filing_required"]:
            print("✅ No filing required")
        else:
            print("⚠️  Filing status unclear - needs review")
        
        if result["reasons"]:
            print("\nReasons:")
            for reason in result["reasons"]:
                print(f"  • {reason}")
        
        if result["inferred_classes"]:
            print(f"\nInferred classifications: {', '.join(result['inferred_classes'])}")
    
    def _list_all_entities(self):
        """List all entities in the knowledge base"""
        entities = set()
        for entity_uri, _, _ in self.graph.triples((None, RDF.type, TAX.TaxableEntity)):
            if str(entity_uri).startswith(str(PERSON_KB)):
                entity_id = str(entity_uri).split('#')[-1]
                entities.add(entity_id)
        
        print(f"Entities in knowledge base: {sorted(entities)}")

    def process_inferred_classes(self, inferred_classes, result):
        """Process inferred classes to determine filing requirements."""
        for class_name, class_uri in inferred_classes:
            if class_uri:
                result["inferred_classes"].append(class_name)
                
                if class_uri == TAX.MandatoryFilingL1:
                    result["must_file"] = True
                    result["reasons"].append("Entity classified as 'Mandatory Filing L1'")
                elif class_uri == TAX.VoluntaryFilingL1:
                    result["optional_filing"] = True
                    result["reasons"].append("Entity classified as 'Voluntary Filing L1'")
                elif class_uri == TAX.MandatoryFilingE1:
                    result["must_file"] = True
                    result["reasons"].append("Entity classified as 'Mandatory Filing E1'")
                elif class_uri == TAX.NoFilingRequired:
                    result["no_filing_required"] = True
                    result["reasons"].append("Entity classified as 'No Filing Required'")

    def get_filing_class_uri(self, status):
        """Get the URI for a filing status class."""
        if status == 'must_file':
            class_uri = TAX.MandatoryFilingL1
        elif status == 'optional':
            class_uri = TAX.VoluntaryFilingL1
        elif status == 'no_filing':
            class_uri = TAX.NoFilingRequired
        elif status == 'mandatory_e1':
            class_uri = TAX.MandatoryFilingE1
        else:
            class_uri = None
        return class_uri

    def determine_filing_requirement(self, entity_id: str) -> Dict[str, Any]:
        """
        Determine filing requirements for a specific entity
        Returns a dictionary with filing status and reasoning
        """
        entity_uri = PERSON_KB[entity_id]
        
        # Check if entity exists
        if (entity_uri, None, None) not in self.graph:
            return {"error": f"Entity {entity_id} not found in knowledge base"}
        
        result = {
            "entity_id": entity_id,
            "must_file": False,
            "optional_filing": False,
            "no_filing_required": False,
            "reasons": [],
            "inferred_classes": []
        }
        
        # Get all inferred classes for the entity
        for _, _, class_uri in self.graph.triples((entity_uri, RDF.type, None)):
            if class_uri in [TAX.MandatoryL1Filer, TAX.VoluntaryL1Filer, TAX.MandatoryE1Filer, TAX.NoFilingRequired]:
                result["inferred_classes"].append(class_uri.split("#")[-1])
        
        # Determine filing requirement based on classifications
        if (entity_uri, RDF.type, TAX.MandatoryFilingL1) in self.graph:
            result["filing_requirement"] = "MandatoryFilingL1"
            result["must_file"] = True
            result["reasons"].append("Entity classified as 'Mandatory Filing L1'")
        elif (entity_uri, RDF.type, TAX.MandatoryFilingE1) in self.graph:
            result["filing_requirement"] = "MandatoryFilingE1"
            result["must_file"] = True
            result["reasons"].append("Entity classified as 'Mandatory Filing E1'")
        elif (entity_uri, RDF.type, TAX.VoluntaryFilingL1) in self.graph:
            result["filing_requirement"] = "VoluntaryFilingL1"
            result["optional_filing"] = True
            result["reasons"].append("Entity classified as 'Voluntary Filing L1'")
        else:
            result["filing_requirement"] = "NoFilingRequired"
            result["no_filing_required"] = True
            result["reasons"].append("Entity classified as 'No Filing Required'")
            # Ensure NoFilingRequired is in inferred_classes
            if "NoFilingRequired" not in result["inferred_classes"]:
                result["inferred_classes"].append("NoFilingRequired")
        
        return result


def main():
    """Main function to run the tax reasoning system"""
    print("Initializing Austrian Tax Reasoning Engine...")
    
    try:
        engine = TaxReasoningEngine()
        
        # Add some example entities for demonstration
        print("\nAdding example entities...")
        
        # Example 1: High-income Austrian resident
        entity1 = TaxEntity(
            id="person_001",
            name="Maria Schmidt",
            entity_type="Person",
            annual_income=45000.0,
            is_austrian_resident=True,
            has_self_employment_income=False,
            has_multiple_income_streams=False
        )
        engine.add_entity_to_kb(entity1)
        
        # Example 2: Self-employed person
        entity2 = TaxEntity(
            id="person_002", 
            name="Hans Mueller",
            entity_type="Person",
            annual_income=8000.0,
            is_austrian_resident=True,
            has_self_employment_income=True,
            has_multiple_income_streams=False
        )
        engine.add_entity_to_kb(entity2)
        
        # Example 3: Non-resident with Austrian income
        entity3 = TaxEntity(
            id="person_003",
            name="John Smith",
            entity_type="Person",
            annual_income=25000.0,
            is_austrian_resident=False,
            has_austrian_source_income=True,
            has_multiple_income_streams=False
        )
        engine.add_entity_to_kb(entity3)
        
        # Example 4: Low income Austrian resident (optional filing)
        entity4 = TaxEntity(
            id="person_004",
            name="Anna Weber",
            entity_type="Person",
            annual_income=9000.0,
            is_austrian_resident=True,
            has_self_employment_income=False,
            has_multiple_income_streams=False
        )
        engine.add_entity_to_kb(entity4)
        
        # Check filing requirements for examples
        print("\n=== Example Results ===")
        for entity_id in ["person_001", "person_002", "person_003", "person_004"]:
            result = engine.check_filing_requirement(entity_id)
            engine._print_filing_result(result)
        
        # Start interactive mode
        engine.interactive_query()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()