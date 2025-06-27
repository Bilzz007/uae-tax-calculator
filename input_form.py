# input_form.py

import streamlit as st

def show_guidance(field_key: str, message: str):
    if st.session_state.get(field_key) not in [None, "", 0.0]:
        st.markdown(f"🛈 **Guidance:** {message}")

def get_user_inputs():
    with st.form("tax_input_form"):
        st.subheader("📋 Business Information")

        # ENTITY TYPE
        entity_type = st.selectbox(
            "Entity Type",
            ["Legal Entity", "Natural Person"],
            key="entity_type"
        )
        show_guidance("entity_type", "Select if you're a company (Legal) or self-employed individual (Natural). *Ref: Article 11.3*")

        # FREE ZONE
        free_zone = st.radio(
            "Are you in a UAE Free Zone?",
            ["Yes", "No"],
            key="free_zone"
        )
        show_guidance("free_zone", "Only Free Zone entities can qualify for special 0% tax incentives. *Ref: Article 18*")

        # QUALIFYING FREE ZONE
        qualifying_fz = st.radio(
            "Do you meet the conditions of a Qualifying Free Zone Person?",
            ["Yes", "No", "Not Applicable"],
            key="qualifying_fz"
        )
        show_guidance("qualifying_fz", "Must have sufficient UAE presence, audited accounts, and earn qualifying income. *Ref: Article 18*")

        # EXEMPTIONS
        exempt_type = st.multiselect(
            "Any exemptions apply?",
            [
                "Government Entity",
                "Government Controlled Entity",
                "Extractive Business",
                "Non-Extractive Natural Resource Business",
                "Qualifying Public Benefit Entity",
                "Qualifying Mutual Fund",
                "Public or Private Pension Fund"
            ],
            key="exempt_type"
        )
        show_guidance("exempt_type", "Entities listed above may be fully exempt from corporate tax. *Ref: Article 4*")

        st.divider()
        st.subheader("💰 Financial Details")

        # REVENUE
        revenue = st.number_input("Total Revenue (AED)", min_value=0.0, step=1000.0, key="revenue")
        show_guidance("revenue", "Enter gross revenue earned in the financial year. Used to check SBR and taxability. *Ref: Article 12*")

        # DEDUCTIONS
        deductions = st.number_input("Deductible Expenses (AED)", min_value=0.0, step=100.0, key="deductions")
        show_guidance("deductions", "Only expenses incurred wholly for business and not capital in nature are allowed. *Ref: Article 28*")

        # EXEMPT INCOME
        exempt_income = st.number_input("Exempt Income (AED)", min_value=0.0, step=100.0, key="exempt_income")
        show_guidance("exempt_income", "Dividends from UAE companies or foreign participations may be exempt. *Ref: Article 22*")

        # FREE ZONE SPLIT
        qualifying_income = 0.0
        non_qualifying_income = 0.0

        if free_zone == "Yes" and qualifying_fz == "Yes":
            st.subheader("🏗️ Free Zone Income Breakdown")

            qualifying_income = st.number_input("Qualifying Income (0% Tax)", min_value=0.0, step=100.0, key="q_income")
            show_guidance("q_income", "Income from transactions within Free Zones or with foreign customers. *Ref: Cabinet Decision 55 & Article 18*")

            non_qualifying_income = st.number_input("Non-Qualifying Income (9% Tax)", min_value=0.0, step=100.0, key="nq_income")
            show_guidance("nq_income", "Income from mainland UAE or non-qualifying sources. *Ref: Article 18.2(b)*")

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
