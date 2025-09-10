import streamlit as st

# -------------------------------
# Header Section
# -------------------------------
st.markdown(
    """
    <h1 style="text-align:center; color:#2C3E50;">
        Ninth Direction Greeting Form
    </h1>
    <h4 style="text-align:center; color:#7F8C8D;">
        Right Direction for Your Business Promotion
    </h4>
    <hr style="border:1px solid #BDC3C7;"/>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Input Section
# -------------------------------
name = st.text_input("👤 Enter your name:")
age = st.slider("🎂 Select your age:", 1, 100, 18)
submitted = st.button("Submit")

# -------------------------------
# Output Section (styled in light green boxes)
# -------------------------------
if submitted:
    if name.strip():
        st.markdown(
            f"""
            <div style="margin-top:20px;">
                <div style="padding:10px 15px; border-radius:8px; 
                            background-color:#D4EFDF; border:1px solid #A9DFBF;
                            font-size:16px; color:#145A32;">
                    Hi {name}, Welcome to our Community.
                </div>
                <div style="margin-top:10px; padding:10px 15px; border-radius:8px; 
                            background-color:#D4EFDF; border:1px solid #A9DFBF;
                            font-size:16px; color:#145A32;">
                    We're thrilled to connect with you.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Please enter your name.")
