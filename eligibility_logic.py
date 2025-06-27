# eligibility_logic.py

def check_eligibility(inputs: dict) -> dict:
    # Check exemptions (Article 4)
    if inputs["exempt_type"]:
        return {
            "is_taxable": False,
            "message": f"❌ Entity is exempt from UAE Corporate Tax under Article 4 due to: {', '.join(inputs['exempt_type'])}."
        }

    # Free Zone logic (Article 18)
    if inputs["free_zone"] == "Yes":
        if inputs["qualifying_fz"] == "Yes":
            return {
                "is_taxable": True,
                "message": "✅ You are a Qualifying Free Zone Person. 0% tax on Qualifying Income (Article 18), 9% on others."
            }
        elif inputs["qualifying_fz"] == "No":
            return {
                "is_taxable": True,
                "message": "ℹ️ You are a Free Zone Person but not qualifying. Standard 0% / 9% rates apply."
            }

    # Automatic Small Business Relief (Article 21)
    if inputs["revenue"] <= 3_000_000:
        return {
            "is_taxable": False,
            "message": "✅ You qualify for Small Business Relief (Article 21) – Revenue ≤ AED 3M. No corporate tax."
        }

    # Default: taxable if natural/legal person with business income
    if inputs["entity_type"] in ["Legal Entity", "Natural Person"]:
        return {
            "is_taxable": True,
            "message": "✅ You are subject to UAE Corporate Tax based on income and entity profile."
        }

    return {
        "is_taxable": False,
        "message": "❌ Corporate Tax does not apply based on your profile."
    }
