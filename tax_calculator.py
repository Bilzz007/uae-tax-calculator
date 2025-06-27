# tax_calculator.py

def calculate_tax(inputs: dict) -> dict:
    # Step 1: Calculate taxable income
    taxable_income = inputs["revenue"] - inputs["deductions"] - inputs["exempt_income"]
    taxable_income = max(taxable_income, 0)  # no negative tax

    # Step 2: Apply slab
    if taxable_income <= 375000:
        tax_payable = 0
    else:
        tax_payable = 0.09 * (taxable_income - 375000)

    return {
        "taxable_income": round(taxable_income, 2),
        "tax_payable": round(tax_payable, 2)
    }
