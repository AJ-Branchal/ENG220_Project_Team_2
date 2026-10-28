import streamlit as st

# 1. Set up the browser tab
st.set_page_config(
    page_title="Cuba NM Safety Dashboard",
    page_icon="🚨",
    layout="wide"
)

# 2. Create the Sidebar Navigation Menu
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Project Introduction", "State-Wide Data Baseline", "Local Village Analysis"])

# =========================================================================
# PAGE 1: PROJECT INTRODUCTION
# =========================================================================
if page == "Project Introduction":
    st.title("🚨 Safety, Security & Crime: Cuba, New Mexico")
    st.subheader("Data-Driven Community Analysis")
    
    st.markdown("""
    Welcome to our team's data analysis platform. This application explores public safety, 
    crime metrics, and infrastructure security factors affecting New Mexico, with a focus 
    on the rural community of **Cuba, NM**.
    """)

# =========================================================================
# PAGE 2: STATE-WIDE DATA BASELINE
# =========================================================================
elif page == "State-Wide Data Baseline":
    st.title("📊 New Mexico vs. United States Baseline")
    st.write("This section tracks comparative data sourced from the FBI and CDC.")
    
    # Places for Graph 1 and Graph 2
    st.warning("⏳ Graph 1 Placeholder: New Mexico vs. US Violent Crime Rates goes here.")
    st.warning("⏳ Graph 2 Placeholder: New Mexico vs. US Firearm Mortality Rates goes here.")

# =========================================================================
# PAGE 3: LOCAL VILLAGE ANALYSIS
# =========================================================================
elif page == "Local Village Analysis":
    st.title("🏡 Local Impact: Village of Cuba & Sandoval County")
    st.write("This section focuses on our team's specific local data.")
    
    # Place for Graph 3
    st.warning("⏳ Graph 3 Placeholder: Local Cuba NM / Sandoval County Metric goes here.")