import streamlit as st

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
            # Call your Gemini function here
            # result = get_medical_data(user_input)
            st.success(f"Likely Condition: Heartburn") # Mock for now
            
        with st.spinner("Fetching drugs from openFDA..."):
            # Call your openFDA function here
            st.write("### Recommended Over-the-Counter Drugs:")
            st.write("- Antacids (Tums)")
            st.write("- H2 Blockers (Pepcid)")
    else:
        st.warning("Please enter some symptoms first.")