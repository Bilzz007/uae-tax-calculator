# utils/tax_calculator.py

def calculate_tax(inputs: dict) -> dict:
    # Base taxable income
    base_income = inputs["revenue"] - inputs["deductions"] - inputs["exempt_income"]
    base_income = max(base_income, 0)

    # Free Zone case
    if inputs["free_zone"] == "Yes" and inputs["qualifying_fz"] == "Yes":
        non_q_income = inputs["non_qualifying_income"]
        taxable_income = max(non_q_income, 0)
        tax_payable = 0.09 * max(taxable_income - 375000, 0)
    else:
        # Regular slab
        taxable_income = base_income
        tax_payable = 0 if taxable_income <= 375000 else 0.09 * (taxable_income - 375000)

    return {
        "taxable_income": round(taxable_income, 2),
        "tax_payable": round(tax_payable, 2)
    }
