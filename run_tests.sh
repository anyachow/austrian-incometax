#!/bin/bash

# Austrian Tax Filing Requirements - Test Runner
# ==============================================

set -e  # Exit on any error

echo "🇦🇹 Austrian Tax Filing Requirements - Test Suite"
echo "=================================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if virtual environment should be created
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Check if ontology file exists
if [ ! -f "austrian_tax_ontology.owl" ]; then
    echo "🔄 OWL/XML ontology file not found, checking for Turtle version..."
    if [ ! -f "austrian_tax_ontology.ttl" ]; then
        echo "❌ No Austrian tax ontology file found!"
        echo "Please ensure either austrian_tax_ontology.owl or austrian_tax_ontology.ttl is in the current directory."
        exit 1
    else
        echo "📝 Converting Turtle ontology to OWL/XML format for better compatibility..."
        python3 -c "import rdflib; g = rdflib.Graph(); g.parse('austrian_tax_ontology.ttl', format='turtle'); g.serialize('austrian_tax_ontology.owl', format='xml')"
        echo "✓ Conversion completed"
    fi
fi

echo ""
echo "🚀 Running Austrian Tax Filing Requirements Test Suite..."
echo "========================================================="
echo ""

# Run the test suite
python3 test_austrian_tax_rules.py

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests completed successfully!"
else
    echo "❌ Some tests failed. Please review the results above."
fi

echo ""
echo "Test suite execution completed."

exit $EXIT_CODE 