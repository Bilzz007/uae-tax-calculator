# components/input_form.py

import streamlit as st
from components.precheck_taxable_person import taxable_person_precheck
from components.business_info_section import get_business_info
from components.financial_info_section import get_financial_info
from datetime import date

st.info("🧠 Modular input_form.py loaded!")

def get_user_inputs():
    """
    Collect user inputs for the UAE Corporate Tax Calculator.
    Returns:
        tuple: (submitted, user_inputs_dict)
    """
    # Pre-check for Taxable Person (Article 11)
    entity_type, is_taxable_person = taxable_person_precheck()

    with st.form("tax_input_form"):
        st.markdown("### 📋 Business and Financial Inputs")

        # Business Info Section
        (entity_type, residency_status, pe_status, sector, sector_details, free_zone, qualifying_fz, exempt_type, advanced_exemptions, is_mne_group, global_revenue, globe_income, covered_taxes, gaar_warning) = get_business_info()

        st.divider()

        # License Issue Date (for registration deadline)
        license_issue_date = st.date_input(
            "Business License Issue Date",
            value=date.today(),
            help="Used to determine your Corporate Tax registration deadline."
        )

        # Financial Info Section
        (revenue, deductions, exempt_income, qualifying_income, non_qualifying_income,
         foreign_tax_paid, zakat_paid, entertainment_expenses, related_party_loan_interest, transitional_period) = get_financial_info(
            free_zone, qualifying_fz
        )

        # Input validation: Ensure qualifying + non-qualifying income ≤ revenue
        if free_zone == "Yes" and qualifying_fz == "Yes":
            if qualifying_income + non_qualifying_income > revenue:
                st.warning("Sum of Qualifying and Non-Qualifying Income cannot exceed Total Revenue. Please adjust your inputs.")
                qualifying_income = 0.0
                non_qualifying_income = 0.0

        # Group Membership
        in_tax_group = st.radio(
            "Is your business part of a UAE Tax Group?",
            ["No", "Yes"],
            help="Tax groups allow certain UAE entities to file a single tax return. QFZPs cannot join tax groups."
        )

        # Related Party Transactions
        has_related_party_tx = st.radio(
            "Did your business have related party or connected person transactions?",
            ["No", "Yes"],
            help="Transfer pricing rules apply to related party and connected person transactions."
        )

        # Audited Accounts
        has_audited_accounts = st.radio(
            "Do you have audited financial statements?",
            ["No", "Yes"],
            help="Required for QFZPs and some other entities."
        )

        # --- New: Prior Year Tax Losses (Carry-forward) ---
        prior_year_tax_losses = st.number_input(
            "Prior Year Tax Losses to Carry Forward (AED)",
            min_value=0.0,
            step=100.0,
            help="Enter the amount of unused tax losses from previous years that can be carried forward (subject to 75% offset rule)."
        )

        # --- New: Participation Exemption ---
        participation_exempt_income = st.number_input(
            "Participation Exempt Income (Dividends/Capital Gains from Qualifying Shareholdings, AED)",
            min_value=0.0,
            step=100.0,
            help="Dividends and capital gains from qualifying shareholdings are exempt from corporate tax."
        )

        # --- New: Advanced Non-Deductibles ---
        st.markdown("#### Non-Deductible Expenses (Enter total for each category)")
        fines = st.number_input("Fines and Penalties (AED)", min_value=0.0, step=100.0)
        bribes = st.number_input("Bribes (AED)", min_value=0.0, step=100.0)
        non_approved_donations = st.number_input("Non-Approved Donations (AED)", min_value=0.0, step=100.0)
        other_non_deductibles = st.number_input("Other Non-Deductible Expenses (AED)", min_value=0.0, step=100.0)

        # --- New: Group Relief Eligibility ---
        eligible_for_group_relief = st.radio(
            "Is your company eligible for group relief (offset group losses/profits)?",
            ["No", "Yes"],
            help="Group relief allows eligible group companies to offset losses/profits as per FTA rules."
        )

        # --- New: Documentation Upload/Confirmation ---
        st.markdown("#### Compliance Documentation")
        docs_uploaded = st.checkbox("I confirm that all required documentation (audited accounts, transfer pricing file, etc.) is available and up to date.")

        submitted = st.form_submit_button("Check Eligibility and Calculate Tax")

    return submitted, {
        "entity_type": entity_type,
        "residency_status": residency_status,
        "pe_status": pe_status,
        "sector": sector,
        "sector_details": sector_details,
        "free_zone": free_zone,
        "qualifying_fz": qualifying_fz,
        "exempt_type": exempt_type,
        "advanced_exemptions": advanced_exemptions,
        "is_mne_group": is_mne_group,
        "global_revenue": global_revenue,
        "globe_income": globe_income,
        "covered_taxes": covered_taxes,
        "gaar_warning": gaar_warning,
        "license_issue_date": license_issue_date,
        "revenue": revenue,
        "deductions": deductions,
        "exempt_income": exempt_income,
        "qualifying_income": qualifying_income,
        "non_qualifying_income": non_qualifying_income,
        "foreign_tax_paid": foreign_tax_paid,
        "zakat_paid": zakat_paid,
        "entertainment_expenses": entertainment_expenses,
        "related_party_loan_interest": related_party_loan_interest,
        "transitional_period": transitional_period,
        "in_tax_group": in_tax_group,
        "has_related_party_tx": has_related_party_tx,
        "has_audited_accounts": has_audited_accounts,
        "prior_year_tax_losses": prior_year_tax_losses,
        "participation_exempt_income": participation_exempt_income,
        "fines": fines,
        "bribes": bribes,
        "non_approved_donations": non_approved_donations,
        "other_non_deductibles": other_non_deductibles,
        "eligible_for_group_relief": eligible_for_group_relief,
        "docs_uploaded": docs_uploaded,
    }
