import streamlit as st

st.set_page_config(
    page_title="BMI Calculator - Ninth Direction Hospital",
    page_icon="🏥",
    layout="centered",
)

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Return BMI value (kg/m^2)."""
    height_m = height_cm / 100.0
    if height_m <= 0:
        return 0.0
    return weight_kg / (height_m ** 2)

def bmi_category(bmi: float) -> str:
    """Classify BMI into Underweight, Normal, Overweight."""
    if bmi <= 0:
        return "Invalid"
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    else:
        return "Overweight"

def main():
    # --- Header (centered) ---
    st.markdown(
        """<div style="text-align:center;">
               <h1 style="margin:0;">BMI Calculator</h1>
               <h3 style="margin:0;font-weight:600;">Powered by Ninth Direction Hospital</h3>
           </div>""",
        unsafe_allow_html=True,
    )

    # Small CSS tweaks to reduce spacing a bit
    st.markdown(
        """<style>
            .small-label { font-size:14px; font-weight:600; margin:6px 0 4px 0; }
            .compact { margin-bottom: 6px; }
           </style>""",
        unsafe_allow_html=True,
    )

    # --- Gender label + radio (no extra space under label, radios in same row) ---
    st.markdown('<div class="small-label">Gender</div>', unsafe_allow_html=True)
    # zero-width label hides the default radio label while keeping accessibility
    gender = st.radio("\u200b", ["Male", "Female", "Other"], horizontal=True)

    # --- Height (choose unit) header (we do NOT show 'Choose unit' helper text) ---
    st.markdown('<div class="small-label">Height (choose unit)</div>', unsafe_allow_html=True)
    # unit selection inline
    height_option = st.radio("\u200b", ["Centimeters", "Feet & Inches"], horizontal=True)

    # show inputs
    if height_option == "Centimeters":
        # label shown via markdown above; hide the number_input label using a zero-width space
        height_cm = st.number_input("\u200b", min_value=0.0, max_value=300.0, value=0.0, step=0.1, format="%.1f", key="height_cm")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div style="font-size:13px;margin-bottom:4px;">Feet</div>', unsafe_allow_html=True)
            feet = st.number_input("\u200b", min_value=0, max_value=8, value=0, step=1, key="feet")
        with c2:
            st.markdown('<div style="font-size:13px;margin-bottom:4px;">Inches</div>', unsafe_allow_html=True)
            inches = st.number_input("\u200b", min_value=0, max_value=11, value=0, step=1, key="inches")
        height_cm = (feet * 30.48) + (inches * 2.54)

    # --- Weight (kg) label + input (label size same as others, default 0) ---
    st.markdown('<div class="small-label">Weight (kg)</div>', unsafe_allow_html=True)
    weight_kg = st.number_input("\u200b", min_value=0.0, max_value=500.0, value=0.0, step=0.1, format="%.1f", key="weight_kg")

    # --- Calculate button ---
    if st.button("Calculate BMI"):
        if height_cm <= 0 or weight_kg <= 0:
            st.error("Please enter valid height and weight (values must be greater than zero).")
        else:
            bmi = calculate_bmi(weight_kg, height_cm)
            bmi_rounded = round(bmi, 1)
            category = bmi_category(bmi)

            # Color according to BMI: green = normal, red = otherwise
            color = "green" if category == "Normal" else "red"

            st.markdown("### Result")
            st.markdown(f'<div style="font-size:32px;color:{color};margin:6px 0">{bmi_rounded}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-weight:600;">Category: <span style="color:{color};">{category}</span></div>', unsafe_allow_html=True)

            st.markdown("**Interpretation (general):**")
            st.write("- Underweight: BMI < 18.5")
            st.write("- Normal: 18.5 – 24.9")
            st.write("- Overweight: BMI ≥ 25")

            # Advice (kept non-prescriptive and aligned with IMA-style wording)
            if category == "Underweight":
                st.info("Your BMI suggests you may be underweight. Please consult a registered medical practitioner for evaluation.")
            elif category == "Normal":
                st.success("Your BMI is within the normal range. Continue regular health checks and a balanced lifestyle.")
            else:
                st.warning("Your BMI suggests you may be overweight. Please consult a qualified healthcare professional for personalised advice.")

    # Footer / Medical disclaimer (IMA-aligned)
    st.markdown("---")
    st.markdown(
        """<small><i>Disclaimer:</i> This BMI calculator is intended for general health awareness only and does not replace professional medical consultation. BMI is a screening tool, not a diagnostic test. For diagnosis or treatment, please consult a qualified doctor as per medical council / IMA guidance.</small>""",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
