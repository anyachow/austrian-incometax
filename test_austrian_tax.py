from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import XSD
import sys
import os

def main():
    # Create a new RDF graph
    g = Graph()
    
    # Load the ontology file
    ontology_path = os.path.join("at_tax", "austrian_tax_ontology_resident_only.ttl")
    print(f"Loading ontology from {ontology_path}...")
    g.parse(ontology_path, format="turtle")
    print("Ontology loaded successfully!")
    
    # Define namespaces
    AT = Namespace("http://example.org/austrian-tax-resident#")
    
    # Add some basic inference rules
    print("Adding inference rules...")
    
    # Rule 1: Multiple Employment -> Must File
    g.add((AT.MultipleEmploymentTaxpayer, RDFS.subClassOf, AT.MustFileReturn))
    
    # Rule 2: Self-Employed -> Must File
    g.add((AT.SelfEmployedTaxpayer, RDFS.subClassOf, AT.MustFileReturn))
    
    # Rule 3: Rental Income -> Must File
    g.add((AT.RentalIncomeTaxpayer, RDFS.subClassOf, AT.MustFileReturn))
    
    # Rule 4: Investment Income -> Must File
    g.add((AT.InvestmentIncomeTaxpayer, RDFS.subClassOf, AT.MustFileReturn))
    
    # Rule 5: Significant Other Income -> Must File
    g.add((AT.SignificantOtherIncomeTaxpayer, RDFS.subClassOf, AT.MustFileReturn))
    
    # Rule 6: Low Income -> Optional Filing
    g.add((AT.LowIncomeTaxpayer, RDFS.subClassOf, AT.OptionalFiling))
    
    # Rule 7: Simple Employee -> No Filing Required
    g.add((AT.SimpleEmployee, RDFS.subClassOf, AT.NoFilingRequired))
    
    # Add classification rules
    print("Classifying test cases...")
    
    # Multiple Employment Rule
    multiple_employment_query = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/austrian-tax-resident#>
        
        SELECT ?testCase
        WHERE {
            ?testCase :hasMultipleEmployments "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
        }
    """)
    
    # Self-Employed Rule
    self_employed_query = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/austrian-tax-resident#>
        
        SELECT ?testCase
        WHERE {
            ?testCase :hasSelfEmploymentIncome "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
        }
    """)
    
    # Rental Income Rule
    rental_income_query = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/austrian-tax-resident#>
        
        SELECT ?testCase
        WHERE {
            ?testCase :hasRentalIncome "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
        }
    """)
    
    # Investment Income Rule
    investment_income_query = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/austrian-tax-resident#>
        
        SELECT ?testCase
        WHERE {
            ?testCase :hasInvestmentIncome "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
        }
    """)
    
    # Simple Employee Rule
    simple_employee_query = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/austrian-tax-resident#>
        
        SELECT ?testCase
        WHERE {
            ?testCase :hasMultipleEmployments "false"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                     :hasSelfEmploymentIncome "false"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                     :hasRentalIncome "false"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                     :hasInvestmentIncome "false"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                     :hasOtherIncome ?other ;
                     :hasAnnualWageIncome ?wage .
            FILTER(?other <= 730.0)
            FILTER(?wage >= 14300.0)
        }
    """)
    
    # Low Income Rule
    low_income_query = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/austrian-tax-resident#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?testCase
        WHERE {
            ?testCase :hasAnnualWageIncome ?wage ;
                     :hasOtherIncome ?other ;
                     :hasMultipleEmployments "false"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                     :hasSelfEmploymentIncome "false"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                     :hasRentalIncome "false"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                     :hasInvestmentIncome "false"^^<http://www.w3.org/2001/XMLSchema#boolean> .
            FILTER(?wage < 14300.0)
            FILTER(?other <= 730.0)
        }
    """)
    
    # Significant Other Income Rule
    significant_other_query = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/austrian-tax-resident#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?testCase
        WHERE {
            ?testCase :hasOtherIncome ?other .
            FILTER(?other > 730.0)
        }
    """)
    
    # Apply classifications
    for result in g.query(multiple_employment_query):
        g.add((result.testCase, RDF.type, AT.MultipleEmploymentTaxpayer))
        g.add((result.testCase, RDF.type, AT.MustFileReturn))
    
    for result in g.query(self_employed_query):
        g.add((result.testCase, RDF.type, AT.SelfEmployedTaxpayer))
        g.add((result.testCase, RDF.type, AT.MustFileReturn))
    
    for result in g.query(rental_income_query):
        g.add((result.testCase, RDF.type, AT.RentalIncomeTaxpayer))
        g.add((result.testCase, RDF.type, AT.MustFileReturn))
    
    for result in g.query(investment_income_query):
        g.add((result.testCase, RDF.type, AT.InvestmentIncomeTaxpayer))
        g.add((result.testCase, RDF.type, AT.MustFileReturn))
    
    for result in g.query(low_income_query):
        g.add((result.testCase, RDF.type, AT.LowIncomeTaxpayer))
        g.add((result.testCase, RDF.type, AT.OptionalFiling))
    
    for result in g.query(significant_other_query):
        g.add((result.testCase, RDF.type, AT.SignificantOtherIncomeTaxpayer))
        g.add((result.testCase, RDF.type, AT.MustFileReturn))
    
    for result in g.query(simple_employee_query):
        g.add((result.testCase, RDF.type, AT.SimpleEmployee))
        g.add((result.testCase, RDF.type, AT.NoFilingRequired))
    
    # Query to find all test cases and their properties
    test_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://example.org/austrian-tax-resident#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT DISTINCT ?testCase ?label ?comment ?wage ?other ?multi ?self ?rental ?invest
    WHERE {
        ?testCase rdf:type :AustrianResident ;
                 rdfs:label ?label .
        OPTIONAL { ?testCase rdfs:comment ?comment }
        OPTIONAL { ?testCase :hasAnnualWageIncome ?wage }
        OPTIONAL { ?testCase :hasOtherIncome ?other }
        OPTIONAL { ?testCase :hasMultipleEmployments ?multi }
        OPTIONAL { ?testCase :hasSelfEmploymentIncome ?self }
        OPTIONAL { ?testCase :hasRentalIncome ?rental }
        OPTIONAL { ?testCase :hasInvestmentIncome ?invest }
        FILTER(STRSTARTS(STR(?testCase), "http://example.org/austrian-tax-resident#TestCase_"))
    }
    ORDER BY ?testCase
    """
    
    # Query to find classifications for each test case
    classification_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://example.org/austrian-tax-resident#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT DISTINCT ?classification
    WHERE {
        <%s> rdf:type ?classification .
        FILTER(
            ?classification IN (
                :SimpleEmployee, 
                :MultipleEmploymentTaxpayer,
                :SelfEmployedTaxpayer,
                :RentalIncomeTaxpayer,
                :InvestmentIncomeTaxpayer,
                :SignificantOtherIncomeTaxpayer,
                :LowIncomeTaxpayer,
                :MustFileReturn,
                :OptionalFiling,
                :NoFilingRequired
            )
        )
    }
    ORDER BY ?classification
    """
    
    # Execute test cases query
    print("\nAnalyzing test cases...\n")
    for row in g.query(test_query):
        test_case_uri = str(row.testCase)
        print("=" * 80)
        print(f"Test Case: {row.label}")
        print(f"Description: {row.comment}")
        print("-" * 40)
        
        # Print properties
        print("Properties:")
        if row.wage is not None:
            print(f"- hasAnnualWageIncome: {row.wage}")
        if row.other is not None:
            print(f"- hasOtherIncome: {row.other}")
        if row.multi is not None:
            print(f"- hasMultipleEmployments: {row.multi}")
        if row.self is not None:
            print(f"- hasSelfEmploymentIncome: {row.self}")
        if row.rental is not None:
            print(f"- hasRentalIncome: {row.rental}")
        if row.invest is not None:
            print(f"- hasInvestmentIncome: {row.invest}")
        
        # Get classifications
        print("\nClassifications:")
        for class_row in g.query(classification_query % test_case_uri):
            class_name = str(class_row.classification).split("#")[1]
            if class_name != "AustrianResident":
                print(f"- {class_name}")
        
        print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1) 