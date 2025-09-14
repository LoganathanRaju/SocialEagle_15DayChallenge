import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import time
import json
import os

# Page configuration
st.set_page_config(
    page_title="Hydration Tracker",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
    }
    .goal-box {
        background-color: #e6f2ff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .progress-bar {
        height: 30px;
        border-radius: 15px;
        background-color: #e0e0e0;
        margin: 10px 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 15px;
        background-color: #1f77b4;
        transition: width 0.5s ease-in-out;
        text-align: center;
        color: white;
        font-weight: bold;
        line-height: 30px;
    }
    .intake-box {
        background-color: #f0f7ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .celebration {
        text-align: center;
        color: #ff6b6b;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }
    .history-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Data storage functions
def load_data():
    """Load historical data from JSON file"""
    if os.path.exists("water_intake_data.json"):
        with open("water_intake_data.json", "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    """Save historical data to JSON file"""
    with open("water_intake_data.json", "w") as f:
        json.dump(data, f)

def get_daily_goal(target_date):
    """Get the daily goal for a specific date"""
    data = load_data()
    date_str = target_date.isoformat()
    if date_str in data and "daily_goal" in data[date_str]:
        return data[date_str]["daily_goal"]
    return 3000  # Default goal

def update_daily_goal(target_date, goal):
    """Update the daily goal for a specific date"""
    data = load_data()
    date_str = target_date.isoformat()
    if date_str not in data:
        data[date_str] = {"intake": 0, "history": []}
    data[date_str]["daily_goal"] = goal
    save_data(data)

# Initialize session state variables
if 'water_intake' not in st.session_state:
    st.session_state.water_intake = 0
if 'intake_history' not in st.session_state:
    st.session_state.intake_history = []
if 'goal_reached' not in st.session_state:
    st.session_state.goal_reached = False
if 'last_reset' not in st.session_state:
    st.session_state.last_reset = datetime.now().date()
if 'view_date' not in st.session_state:
    st.session_state.view_date = datetime.now().date()
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'custom_goal' not in st.session_state:
    st.session_state.custom_goal = 3000
if 'hist_time' not in st.session_state:
    st.session_state.hist_time = datetime.now().time()

# Check if it's a new day and reset if needed
current_date = datetime.now().date()
if current_date != st.session_state.last_reset:
    # Save yesterday's data
    data = load_data()
    yesterday_str = st.session_state.last_reset.isoformat()
    if st.session_state.water_intake > 0:
        data[yesterday_str] = {
            "intake": st.session_state.water_intake,
            "history": st.session_state.intake_history,
            "daily_goal": get_daily_goal(st.session_state.last_reset)
        }
        save_data(data)
    
    # Reset daily values
    st.session_state.water_intake = 0
    st.session_state.intake_history = []
    st.session_state.goal_reached = False
    st.session_state.last_reset = current_date

# Load data for the current view date
view_date_str = st.session_state.view_date.isoformat()
data = load_data()
if view_date_str in data:
    st.session_state.water_intake = data[view_date_str]["intake"]
    st.session_state.intake_history = data[view_date_str]["history"]
    st.session_state.custom_goal = data[view_date_str].get("daily_goal", 3000)
else:
    st.session_state.water_intake = 0
    st.session_state.intake_history = []
    st.session_state.custom_goal = get_daily_goal(st.session_state.view_date)

# Check if goal is reached for the viewed date
daily_goal = st.session_state.custom_goal
if st.session_state.water_intake >= daily_goal and daily_goal > 0:
    st.session_state.goal_reached = True
else:
    st.session_state.goal_reached = False

# App title
st.markdown('<h1 class="main-header">💧 Hydration Tracker</h1>', unsafe_allow_html=True)

# Sidebar for navigation and settings
with st.sidebar:
    st.header("Navigation & Settings")
    
    # Date selection
    selected_date = st.date_input(
        "Select date to view:",
        value=st.session_state.view_date,
        max_value=datetime.now().date()
    )
    
    if selected_date != st.session_state.view_date:
        st.session_state.view_date = selected_date
        st.rerun()
    
    # Edit mode toggle
    st.session_state.edit_mode = st.checkbox("Enable Edit Mode", value=st.session_state.edit_mode)
    
    if st.session_state.edit_mode:
        st.info("Edit mode enabled. You can modify historical data.")
        
        # Custom goal setting
        new_goal = st.number_input(
            "Set custom daily goal (ml):",
            min_value=500,
            max_value=5000,
            value=st.session_state.custom_goal,
            step=250
        )
        
        if new_goal != st.session_state.custom_goal:
            st.session_state.custom_goal = new_goal
            update_daily_goal(st.session_state.view_date, new_goal)
            st.success(f"Daily goal updated to {new_goal}ml")
            time.sleep(0.5)
            st.rerun()
    
    st.markdown("---")
    st.header("Add Water Intake")
    
    intake_options = {
        "Small Glass (200ml)": 200,
        "Medium Glass (300ml)": 300,
        "Large Glass (500ml)": 500,
        "Bottle (1000ml)": 1000
    }
    
    selected_intake = st.radio("Select intake amount:", list(intake_options.keys()))
    custom_intake = st.number_input("Or enter custom amount (ml):", min_value=0, max_value=2000, value=0, step=50)
    
    add_intake = st.button("Add Intake 💧")
    
    if add_intake:
        if custom_intake > 0:
            amount = custom_intake
        else:
            amount = intake_options[selected_intake]
        
        # Update current data
        st.session_state.water_intake += amount
        
        # Use current time for today's entries, stored time for historical entries
        if st.session_state.view_date == datetime.now().date():
            timestamp = datetime.now().strftime("%H:%M:%S")
        else:
            timestamp = st.session_state.hist_time.strftime("%H:%M:%S")
            
        intake_record = {
            "timestamp": timestamp,
            "amount": amount,
            "daily_total": st.session_state.water_intake
        }
        st.session_state.intake_history.append(intake_record)
        
        # Save to storage
        data = load_data()
        date_str = st.session_state.view_date.isoformat()
        if date_str not in data:
            data[date_str] = {"intake": 0, "history": []}
        
        data[date_str]["intake"] = st.session_state.water_intake
        data[date_str]["history"] = st.session_state.intake_history
        data[date_str]["daily_goal"] = st.session_state.custom_goal
        save_data(data)
        
        # Check if goal is reached
        if st.session_state.water_intake >= daily_goal and not st.session_state.goal_reached:
            st.session_state.goal_reached = True
            st.balloons()
        
        st.success(f"Added {amount}ml of water!")
        time.sleep(0.5)
        st.rerun()
    
    st.markdown("---")
    st.subheader("Weekly Progress")
    
    # Generate weekly data for chart
    dates = [datetime.now().date() - timedelta(days=i) for i in range(6, -1, -1)]
    water_intakes = []
    
    for d in dates:
        date_str = d.isoformat()
        data = load_data()
        if date_str in data:
            water_intakes.append(data[date_str]["intake"])
        else:
            water_intakes.append(0)
    
    weekly_data = {
        "Date": dates,
        "Water Intake (ml)": water_intakes
    }
    
    weekly_df = pd.DataFrame(weekly_data)
    
    # Display chart using Streamlit's built-in bar chart
    if not weekly_df.empty:
        st.bar_chart(weekly_df.set_index("Date")["Water Intake (ml)"])
        st.caption("Weekly Water Intake (ml)")
        
        # Add goal line
        avg_goal = sum([get_daily_goal(d) for d in dates]) / len(dates)
        st.write(f"Average Daily Goal: {avg_goal:.0f}ml")
    else:
        st.info("No data available for weekly chart yet.")

# Main content area
st.markdown(f'<div class="goal-box">', unsafe_allow_html=True)

# Show which date we're viewing
if st.session_state.view_date == datetime.now().date():
    st.subheader("Today's Hydration Goal")
else:
    st.subheader(f"Hydration Goal for {st.session_state.view_date.strftime('%B %d, %Y')}")

st.write(f"**Daily Goal:** {st.session_state.custom_goal}ml")

# Progress bar
if st.session_state.custom_goal > 0:
    progress_percent = min(st.session_state.water_intake / st.session_state.custom_goal * 100, 100)
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percent}%;">{progress_percent:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.write(f"**Current Intake:** {st.session_state.water_intake}ml / {st.session_state.custom_goal}ml")
st.markdown('</div>', unsafe_allow_html=True)

# Celebration message if goal reached
if st.session_state.goal_reached:
    st.markdown('<div class="celebration">🎉 Congratulations! You reached your daily water goal! 🎉</div>', unsafe_allow_html=True)

# Intake history
st.subheader(f"Intake History for {st.session_state.view_date.strftime('%B %d, %Y')}")
if st.session_state.intake_history:
    for i, intake in enumerate(reversed(st.session_state.intake_history)):
        st.markdown(f"""
        <div class="intake-box">
            <b>Intake {i+1}:</b> {intake["amount"]}ml at {intake["timestamp"]}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No water intake recorded for this day.")

# Manual intake addition for historical dates
if st.session_state.edit_mode and st.session_state.view_date != datetime.now().date():
    st.markdown("---")
    st.subheader("Add Historical Intake")
    
    hist_amount = st.number_input("Enter amount (ml):", min_value=0, max_value=2000, value=0, step=50, key="hist_intake")
    
    # Store the selected time in session state to prevent reset
    selected_time = st.time_input("Select time:", value=st.session_state.hist_time, key="hist_time")
    if selected_time != st.session_state.hist_time:
        st.session_state.hist_time = selected_time
    
    if st.button("Add Historical Record"):
        if hist_amount > 0:
            # Update current data
            st.session_state.water_intake += hist_amount
            
            # Use the selected time for historical entries
            intake_record = {
                "timestamp": st.session_state.hist_time.strftime("%H:%M:%S"),
                "amount": hist_amount,
                "daily_total": st.session_state.water_intake
            }
            st.session_state.intake_history.append(intake_record)
            
            # Save to storage
            data = load_data()
            date_str = st.session_state.view_date.isoformat()
            if date_str not in data:
                data[date_str] = {"intake": 0, "history": []}
            
            data[date_str]["intake"] = st.session_state.water_intake
            data[date_str]["history"] = st.session_state.intake_history
            data[date_str]["daily_goal"] = st.session_state.custom_goal
            save_data(data)
            
            st.success(f"Added {hist_amount}ml for {st.session_state.view_date.strftime('%B %d, %Y')} at {st.session_state.hist_time.strftime('%H:%M')}")
            time.sleep(0.5)
            st.rerun()

# Monthly summary
st.markdown("---")
with st.expander("Monthly Summary"):
    # Get current month data
    today = datetime.now().date()
    first_day = today.replace(day=1)
    next_month = first_day.replace(day=28) + timedelta(days=4)  # Ensure we get to the next month
    last_day = next_month - timedelta(days=next_month.day)
    
    month_days = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]
    
    month_data = []
    for day in month_days:
        day_str = day.isoformat()
        data = load_data()
        if day_str in data:
            intake = data[day_str]["intake"]
            goal = data[day_str].get("daily_goal", 3000)
            achieved = "✅" if intake >= goal else "❌"
            month_data.append({
                "Date": day.strftime("%Y-%m-%d"),
                "Intake (ml)": intake,
                "Goal (ml)": goal,
                "Achieved": achieved
            })
        else:
            month_data.append({
                "Date": day.strftime("%Y-%m-%d"),
                "Intake (ml)": 0,
                "Goal (ml)": get_daily_goal(day),
                "Achieved": "❌"
            })
    
    month_df = pd.DataFrame(month_data)
    st.dataframe(month_df, use_container_width=True)
    
    # Calculate success rate
    achieved_days = len([d for d in month_data if d["Achieved"] == "✅"])
    total_days = len(month_data)
    success_rate = (achieved_days / total_days) * 100 if total_days > 0 else 0
    
    st.metric("Monthly Success Rate", f"{success_rate:.1f}%", f"{achieved_days}/{total_days} days")

# Hydration tips
st.markdown("---")
st.subheader("💡 Hydration Tips")
tips = [
    "Start your day with a glass of water",
    "Keep a water bottle handy at all times",
    "Set reminders to drink water regularly",
    "Eat water-rich foods like fruits and vegetables",
    "Drink water before, during, and after exercise"
]

for tip in tips:
    st.write(f"- {tip}")

# Reset button (for testing purposes)
if st.button("Reset Current Day Data (for testing)"):
    data = load_data()
    date_str = st.session_state.view_date.isoformat()
    if date_str in data:
        del data[date_str]
        save_data(data)
    
    st.session_state.water_intake = 0
    st.session_state.intake_history = []
    st.session_state.goal_reached = False
    st.rerun()