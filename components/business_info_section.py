# components/business_info_section.py

import streamlit as st

def get_business_info():
    st.subheader("📋 Business Information")

    # Entity Type (expanded)
    entity_type = st.selectbox(
        "Select your business type",
        [
            "Legal Entity",
            "Natural Person",
            "Partnership",
            "Trust",
            "Sole Proprietor",
            "Non-Resident"
        ],
        help="Choose the legal form of your business. Non-residents should select 'Non-Resident'."
    )

    # Residency Status
    residency_status = st.radio(
        "Are you a UAE resident for tax purposes?",
        ["Yes", "No"],
        help="This affects taxability and PE rules."
    )

    # Permanent Establishment (PE) Status
    pe_status = st.radio(
        "Does your business have a Permanent Establishment (PE) in the UAE?",
        ["No", "Yes", "Not Applicable"],
        help="Non-residents with a PE in the UAE may be subject to tax on UAE-sourced income."
    )

    # Sector
    sector = st.selectbox(
        "Select your business sector",
        [
            "General Business",
            "Banking",
            "Insurance",
            "Extractive Business",
            "Non-Extractive Natural Resource Business",
            "Other"
        ],
        help="Some sectors have special tax rules (e.g., banking, insurance, extractive)."
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

    # BEPS Pillar 2 (Global Minimum Tax)
    st.markdown('---')
    st.subheader('🌍 BEPS Pillar 2 (Global Minimum Tax)')
    is_mne_group = st.radio(
        'Is your business part of a Multinational Enterprise (MNE) Group?',
        ['No', 'Yes'],
        help='MNE Groups are groups with consolidated global revenue of at least EUR 750 million.'
    )
    global_revenue = 0.0
    globe_income = 0.0
    covered_taxes = 0.0
    if is_mne_group == 'Yes':
        global_revenue = st.number_input(
            'Global Consolidated Revenue (EUR)',
            min_value=0.0,
            step=1000000.0,
            help='Total consolidated revenue for the group (EUR).'
        )
        globe_income = st.number_input(
            'GloBE Income (EUR)',
            min_value=0.0,
            step=100000.0,
            help='GloBE income for the group (EUR).'
        )
        covered_taxes = st.number_input(
            'Covered Taxes (EUR)',
            min_value=0.0,
            step=100000.0,
            help='Total covered taxes for the group (EUR).'
        )

    # Sector sub-type/details
    sector_details = ''
    if sector == 'Banking':
        sector_details = st.text_input('Banking Sub-Sector/Details', help='Provide details if your business is a bank or financial institution.')
    elif sector == 'Insurance':
        sector_details = st.text_input('Insurance Sub-Sector/Details', help='Provide details if your business is an insurance company.')
    elif sector in ['Extractive Business', 'Non-Extractive Natural Resource Business']:
        sector_details = st.text_input('Extractive/Resource Sector Details', help='Provide details if your business is in extractive or resource sectors.')

    # Advanced/edge-case exemptions (placeholder)
    advanced_exemptions = st.text_area('Other Exemptions (if any, per latest FTA law/circulars)', help='Enter any new or edge-case exemptions not listed above.')

    # Anti-avoidance/GAAR warning
    gaar_warning = st.checkbox('I confirm that my business does not engage in artificial arrangements or hybrid mismatches (GAAR/anti-avoidance).', value=True)

    return entity_type, residency_status, pe_status, sector, sector_details, free_zone, qualifying_fz, exempt_type, advanced_exemptions, is_mne_group, global_revenue, globe_income, covered_taxes, gaar_warning
