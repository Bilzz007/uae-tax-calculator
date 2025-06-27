# eligibility_logic.py

def check_eligibility(inputs: dict) -> dict:
    # Exempt persons (Article 4)
    if inputs["exempt_type"]:
        return {
            "is_taxable": False,
            "message": f"❌ You are exempt under Article 4: {', '.join(inputs['exempt_type'])}."
        }

    # Qualifying Free Zone (Article 18)
    if inputs["free_zone"] == "Yes":
        if inputs["qualifying_fz"] == "Yes":
            return {
                "is_taxable": True,
                "message": "✅ Qualifying Free Zone Person: 0% on qualifying income, 9% on non-qualifying income (Article 18)."
            }
        elif inputs["qualifying_fz"] == "No":
            return {
                "is_taxable": True,
                "message": "ℹ️ Free Zone Person (not qualifying). Standard tax rates apply (0%/9%)."
            }

    # Small Business Relief (Article 21)
    if inputs["revenue"] <= 3_000_000:
        return {
            "is_taxable": False,
            "message": "✅ Small Business Relief: Revenue ≤ AED 3M. You are not subject to corporate tax."
        }

    # General business income
    if inputs["entity_type"] in ["Legal Entity", "Natural Person"]:
        return {
            "is_taxable": True,
            "message": "✅ You are subject to UAE Corporate Tax based on business activity and income."
        }

    return {
        "is_taxable": False,
        "message": "❌ Based on your inputs, UAE Corporate Tax does not apply."
    }
