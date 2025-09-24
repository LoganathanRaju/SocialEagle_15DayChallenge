import streamlit as st
import time
import datetime

# Configure page
st.set_page_config(
    page_title="Stopwatch App",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with basic solid colors
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF0000;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
        padding: 10px;
        background-color: #FFE4E1;
        border-radius: 10px;
        border: 3px solid #FF0000;
    }
    .time-display {
        font-size: 4rem;
        text-align: center;
        color: #008000;
        font-weight: bold;
        margin: 2rem 0;
        padding: 20px;
        background-color: #F0FFF0;
        border: 4px solid #008000;
        border-radius: 15px;
    }
    .start-button {
        background-color: #008000 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: 2px solid #006400 !important;
    }
    .start-button:hover {
        background-color: #006400 !important;
    }
    .stop-button {
        background-color: #FF0000 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: 2px solid #8B0000 !important;
    }
    .stop-button:hover {
        background-color: #8B0000 !important;
    }
    .reset-button {
        background-color: #0000FF !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: 2px solid #00008B !important;
    }
    .reset-button:hover {
        background-color: #00008B !important;
    }
    .status-running {
        color: #008000;
        font-weight: bold;
        font-size: 20px;
        background-color: #F0FFF0;
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #008000;
    }
    .status-stopped {
        color: #FF0000;
        font-weight: bold;
        font-size: 20px;
        background-color: #FFE4E1;
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #FF0000;
    }
    .instruction-box {
        background-color: #FFF8DC;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #FFA500;
        color: #000000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'last_time' not in st.session_state:
    st.session_state.last_time = 0
if 'laps' not in st.session_state:
    st.session_state.laps = []

# Header
st.markdown('<div class="main-header">⏱️ STOPWATCH TIMER</div>', unsafe_allow_html=True)

# Calculate current time
if st.session_state.running:
    current_elapsed = time.time() - st.session_state.start_time
    total_elapsed = st.session_state.last_time + current_elapsed
else:
    total_elapsed = st.session_state.last_time

# Format time display
time_str = str(datetime.timedelta(seconds=total_elapsed))
if '.' in time_str:
    hours, remainder = time_str.split(':')[0], time_str.split(':')[1:]
    minutes, seconds = remainder[0], remainder[1].split('.')[0]
    milliseconds = remainder[1].split('.')[1][:3]
else:
    hours, minutes, seconds = time_str.split(':')
    milliseconds = "000"

formatted_time = f"{int(hours):02d}:{minutes}:{seconds}.{milliseconds}"

# Display timer
st.markdown(f'<div class="time-display">{formatted_time}</div>', unsafe_allow_html=True)

# Status indicator
if st.session_state.running:
    st.markdown('<div class="status-running">🟢 TIMER IS RUNNING</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-stopped">🔴 TIMER IS STOPPED</div>', unsafe_allow_html=True)

# Control buttons
col1, col2, col3 = st.columns(3)

with col1:
    # Start button
    st.markdown("""
    <style>
        div[data-testid="stButton"] button[kind="secondary"]:first-child {
            background-color: #008000 !important;
            color: white !important;
            font-weight: bold !important;
            border: 2px solid #006400 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    start_clicked = st.button("▶️ START", key="start", use_container_width=True)

with col2:
    # Stop button
    st.markdown("""
    <style>
        div[data-testid="stButton"] button[kind="secondary"]:nth-child(2) {
            background-color: #FF0000 !important;
            color: white !important;
            font-weight: bold !important;
            border: 2px solid #8B0000 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    stop_clicked = st.button("⏸️ STOP", key="stop", use_container_width=True)

with col3:
    # Reset button
    st.markdown("""
    <style>
        div[data-testid="stButton"] button[kind="secondary"]:nth-child(3) {
            background-color: #0000FF !important;
            color: white !important;
            font-weight: bold !important;
            border: 2px solid #00008B !important;
        }
    </style>
    """, unsafe_allow_html=True)
    reset_clicked = st.button("🔄 RESET", key="reset", use_container_width=True)

# Button functionality
if start_clicked and not st.session_state.running:
    st.session_state.running = True
    st.session_state.start_time = time.time()
    st.success("Timer started!")

if stop_clicked and st.session_state.running:
    st.session_state.running = False
    st.session_state.last_time += time.time() - st.session_state.start_time
    st.error("Timer stopped!")

if reset_clicked:
    st.session_state.running = False
    st.session_state.start_time = None
    st.session_state.last_time = 0
    st.session_state.laps = []
    st.warning("Timer reset!")

# Lap functionality
st.markdown("---")
st.subheader("Lap Times")

lap_col1, lap_col2 = st.columns([3, 1])

with lap_col1:
    lap_clicked = st.button("⏱️ Record Lap", use_container_width=True)

with lap_col2:
    clear_laps = st.button("🗑️ Clear Laps", use_container_width=True)

if lap_clicked and st.session_state.running:
    current_time = st.session_state.last_time + (time.time() - st.session_state.start_time)
    st.session_state.laps.append(current_time)
    st.success(f"Lap {len(st.session_state.laps)} recorded!")

if clear_laps:
    st.session_state.laps = []
    st.info("Lap times cleared!")

# Display laps
if st.session_state.laps:
    st.write("### Lap History:")
    for i, lap in enumerate(st.session_state.laps, 1):
        lap_str = str(datetime.timedelta(seconds=lap))
        if '.' in lap_str:
            lap_display = lap_str.split('.')[0] + "." + lap_str.split('.')[1][:3]
        else:
            lap_display = lap_str
        st.write(f"**Lap {i}:** {lap_display}")

# Instructions
st.markdown("---")
st.markdown("### Instructions:")
st.markdown("""
<div class="instruction-box">
• Click <span style="color:#008000; font-weight:bold;">▶️ START</span> to begin the timer<br>
• Click <span style="color:#FF0000; font-weight:bold;">⏸️ STOP</span> to pause the timer<br>
• Click <span style="color:#0000FF; font-weight:bold;">🔄 RESET</span> to reset to zero<br>
• Click <span style="color:#FFA500; font-weight:bold;">⏱️ Record Lap</span> to record split times<br>
• Format: HH:MM:SS.mmm
</div>
""", unsafe_allow_html=True)

# Auto-refresh when running
if st.session_state.running:
    time.sleep(0.01)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #000000; font-weight: bold;'>Built with Streamlit • Basic Stopwatch App</div>", unsafe_allow_html=True)