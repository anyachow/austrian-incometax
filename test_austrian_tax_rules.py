#!/usr/bin/env python3
"""Test cases for Austrian tax filing requirements (fully aligned with TTL/OWL individuals)."""

from tax_reasoning_engine import TaxReasoningEngine, TaxEntity

test_cases = {
    # Test Case 1: Mandatory L1 - High Income with Incorrect Tax Credits
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
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=True,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 2: Mandatory L1 - Multiple Employments Without Joint Tax
    "TestCase_MandatoryL1_MultipleJobs": {
        "description": "Austrian resident with two jobs totaling €45,000 (multiple employments without joint tax)",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_MultipleJobs",
            name="Multiple Jobs Employee",
            entity_type="Person",
            annual_income=45000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=True,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 3: Mandatory E1 - Non-Wage Income
    "TestCase_MandatoryE1_NonWageIncome": {
        "description": "Austrian resident with non-wage income €25,000 (self-employment, rental, or investment)",
        "expected_filing": "MandatoryFilingE1",
        "expected_classifications": ["MandatoryE1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryE1_NonWageIncome",
            name="Non-Wage Income Person",
            entity_type="Person",
            annual_income=0.0,
            is_austrian_resident=True,
            has_non_wage_income=25000.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 4: Voluntary L1 - Single Employer with Correct Tax
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
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 5: Voluntary L1 - Tax Refund Expected (Varying Income No Rollup)
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
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=True,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 6: Mandatory L1 - No Wage Tax (employment tax not filed)
    "TestCase_MandatoryL1_NoWageTax": {
        "description": "Austrian resident with income above €13,308 but no wage tax filed",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["AdditionalMandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_NoWageTax",
            name="No Wage Tax Employee",
            entity_type="Person",
            annual_income=15000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=False,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 7: Voluntary L1 - Unclaimed Deductions
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
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=True
        )
    },
    # Test Case 8: No Filing Required - Simple Employee
    "TestCase_NoFiling": {
        "description": "Austrian resident with simple employment below threshold, eligible for voluntary filing",
        "expected_filing": "NoFilingRequired",
        "expected_classifications": ["NoFilingRequired"],
        "entity": TaxEntity(
            id="TestCase_NoFiling",
            name="Simple Employee Below Threshold",
            entity_type="Person",
            annual_income=12000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 9: Mandatory L1 - Special Payment Situations
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
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=True,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 10: Mandatory L1 - High Income with Correct Tax Credits
    "TestCase_MandatoryL1_HighIncome_CorrectCredits": {
        "description": "Austrian resident with income over €14,517 and correctly applied single-earner credit",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_HighIncome_CorrectCredits",
            name="High Income with Correct Credits",
            entity_type="Person",
            annual_income=35000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 11: Mandatory L1 - Low Income with Incorrect Tax Credits
    "TestCase_MandatoryL1_LowIncome_IncorrectCredits": {
        "description": "Austrian resident with income below €14,517 and incorrectly applied tax credits",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_LowIncome_IncorrectCredits",
            name="Low Income with Incorrect Credits",
            entity_type="Person",
            annual_income=12000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=True,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 12: Mandatory L1 - Low Income with Correct Tax Credits
    "TestCase_MandatoryL1_LowIncome_CorrectCredits": {
        "description": "Austrian resident with income below €14,517 and correctly applied tax credits",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_LowIncome_CorrectCredits",
            name="Low Income with Correct Credits",
            entity_type="Person",
            annual_income=12000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 13: Mandatory E1 - High Non-Wage Income
    "TestCase_MandatoryE1_HighNonWageIncome": {
        "description": "Austrian resident with non-wage income €50,000 (self-employment, rental, or investment)",
        "expected_filing": "MandatoryFilingE1",
        "expected_classifications": ["MandatoryE1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryE1_HighNonWageIncome",
            name="High Non-Wage Income Person",
            entity_type="Person",
            annual_income=0.0,
            is_austrian_resident=True,
            has_non_wage_income=50000.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 14: Voluntary L1 - High Income with Unclaimed Tax Credits
    "TestCase_VoluntaryL1_HighIncome_UnclaimedCredits": {
        "description": "Austrian resident with income over €14,517 and unclaimed tax credits",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_HighIncome_UnclaimedCredits",
            name="High Income with Unclaimed Credits",
            entity_type="Person",
            annual_income=35000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=True,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 15: Voluntary L1 - Low Income with Unclaimed Tax Credits
    "TestCase_VoluntaryL1_LowIncome_UnclaimedCredits": {
        "description": "Austrian resident with income below €14,517 and unclaimed tax credits",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_LowIncome_UnclaimedCredits",
            name="Low Income with Unclaimed Credits",
            entity_type="Person",
            annual_income=12000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=True,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 16: Mandatory L1 - Commuter Allowance Issues
    "TestCase_MandatoryL1_CommuterAllowance": {
        "description": "Austrian resident with income above €14,517 and incorrect commuter allowance",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_CommuterAllowance",
            name="Commuter Allowance Issues",
            entity_type="Person",
            annual_income=20000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=True,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 17: Mandatory L1 - Family Bonus Issues
    "TestCase_MandatoryL1_FamilyBonus": {
        "description": "Austrian resident with income above €14,517 and incorrect family bonus",
        "expected_filing": "MandatoryFilingL1",
        "expected_classifications": ["MandatoryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_MandatoryL1_FamilyBonus",
            name="Family Bonus Issues",
            entity_type="Person",
            annual_income=20000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=True,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 18: Voluntary L1 - High Income with Commuter Allowance
    "TestCase_VoluntaryL1_HighIncome_CommuterAllowance": {
        "description": "Austrian resident with income over €14,517 and correct commuter allowance",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_HighIncome_CommuterAllowance",
            name="High Income with Commuter Allowance",
            entity_type="Person",
            annual_income=35000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=False,
            has_correct_wage_tax=False,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    },
    # Test Case 19: Voluntary L1 - Low Income with Commuter Allowance
    "TestCase_VoluntaryL1_LowIncome_CommuterAllowance": {
        "description": "Austrian resident with income below €14,517 and correct commuter allowance",
        "expected_filing": "VoluntaryFilingL1",
        "expected_classifications": ["VoluntaryL1Filer"],
        "entity": TaxEntity(
            id="TestCase_VoluntaryL1_LowIncome_CommuterAllowance",
            name="Low Income with Commuter Allowance",
            entity_type="Person",
            annual_income=12000.0,
            is_austrian_resident=True,
            has_non_wage_income=0.0,
            has_incorrect_tax_credits=False,
            has_multiple_employments_without_joint_tax=False,
            has_special_payment_situations=False,
            has_incorrect_commuter_allowance=False,
            has_incorrect_family_bonus=False,
            has_discretionary_assessment=False,
            has_filed_employment_tax=True,
            has_single_employer=True,
            has_correct_wage_tax=True,
            has_varying_income_no_rollup=False,
            has_employer_change=False,
            has_sv_repayment_eligibility=False,
            has_unclaimed_tax_credits=False,
            has_unclaimed_deductions=False
        )
    }
}

def test_filing_requirements():
    """Test the tax filing requirements for various scenarios."""
    engine = TaxReasoningEngine(ontology_path="austrian_tax_ontology_resident_only.ttl")
    
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
        if getattr(entity, 'has_non_wage_income', 0.0) > 0:
            print(f"Non-Wage Income: €{entity.has_non_wage_income:,.2f}")
        print(f"Austrian Resident: {entity.is_austrian_resident}")
        
        # Print L1 Mandatory Filing Conditions if any are True
        if any([entity.has_incorrect_tax_credits, entity.has_multiple_employments_without_joint_tax,
                entity.has_incorrect_commuter_allowance, entity.has_incorrect_family_bonus]):
            print("\nL1 Mandatory Filing Conditions:")
            if entity.has_incorrect_tax_credits:
                print("- Has incorrect tax credits")
            if entity.has_multiple_employments_without_joint_tax:
                print("- Has multiple employments without joint tax")
            if entity.has_incorrect_commuter_allowance:
                print("- Has incorrect commuter allowance")
            if entity.has_incorrect_family_bonus:
                print("- Has incorrect family bonus")
        
        # Print Additional L1 Mandatory Filing Conditions if any are True
        if any([getattr(entity, 'has_filed_employment_tax', True) is False, entity.has_special_payment_situations,
                entity.has_discretionary_assessment]):
            print("\nAdditional L1 Mandatory Filing Conditions:")
            if getattr(entity, 'has_filed_employment_tax', True) is False:
                print("- Has not filed employment tax")
            if entity.has_special_payment_situations:
                print("- Has special payment situations")
            if entity.has_discretionary_assessment:
                print("- Has discretionary assessment")
        
        # Print E1 Filing Conditions if any are True
        if getattr(entity, 'has_non_wage_income', 0.0) > 730.0:
            print("\nE1 Filing Conditions:")
            print(f"- Has non-wage income: €{entity.has_non_wage_income:,.2f}")
        
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