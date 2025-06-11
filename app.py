import streamlit as st
import random
from streamlit.components.v1 import html

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Game logic
def determine_winner(player_choice, opponent_choice):
    if player_choice == opponent_choice:
        return "It's a tie!"
    elif (player_choice == "Rock" and opponent_choice == "Scissors") or \
         (player_choice == "Paper" and opponent_choice == "Rock") or \
         (player_choice == "Scissors" and opponent_choice == "Paper"):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!" if st.session_state.game_mode == "Multiplayer" else "Computer wins!"

# Initialize session state
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'opponent_score' not in st.session_state:
    st.session_state.opponent_score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'max_streak' not in st.session_state:
    st.session_state.max_streak = 0
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "AI"
if 'last_winner' not in st.session_state:
    st.session_state.last_winner = None
if 'player1_choice' not in st.session_state:
    st.session_state.player1_choice = None
if 'player2_choice' not in st.session_state:
    st.session_state.player2_choice = None
if 'show_player2' not in st.session_state:
    st.session_state.show_player2 = False
if 'hide_player1' not in st.session_state:
    st.session_state.hide_player1 = False

# App layout
st.title("🎯 Rock-Paper-Scissors")
st.markdown("---")

# Game mode selection
game_mode = st.radio("Select game mode:", ["AI", "Multiplayer"], horizontal=True, key="game_mode_selector")
st.session_state.game_mode = game_mode

# Player choices
col1, col2 = st.columns(2)

with col1:
    st.subheader("Player 1")
    
    if not st.session_state.hide_player1:
        player1_choice = st.radio(
            "Your choice:", 
            ["Rock", "Paper", "Scissors"], 
            key="player1", 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if st.button("Submit Choice", key="submit_player1"):
            st.session_state.player1_choice = player1_choice
            st.session_state.show_player2 = True
            st.session_state.hide_player1 = True
            st.experimental_rerun()
    else:
        st.write("Choice submitted!")
        st.write("Waiting for Player 2..." if game_mode == "Multiplayer" else "Waiting for Computer...")

with col2:
    st.subheader("Player 2" if game_mode == "Multiplayer" else "Computer")
    
    if st.session_state.show_player2:
        if game_mode == "AI":
            opponent_choice = random.choice(["Rock", "Paper", "Scissors"])
            st.session_state.player2_choice = opponent_choice
            st.write(f"Computer chooses: *{opponent_choice}*")
        else:
            player2_choice = st.radio(
                "Your choice:", 
                ["Rock", "Paper", "Scissors"], 
                key="player2", 
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state.player2_choice = player2_choice
        
        if st.button("Reveal Result", key="reveal_result"):
            result = determine_winner(st.session_state.player1_choice, st.session_state.player2_choice)
            
            # Update scores and streaks
            if result == "Player 1 wins!":
                st.session_state.player_score += 1
                if st.session_state.last_winner == "player":
                    st.session_state.streak += 1
                else:
                    st.session_state.streak = 1
                st.session_state.last_winner = "player"
            elif result in ["Player 2 wins!", "Computer wins!"]:
                st.session_state.opponent_score += 1
                if st.session_state.last_winner == "opponent":
                    st.session_state.streak += 1
                else:
                    st.session_state.streak = 1
                st.session_state.last_winner = "opponent"
            else:  # Tie
                st.session_state.last_winner = None
            
            # Update max streak
            if st.session_state.streak > st.session_state.max_streak:
                st.session_state.max_streak = st.session_state.streak
            
            # Display result with animation
            html(f"""
            <div class="result-animation">
                <h2>{result}</h2>
                <p>Player 1 chose: {st.session_state.player1_choice}</p>
                <p>{'Player 2' if game_mode == 'Multiplayer' else 'Computer'} chose: {st.session_state.player2_choice}</p>
            </div>
            """)
            
            # Reset for next round
            st.session_state.show_player2 = False
            st.session_state.hide_player1 = False
            st.session_state.player1_choice = None
            st.session_state.player2_choice = None
            st.experimental_rerun()
    else:
        st.write("Waiting for Player 1..." if not st.session_state.hide_player1 else "Make your choice!")

# Score display
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Player 1 Score", st.session_state.player_score)

with col2:
    st.metric("Player 2 Score" if game_mode == "Multiplayer" else "Computer Score", 
              st.session_state.opponent_score)

with col3:
    st.metric("Max Win Streak", st.session_state.max_streak)

# Reset button
if st.button("Reset Game", type="secondary"):
    st.session_state.player_score = 0
    st.session_state.opponent_score = 0
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    st.session_state.last_winner = None
    st.session_state.player1_choice = None
    st.session_state.player2_choice = None
    st.session_state.show_player2 = False
    st.session_state.hide_player1 = False
    st.experimental_rerun()

# Rules expander
with st.expander("Game Rules"):
    st.write("""
    - Rock crushes Scissors
    - Scissors cut Paper
    - Paper covers Rock
    
    If both players choose the same item, it's a tie!
    
    *How to play:*
    1. Player 1 selects their choice and clicks "Submit Choice" (choice will be hidden)
    2. Player 2 (or Computer) then makes their selection
    3. Click "Reveal Result" to see who won and what choices were made
    """)