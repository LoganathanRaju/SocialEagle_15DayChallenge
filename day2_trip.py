import streamlit as st

# -------------------------------
# Title and Description
# -------------------------------
st.title("💰 Bill Splitter App")
st.write("Easily split expenses among friends during a trip.")

# -------------------------------
# Input Section (Top row)
# -------------------------------
label_style = "font-size:18px; font-weight:bold;"  # Uniform label style

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f'<span style="{label_style}">Total Amount Spent (₹)</span>', unsafe_allow_html=True)
    total_amount = st.number_input("", min_value=0.0, step=100.0, key="total_amount")
with col2:
    st.markdown(f'<span style="{label_style}">Number of People</span>', unsafe_allow_html=True)
    num_people = st.number_input("", min_value=1, step=1, key="num_people")

# -------------------------------
# Collect names and amounts spent
# -------------------------------
expenses = {}
if num_people > 0:
    st.subheader("Enter Name and Amount Spent")
    for i in range(int(num_people)):
        col1, col2 = st.columns([2, 1])  # Name wider than amount
        with col1:
            st.markdown(f'<span style="{label_style}">Name of Person {i+1}</span>', unsafe_allow_html=True)
            name = st.text_input("", key=f"name_{i}")
        with col2:
            st.markdown(f'<span style="{label_style}">Amount (₹)</span>', unsafe_allow_html=True)
            spent = st.number_input("", min_value=0.0, step=50.0, key=f"spent_{i}")
        expenses[name] = spent

# -------------------------------
# Calculation & Validation
# -------------------------------
if st.button("Calculate Settlement") and expenses:

    # 1️⃣ Check for empty names
    if "" in expenses.keys():
        st.error("😅 Oops! Looks like someone forgot to write their name. Please fill in all name fields.")
    else:
        # 2️⃣ Check if total of amounts matches total_amount
        sum_entered = sum(expenses.values())
        if sum_entered != total_amount:
            st.error(f"🤔 Hmm, the numbers are having a little disagreement. "
                     f"The total of the amounts (₹{sum_entered:.2f}) doesn't equal the total you entered (₹{total_amount:.2f}). Please check again!")
        else:
            # Proceed with calculation
            equal_share = total_amount / num_people
            st.subheader("📊 Settlement Summary")

            for name, spent in expenses.items():
                balance = spent - equal_share
                if balance > 0:
                    st.success(f"{name} should **get back ₹{balance:.2f}**")
                elif balance < 0:
                    st.error(f"{name} should **pay ₹{-balance:.2f}**")
                else:
                    st.info(f"{name} is **settled up** ✅")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:16px;">
        ✈️ Happy trips, happy friendships!
    </div>
    """,
    unsafe_allow_html=True
)
