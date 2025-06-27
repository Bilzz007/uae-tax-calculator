# components/input_form.py

import streamlit as st

def get_user_inputs():
    with st.form("tax_input_form"):
        st.subheader("📋 Business Information")

        # --- Entity Type ---
        col1, col2 = st.columns([3, 1])
        with col1:
            entity_type = st.selectbox("Entity Type", ["Legal Entity", "Natural Person"])
        with col2:
            with st.expander("ℹ️ Guidance"):
                st.markdown("""
**Legal Entity** means a juridical person registered or recognized under UAE law — e.g., LLCs, PSCs, Free Zone companies.

**Natural Person** means an individual conducting business activity, such as freelancers or sole proprietors.

📚 _This distinction impacts whether income from business activities qualifies for corporate tax._
                """)

        # --- Free Zone ---
        col1, col2 = st.columns([3, 1])
        with col1:
            free_zone = st.radio("Are you registered in a UAE Free Zone?", ["Yes", "No"])
        with col2:
            with st.expander("ℹ️ Guidance"):
                st.markdown("""
A **Free Zone Person** is a legal entity registered in one of the UAE’s designated Free Zones.

Some Free Zone entities may qualify for a 0% tax rate on certain types of income — if they meet substance and income requirements.

📚 _See: Article 18 & Cabinet Decision No. 55 of 2023._
                """)

        # --- Qualifying Free Zone Person ---
        col1, col2 = st.columns([3, 1])
        with col1:
            qualifying_fz = st.radio("Do you meet the conditions of a Qualifying Free Zone Person?", ["Yes", "No", "Not Applicable"])
        with col2:
            with st.expander("ℹ️ Guidance"):
                st.markdown("""
To be a **Qualifying Free Zone Person**, you must:

- Maintain **adequate substance** in the UAE
- Earn **Qualifying Income** (e.g., exports, other Free Zone transactions)
- Not opt-in for regular tax
- Prepare audited financials
- Comply with transfer pricing rules

📚 _See: Article 18 of Federal Decree-Law No. 47 and Ministerial Decision No. 265 of 2023._
                """)

        # --- Exemptions ---
        col1, col2 = st.columns([3, 1])
        with col1:
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
                ]
            )
        with col2:
            with st.expander("ℹ️ Guidance"):
                st.markdown("""
The following persons are **fully exempt** from corporate tax:

- Federal & Local **Government Entities**
- Entities conducting **Extractive** or **Natural Resource Businesses** under Emirate law
- **Qualifying Public Benefit Entities** (e.g., charities, chambers)
- **Mutual Funds** and **Pension Funds**

📚 _See: Article 4 of the Corporate Tax Law._
                """)

        st.divider()
        st.subheader("💰 Financial Information")

        # --- Revenue ---
        revenue = st.number_input("Total Revenue (AED)", min_value=0.0, step=1000.0)
        st.caption("Enter your gross income for the tax period. Revenue is used to determine thresholds like AED 3 million for Small Business Relief.")

        # --- Deductions ---
        deductions = st.number_input("Deductible Expenses (AED)", min_value=0.0, step=100.0)
        st.caption("Only expenses incurred **wholly and exclusively** for business, and not capital in nature, are deductible (e.g., salaries, rent).")

        # --- Exempt Income ---
        exempt_income = st.number_input("Exempt Income (AED)", min_value=0.0, step=100.0)
        st.caption("Income like dividends from UAE companies, profits from foreign subsidiaries (if qualifying) are exempt under Article 22.")

        # --- Free Zone Income Breakdown ---
        qualifying_income = 0.0
        non_qualifying_income = 0.0

        if free_zone == "Yes" and qualifying_fz == "Yes":
            st.subheader("🏗️ Free Zone Income Breakdown")
            qualifying_income = st.number_input("Qualifying Income (0% Tax)", min_value=0.0, step=100.0)
            non_qualifying_income = st.number_input("Non-Qualifying Income (9% Tax)", min_value=0.0, step=100.0)

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
