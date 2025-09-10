import streamlit as st

# -------------------------------
# Header Section
# -------------------------------
st.markdown(
    """
    <h1 style="text-align:center; color:#2C3E50;">
        Ninth Direction Calculator
    </h1>
    <hr style="border:1px solid #BDC3C7;">
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Input Section
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("Enter First Number", step=1.0, format="%.2f")

with col2:
    num2 = st.number_input("Enter Second Number", step=1.0, format="%.2f")

# Operator selection
operation = st.radio(
    "Choose Operation:",
    ("Add", "Subtract", "Multiply", "Divide"),
    horizontal=True
)

# -------------------------------
# Calculation Logic
# -------------------------------
if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
        st.success(f"Result: {num1} + {num2} = {result}")

    elif operation == "Subtract":
        result = num1 - num2
        st.success(f"Result: {num1} - {num2} = {result}")

    elif operation == "Multiply":
        result = num1 * num2
        st.success(f"Result: {num1} × {num2} = {result}")

    elif operation == "Divide":
        if num2 == 0:
            st.error("Hey... Its not possible")
        else:
            result = num1 / num2
            st.success(f"Result: {num1} ÷ {num2} = {result}")

# -------------------------------
# Footer Section
# -------------------------------
st.markdown(
    """
    <hr style="border:1px solid #BDC3C7;">
    <p style="text-align:center; color:#7F8C8D; font-style:italic;">
        I like big numbers and I cannot lie.
    </p>
    """,
    unsafe_allow_html=True
)
