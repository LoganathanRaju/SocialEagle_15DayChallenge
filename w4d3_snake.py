import streamlit as st
import random
import time
from enum import Enum

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class SnakeGame:
    def __init__(self, width=15, height=15):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = [(self.height // 2, self.width // 2)]  # Start in center
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
    
    def generate_food(self):
        """Generate food at random position not occupied by snake"""
        while True:
            food = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
            if food not in self.snake:
                return food
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent reverse direction)"""
        if self.game_over:
            return
        
        # Prevent moving in opposite direction
        current_dir = self.direction.value
        new_dir = new_direction.value
        if (current_dir[0] + new_dir[0], current_dir[1] + new_dir[1]) != (0, 0):
            self.direction = new_direction
    
    def move(self):
        """Move the snake one step"""
        if self.game_over:
            return
        
        head = self.snake[0]
        new_head = (
            head[0] + self.direction.value[0],
            head[1] + self.direction.value[1]
        )
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.height or 
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def get_board_display(self):
        """Generate the visual representation of the game board"""
        board = [["⬜" for _ in range(self.width)] for _ in range(self.height)]
        
        # Place food
        board[self.food[0]][self.food[1]] = "🍎"
        
        # Place snake
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                board[segment[0]][segment[1]] = "🐍"
            else:  # Body
                board[segment[0]][segment[1]] = "🟢"
        
        return board

def main():
    st.set_page_config(page_title="Snake Game", page_icon="🐍", layout="centered")
    
    st.title("🐍 Snake Game")
    st.markdown("Use the buttons below to control the snake!")
    
    # Initialize game in session state
    if 'game' not in st.session_state:
        st.session_state.game = SnakeGame()
        st.session_state.auto_play = False
    
    game = st.session_state.game
    
    # Auto-play toggle
    auto_play = st.checkbox("🎮 Auto Play", value=st.session_state.auto_play)
    st.session_state.auto_play = auto_play
    
    # Game speed control
    speed = st.slider("🚀 Game Speed", min_value=1, max_value=10, value=3, 
                     help="Higher values = faster game")
    
    # Display score and status
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 Score", game.score)
    with col2:
        status = "💀 Game Over!" if game.game_over else "🎮 Playing..."
        st.metric("🎯 Status", status)
    
    # Game board and controls layout
    game_col, control_col = st.columns([2, 1])
    
    with game_col:
        # Display game board
        board = game.get_board_display()
        board_html = "<div style='font-size: 20px; line-height: 1.2; font-family: monospace;'>"
        for row in board:
            board_html += "".join(row) + "<br>"
        board_html += "</div>"
        
        st.markdown(board_html, unsafe_allow_html=True)
    
    with control_col:
        st.markdown("### 🎮 Controls")
        
        # Direction controls in cross pattern
        st.markdown("<br>", unsafe_allow_html=True)
        
        # UP button (centered)
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button("⬆️\nUP", key="up_btn", help="Move Up"):
                game.change_direction(Direction.UP)
        
        # LEFT and RIGHT buttons
        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("⬅️\nLEFT", key="left_btn", help="Move Left"):
                game.change_direction(Direction.LEFT)
        with col_right:
            if st.button("➡️\nRIGHT", key="right_btn", help="Move Right"):
                game.change_direction(Direction.RIGHT)
        
        # DOWN button (centered)
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button("⬇️\nDOWN", key="down_btn", help="Move Down"):
                game.change_direction(Direction.DOWN)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Restart button
        if st.button("🔄 RESTART", key="restart_btn", type="primary"):
            st.session_state.game = SnakeGame()
            st.rerun()
    
    # Game instructions
    with st.expander("📖 How to Play"):
        st.markdown("""
        - **Objective**: Control the snake to eat food (🍎) and grow longer
        - **Controls**: Use the arrow buttons to change direction
        - **Scoring**: Each food eaten gives you 10 points
        - **Game Over**: Avoid hitting walls or the snake's own body
        - **Auto Play**: Enable for continuous movement
        - **Speed**: Adjust how fast the snake moves
        
        **Tips**:
        - Plan your moves ahead to avoid trapping yourself
        - Try to create open spaces as you grow longer
        - Use the restart button to start a new game anytime
        """)
    
    # Auto-play logic
    if auto_play and not game.game_over:
        game.move()
        time.sleep(1.0 / speed)  # Adjust speed based on slider
        st.rerun()
    
    # Manual move button (when auto-play is off)
    if not auto_play:
        st.markdown("---")
        if st.button("👈 Move One Step", disabled=game.game_over):
            game.move()
            st.rerun()
    
    # Game over handling
    if game.game_over:
        st.error("💀 Game Over! The snake hit a wall or itself.")
        
        # Celebration for good scores
        if game.score > 50:
            st.balloons()
        
        if st.button("🎮 Play Again", type="primary"):
            st.session_state.game = SnakeGame()
            st.rerun()

if __name__ == "__main__":
    main()