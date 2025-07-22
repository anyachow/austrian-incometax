#!/usr/bin/env python3
"""Test cases for Austrian tax filing requirements."""

from tax_reasoning_engine import TaxReasoningEngine, TaxEntity

test_cases = {
    "TestCase_MandatoryL1_HighIncome": {
        "description": "Austrian resident with income over €14,517 and incorrectly applied single-earner credit",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_HighIncome",
            name="High Income with Incorrect Credits",
            entity_type="Person",
            annual_income=35000.0,
            is_austrian_resident=True,
            has_incorrect_tax_credits=True,
            has_multiple_employments=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    },
    "TestCase_MandatoryL1_MultipleJobs": {
        "description": "Austrian resident with two jobs totaling €45,000",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_MultipleJobs",
            name="Multiple Jobs Employee",
            entity_type="Person",
            annual_income=45000.0,
            is_austrian_resident=True,
            has_multiple_employments=True,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    },
    "TestCase_MandatoryE1_SelfEmployed": {
        "description": "Austrian resident with freelance income €25,000",
        "expected_filing": "MandatoryFilingE1",
        "expected_classifications": ["MandatoryE1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryE1_SelfEmployed",
            name="Self Employed Person",
            entity_type="Person",
            annual_income=0.0,
            other_income=25000.0,
            is_austrian_resident=True,
            has_self_employment_income=True
        )
    },
    "TestCase_VoluntaryL1_SingleEmployer": {
        "description": "Austrian resident with single employer and correct wage tax",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_SingleEmployer",
            name="Single Employer with Correct Tax",
            entity_type="Person",
            annual_income=40000.0,
            is_austrian_resident=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    "TestCase_VoluntaryL1_Refund": {
        "description": "Austrian resident with varying income levels without rollup",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_Refund",
            name="Varying Income Employee",
            entity_type="Person",
            annual_income=30000.0,
            is_austrian_resident=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=True,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    "TestCase_MandatoryL1_NoWageTax": {
        "description": "Austrian resident with income above €13,308 but no wage tax withheld",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["AdditionalMandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_NoWageTax",
            name="No Wage Tax Employee",
            entity_type="Person",
            annual_income=15000.0,
            is_austrian_resident=True,
            has_no_wage_tax=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    },
    "TestCase_VoluntaryL1_Deductions": {
        "description": "Austrian resident with unclaimed special expenses",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_Deductions",
            name="Employee with Unclaimed Deductions",
            entity_type="Person",
            annual_income=35000.0,
            is_austrian_resident=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=True
        )
    },
    "TestCase_SimpleEmployee_Voluntary": {
        "description": "Austrian resident with simple employment below threshold, eligible for voluntary filing (default case)",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_SimpleEmployee_Voluntary",
            name="Simple Employee (Voluntary Filing Default)",
            entity_type="Person",
            annual_income=12000.0,
            is_austrian_resident=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    "TestCase_MandatoryL1_SpecialPayment": {
        "description": "Austrian resident with wage income above threshold and special payment situations (e.g., sick pay, service vouchers)",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["AdditionalMandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_SpecialPayment",
            name="Special Payment Situations",
            entity_type="Person",
            annual_income=20000.0,
            is_austrian_resident=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=True,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    },
    "TestCase_MandatoryL1_IncorrectCommuter": {
        "description": "Austrian resident with high wage income and incorrectly applied commuter allowance",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_IncorrectCommuter",
            name="Incorrect Commuter Allowance",
            entity_type="Person",
            annual_income=25000.0,
            is_austrian_resident=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=True,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    },
    "TestCase_MandatoryL1_IncorrectFamilyBonus": {
        "description": "Austrian resident with high wage income and incorrectly applied Family Bonus Plus",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_IncorrectFamilyBonus",
            name="Incorrect Family Bonus",
            entity_type="Person",
            annual_income=18000.0,
            is_austrian_resident=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=True,
            has_discretionary_assessment=False
        )
    },
    "TestCase_MandatoryL1_DiscretionaryAssessment": {
        "description": "Austrian resident with wage income and a discretionary assessment included in salary calculation",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["AdditionalMandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_DiscretionaryAssessment",
            name="Discretionary Assessment",
            entity_type="Person",
            annual_income=17000.0,
            is_austrian_resident=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=True
        )
    },
    "TestCase_MandatoryE1_RentalIncome": {
        "description": "Austrian resident with rental income above €730 triggering mandatory E1 filing",
        "expected_filing": "MandatoryFilingE1",
        "expected_classifications": ["MandatoryE1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryE1_RentalIncome",
            name="Rental Income",
            entity_type="Person",
            annual_income=0.0,
            other_income=2000.0,
            is_austrian_resident=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False
        )
    },
    "TestCase_VoluntaryL1_EmployerChange": {
        "description": "Austrian resident with employer change eligible for voluntary L1 filing",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_EmployerChange",
            name="Employer Change",
            entity_type="Person",
            annual_income=25000.0,
            is_austrian_resident=True,
            has_single_employer=False,
            has_correct_wage_tax=True,
            has_employer_change=True,
            has_varying_income_no_rollup=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    "TestCase_VoluntaryL1_SVRepayment": {
        "description": "Austrian resident eligible for SV repayment, can file voluntary L1",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_SVRepayment",
            name="SV Repayment Eligibility",
            entity_type="Person",
            annual_income=9000.0,
            is_austrian_resident=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_sv_repayment_eligibility=True,
            has_employer_change=False,
            has_varying_income_no_rollup=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    "TestCase_MandatoryL1_MultipleTriggers": {
        "description": "Austrian resident with high income, multiple employments, and incorrect tax credits",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_MultipleTriggers",
            name="Multiple Triggers",
            entity_type="Person",
            annual_income=50000.0,
            is_austrian_resident=True,
            has_multiple_employments=True,
            has_incorrect_tax_credits=True,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    },
    "TestCase_BothL1E1": {
        "description": "Austrian resident with high wage income, incorrect tax credits, and other income above E1 threshold",
        "expected_filing": "MandatoryFilingE1",
        "expected_classifications": ["MandatoryL1Filer", "MandatoryE1Filer"],
        "entity": TaxEntity(
            id="TestCase_BothL1E1",
            name="High Income, Incorrect Credits, Other Income",
            entity_type="Person",
            annual_income=20000.0,
            other_income=2000.0,
            is_austrian_resident=True,
            has_incorrect_tax_credits=True
        )
    },
    "TestCase_MandatoryE1_Employment_SelfEmp": {
        "description": "Austrian resident with employment income, self-employment income as a musician above €730.",
        "expected_filing": "MandatoryFilingE1",
        "expected_classifications": ["MandatoryE1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryE1_Employment_SelfEmp",
            name="Employment and Self-Employment",
            entity_type="Person",
            annual_income=25000.0,
            other_income=2000.0,
            is_austrian_resident=True,
            has_self_employment_income=True,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    },
    # New test case for the secretary scenario (TestCase 18)
    "TestCase_VoluntaryL1_SpecialExpenses": {
        "description": "A secretary with a single employer can file voluntarily to claim special expenses for a tax refund.",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_SpecialExpenses",
            name="Secretary with Special Expenses",
            entity_type="Person",
            annual_income=32000.0,
            other_income=0.0,
            is_austrian_resident=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_unclaimed_deductions=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_multiple_employments=False,
            has_incorrect_tax_credits=False,
            has_special_payment_situations=False,
            has_no_wage_tax=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False
        )
    }
}

def test_filing_requirements():
    """Test the tax filing requirements for various scenarios."""
    engine = TaxReasoningEngine(ontology_path="austrian_tax_ontology_resident_only.owl")
    
    print("\n=== Testing Tax Filing Requirements ===")
    print("=" * 100)
    
    for test_name, test_data in test_cases.items():
        print(f"\nTest Case: {test_name}")
        print("=" * 50)
        
        # Print input parameters
        entity = test_data["entity"]
        print("\nInput Parameters:")
        print("-" * 30)
        print(f"Name: {entity.name}")
        print(f"Type: {entity.entity_type}")
        print(f"Annual Income: €{entity.annual_income:,.2f}")
        if entity.other_income:
            print(f"Other Income: €{entity.other_income:,.2f}")
        print(f"Austrian Resident: {entity.is_austrian_resident}")
        
        # Print L1 Mandatory Filing Conditions if any are True
        if any([entity.has_incorrect_tax_credits, entity.has_multiple_employments,
                entity.has_incorrect_commuter_allowance, entity.has_incorrect_family_bonus]):
            print("\nL1 Mandatory Filing Conditions:")
            if entity.has_incorrect_tax_credits:
                print("- Has incorrect tax credits")
            if entity.has_multiple_employments:
                print("- Has multiple employments")
            if entity.has_incorrect_commuter_allowance:
                print("- Has incorrect commuter allowance")
            if entity.has_incorrect_family_bonus:
                print("- Has incorrect family bonus")
        
        # Print Additional L1 Mandatory Filing Conditions if any are True
        if any([entity.has_no_wage_tax, entity.has_special_payment_situations,
                entity.has_discretionary_assessment]):
            print("\nAdditional L1 Mandatory Filing Conditions:")
            if entity.has_no_wage_tax:
                print("- Has no wage tax")
            if entity.has_special_payment_situations:
                print("- Has special payment situations")
            if entity.has_discretionary_assessment:
                print("- Has discretionary assessment")
        
        # Print Voluntary L1 Filing Conditions if any are True
        if any([entity.has_single_employer, entity.has_correct_wage_tax,
                entity.has_varying_income_no_rollup, entity.has_employer_change,
                entity.has_sv_repayment_eligibility, entity.has_unclaimed_tax_credits,
                entity.has_unclaimed_deductions]):
            print("\nVoluntary L1 Filing Conditions:")
            if entity.has_single_employer:
                print("- Has single employer")
            if entity.has_correct_wage_tax:
                print("- Has correct wage tax")
            if entity.has_varying_income_no_rollup:
                print("- Has varying income without rollup")
            if entity.has_employer_change:
                print("- Has employer change")
            if entity.has_sv_repayment_eligibility:
                print("- Has SV repayment eligibility")
            if entity.has_unclaimed_tax_credits:
                print("- Has unclaimed tax credits")
            if entity.has_unclaimed_deductions:
                print("- Has unclaimed deductions")
        
        # Print E1 Filing Conditions if any are True
        if entity.has_self_employment_income:
            print("\nE1 Filing Conditions:")
            print("- Has self-employment income")
        
        # Add the test entity to the knowledge base
        engine.add_entity_to_kb(test_data["entity"])
        
        # Check filing requirements
        result = engine.determine_filing_requirement(test_name)
        
        # Print test results
        print("\nResults:")
        print("-" * 30)
        print(f"Classifications: {', '.join(result['inferred_classes'])}")
        print(f"Filing Requirement: {result.get('filing_requirement')}")
        print(f"Must File: {result['must_file']}")
        print(f"Optional Filing: {result['optional_filing']}")
        print(f"No Filing Required: {result['no_filing_required']}")
        
        if result["reasons"]:
            print("\nReasons:")
            for reason in result["reasons"]:
                print(f"• {reason}")
        
        # Verify classifications
        classifications_match = set(result["inferred_classes"]) == set(test_data["expected_classifications"])
        print(f"\nClassifications {'✅ MATCH' if classifications_match else '❌ DO NOT MATCH'}")
        if not classifications_match:
            print(f"Expected: {test_data['expected_classifications']}")
            print(f"Got: {result['inferred_classes']}")
        
        # Verify filing requirement
        filing_matches = result.get("filing_requirement") == test_data["expected_filing"]
        print(f"Filing Requirement {'✅ MATCHES' if filing_matches else '❌ DOES NOT MATCH'}")
        if not filing_matches:
            print(f"Expected: {test_data['expected_filing']}")
            print(f"Got: {result.get('filing_requirement')}")
        
        print("=" * 100)
        
        # Assert the results
        assert classifications_match, \
            f"Test {test_name} failed: Expected classifications {test_data['expected_classifications']}, got {result['inferred_classes']}"
        assert filing_matches, \
            f"Test {test_name} failed: Expected filing {test_data['expected_filing']}, got {result.get('filing_requirement')}"

if __name__ == "__main__":
    test_filing_requirements() 