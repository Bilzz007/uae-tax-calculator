# components/input_form.py

import streamlit as st

def get_user_inputs():
    with st.form("tax_input_form"):
        st.subheader("📋 Business Information")

        # Entity Type
        entity_type = st.selectbox(
            "Entity Type",
            ["Legal Entity", "Natural Person"],
            help="Legal Entity: company registered in UAE (e.g., LLC, PSC, Free Zone entity). "
                 "Natural Person: individual conducting business (e.g., freelancer)."
        )

        # Free Zone
        free_zone = st.radio(
            "Are you registered in a UAE Free Zone?",
            ["Yes", "No"],
            help="Free Zone entities may qualify for special tax benefits if they meet QFZ conditions. See Article 18."
        )

        # Qualifying Free Zone Person
        qualifying_fz = st.radio(
            "Do you meet the conditions of a Qualifying Free Zone Person?",
            ["Yes", "No", "Not Applicable"],
            help="Qualifying FZ Persons must maintain UAE substance, earn qualifying income, "
                 "submit audited accounts, and follow transfer pricing rules."
        )

        # Exemptions
        exempt_type = st.multiselect(
            "Any of the following exemptions apply?",
            [
                "Government Entity",
                "Government Controlled Entity",
                "Extractive Business",
                "Non-Extractive Natural Resource Business",
                "Qualifying Public Benefit Entity",
                "Qualifying Mutual Fund",
                "Public or Private Pension Fund"
            ],
            help="Entities listed are fully exempt under Article 4, including public benefit entities and pension funds."
        )

        st.divider()
        st.subheader("💰 Financial Information")

        # Revenue
        revenue = st.number_input(
            "Total Revenue (AED)",
            min_value=0.0,
            step=1000.0,
            help="Gross business income for the financial year. Used to determine taxability and small business relief."
        )

        # Deductions
        deductions = st.number_input(
            "Deductible Expenses (AED)",
            min_value=0.0,
            step=100.0,
            help="Expenses incurred wholly for business purposes (e.g., salaries, rent). Must not be capital in nature."
        )

        # Exempt Income
        exempt_income = st.number_input(
            "Exempt Income (AED)",
            min_value=0.0,
            step=100.0,
            help="Includes dividends from UAE companies, qualifying foreign subsidiaries, and certain participations."
        )

        # Free Zone Income Breakdown
        qualifying_income = 0.0
        non_qualifying_income = 0.0
        if free_zone == "Yes" and qualifying_fz == "Yes":
            st.subheader("🏗️ Free Zone Income Breakdown")
            qualifying_income = st.number_input(
                "Qualifying Income (0% Tax)",
                min_value=0.0,
                step=100.0,
                help="Income from other Free Zone Persons or foreign customers under qualifying activities."
            )
            non_qualifying_income = st.number_input(
                "Non-Qualifying Income (9% Tax)",
                min_value=0.0,
                step=100.0,
                help="Income from mainland UAE or non-qualifying sources. Taxed at standard 9%."
            )

        submitted = st.form_submit_button("Check Eligibility and Calculate Tax")

    return submitted, {
        "entity_type": entity_type,
        "free_zone": free_zone,
        "qualifying_fz": qualifying_fz,
        "exempt_type": exempt_type,
        "revenue": revenue,
        "deductions": deductions,
        "exempt_income": exempt_income,
        "qualifying_income": qualifying_income,
        "non_qualifying_income": non_qualifying_income,
    }
