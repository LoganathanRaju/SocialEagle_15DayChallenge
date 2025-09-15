import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Gum Workout Logger",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
    }
    .subheader {
        font-size: 1.5rem;
        color: #A23B72;
    }
    .metric-card {
        background-color: #F5F5F5;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .progress-bar {
        background-color: #2E86AB;
        height: 10px;
        border-radius: 5px;
    }
    .exercise-card {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #A23B72;
    }
    .success-message {
        background-color: #D4EDDA;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .week-table {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .graph-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to ensure consistent date format
def normalize_date(date_obj):
    """Convert date to pandas Timestamp for consistent comparison"""
    if isinstance(date_obj, pd.Timestamp):
        return date_obj
    elif isinstance(date_obj, datetime.date):
        return pd.Timestamp(date_obj)
    else:
        return pd.to_datetime(date_obj)

# Initialize session state for data storage
if 'workouts' not in st.session_state:
    st.session_state.workouts = pd.DataFrame(columns=[
        'date', 'exercise', 'sets', 'reps', 'weight'
    ])

if 'exercises' not in st.session_state:
    st.session_state.exercises = [
        'Bench Press', 'Squat', 'Deadlift', 'Shoulder Press', 
        'Pull-ups', 'Bicep Curls', 'Tricep Extensions', 'Leg Press'
    ]

# App header
st.markdown('<h1 class="main-header">💪 Gum Workout Logger</h1>', unsafe_allow_html=True)
st.markdown("Track your progress, set new records, and become your best self!")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ["Log Workout", "View History", "Progress Dashboard"])
    
    st.header("Info")
    st.info("""
    Welcome to Gum Workout Logger! 
    - Log your daily exercises
    - Track sets, reps, and weight
    - Monitor your weekly progress
    """)
    
    # Add a new exercise
    st.header("Add New Exercise")
    new_exercise = st.text_input("Exercise Name")
    if st.button("Add Exercise") and new_exercise:
        if new_exercise not in st.session_state.exercises:
            st.session_state.exercises.append(new_exercise)
            st.success(f"Added {new_exercise} to exercises!")
        else:
            st.warning("Exercise already exists!")

# Log Workout Page
if page == "Log Workout":
    st.markdown('<h2 class="subheader">Log Your Workout</h2>', unsafe_allow_html=True)
    
    with st.form("workout_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", datetime.date.today())
            exercise = st.selectbox("Exercise", st.session_state.exercises)
        
        with col2:
            sets = st.number_input("Sets", min_value=1, max_value=20, value=3)
            reps = st.number_input("Reps", min_value=1, max_value=50, value=10)
            weight = st.number_input("Weight (lbs)", min_value=0, max_value=1000, value=50)
        
        submitted = st.form_submit_button("Save Workout")
        
        if submitted:
            # Convert date to Timestamp for consistency
            date_ts = pd.Timestamp(date)
            new_workout = pd.DataFrame({
                'date': [date_ts],
                'exercise': [exercise],
                'sets': [sets],
                'reps': [reps],
                'weight': [weight]
            })
            
            st.session_state.workouts = pd.concat([st.session_state.workouts, new_workout], ignore_index=True)
            st.markdown('<div class="success-message">Workout logged successfully! 💪</div>', unsafe_allow_html=True)
            
            # Show recent workouts
            if not st.session_state.workouts.empty:
                st.subheader("Recent Workouts")
                recent_workouts = st.session_state.workouts.sort_values('date', ascending=False).head(3)
                for _, row in recent_workouts.iterrows():
                    # Convert back to date for display
                    display_date = row['date'].date() if hasattr(row['date'], 'date') else row['date']
                    st.markdown(f"""
                    <div class="exercise-card">
                        <strong>{row['exercise']}</strong> on {display_date}<br>
                        {row['sets']} sets × {row['reps']} reps × {row['weight']} lbs
                    </div>
                    """, unsafe_allow_html=True)

# View History Page
elif page == "View History":
    st.markdown('<h2 class="subheader">Workout History</h2>', unsafe_allow_html=True)
    
    if st.session_state.workouts.empty:
        st.info("No workouts logged yet. Start logging to see your history!")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            exercise_filter = st.multiselect(
                "Filter by Exercise",
                options=st.session_state.exercises,
                default=st.session_state.exercises
            )
        
        with col2:
            # Get min and max dates from workouts (convert to date for the date_input)
            min_date = st.session_state.workouts['date'].min()
            max_date = st.session_state.workouts['date'].max()
            
            # Convert to datetime.date for the date_input widget
            if hasattr(min_date, 'date'):
                min_date_display = min_date.date()
            else:
                min_date_display = min_date
                
            if hasattr(max_date, 'date'):
                max_date_display = max_date.date()
            else:
                max_date_display = max_date
                
            date_range = st.date_input(
                "Date Range",
                value=(min_date_display, max_date_display),
                min_value=min_date_display,
                max_value=datetime.date.today()
            )
        
        # Apply filters - convert date_range to Timestamps for comparison
        if len(date_range) == 2:
            start_ts = pd.Timestamp(date_range[0])
            end_ts = pd.Timestamp(date_range[1])
            
            filtered_data = st.session_state.workouts[
                (st.session_state.workouts['exercise'].isin(exercise_filter)) &
                (st.session_state.workouts['date'] >= start_ts) &
                (st.session_state.workouts['date'] <= end_ts)
            ]
        else:
            filtered_data = st.session_state.workouts[
                (st.session_state.workouts['exercise'].isin(exercise_filter))
            ]
        
        # Display data
        if not filtered_data.empty:
            # Create a copy for display with formatted dates
            display_data = filtered_data.copy()
            display_data['date'] = display_data['date'].apply(
                lambda x: x.date() if hasattr(x, 'date') else x
            )
            
            st.dataframe(
                display_data.sort_values('date', ascending=False),
                use_container_width=True
            )
            
            # Export option
            if st.button("Export Data as CSV"):
                csv = filtered_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="workout_history.csv",
                    mime="text/csv"
                )
        else:
            st.info("No workouts match your filters.")

# Progress Dashboard Page
elif page == "Progress Dashboard":
    st.markdown('<h2 class="subheader">Progress Dashboard</h2>', unsafe_allow_html=True)
    
    if st.session_state.workouts.empty:
        st.info("No workouts logged yet. Start logging to see your progress!")
    else:
        # Calculate metrics
        total_workouts = len(st.session_state.workouts)
        total_volume = (st.session_state.workouts['sets'] * st.session_state.workouts['reps'] * st.session_state.workouts['weight']).sum()
        favorite_exercise = st.session_state.workouts['exercise'].mode()[0] if not st.session_state.workouts.empty else "N/A"
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Workouts", total_workouts)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Volume (lbs)", f"{total_volume:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Favorite Exercise", favorite_exercise)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Weekly progress
        st.subheader("Weekly Progress")
        
        # Get data from the last 6 weeks
        end_date = datetime.date.today()
        start_date = end_date - timedelta(days=42)  # 6 weeks
        
        # Convert to Timestamps for comparison
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        
        weekly_data = st.session_state.workouts[
            (st.session_state.workouts['date'] >= start_ts) &
            (st.session_state.workouts['date'] <= end_ts)
        ].copy()
        
        if not weekly_data.empty:
            # Calculate week start date (Monday)
            weekly_data['week'] = weekly_data['date'].apply(
                lambda x: x - timedelta(days=x.weekday())
            )
            weekly_data['volume'] = weekly_data['sets'] * weekly_data['reps'] * weekly_data['weight']
            
            weekly_summary = weekly_data.groupby(['week', 'exercise']).agg({
                'volume': 'sum',
                'weight': 'max',
                'sets': 'count'
            }).reset_index()
            
            # Create weekly summary for all exercises combined
            weekly_totals = weekly_data.groupby('week').agg({
                'volume': 'sum',
                'sets': 'count'
            }).reset_index()
            weekly_totals['week_label'] = weekly_totals['week'].apply(
                lambda x: x.strftime('%Y-%m-%d')
            )
            
            # Weekly Volume Graph
            st.markdown("#### Weekly Training Volume")
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            if len(weekly_totals) > 1:
                # Create a bar chart for weekly volume
                chart_data = weekly_totals.set_index('week_label')[['volume']]
                st.bar_chart(chart_data, use_container_width=True)
            else:
                st.info("Need at least 2 weeks of data to show volume trends")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Weekly Workouts Graph
            st.markdown("#### Weekly Workouts Count")
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            if len(weekly_totals) > 1:
                # Create a line chart for workout frequency
                workout_data = weekly_totals.set_index('week_label')[['sets']]
                workout_data.columns = ['Workouts']
                st.line_chart(workout_data, use_container_width=True)
            else:
                st.info("Need at least 2 weeks of data to show workout frequency trends")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Exercise-specific progress
            selected_exercise = st.selectbox(
                "Select Exercise for Detailed Progress",
                options=st.session_state.exercises
            )
            
            if selected_exercise:
                exercise_data = weekly_summary[weekly_summary['exercise'] == selected_exercise].copy()
                if not exercise_data.empty:
                    exercise_data['week_label'] = exercise_data['week'].apply(
                        lambda x: x.strftime('%Y-%m-%d')
                    )
                    
                    st.markdown(f"#### {selected_exercise} Progress")
                    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
                    
                    # Create two columns for weight and volume
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Max Weight Progress**")
                        if len(exercise_data) > 1:
                            weight_data = exercise_data.set_index('week_label')[['weight']]
                            st.line_chart(weight_data, use_container_width=True)
                        else:
                            st.info("Need more data for weight trends")
                    
                    with col2:
                        st.write("**Volume Progress**")
                        if len(exercise_data) > 1:
                            volume_data = exercise_data.set_index('week_label')[['volume']]
                            st.area_chart(volume_data, use_container_width=True)
                        else:
                            st.info("Need more data for volume trends")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Display weekly summary as a table
            st.markdown("#### Weekly Summary Table")
            display_summary = weekly_summary.copy()
            display_summary['week'] = display_summary['week'].apply(
                lambda x: x.date() if hasattr(x, 'date') else x
            )
            st.dataframe(
                display_summary.sort_values('week', ascending=False),
                use_container_width=True
            )
            
            # Show progress using metrics
            st.markdown("#### Progress This Week")
            this_week_start = end_date - timedelta(days=end_date.weekday())
            this_week_ts = pd.Timestamp(this_week_start)
            this_week_data = weekly_data[weekly_data['date'] >= this_week_ts]
            
            if not this_week_data.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Workouts This Week", len(this_week_data))
                with col2:
                    week_volume = (this_week_data['sets'] * this_week_data['reps'] * this_week_data['weight']).sum()
                    st.metric("Volume This Week", f"{week_volume:,} lbs")
                with col3:
                    max_weight = this_week_data['weight'].max()
                    st.metric("Max Weight This Week", f"{max_weight} lbs")
            
            # Recent workouts
            st.subheader("Recent Workouts")
            for _, row in weekly_data.sort_values('date', ascending=False).head(5).iterrows():
                display_date = row['date'].date() if hasattr(row['date'], 'date') else row['date']
                st.markdown(f"""
                <div class="exercise-card">
                    <strong>{row['exercise']}</strong> on {display_date}<br>
                    {row['sets']} sets × {row['reps']} reps × {row['weight']} lbs
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No workout data available for the last 6 weeks.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6c757d;'>Gum Workout Logger • Stay Strong 💪</div>", 
    unsafe_allow_html=True
)