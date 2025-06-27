# components/precheck_taxable_person.py

import streamlit as st

def taxable_person_precheck():
    st.subheader("⚖️ Taxable Person Pre-Check (Article 11)")

    col1, col2 = st.columns(2)
    with col1:
        is_uae_resident = st.radio("Are you a UAE Resident?", ["Yes", "No"], help="Includes Free Zone and mainland residency.")
        entity_type = st.selectbox("What type of person are you?", ["Legal Entity", "Natural Person"],
                                   help="Legal Entity = company, Natural = self-employed individual")
    with col2:
        is_doing_business = st.radio("Are you conducting business in the UAE?", ["Yes", "No"],
                                     help="E.g., sales, services, consultancy, manufacturing, etc.")
        is_non_resident_with_income = st.radio(
            "Are you a non-resident with UAE-sourced income or Permanent Establishment?",
            ["No", "Yes"],
            help="Only applies to non-residents earning in UAE."
        )

    # Logic
    is_taxable_person = False
    if is_uae_resident == "Yes" and is_doing_business == "Yes":
        is_taxable_person = True
    elif is_uae_resident == "No" and is_non_resident_with_income == "Yes":
        is_taxable_person = True

    if is_taxable_person:
        st.success("✅ Based on your inputs, you fall under the definition of a **Taxable Person** (Article 11).")
    else:
        st.warning("❌ You are not considered a Taxable Person under UAE Corporate Tax — no tax calculation will apply.")

    st.markdown("---")

    return entity_type, is_taxable_person
