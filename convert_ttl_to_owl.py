#!/usr/bin/env python3
from rdflib import Graph

def convert_ttl_to_owl():
    # Create a new graph
    g = Graph()
    
    # Parse the TTL file
    g.parse("austrian_tax_ontology_resident_only.ttl", format="turtle")
    
    # Serialize to OWL/XML format
    owl_xml = g.serialize(format="xml")
    
    # Write to file
    with open("austrian_tax_ontology_resident_only.owl", "w", encoding="utf-8") as f:
        f.write(owl_xml)

if __name__ == "__main__":
    convert_ttl_to_owl()
    print("Conversion completed successfully!") 