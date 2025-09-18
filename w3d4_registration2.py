import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os

# Page configuration
st.set_page_config(
    page_title="Heart Beat Registration",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem !important;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem !important;
        color: #FF9B73;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF9B73;
        color: white;
    }
    .success-box {
        background-color: #D4EDDA;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #C3E6CB;
    }
    .registration-count {
        background-color: #E9ECEF;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    .section-header {
        background-color: #FF9B73;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-top: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# App title and information
st.markdown('<h1 class="main-header">🎭 Heart Beat</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">College Cultural Program</h2>', unsafe_allow_html=True)

st.write("**Venue:** PSG College, Cauvery Auditorium")
st.write("**Date:** September 21, 2025")

# Initialize session state for registration count and form
if 'registration_count' not in st.session_state:
    # Load existing count from CSV if available
    if os.path.exists("registrations.csv"):
        df = pd.read_csv("registrations.csv")
        st.session_state.registration_count = len(df)
    else:
        st.session_state.registration_count = 0
        
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'last_registration' not in st.session_state:
    st.session_state.last_registration = {}
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = "Student Registration"

# Define events
events = ["Dance", "Singing", "Mono acting", "Standup comedy"]

# CSV file path
CSV_FILE = "registrations.csv"

# Function to load existing registrations
def load_registrations():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Major", "Phone", "Event", "Timestamp"])

# Function to save registration
def save_registration(name, major, phone, event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = {
        "Name": name,
        "Major": major,
        "Phone": phone,
        "Event": event,
        "Timestamp": timestamp
    }
    
    # Write to CSV file
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_data.keys())
        if f.tell() == 0:  # Check if file is empty to write header
            writer.writeheader()
        writer.writerow(new_data)
    
    # Update registration count and last registration
    st.session_state.registration_count += 1
    st.session_state.last_registration = {
        "name": name,
        "event": event
    }
    st.session_state.form_submitted = True

# Navigation options
option = st.radio(
    "Select Option:",
    ["Student Registration", "Admin Panel"],
    horizontal=True,
    index=0
)

# Student Registration Section
if option == "Student Registration":
    st.markdown('<div class="section-header"><h3>🎟️ Student Registration</h3></div>', unsafe_allow_html=True)

    # Show success message if form was just submitted
    if st.session_state.form_submitted:
        name = st.session_state.last_registration["name"]
        event = st.session_state.last_registration["event"]
        st.markdown(f"""
        <div class="success-box">
            <h3>Thank you, {name}!</h3>
            <p>You have successfully registered for <strong>{event}</strong>.</p>
            <p>We look forward to seeing you at the event!</p>
        </div>
        """, unsafe_allow_html=True)

    # Registration form
    with st.form("registration_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            major = st.text_input("Major/Department*", placeholder="e.g., Computer Science")
        
        with col2:
            phone = st.text_input("Phone Number*", placeholder="10-digit phone number")
            event = st.selectbox("Choose Event*", events, index=0)
        
        submitted = st.form_submit_button("Register Now")
        
        if submitted:
            if not name or not major or not phone:
                st.error("Please fill all required fields (*)")
            elif len(phone) < 10 or not phone.isdigit():
                st.error("Please enter a valid 10-digit phone number")
            else:
                save_registration(name, major, phone, event)
                st.rerun()

    # Display live registration count
    st.markdown("---")
    st.markdown('<div class="registration-count">', unsafe_allow_html=True)
    st.metric("Total Registrations", st.session_state.registration_count)
    st.markdown('</div>', unsafe_allow_html=True)

    # Show event-wise breakdown if we have registrations
    if st.session_state.registration_count > 0:
        df = load_registrations()
        if not df.empty:
            event_counts = df['Event'].value_counts()
            st.write("**Registrations by Event:**")
            col1, col2, col3, col4 = st.columns(4)
            cols = [col1, col2, col3, col4]
            
            for i, (event_name, count) in enumerate(event_counts.items()):
                with cols[i % 4]:
                    st.metric(event_name, count)

# Admin Panel Section
elif option == "Admin Panel":
    st.markdown('<div class="section-header"><h3>🔧 Admin Panel</h3></div>', unsafe_allow_html=True)
    st.write("Organizer tools for managing registrations")

    if os.path.exists(CSV_FILE):
        df = load_registrations()
        if not df.empty:
            # Display metrics
            st.subheader("Registration Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Registrations", len(df))
            
            with col2:
                st.metric("Unique Events", df['Event'].nunique())
            
            with col3:
                latest_reg = df['Timestamp'].max()
                if isinstance(latest_reg, str):
                    st.metric("Latest Registration", latest_reg.split()[0])
                else:
                    st.metric("Latest Registration", "N/A")
            
            # Event distribution chart
            st.subheader("Event Distribution")
            event_counts = df['Event'].value_counts()
            st.bar_chart(event_counts)
            
            # Data export
            st.subheader("Data Export")
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Full CSV",
                data=csv_data,
                file_name="heart_beat_registrations.csv",
                mime="text/csv",
                help="Download all registration data as a CSV file"
            )
            
            # Show data preview
            st.subheader("Registration Data Preview")
            st.dataframe(df)
            
            # Show raw data
            with st.expander("View Raw Data"):
                st.write(df)
        else:
            st.info("No registrations yet.")
    else:
        st.info("No registrations yet.")