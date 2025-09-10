import streamlit as st

# -------------------------------
# Header
# -------------------------------
st.title("Welcome to Ninth Direction School")
st.subheader("10th Marks Evaluation for 11th Group Eligibility")

# -------------------------------
# Input: Student Name
# -------------------------------
name = st.text_input("Enter Your Name")

# -------------------------------
# Input: Marks
# -------------------------------
st.markdown("### Enter Your 10th Standard Marks (out of 100)")
tamil = st.number_input("Tamil", min_value=0, max_value=100, step=1, key="tamil")
english = st.number_input("English", min_value=0, max_value=100, step=1, key="english")
maths = st.number_input("Maths", min_value=0, max_value=100, step=1, key="maths")
science = st.number_input("Science", min_value=0, max_value=100, step=1, key="science")
social = st.number_input("Social Science", min_value=0, max_value=100, step=1, key="social")

# -------------------------------
# Process Button (renamed to Validate)
# -------------------------------
if st.button("Validate"):
    # Check if name is entered
    if name.strip() == "":
        st.error("⚠️ Please enter your name.")
    else:
        marks = [tamil, english, maths, science, social]

        # Check if all fields filled
        if any(m == 0 for m in marks):
            st.error("⚠️ Please Enter All the Fields")
        else:
            # Fail condition
            if any(m < 35 for m in marks):
                st.error("❌ You are not eligible for Higher Secondary")
            # Weak student condition
            elif any(m < 50 for m in marks):
                st.warning("⚠️ Please Try Another School")
            else:
                # Calculate total and group eligibility
                total = sum(marks)
                st.write(f"📘 Total Marks: {total}/500")

                if total >= 450:
                    st.success("✅ You are Eligible For Science Group")
                elif 350 <= total < 450:
                    st.success("✅ You are Eligible For Arts Group")
                else:
                    st.success("✅ You are Eligible For Vocational Group")
