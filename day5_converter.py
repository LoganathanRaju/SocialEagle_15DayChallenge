import streamlit as st

# Custom CSS for nice coloring
st.markdown(
    """
    <style>
    .main {background-color: #def7e5;}
    .stButton>button {background-color:#00897B; color:white;}
    .stSelectbox, .stTextInput {background-color: #fff9e6;}
    .result-box {background-color: #ffefef; padding: 10px; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True
)

# Title and description
st.title("✨ Friendly Unit Converter")
st.write("Convert **Currency, Temperature, Length, Weight** — instantly and beautifully!")

conversion_type = st.selectbox(
    "Select conversion type:",
    ["Currency", "Temperature", "Length", "Weight"]
)

amount = st.number_input("Enter value to convert:", min_value=0.0, format="%.2f")

# Definitions for units
units = {
    "Currency": ["USD", "EUR", "INR"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Length": ["Meter", "Kilometer", "Mile", "Foot"],
    "Weight": ["Gram", "Kilogram", "Pound", "Ounce"]
}

from_unit = st.selectbox("Convert from:", units[conversion_type])
to_unit = st.selectbox("Convert to:", units[conversion_type])

def convert(amount, from_unit, to_unit, conversion_type):
    # Currency conversion rates (example; in production use a live API)
    rates = {'USD': 1.0, 'EUR': 0.94, 'INR': 83.2}
    if conversion_type == 'Currency':
        result = amount / rates[from_unit] * rates[to_unit]
    # Temperature conversions
    elif conversion_type == 'Temperature':
        if from_unit == to_unit:
            result = amount
        elif from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                result = (amount * 9/5) + 32
            elif to_unit == "Kelvin":
                result = amount + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                result = (amount - 32) * 5/9
            elif to_unit == "Kelvin":
                result = ((amount - 32) * 5/9) + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                result = amount - 273.15
            elif to_unit == "Fahrenheit":
                result = ((amount - 273.15) * 9/5) + 32
    # Length conversions
    elif conversion_type == "Length":
        factors = {"Meter": 1.0, "Kilometer": 1000.0, "Mile": 1609.34, "Foot": 0.3048}
        result = amount * factors[from_unit] / factors[to_unit]
    # Weight conversions
    elif conversion_type == "Weight":
        factors = {"Gram": 1.0, "Kilogram": 1000.0, "Pound": 453.592, "Ounce": 28.3495}
        result = amount * factors[from_unit] / factors[to_unit]
    else:
        result = amount
    return result

if st.button("Convert"):
    try:
        converted = convert(amount, from_unit, to_unit, conversion_type)
        st.markdown(
            f'<div class="result-box">🔄 <b>{amount} {from_unit}</b> = <span style="color:#d81b60;"><b>{converted:.2f} {to_unit}</b></span></div>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("""<hr style="border:gray 1px solid;">
    <small>Made with Streamlit. For demo only — currency rates are fixed for simplicity.</small>
    """, unsafe_allow_html=True)
