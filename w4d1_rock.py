import streamlit as st
import random
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="✊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .score-board {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .choice-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border: none;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        font-size: 3rem;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .choice-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .result-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .winner-animation {
        animation: pulse 0.5s ease-in-out;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .reset-btn {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        margin-top: 1rem;
    }
    .current-result {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .win {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .lose {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .tie {
        background-color: #e2e3e5;
        color: #383d41;
        border: 2px solid #d6d8db;
    }
    .welcome-message {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        border-left: 5px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0
if 'round' not in st.session_state:
    st.session_state.round = 0  # Changed from 1 to 0 - we start at round 0 (no rounds played)
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""
if 'user_choice' not in st.session_state:
    st.session_state.user_choice = None
if 'computer_choice' not in st.session_state:
    st.session_state.computer_choice = None
if 'current_round_result' not in st.session_state:
    st.session_state.current_round_result = ""
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "user"
    else:
        return "computer"

def get_emoji(choice):
    emoji_map = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
    return emoji_map.get(choice, "")

def play_round(choice):
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    
    st.session_state.user_choice = choice
    st.session_state.computer_choice = computer_choice
    st.session_state.game_started = True
    
    winner = determine_winner(choice, computer_choice)
    
    # Increment round when a round is actually played
    st.session_state.round += 1
    
    if winner == "user":
        st.session_state.user_score += 1
        st.session_state.last_result = "win"
        st.session_state.current_round_result = "win"
    elif winner == "computer":
        st.session_state.computer_score += 1
        st.session_state.last_result = "lose"
        st.session_state.current_round_result = "lose"
    else:
        st.session_state.last_result = "tie"
        st.session_state.current_round_result = "tie"

def reset_game():
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.round = 0
    st.session_state.last_result = ""
    st.session_state.user_choice = None
    st.session_state.computer_choice = None
    st.session_state.current_round_result = ""
    st.session_state.game_started = False

# Main app layout
st.markdown('<div class="main-header">🎮 Rock Paper Scissors</div>', unsafe_allow_html=True)

# Score board
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="score-board">
        <h3>👤 You</h3>
        <h1>{st.session_state.user_score}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Show "Ready!" when no rounds played, otherwise show current round
    round_display = "Ready!" if st.session_state.round == 0 else f"Round {st.session_state.round}"
    st.markdown(f"""
    <div class="score-board">
        <h3>Game Status</h3>
        <h2>{round_display}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="score-board">
        <h3>🤖 Computer</h3>
        <h1>{st.session_state.computer_score}</h1>
    </div>
    """, unsafe_allow_html=True)

# Welcome message or current round result
if not st.session_state.game_started:
    st.markdown("""
    <div class="welcome-message">
        <h3>🎯 Welcome to Rock Paper Scissors!</h3>
        <p>Choose your weapon below to start the game!</p>
    </div>
    """, unsafe_allow_html=True)
elif st.session_state.current_round_result:
    if st.session_state.current_round_result == "win":
        st.markdown(f'<div class="current-result win">🎉 Round {st.session_state.round}: You won!</div>', unsafe_allow_html=True)
    elif st.session_state.current_round_result == "lose":
        st.markdown(f'<div class="current-result lose">💻 Round {st.session_state.round}: Computer won!</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="current-result tie">🤝 Round {st.session_state.round}: It\'s a tie!</div>', unsafe_allow_html=True)

# Game choices
st.markdown("### Choose your weapon!")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✊\nRock", key="rock", use_container_width=True, 
                 help="Rock crushes scissors"):
        play_round("rock")
        st.rerun()

with col2:
    if st.button("✋\nPaper", key="paper", use_container_width=True,
                 help="Paper covers rock"):
        play_round("paper")
        st.rerun()

with col3:
    if st.button("✌️\nScissors", key="scissors", use_container_width=True,
                 help="Scissors cut paper"):
        play_round("scissors")
        st.rerun()

# Detailed results display
if st.session_state.user_choice is not None:
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    
    # Display choices
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(f"### Your Choice\n# {get_emoji(st.session_state.user_choice)}")
    
    with col2:
        st.markdown("# 🆚")
    
    with col3:
        st.markdown(f"### Computer's Choice\n# {get_emoji(st.session_state.computer_choice)}")
    
    # Display detailed result
    if st.session_state.last_result == "win":
        st.success(f"## 🎉 You Win Round {st.session_state.round}! {get_emoji(st.session_state.user_choice)} beats {get_emoji(st.session_state.computer_choice)}")
    elif st.session_state.last_result == "lose":
        st.error(f"## 💻 Computer Wins Round {st.session_state.round}! {get_emoji(st.session_state.computer_choice)} beats {get_emoji(st.session_state.user_choice)}")
    else:
        st.info(f"## 🤝 Round {st.session_state.round} is a Tie!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Game instructions and reset
with st.expander("📖 How to Play"):
    st.markdown("""
    **Rules:**
    - ✊ Rock crushes ✌️ Scissors
    - ✋ Paper covers ✊ Rock  
    - ✌️ Scissors cut ✋ Paper
    
    First to score 5 points wins the game!
    """)

# Game over conditions
if st.session_state.user_score >= 5:
    st.balloons()
    st.success("## 🏆 Congratulations! You won the game!")
    if st.button("🔄 Play Again", key="play_again_win", use_container_width=True):
        reset_game()
        st.rerun()

elif st.session_state.computer_score >= 5:
    st.error("## 💻 Game Over! Computer won the game!")
    if st.button("🔄 Play Again", key="play_again_lose", use_container_width=True):
        reset_game()
        st.rerun()

# Reset button
if st.button("🔄 Reset Game", key="reset_game", use_container_width=True):
    reset_game()
    st.rerun()

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ using Streamlit*")