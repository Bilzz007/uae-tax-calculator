# eligibility_logic.py
"""
Eligibility logic for UAE Corporate Tax Calculator.
"""

def check_eligibility(inputs: dict) -> dict:
    """
    Determine eligibility for UAE Corporate Tax based on user inputs.
    Args:
        inputs (dict): User input data.
    Returns:
        dict: Eligibility status and message.
    """
    # Exempt persons (Article 4)
    if inputs["exempt_type"]:
        return {
            "is_taxable": False,
            "message": f"❌ You are exempt under Article 4: {', '.join(inputs['exempt_type'])}."
        }

    # Transitional period logic
    if inputs.get("transitional_period", "No") == "Yes":
        return {
            "is_taxable": True,
            "message": "⚠️ Transitional period: Special rules may apply for the first tax period. Please consult the FTA guidance."
        }

    # Sector-specific exemptions or rules
    if inputs.get("sector") in ["Extractive Business", "Non-Extractive Natural Resource Business"]:
        return {
            "is_taxable": False,
            "message": f"❌ You are exempt as an {inputs['sector']} (subject to FTA approval and registration)."
        }
    if inputs.get("sector") in ["Banking", "Insurance"]:
        return {
            "is_taxable": True,
            "message": f"✅ {inputs['sector']} sector: Subject to special UAE Corporate Tax rules."
        }

    # Non-resident logic
    if inputs.get("entity_type") == "Non-Resident":
        if inputs.get("pe_status") == "Yes":
            return {
                "is_taxable": True,
                "message": "✅ Non-resident with UAE Permanent Establishment: Subject to UAE Corporate Tax on UAE-sourced income."
            }
        else:
            return {
                "is_taxable": False,
                "message": "❌ Non-resident without UAE PE: Not subject to UAE Corporate Tax (except on certain UAE-sourced income)."
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

    # General business income (expanded entity types)
    if inputs["entity_type"] in ["Legal Entity", "Natural Person", "Partnership", "Trust", "Sole Proprietor"]:
        if inputs.get("residency_status") == "Yes":
            return {
                "is_taxable": True,
                "message": "✅ You are subject to UAE Corporate Tax based on business activity and income."
            }
        else:
            return {
                "is_taxable": False,
                "message": "❌ Not a UAE resident for tax purposes. Check PE and source rules."
            }

    advanced_exemptions = inputs.get("advanced_exemptions", "")
    is_mne_group = inputs.get("is_mne_group", "No")
    global_revenue = inputs.get("global_revenue", 0.0)
    globe_income = inputs.get("globe_income", 0.0)
    covered_taxes = inputs.get("covered_taxes", 0.0)
    gaar_warning = inputs.get("gaar_warning", True)
    sector_details = inputs.get("sector_details", "")
    # --- Advanced/edge-case exemptions ---
    if advanced_exemptions and advanced_exemptions.strip():
        return {
            "is_taxable": False,
            "message": f"❌ Advanced/edge-case exemption claimed: {advanced_exemptions} [Check FTA law/circulars]."
        }
    # --- BEPS Pillar 2 (informative only for eligibility) ---
    if is_mne_group == "Yes" and global_revenue >= 750_000_000:
        globe_etr = 0.0
        if globe_income > 0:
            globe_etr = (covered_taxes / globe_income) * 100
        return {
            "is_taxable": True,
            "message": f"🌍 BEPS Pillar 2: MNE group with global revenue EUR {global_revenue:,.0f}, GloBE ETR: {globe_etr:.2f}%. Top-up tax may apply if ETR < 15%."
        }
    # --- Sector details for eligibility ---
    if sector_details:
        return {
            "is_taxable": True,
            "message": f"ℹ️ Sector details provided: {sector_details}. Please ensure all sector-specific rules are met."
        }
    # --- GAAR/anti-avoidance warning ---
    if not gaar_warning:
        return {
            "is_taxable": True,
            "message": "⚠️ You have not confirmed compliance with GAAR/anti-avoidance rules. Artificial arrangements may be challenged by the FTA. [Article 50]"
        }

    return {
        "is_taxable": False,
        "message": "❌ Based on your inputs, UAE Corporate Tax does not apply."
    }
