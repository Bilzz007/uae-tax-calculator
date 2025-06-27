# components/business_info_section.py

import streamlit as st

def get_business_info():
    st.subheader("📋 Business Information")

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

    return free_zone, qualifying_fz, exempt_type
