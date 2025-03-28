import streamlit as st
import hashlib
import json

# Initialize an empty hospital ledger
if "hospital_ledger" not in st.session_state:
    st.session_state.hospital_ledger = {}

def generate_hash(patient_name, treatment, cost, date_of_visit):
    """Generate a unique hash for a visit."""
    hash_input = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.sha256(hash_input.encode()).hexdigest()

# Streamlit UI
st.title("🏥 Hospital Ledger System")

# Section to add a new patient visit
st.header("Add a Patient Visit")
patient_name = st.text_input("Patient Name").lower()
treatment = st.text_input("Treatment Received")
cost = st.number_input("Cost of Treatment ($)", min_value=0.0, format="%.2f")
date_of_visit = st.date_input("Date of Visit")

if st.button("Add/Update Visit"):
    if patient_name and treatment and cost and date_of_visit:
        visit_hash = generate_hash(patient_name, treatment, cost, str(date_of_visit))
        visit = {
            "treatment": treatment,
            "cost": cost,
            "date_of_visit": str(date_of_visit),
            "visit_hash": visit_hash,
        }
        
        if patient_name not in st.session_state.hospital_ledger:
            st.session_state.hospital_ledger[patient_name] = []
        
        st.session_state.hospital_ledger[patient_name].append(visit)
        st.success(f"Visit added for {patient_name} on {date_of_visit}.")
    else:
        st.error("Please fill in all fields.")

# Section to search for a patient's visits
st.header("Search Patient Records")
search_patient = st.text_input("Enter patient name to search").lower()

if st.button("Search"):
    if search_patient in st.session_state.hospital_ledger:
        st.write(f"### Visit Records for {search_patient}")
        for visit in st.session_state.hospital_ledger[search_patient]:
            st.json(visit, expanded=False)
    else:
        st.warning(f"Patient {search_patient} not found in the ledger.")

# Display the full ledger
st.header("📋 Full Hospital Ledger")
if st.session_state.hospital_ledger:
    st.json(st.session_state.hospital_ledger, expanded=False)
else:
    st.write("No records found.")
