import streamlit as st
import pandas as pd

# Static exchange rates as of September 16 (base: USD)
EXCHANGE_RATES = {
    'USD': {
        'USD': 1.0,
        'INR': 83.25,    # Indian Rupee
        'EUR': 0.93,     # Euro
        'SGD': 1.36,     # Singapore Dollar
        'MYR': 4.68,     # Malaysian Ringgit
        'AED': 3.67,     # UAE Dirham
        'JPY': 147.50,   # Japanese Yen
        'IDR': 15320.0,  # Indonesian Rupiah
        'LKR': 325.0,    # Sri Lankan Rupee
        'PHP': 56.80,    # Philippine Peso
        'AUD': 1.54,     # Australian Dollar
        'PLN': 4.25,     # Polish Złoty
        'NPR': 132.0     # Nepalese Rupee
    },
    'INR': {
        'USD': 0.012,
        'INR': 1.0,
        'EUR': 0.011,
        'SGD': 0.016,
        'MYR': 0.056,
        'AED': 0.044,
        'JPY': 1.77,
        'IDR': 184.0,
        'LKR': 3.90,
        'PHP': 0.68,
        'AUD': 0.0185,
        'PLN': 0.051,
        'NPR': 1.59
    },
    'EUR': {
        'USD': 1.075,
        'INR': 89.52,
        'EUR': 1.0,
        'SGD': 1.46,
        'MYR': 5.03,
        'AED': 3.95,
        'JPY': 158.6,
        'IDR': 16473.0,
        'LKR': 349.5,
        'PHP': 61.1,
        'AUD': 1.66,
        'PLN': 4.57,
        'NPR': 142.0
    },
    'SGD': {
        'USD': 0.735,
        'INR': 61.18,
        'EUR': 0.685,
        'SGD': 1.0,
        'MYR': 3.44,
        'AED': 2.70,
        'JPY': 108.5,
        'IDR': 11265.0,
        'LKR': 239.0,
        'PHP': 41.8,
        'AUD': 1.13,
        'PLN': 3.12,
        'NPR': 97.1
    },
    'MYR': {
        'USD': 0.214,
        'INR': 17.81,
        'EUR': 0.199,
        'SGD': 0.291,
        'MYR': 1.0,
        'AED': 0.785,
        'JPY': 31.5,
        'IDR': 3275.0,
        'LKR': 69.5,
        'PHP': 12.15,
        'AUD': 0.33,
        'PLN': 0.91,
        'NPR': 28.2
    },
    'AED': {
        'USD': 0.272,
        'INR': 22.65,
        'EUR': 0.253,
        'SGD': 0.370,
        'MYR': 1.274,
        'AED': 1.0,
        'JPY': 40.2,
        'IDR': 4175.0,
        'LKR': 88.5,
        'PHP': 15.48,
        'AUD': 0.42,
        'PLN': 1.16,
        'NPR': 36.0
    },
    'JPY': {
        'USD': 0.00678,
        'INR': 0.565,
        'EUR': 0.0063,
        'SGD': 0.00922,
        'MYR': 0.0317,
        'AED': 0.0249,
        'JPY': 1.0,
        'IDR': 103.9,
        'LKR': 2.20,
        'PHP': 0.385,
        'AUD': 0.0104,
        'PLN': 0.0288,
        'NPR': 0.895
    },
    'IDR': {
        'USD': 0.000065,
        'INR': 0.00543,
        'EUR': 0.000061,
        'SGD': 0.000089,
        'MYR': 0.000305,
        'AED': 0.00024,
        'JPY': 0.00962,
        'IDR': 1.0,
        'LKR': 0.0212,
        'PHP': 0.00371,
        'AUD': 0.0001,
        'PLN': 0.000277,
        'NPR': 0.00862
    },
    'LKR': {
        'USD': 0.00308,
        'INR': 0.256,
        'EUR': 0.00286,
        'SGD': 0.00418,
        'MYR': 0.0144,
        'AED': 0.0113,
        'JPY': 0.455,
        'IDR': 47.2,
        'LKR': 1.0,
        'PHP': 0.175,
        'AUD': 0.00474,
        'PLN': 0.0131,
        'NPR': 0.406
    },
    'PHP': {
        'USD': 0.0176,
        'INR': 1.47,
        'EUR': 0.0164,
        'SGD': 0.0239,
        'MYR': 0.0823,
        'AED': 0.0646,
        'JPY': 2.60,
        'IDR': 270.0,
        'LKR': 5.71,
        'PHP': 1.0,
        'AUD': 0.0271,
        'PLN': 0.0748,
        'NPR': 2.32
    },
    'AUD': {
        'USD': 0.65,
        'INR': 54.1,
        'EUR': 0.602,
        'SGD': 0.885,
        'MYR': 3.03,
        'AED': 2.38,
        'JPY': 96.2,
        'IDR': 10000.0,
        'LKR': 211.0,
        'PHP': 36.9,
        'AUD': 1.0,
        'PLN': 2.76,
        'NPR': 85.7
    },
    'PLN': {
        'USD': 0.235,
        'INR': 19.6,
        'EUR': 0.219,
        'SGD': 0.321,
        'MYR': 1.10,
        'AED': 0.862,
        'JPY': 34.7,
        'IDR': 3610.0,
        'LKR': 76.5,
        'PHP': 13.37,
        'AUD': 0.362,
        'PLN': 1.0,
        'NPR': 31.1
    },
    'NPR': {
        'USD': 0.00758,
        'INR': 0.631,
        'EUR': 0.00704,
        'SGD': 0.0103,
        'MYR': 0.0354,
        'AED': 0.0278,
        'JPY': 1.12,
        'IDR': 116.0,
        'LKR': 2.46,
        'PHP': 0.431,
        'AUD': 0.0117,
        'PLN': 0.0322,
        'NPR': 1.0
    }
}

# Currency symbols and full names
CURRENCY_INFO = {
    'USD': {'symbol': '$', 'name': 'US Dollar', 'color': '#2E86AB'},
    'EUR': {'symbol': '€', 'name': 'Euro', 'color': '#A23B72'},
    'INR': {'symbol': '₹', 'name': 'Indian Rupee', 'color': '#FF9F1C'},
    'SGD': {'symbol': 'S$', 'name': 'Singapore Dollar', 'color': '#20BF55'},
    'MYR': {'symbol': 'RM', 'name': 'Malaysian Ringgit', 'color': '#F39237'},
    'AED': {'symbol': 'د.إ', 'name': 'UAE Dirham', 'color': '#5C2751'},
    'JPY': {'symbol': '¥', 'name': 'Japanese Yen', 'color': '#E71D36'},
    'IDR': {'symbol': 'Rp', 'name': 'Indonesian Rupiah', 'color': '#2A9D8F'},
    'LKR': {'symbol': 'Rs', 'name': 'Sri Lankan Rupee', 'color': '#7209B7'},
    'PHP': {'symbol': '₱', 'name': 'Philippine Peso', 'color': '#F72585'},
    'AUD': {'symbol': 'A$', 'name': 'Australian Dollar', 'color': '#4CC9F0'},
    'PLN': {'symbol': 'zł', 'name': 'Polish Złoty', 'color': '#560BAD'},
    'NPR': {'symbol': 'Rs', 'name': 'Nepalese Rupee', 'color': '#FB8500'}
}

def convert_currency(amount, from_currency, to_currency):
    """Convert currency using the static exchange rates"""
    if from_currency == to_currency:
        return amount
    
    try:
        conversion_rate = EXCHANGE_RATES[from_currency][to_currency]
        return amount * conversion_rate
    except KeyError:
        return None

def main():
    st.set_page_config(
        page_title="Global Currency Converter",
        page_icon="💱",
        layout="centered"
    )
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #5C2751;
        text-align: center;
        margin-bottom: 2rem;
    }
    .currency-box {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    .stButton button {
        width: 100%;
        background-color: #5C2751;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }
    .result-box {
        background-color: #E8EBEE;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    .currency-info {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .currency-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
        margin: 20px 0;
    }
    .currency-card {
        background: white;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">💱 Global Currency Converter</h1>', unsafe_allow_html=True)
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        # From currency selection with colored box
        from_currency = st.selectbox(
            "From Currency:",
            options=list(EXCHANGE_RATES.keys()),
            index=0,  # Default to USD
            format_func=lambda x: f"{CURRENCY_INFO[x]['symbol']} {x} - {CURRENCY_INFO[x]['name']}"
        )
        
        # Display colored box for from currency
        from_color = CURRENCY_INFO[from_currency]['color']
        st.markdown(f"""
        <div class="currency-box" style="border-color: {from_color}">
            <h3 style="color: {from_color}; margin: 0;">From Currency</h3>
            <p style="font-size: 1.5rem; margin: 0;">{CURRENCY_INFO[from_currency]['symbol']} {from_currency}</p>
            <p style="margin: 0;">{CURRENCY_INFO[from_currency]['name']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # To currency selection with colored box
        to_currency = st.selectbox(
            "To Currency:",
            options=list(EXCHANGE_RATES.keys()),
            index=1,  # Default to INR
            format_func=lambda x: f"{CURRENCY_INFO[x]['symbol']} {x} - {CURRENCY_INFO[x]['name']}"
        )
        
        # Display colored box for to currency
        to_color = CURRENCY_INFO[to_currency]['color']
        st.markdown(f"""
        <div class="currency-box" style="border-color: {to_color}">
            <h3 style="color: {to_color}; margin: 0;">To Currency</h3>
            <p style="font-size: 1.5rem; margin: 0;">{CURRENCY_INFO[to_currency]['symbol']} {to_currency}</p>
            <p style="margin: 0;">{CURRENCY_INFO[to_currency]['name']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Amount input - placed below the currency selection
    amount = st.number_input(
        "Enter Amount:",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.2f"
    )
    
    # Convert button
    convert_button = st.button("Convert Currency", type="primary")
    
    # Display result
    if convert_button:
        if amount <= 0:
            st.error("Please enter a positive amount.")
        else:
            result = convert_currency(amount, from_currency, to_currency)
            if result is not None:
                # Format numbers with appropriate decimal places
                if result < 1:
                    result_str = f"{result:,.4f}"
                elif result > 1000:
                    result_str = f"{result:,.0f}"
                else:
                    result_str = f"{result:,.2f}"
                
                st.markdown(f"""
                <div class="result-box">
                    <h2 style="color: {from_color};">{CURRENCY_INFO[from_currency]['symbol']} {amount:,.2f} {from_currency}</h2>
                    <h1 style="margin: 10px 0;">⬇️</h1>
                    <h2 style="color: {to_color};">{CURRENCY_INFO[to_currency]['symbol']} {result_str} {to_currency}</h2>
                    <p>Exchange rate: 1 {from_currency} = {EXCHANGE_RATES[from_currency][to_currency]:,.6f} {to_currency}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Conversion failed. Please try again.")
    
    # Currency information section
    st.markdown("---")
    st.subheader("💰 Supported Currencies")
    
    # Display currencies in a grid layout
    st.markdown('<div class="currency-grid">', unsafe_allow_html=True)
    for code, info in CURRENCY_INFO.items():
        st.markdown(f"""
        <div class="currency-card" style="border-color: {info['color']}">
            <h4 style="color: {info['color']}; margin: 0;">{info['symbol']} {code}</h4>
            <p style="margin: 5px 0; font-size: 0.9rem;">{info['name']}</p>
            <p style="margin: 0; font-size: 0.8rem; color: #666;">1 USD = {EXCHANGE_RATES['USD'][code]:.2f} {code}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional information
    st.markdown("---")
    st.markdown("""
    <div class="currency-info">
        <h4>💡 How to use:</h4>
        <ol>
            <li>Select the currency you want to convert <b>FROM</b></li>
            <li>Select the currency you want to convert <b>TO</b></li>
            <li>Enter the amount you want to convert</li>
            <li>Click the <b>Convert Currency</b> button</li>
        </ol>
        <p><i>Note: Exchange rates are static and based on September 16 values.</i></p>
        <p><b>Newly added currencies:</b> JPY (Japan), IDR (Indonesia), LKR (Sri Lanka), PHP (Philippines), AUD (Australia), PLN (Poland), NPR (Nepal)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()