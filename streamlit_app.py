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
    if user_input:
        with st.spinner("Analyzing symptoms with Gemini..."):
            # # Call your Gemini function here
            # result = gemini.get_medical_data(user_input)
            # print(result)  # For debugging
            # if result:
            #     st.success(f"Likely Condition: {result['condition']}")
            # else:
            #     st.error("Could not analyze symptoms. Please try again.")
            #     st.stop()

            # mock result to save api calls
            result = {"condition": user_input, "search_term": "heartburn", "confidence": 85}  # Mock result for testing
            st.success(f"Likely Condition: {result['condition']}")
            
        with st.spinner("Fetching drugs from openFDA..."):
            # Call your openFDA function here
            drugs = openfda.get_drugs_for_condition(result['condition'])
            print(drugs)  # For debugging
            clean_data = [x for x in drugs if x is not None]
            st.write("### Recommended Over-the-Counter Drugs:")
            for drug in clean_data:
                if drug and drug != "Unknown Name":  # Filter out unknown names
                    st.write(f"- {drug}")
    else:
        st.warning("Please enter some symptoms first.")