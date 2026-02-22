import streamlit as st
import gemini
import openfda

# 1. Page Config
st.set_page_config(page_title="Symptom2Drug", page_icon="💊")

# 2. Sidebar for User Info (Adds "Professional" touch for judges)
with st.sidebar:
    st.header("User Profile")
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    st.info("Note: This is a hackathon prototype. Do not use for actual medical advice.")

# 3. Main Input Area
st.title("💊 Symptom to Drug Mapper")
user_input = st.text_area("Describe your symptoms:", placeholder="e.g., I have a burning sensation in my chest...")

if st.button("Find Treatments"):
    with st.spinner("Analyzing symptoms with Gemini..."):
        result = gemini.get_medical_data(user_input)
        print(result)
        # mock result to save api calls
        # result = {"condition": user_input, "search_term": user_input, "confidence": 85}  # Mock result for testing
        # result={"is_emergency": True, "condition": "Allergic Rhinitis", "search_term": "sneezing", "confidence": 90, "advice": "Over-the-counter antihistamines may help."}
        # st.success(f"Likely Condition: {result['condition']}")
    
    if not result:
        st.error("Could not analyze symptoms. Please try again.")
        st.stop()

    # EMERGENCY CHECK: This is the most important part for safety
    if result.get("is_emergency"):
        st.success(f"Likely Condition: **{result['condition']}**")
        st.error(f"🚨 **EMERGENCY:** {result.get('advice')}")
        st.markdown("### **Please call 911 or go to the nearest ER immediately.**")
        st.stop() # Stops the script here so it doesn't recommend drugs!

    # NON-EMERGENCY: Proceed to openFDA
    st.success(f"Likely Condition: **{result['condition']}**")
    
    with st.spinner("Fetching drugs from openFDA..."):
        # Use the search_term from Gemini for better API matching
        search_term = result.get('search_term', result['condition'])
        drugs = openfda.get_drugs_for_condition(search_term)
        
        if drugs:
            st.write("### Recommended Over-the-Counter Drugs:")
            print(drugs)  # For debugging
            for drug in drugs:
                # Our new get_drugs_for_condition already filters duplicates and 'Unknowns'
                # with st.expander(drug['name']):
                #     st.write(drug['snippet'])
                st.write(f"- {drug['name']}")
        else:
            st.info("No common OTC medications found in the FDA database for this condition.")
