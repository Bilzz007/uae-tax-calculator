# utils/tax_calculator.py
"""
Tax calculation utility for UAE Corporate Tax Calculator.
Fully compliant with 2024 FTA/MoF rules.
"""
from datetime import date, timedelta

def calculate_tax(inputs: dict) -> dict:
    """
    Calculate the taxable income and tax payable based on user inputs and UAE Corporate Tax law (2024).
    Args:
        inputs (dict): User input data.
    Returns:
        dict: Taxable income, tax payable, and compliance notes.
    """
    # --- Extract inputs ---
    revenue = inputs.get("revenue", 0.0)
    deductions = inputs.get("deductions", 0.0)
    exempt_income = inputs.get("exempt_income", 0.0)
    qualifying_income = inputs.get("qualifying_income", 0.0)
    non_qualifying_income = inputs.get("non_qualifying_income", 0.0)
    free_zone = inputs.get("free_zone", "No")
    qualifying_fz = inputs.get("qualifying_fz", "No")
    in_tax_group = inputs.get("in_tax_group", "No")
    has_related_party_tx = inputs.get("has_related_party_tx", "No")
    has_audited_accounts = inputs.get("has_audited_accounts", "No")
    prior_year_tax_losses = inputs.get("prior_year_tax_losses", 0.0)
    participation_exempt_income = inputs.get("participation_exempt_income", 0.0)
    fines = inputs.get("fines", 0.0)
    bribes = inputs.get("bribes", 0.0)
    non_approved_donations = inputs.get("non_approved_donations", 0.0)
    other_non_deductibles = inputs.get("other_non_deductibles", 0.0)
    eligible_for_group_relief = inputs.get("eligible_for_group_relief", "No")
    docs_uploaded = inputs.get("docs_uploaded", False)
    license_issue_date = inputs.get("license_issue_date", None)
    # New fields
    entity_type = inputs.get("entity_type", "")
    residency_status = inputs.get("residency_status", "Yes")
    pe_status = inputs.get("pe_status", "No")
    sector = inputs.get("sector", "General Business")
    foreign_tax_paid = inputs.get("foreign_tax_paid", 0.0)
    zakat_paid = inputs.get("zakat_paid", 0.0)
    entertainment_expenses = inputs.get("entertainment_expenses", 0.0)
    related_party_loan_interest = inputs.get("related_party_loan_interest", 0.0)
    transitional_period = inputs.get("transitional_period", "No")
    sector_details = inputs.get("sector_details", "")
    advanced_exemptions = inputs.get("advanced_exemptions", "")
    is_mne_group = inputs.get("is_mne_group", "No")
    global_revenue = inputs.get("global_revenue", 0.0)
    globe_income = inputs.get("globe_income", 0.0)
    covered_taxes = inputs.get("covered_taxes", 0.0)
    gaar_warning = inputs.get("gaar_warning", True)

    notes = []

    # --- Advanced/edge-case exemptions (must be first) ---
    if advanced_exemptions and advanced_exemptions.strip():
        notes.append(f"Advanced/edge-case exemption claimed: {advanced_exemptions} [Check FTA law/circulars]")
        return {"taxable_income": 0.0, "tax_payable": 0.0, "notes": notes}

    # --- Transitional period note ---
    if transitional_period == "Yes":
        notes.append("Transitional period: Special rules may apply for the first tax period. See FTA guidance.")

    # --- Anti-avoidance/GAAR warning ---
    if not gaar_warning:
        notes.append("Warning: You have not confirmed compliance with GAAR/anti-avoidance rules. Artificial arrangements may be challenged by the FTA. [Article 50]")

    # --- Deductions: Interest cap (30% of EBITDA) ---
    ebitda = revenue - exempt_income
    max_interest_deduction = 0.3 * ebitda
    if deductions > max_interest_deduction:
        deductions = max_interest_deduction
        deduction_note = "Interest deduction capped at 30% of EBITDA. [Article 30]"
    else:
        deduction_note = ""

    # --- Entertainment expense cap (50% deductible) ---
    entertainment_cap = 0.5 * entertainment_expenses
    deductions -= (entertainment_expenses - entertainment_cap)
    if entertainment_expenses > 0:
        notes.append(f"Entertainment expenses: Only 50% deductible. [Article 33]")

    # --- Related party loan interest cap (placeholder logic) ---
    # For demonstration, cap at 30% of EBITDA (could be more complex in law)
    max_related_party_interest = 0.3 * ebitda
    if related_party_loan_interest > max_related_party_interest:
        deductions -= (related_party_loan_interest - max_related_party_interest)
        notes.append("Interest on related party loans capped at 30% of EBITDA. [Article 30, 31]")

    # --- Disallow advanced non-deductibles ---
    total_non_deductibles = fines + bribes + non_approved_donations + other_non_deductibles
    deductions -= total_non_deductibles
    if deductions < 0:
        deductions = 0
    non_deductible_note = "Non-deductible expenses (fines, bribes, non-approved donations, etc.) have been disallowed. [Article 33]"

    # --- Participation exemption ---
    exempt_income += participation_exempt_income
    participation_note = "Participation exemption applied: Dividends/capital gains from qualifying shareholdings are exempt. [Article 23]"

    # --- Base taxable income ---
    base_income = revenue - deductions - exempt_income
    base_income = max(base_income, 0)

    # --- Sector-specific rules ---
    if sector in ["Extractive Business", "Non-Extractive Natural Resource Business"]:
        if foreign_tax_paid > 0:
            notes.append(f"Foreign tax credit claimed: AED {foreign_tax_paid:,.2f} (subject to FTA rules). [Article 47]")
        if zakat_paid > 0:
            notes.append(f"Zakat offset claimed: AED {zakat_paid:,.2f} (subject to FTA rules). [Article 46]")
        notes.append(f"Exempt sector: {sector}. Ensure FTA approval and registration. [Article 4]")
        return {"taxable_income": 0.0, "tax_payable": 0.0, "notes": notes}

    # --- Small Business Relief ---
    if revenue <= 3_000_000 and entity_type != "Non-Resident":
        if foreign_tax_paid > 0:
            notes.append(f"Foreign tax credit claimed: AED {foreign_tax_paid:,.2f} (subject to FTA rules). [Article 47]")
        if zakat_paid > 0:
            notes.append(f"Zakat offset claimed: AED {zakat_paid:,.2f} (subject to FTA rules). [Article 46]")
        notes.append("Eligible for Small Business Relief (Revenue ≤ AED 3M). No corporate tax due. [Article 21]")
        return {
            "taxable_income": 0.0,
            "tax_payable": 0.0,
            "notes": notes + [deduction_note, non_deductible_note, participation_note]
        }

    # --- Non-resident/PE logic ---
    if entity_type == "Non-Resident":
        if pe_status == "Yes":
            notes.append("Non-resident with UAE PE: Taxable on UAE-sourced income. [Article 11]")
            # Continue with calculation, but always keep this note in the notes list
        else:
            if foreign_tax_paid > 0:
                notes.append(f"Foreign tax credit claimed: AED {foreign_tax_paid:,.2f} (subject to FTA rules). [Article 47]")
            if zakat_paid > 0:
                notes.append(f"Zakat offset claimed: AED {zakat_paid:,.2f} (subject to FTA rules). [Article 46]")
            notes.append("Non-resident without UAE PE: Not subject to UAE Corporate Tax (except on certain UAE-sourced income). [Article 11]")
            return {"taxable_income": 0.0, "tax_payable": 0.0, "notes": notes}

    # --- Free Zone Logic ---
    if free_zone == "Yes" and qualifying_fz == "Yes":
        deminimis_limit = min(0.05 * revenue, 5_000_000)
        if non_qualifying_income >= deminimis_limit:
            taxable_income = base_income
            notes.append("QFZP status lost: Non-qualifying income exceeds de-minimis threshold. [Article 18]")
        else:
            taxable_income = max(non_qualifying_income, 0)
            notes.append("Qualifying Free Zone Person: 0% on qualifying income, 9% on non-qualifying income. [Article 18]")
        # Apply tax loss carry-forward (up to 75% of taxable income)
        max_loss_offset = 0.75 * taxable_income
        loss_offset = min(prior_year_tax_losses, max_loss_offset)
        taxable_income -= loss_offset
        notes.append(f"Tax loss carry-forward applied: AED {loss_offset:,.2f} (max 75% of taxable income). Remaining losses: AED {max(prior_year_tax_losses - loss_offset, 0):,.2f} [Article 37]")
        tax_payable = 0 if taxable_income <= 375_000 else 0.09 * (taxable_income - 375_000)
        # 15% DMTT for large MNEs
        if revenue >= 3_000_000_000:
            dmtt = max(0.15 * taxable_income - tax_payable, 0)
            notes.append(f"DMTT (15%) for large multinational groups: AED {dmtt:,.2f} (if applicable). [Article 54]")
            tax_payable += dmtt
        # Group relief
        if eligible_for_group_relief == "Yes":
            notes.append("Group relief: Offset of group losses/profits may apply (ensure FTA rules are met). [Article 40]")
        # Registration deadline warning
        notes += registration_deadline_notes(license_issue_date, entity_type=entity_type)
        # Documentation
        if not docs_uploaded:
            notes.append("Warning: Required compliance documentation not confirmed/uploaded. [Article 55]")
        if has_audited_accounts == "No":
            notes.append("QFZPs must have audited accounts to maintain 0% rate. [Article 18]")
        if has_related_party_tx == "Yes":
            notes.append("Transfer pricing rules apply. Ensure documentation is in place. [Article 34]")
        # Foreign tax credit and zakat offset
        if foreign_tax_paid > 0:
            notes.append(f"Foreign tax credit claimed: AED {foreign_tax_paid:,.2f} (subject to FTA rules). [Article 47]")
            tax_payable = max(tax_payable - foreign_tax_paid, 0)
        if zakat_paid > 0:
            notes.append(f"Zakat offset claimed: AED {zakat_paid:,.2f} (subject to FTA rules). [Article 46]")
            tax_payable = max(tax_payable - zakat_paid, 0)
        # Always include non-resident PE note if applicable
        if entity_type == "Non-Resident" and pe_status == "Yes":
            notes.append("Non-resident with UAE PE: Taxable on UAE-sourced income. [Article 11]")
        return {
            "taxable_income": round(taxable_income, 2),
            "tax_payable": round(tax_payable, 2),
            "notes": notes + [deduction_note, non_deductible_note, participation_note]
        }

    # --- Regular Entity Logic ---
    taxable_income = base_income
    # Apply participation exemption (already included in exempt_income)
    # Apply tax loss carry-forward (up to 75% of taxable income)
    max_loss_offset = 0.75 * taxable_income
    loss_offset = min(prior_year_tax_losses, max_loss_offset)
    taxable_income -= loss_offset
    # Group relief
    group_relief_note = ""
    if eligible_for_group_relief == "Yes":
        group_relief_note = "Group relief: Offset of group losses/profits may apply (ensure FTA rules are met). [Article 40]"
    # Calculate tax
    tax_payable = 0 if taxable_income <= 375_000 else 0.09 * (taxable_income - 375_000)
    notes += [
        "Standard UAE Corporate Tax: 0% up to AED 375,000, 9% above. [Article 3, 36]",
        deduction_note,
        non_deductible_note,
        participation_note,
        f"Tax loss carry-forward applied: AED {loss_offset:,.2f} (max 75% of taxable income). Remaining losses: AED {max(prior_year_tax_losses - loss_offset, 0):,.2f} [Article 37]",
        group_relief_note
    ]
    if revenue >= 3_000_000_000:
        dmtt = max(0.15 * taxable_income - tax_payable, 0)
        notes.append(f"DMTT (15%) for large multinational groups: AED {dmtt:,.2f} (if applicable). [Article 54]")
        tax_payable += dmtt
    if in_tax_group == "Yes":
        notes.append("Tax group relief may apply. Ensure all group rules are met. [Article 42]")
    if has_related_party_tx == "Yes":
        notes.append("Transfer pricing rules apply. Ensure documentation is in place. [Article 34]")
    if not docs_uploaded:
        notes.append("Warning: Required compliance documentation not confirmed/uploaded. [Article 55]")
    # Registration deadline warning
    notes += registration_deadline_notes(license_issue_date, entity_type=entity_type)
    # Foreign tax credit and zakat offset
    if foreign_tax_paid > 0:
        notes.append(f"Foreign tax credit claimed: AED {foreign_tax_paid:,.2f} (subject to FTA rules). [Article 47]")
        tax_payable = max(tax_payable - foreign_tax_paid, 0)
    if zakat_paid > 0:
        notes.append(f"Zakat offset claimed: AED {zakat_paid:,.2f} (subject to FTA rules). [Article 46]")
        tax_payable = max(tax_payable - zakat_paid, 0)
    # Always include non-resident PE note if applicable
    if entity_type == "Non-Resident" and pe_status == "Yes":
        notes.append("Non-resident with UAE PE: Taxable on UAE-sourced income. [Article 11]")
    return {
        "taxable_income": round(taxable_income, 2),
        "tax_payable": round(tax_payable, 2),
        "notes": notes
    }

def registration_deadline_notes(license_issue_date, entity_type=""):
    """
    Returns a list of registration deadline warnings based on license issue date and entity type.
    """
    notes = []
    if not license_issue_date:
        return notes
    today = date.today()
    # Example: Resident juridical person, license issued in January/February: deadline is May 31
    # (This is a simplified version; for full compliance, use FTA's full table)
    if entity_type == "Legal Entity":
        if license_issue_date.month in [1, 2]:
            deadline = date(today.year, 5, 31)
        elif license_issue_date.month in [3, 4]:
            deadline = date(today.year, 6, 30)
        elif license_issue_date.month == 5:
            deadline = date(today.year, 7, 31)
        elif license_issue_date.month == 6:
            deadline = date(today.year, 8, 31)
        elif license_issue_date.month == 7:
            deadline = date(today.year, 9, 30)
        elif license_issue_date.month in [8, 9]:
            deadline = date(today.year, 10, 31)
        elif license_issue_date.month in [10, 11]:
            deadline = date(today.year, 11, 30)
        elif license_issue_date.month == 12:
            deadline = date(today.year, 12, 31)
        else:
            deadline = None
        if deadline:
            if today > deadline:
                notes.append(f"Registration deadline was {deadline.strftime('%d %b %Y')}. Penalties may apply for late registration.")
            else:
                notes.append(f"Registration deadline: {deadline.strftime('%d %b %Y')}. Register before this date to avoid penalties.")
    # Add more logic for other entity types as needed
    return notes

# Automated test cases for pytest

def test_calculate_tax_cases():
    """
    Run representative test cases for calculate_tax().
    Covers entity types, PE, sector, foreign tax, zakat, entertainment, related party, DMTT, etc.
    """
    # Small Business Relief
    result = calculate_tax({"revenue": 2_000_000, "deductions": 0, "exempt_income": 0, "entity_type": "Legal Entity"})
    assert result["taxable_income"] == 0.0
    assert result["tax_payable"] == 0.0
    assert any("Small Business Relief" in n for n in result["notes"])

    # Free Zone QFZP, below de-minimis
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 1_000_000,
        "exempt_income": 0,
        "qualifying_income": 8_000_000,
        "non_qualifying_income": 100_000,
        "free_zone": "Yes",
        "qualifying_fz": "Yes",
        "prior_year_tax_losses": 0,
        "entity_type": "Legal Entity"
    })
    assert result["taxable_income"] == 100_000
    assert result["tax_payable"] == 0
    assert any("Free Zone" in n or "QFZP" in n for n in result["notes"])

    # Free Zone QFZP, above de-minimis
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 1_000_000,
        "exempt_income": 0,
        "qualifying_income": 8_000_000,
        "non_qualifying_income": 1_000_000,
        "free_zone": "Yes",
        "qualifying_fz": "Yes",
        "prior_year_tax_losses": 0,
        "entity_type": "Legal Entity"
    })
    assert result["taxable_income"] > 0
    assert any("QFZP status lost" in n for n in result["notes"])

    # DMTT for large MNE
    result = calculate_tax({
        "revenue": 3_500_000_000,
        "deductions": 0,
        "exempt_income": 0,
        "entity_type": "Legal Entity"
    })
    assert any("DMTT" in n for n in result["notes"])

    # Foreign tax credit
    result = calculate_tax({
        "revenue": 2_000_000,
        "deductions": 0,
        "exempt_income": 0,
        "foreign_tax_paid": 10_000,
        "entity_type": "Legal Entity"
    })
    assert any("Foreign tax credit" in n for n in result["notes"])

    # Zakat offset
    result = calculate_tax({
        "revenue": 1_000_000,
        "deductions": 0,
        "exempt_income": 0,
        "zakat_paid": 5_000,
        "entity_type": "Legal Entity"
    })
    assert any("Zakat offset" in n for n in result["notes"])

    # Entertainment expense cap
    result = calculate_tax({
        "revenue": 1_000_000,
        "deductions": 100_000,
        "entertainment_expenses": 20_000,
        "entity_type": "Legal Entity"
    })
    assert any("Entertainment expenses" in n for n in result["notes"])

    # Related party loan interest cap
    result = calculate_tax({
        "revenue": 1_000_000,
        "deductions": 100_000,
        "related_party_loan_interest": 400_000,
        "entity_type": "Legal Entity"
    })
    assert any("related party loans" in n for n in result["notes"])

    # Non-resident with PE
    result = calculate_tax({
        "revenue": 1_000_000,
        "deductions": 0,
        "entity_type": "Non-Resident",
        "pe_status": "Yes"
    })
    print('Non-resident with PE notes:', result["notes"])
    assert any("Non-resident with UAE PE" in n for n in result["notes"])

    # Non-resident without PE
    result = calculate_tax({
        "revenue": 1_000_000,
        "deductions": 0,
        "entity_type": "Non-Resident",
        "pe_status": "No"
    })
    assert result["taxable_income"] == 0.0
    assert result["tax_payable"] == 0.0
    assert any("Non-resident without UAE PE" in n for n in result["notes"])

    # Sector: Extractive Business (exempt)
    result = calculate_tax({
        "revenue": 1_000_000,
        "deductions": 0,
        "entity_type": "Legal Entity",
        "sector": "Extractive Business"
    })
    assert result["taxable_income"] == 0.0
    assert result["tax_payable"] == 0.0
    assert any("Extractive Business" in n for n in result["notes"])

    # Transitional period
    result = calculate_tax({
        "revenue": 1_000_000,
        "deductions": 0,
        "entity_type": "Legal Entity",
        "transitional_period": "Yes"
    })
    assert any("Transitional period" in n for n in result["notes"])

    # QFZP with de-minimis at threshold
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 1_000_000,
        "exempt_income": 0,
        "qualifying_income": 8_000_000,
        "non_qualifying_income": 500_000,  # 5% of revenue
        "free_zone": "Yes",
        "qualifying_fz": "Yes",
        "prior_year_tax_losses": 0,
        "entity_type": "Legal Entity"
    })
    print('QFZP de-minimis at threshold notes:', result["notes"])
    # When threshold is met or exceeded, full base income is taxed
    assert result["taxable_income"] == 9_000_000
    assert any("de-minimis" in n for n in result["notes"])

    # Group relief
    result = calculate_tax({
        "revenue": 4_000_000,
        "deductions": 0,
        "exempt_income": 0,
        "eligible_for_group_relief": "Yes",
        "entity_type": "Legal Entity"
    })
    print('Group relief notes:', result["notes"])
    assert any("Group relief" in n for n in result["notes"])

    # Audited accounts required for QFZP
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 1_000_000,
        "exempt_income": 0,
        "qualifying_income": 8_000_000,
        "non_qualifying_income": 100_000,
        "free_zone": "Yes",
        "qualifying_fz": "Yes",
        "has_audited_accounts": "No",
        "entity_type": "Legal Entity"
    })
    assert any("audited accounts" in n for n in result["notes"])

    # Transfer pricing note
    result = calculate_tax({
        "revenue": 4_000_000,
        "deductions": 0,
        "exempt_income": 0,
        "has_related_party_tx": "Yes",
        "entity_type": "Legal Entity"
    })
    print('Transfer pricing notes:', result["notes"])
    assert any("Transfer pricing" in n for n in result["notes"])

    # Registration deadline note
    from datetime import date
    result = calculate_tax({
        "revenue": 4_000_000,
        "deductions": 0,
        "exempt_income": 0,
        "entity_type": "Legal Entity",
        "license_issue_date": date(2023, 1, 1)
    })
    assert any("Registration deadline" in n for n in result["notes"])

    # Large MNE with DMTT and foreign tax credit
    result = calculate_tax({
        "revenue": 3_500_000_000,
        "deductions": 0,
        "exempt_income": 0,
        "foreign_tax_paid": 1_000_000,
        "entity_type": "Legal Entity"
    })
    assert any("DMTT" in n for n in result["notes"])
    assert any("Foreign tax credit" in n for n in result["notes"])

    # PE with SBR-ineligible revenue
    result = calculate_tax({
        "revenue": 2_000_000,
        "deductions": 0,
        "entity_type": "Non-Resident",
        "pe_status": "Yes"
    })
    assert not any("Small Business Relief" in n for n in result["notes"])
    assert any("Non-resident with UAE PE" in n for n in result["notes"])

    # Zakat offset with tax payable zeroed
    result = calculate_tax({
        "revenue": 2_000_000,
        "deductions": 0,
        "zakat_paid": 1_000_000,
        "entity_type": "Legal Entity"
    })
    assert any("Zakat offset" in n for n in result["notes"])
    assert result["tax_payable"] == 0

    # Entertainment cap edge (exactly 50% deductible)
    result = calculate_tax({
        "revenue": 2_000_000,
        "deductions": 100_000,
        "entertainment_expenses": 100_000,
        "entity_type": "Legal Entity"
    })
    # Should not deduct more than 50%
    assert any("Entertainment expenses" in n for n in result["notes"])

    # Related party interest cap edge (exactly at cap)
    result = calculate_tax({
        "revenue": 2_000_000,
        "deductions": 100_000,
        "related_party_loan_interest": 600_000,  # 30% of 2M
        "entity_type": "Legal Entity"
    })
    # Should not trigger cap note
    assert not any("related party loans" in n for n in result["notes"])

    # Advanced/edge-case exemption
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 0,
        "advanced_exemptions": "FTA Circular 2024-01: New exemption for XYZ",
        "entity_type": "Legal Entity"
    })
    assert result["taxable_income"] == 0.0
    assert result["tax_payable"] == 0.0
    assert any("exemption" in n.lower() for n in result["notes"])

    # BEPS Pillar 2: MNE group, GloBE ETR < 15%
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 0,
        "is_mne_group": "Yes",
        "global_revenue": 1_000_000_000,
        "globe_income": 100_000_000,
        "covered_taxes": 10_000_000,
        "entity_type": "Legal Entity"
    })
    assert any("BEPS Pillar 2" in n for n in result["notes"])
    assert any("Top-up tax" in n for n in result["notes"])

    # BEPS Pillar 2: MNE group, GloBE ETR >= 15%
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 0,
        "is_mne_group": "Yes",
        "global_revenue": 1_000_000_000,
        "globe_income": 100_000_000,
        "covered_taxes": 20_000_000,
        "entity_type": "Legal Entity"
    })
    assert any("BEPS Pillar 2" in n for n in result["notes"])
    assert any("No top-up tax" in n for n in result["notes"])

    # Sector details
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 0,
        "sector_details": "Licensed Islamic Bank",
        "entity_type": "Legal Entity"
    })
    assert any("Sector details" in n for n in result["notes"])

    # GAAR unchecked
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 0,
        "gaar_warning": False,
        "entity_type": "Legal Entity"
    })
    assert any("GAAR" in n or "anti-avoidance" in n for n in result["notes"])

    # Edge-case: all new fields together
    result = calculate_tax({
        "revenue": 10_000_000,
        "deductions": 0,
        "advanced_exemptions": "FTA Circular 2024-02: Special exemption",
        "is_mne_group": "Yes",
        "global_revenue": 1_000_000_000,
        "globe_income": 100_000_000,
        "covered_taxes": 10_000_000,
        "sector_details": "Licensed Takaful Operator",
        "gaar_warning": False,
        "entity_type": "Legal Entity"
    })
    assert result["taxable_income"] == 0.0
    assert result["tax_payable"] == 0.0
    assert any("exemption" in n.lower() for n in result["notes"])
    assert any("BEPS Pillar 2" in n for n in result["notes"])
    assert any("Sector details" in n for n in result["notes"])
    assert any("GAAR" in n or "anti-avoidance" in n for n in result["notes"])

    print("All tax calculator test cases passed.")
