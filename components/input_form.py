# components/input_form.py

import streamlit as st
from components.precheck_taxable_person import taxable_person_precheck
from components.business_info_section import get_business_info
from components.financial_info_section import get_financial_info

def get_user_inputs():
    # Pre-check for Taxable Person (Article 11)
    entity_type, is_taxable_person = taxable_person_precheck()

    with st.form("tax_input_form"):
        # Business Info Section (Free Zone, Exemptions)
        free_zone, qualifying_fz, exempt_type = get_business_info()

        st.divider()

        # Financials (revenue, deductions, etc.)
        revenue, deductions, exempt_income, qualifying_income, non_qualifying_income = get_financial_info(
            free_zone, qualifying_fz
        )

        submitted = st.form_submit_button("Check Eligibility and Calculate Tax")

    return submitted, {
        "entity_type": entity_type,
        "is_taxable_person": is_taxable_person,
        "free_zone": free_zone,
        "qualifying_fz": qualifying_fz,
        "exempt_type": exempt_type,
        "revenue": revenue,
        "deductions": deductions,
        "exempt_income": exempt_income,
        "qualifying_income": qualifying_income,
        "non_qualifying_income": non_qualifying_income,
    }
