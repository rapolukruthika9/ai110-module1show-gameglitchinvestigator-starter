import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    if raw is None:
        return False, None, "Enter a guess."

    if raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: previously any integer was accepted, so a wrong/out-of-range input
    # (e.g. 999 in Easy's 1-20) produced no error. Now reject out-of-range.
    if value < low or value > high:
        return False, None, f"Out of range. Enter a number between {low} and {high}."

    return True, value, None

def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            # FIX: hint was flipped (said "Go HIGHER!" when guess was too high)
            return "Too High", "📉 Go LOWER!"
        else:
            # FIX: hint was flipped (said "Go LOWER!" when guess was too low)
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            # FIX: hint was flipped (said "Go HIGHER!" when guess was too high)
            return "Too High", "📉 Go LOWER!"
        # FIX: hint was flipped (said "Go LOWER!" when guess was too low)
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

#FIXME: Adds 5 points instead of subtracting 5 points for "Too High" on even attempts  
    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

#FIX: Switching difficulty mid-game didn't change the secret (it was generated
# only once and never updated). Now the secret regenerates with the new range
# and starts a fresh round whenever the difficulty changes.
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

#FIX: Initialize attempts to 0 (was 1) so it matches the New Game reset and "Attempts left" is no longer off by one
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Bumped on each New Game so the guess input gets a fresh (empty) key.
if "game_id" not in st.session_state:
    st.session_state.game_id = 0

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "   # FIX: range now follows the selected difficulty instead of being hardcoded to 1-100
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIX: include game_id in the key so each New Game makes a brand-new, empty
# input. Streamlit ties a widget's value to its key, so reusing the same key
# would restore the previous game's typed guess (and the value can't be
# cleared from the New Game handler after the widget is already instantiated).
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.game_id}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game now fully resets game state (status/score/history), not just
# attempts + secret. Previously status stayed "won"/"lost", so the st.stop()
# below halted the game immediately and it never actually restarted.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    # FIX: bump game_id so the guess input gets a new key and renders empty,
    # instead of keeping the previous game's typed value.
    st.session_state.game_id += 1
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: an invalid guess no longer consumes an attempt. Previously the
        # counter was bumped before validation, so bad input burned attempts
        # without ever hitting the limit check below.
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        # FIX: count the attempt only for a valid guess, then run the limit
        # check. The limit check lives in this branch, so incrementing here
        # keeps the counter and the game-over check in sync.
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            # FIX: limit now works for every difficulty — attempts only counts
            # valid guesses (see above) and starts at 0, so this fires exactly
            # when attempt_limit valid guesses have been used.
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
