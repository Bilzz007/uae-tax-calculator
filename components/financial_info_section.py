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

    # Foreign Tax Paid
    foreign_tax_paid = st.number_input(
        "Foreign Tax Paid (AED)",
        min_value=0.0,
        step=100.0,
        help="Enter the amount of foreign tax paid that may be eligible for a tax credit."
    )

    # Zakat Paid
    zakat_paid = st.number_input(
        "Zakat Paid (AED)",
        min_value=0.0,
        step=100.0,
        help="Enter the amount of Zakat paid that may be eligible for offset against corporate tax."
    )

    # Entertainment Expenses
    entertainment_expenses = st.number_input(
        "Entertainment Expenses (AED)",
        min_value=0.0,
        step=100.0,
        help="Subject to a 50% deductibility cap as per UAE Corporate Tax Law."
    )

    # Related Party Loan Interest
    related_party_loan_interest = st.number_input(
        "Interest on Related Party Loans (AED)",
        min_value=0.0,
        step=100.0,
        help="Interest paid to related parties may be subject to additional deductibility restrictions."
    )

    # Transitional Period Details
    transitional_period = st.radio(
        "Does this calculation relate to a transitional period (e.g., first year of tax)?",
        ["No", "Yes"],
        help="Special rules may apply for the first tax period after the law comes into effect."
    )

    return revenue, deductions, exempt_income, qualifying_income, non_qualifying_income, foreign_tax_paid, zakat_paid, entertainment_expenses, related_party_loan_interest, transitional_period
