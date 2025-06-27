# components/financial_info_section.py

import streamlit as st

def get_financial_info(free_zone: str, qualifying_fz: str):
    st.subheader("💰 Financial Information")

    revenue = st.number_input(
        "Total Revenue (AED)",
        min_value=0.0,
        step=1000.0,
        help="Gross business income for the financial year. Used to determine taxability and small business relief."
    )

    deductions = st.number_input(
        "Deductible Expenses (AED)",
        min_value=0.0,
        step=100.0,
        help="Expenses incurred wholly for business purposes (e.g., salaries, rent). Must not be capital in nature."
    )

    exempt_income = st.number_input(
        "Exempt Income (AED)",
        min_value=0.0,
        step=100.0,
        help="Includes dividends from UAE companies, qualifying foreign subsidiaries, and certain participations."
    )

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

    return revenue, deductions, exempt_income, qualifying_income, non_qualifying_income
