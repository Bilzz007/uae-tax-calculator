# eligibility_logic.py

def check_eligibility(inputs: dict) -> dict:
    # If exempt entity
    if inputs["exempt_type"]:
        return {
            "is_taxable": False,
            "message": f"❌ Entity is exempt from UAE Corporate Tax due to: {', '.join(inputs['exempt_type'])}."
        }

    # Small Business Relief
    if inputs["small_business_relief"] and inputs["revenue"] <= 3_000_000:
        return {
            "is_taxable": False,
            "message": "✅ You are eligible for Small Business Relief (Revenue ≤ AED 3M). Corporate tax does not apply."
        }

    # Free Zone: Qualifying or Not
    if inputs["free_zone"] == "Yes":
        if inputs["qualifying_fz"] == "Yes":
            return {
                "is_taxable": True,
                "message": "✅ You are a Qualifying Free Zone Person. 0% tax on Qualifying Income, 9% on non-qualifying."
            }
        elif inputs["qualifying_fz"] == "No":
            return {
                "is_taxable": True,
                "message": "ℹ️ You are a Free Zone Person but not Qualifying. Standard tax rates apply."
            }

    # All other legal entities and natural persons conducting business are taxable
    if inputs["entity_type"] in ["Legal Entity", "Natural Person"] and inputs["revenue"] > 375_000:
        return {
            "is_taxable": True,
            "message": "✅ You are subject to UAE Corporate Tax based on your business profile and income."
        }

    return {
        "is_taxable": False,
        "message": "❌ You do not meet the criteria for UAE Corporate Tax at this time (e.g., revenue ≤ AED 375,000)."
    }
