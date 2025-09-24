import streamlit as st
import random
import time

# Initialize session state variables
if 'board' not in st.session_state:
    st.session_state.board = [' '] * 9
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'two_player'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_line' not in st.session_state:
    st.session_state.winning_line = None
if 'computer_move_needed' not in st.session_state:
    st.session_state.computer_move_needed = False

def check_winner(board):
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
            st.session_state.winning_line = line
            return board[line[0]]
    if ' ' not in board:
        return 'Draw'
    return None

def make_move(position):
    if st.session_state.board[position] == ' ' and not st.session_state.game_over:
        st.session_state.board[position] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            if (st.session_state.game_mode == 'vs_computer' and 
                st.session_state.current_player == 'O' and 
                not st.session_state.game_over):
                st.session_state.computer_move_needed = True

def make_computer_move():
    empty_positions = [i for i, spot in enumerate(st.session_state.board) if spot == ' ']
    if empty_positions:
        time.sleep(0.5)
        position = random.choice(empty_positions)
        st.session_state.board[position] = 'O'
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        else:
            st.session_state.current_player = 'X'
    st.session_state.computer_move_needed = False

def reset_game():
    st.session_state.board = [' '] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = None
    st.session_state.computer_move_needed = False

# Custom CSS - Fixed hex color codes
css_styles = """
<style>
/* Main background */
.main { 
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
}
/* Title styling */
.title {
    text-align: center;
    color: #ff6b6b;
    font-size: 3rem;
    margin-bottom: 0.2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}
/* Subtitle styling */
.subtitle {
    text-align: center;
    color: #4ecdc4;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}
/* Game mode section */
.game-mode {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    backdrop-filter: blur(5px);
}
/* Board styling */
.board {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
}
/* Square buttons */
.stButton > button {
    width: 100px !important;
    height: 100px !important;
    border-radius: 15px !important;
    font-size: 2.5rem !important;
    font-weight: bold !important;
    margin: 5px !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    transition: all 0.3s ease !important;
    border: none !important;
    color: #6c757d !important; /* default gray when empty */
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
}
/* X: green, O: magenta - bold and visible */
.stButton > button {
    font-weight: bold !important;
    font-size: 2.8rem !important;
}
/* Status section */
.status {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    padding: 1rem;
    border-radius: 1rem;
    background-color: rgba(255, 255, 255, 0.8);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    backdrop-filter: blur(5px);
}
/* Reset button style - Yellow rectangle */
.stButton > button[kind="primary"] {
    width: 200px !important;
    height: 50px !important;
    background-color: #FFD600 !important;
    color: #222 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    text-align: center !important;
    border: 2px solid #FFD600 !important;
    margin: 0 auto !important;
    display: block !important;
}
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title">Tic-Tac-Toe ❌⭕</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">The Classic Game!</p>', unsafe_allow_html=True)

# Game mode selection
st.markdown('### Game Mode')
mode = st.radio(
    "Select game mode:",
    ["Two Players", "Player vs Computer"],
    horizontal=True,
    key="mode_selector"
)
if mode == "Two Players":
    st.session_state.game_mode = 'two_player'
else:
    st.session_state.game_mode = 'vs_computer'

# Let computer move if needed
if (st.session_state.computer_move_needed and not st.session_state.game_over):
    make_computer_move()
    st.rerun()

# Game board display
st.markdown('<div class="board">', unsafe_allow_html=True)
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        position = i * 3 + j
        with cols[j]:
            button_text = st.session_state.board[position]
            button_key = f'cell_{position}'

            # Create button with color styling based on content
            button_clicked = st.button(
                button_text,
                key=button_key,
                disabled=st.session_state.game_over or st.session_state.board[position] != ' '
            )
            
            # Add inline CSS for X (green) and O (magenta) colors
            if button_text == 'X':
                st.markdown(
                    f"""
                    <style>
                    div[data-testid="stButton"]:has(button[aria-label="cell_{position}"]) button {{
                        color: #28a745 !important;
                        font-weight: bold !important;
                        font-size: 3rem !important;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
                    }}
                    </style>
                    """, 
                    unsafe_allow_html=True
                )
            elif button_text == 'O':
                st.markdown(
                    f"""
                    <style>
                    div[data-testid="stButton"]:has(button[aria-label="cell_{position}"]) button {{
                        color: #d500f9 !important;
                        font-weight: bold !important;
                        font-size: 3rem !important;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
                    }}
                    </style>
                    """, 
                    unsafe_allow_html=True
                )
            
            if button_clicked:
                make_move(position)
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Game status
st.markdown('<div class="status">', unsafe_allow_html=True)
if st.session_state.winner == 'Draw':
    st.info("It's a draw! 🤝")
elif st.session_state.winner:
    if st.session_state.winner == 'X':
        st.success("Player X wins! 🎉")
        st.balloons()
    else:
        if st.session_state.game_mode == 'two_player':
            st.success("Player O wins! 🎉")
            st.balloons()
        else:
            st.error("Computer wins! 🤖")
else:
    if st.session_state.game_mode == 'two_player':
        st.write(f"Player {st.session_state.current_player}'s turn")
    else:
        if st.session_state.current_player == 'X':
            st.write("Your turn (X)")
        else:
            st.write("Computer's turn (O)")
st.markdown('</div>', unsafe_allow_html=True)

# Reset Game button - Yellow rectangle, single line
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button('Reset Game 🔄', type="primary", use_container_width=True):
        reset_game()
        st.rerun()

# Instructions
with st.expander("How to Play"):
    st.markdown("""
    **Tic-Tac-Toe Rules:**
    1. The game is played on a 3x3 grid.
    2. Players take turns placing their marker (X or O) in an empty cell.
    3. The first player to get 3 of their markers in a row (horizontally, vertically, or diagonally) wins.
    4. If all cells are filled and no player has 3 in a row, the game is a draw.
    
    **Game Modes:**
    - **Two Players**: Play with a friend on the same device
    - **Player vs Computer**: Test your skills against our AI opponent
    """)