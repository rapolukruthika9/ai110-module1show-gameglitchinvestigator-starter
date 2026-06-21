# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
  "Glitchy Guesser" is a Streamlit number-guessing game. The app picks a
  random secret number within a difficulty-based range (Easy 1–20, Normal
  1–100, Hard 1–50), and the player has a limited number of attempts to
  guess it, getting "Too High" / "Too Low" hints after each try. A score is
  tallied based on how quickly the player wins. It was deliberately shipped
  with several bugs for investigation and debugging practice.

- [ ] Detail which bugs you found.
  Hints could be both wrong-worded *and* wrong-outcome: the secret was
    cast to a string on every other attempt, causing a lexicographic
    instead of numeric comparison (e.g. "99" > "100" evaluates True as
    strings), and the hint text was paired with the opposite direction
    of the actual outcome.
  - The attempts counter started at 1 instead of 0, making "Attempts left"
    off by one from the very first guess.
  - "New Game" didn't reset game status, so after a win/loss it looped
    straight back to the "Game Over" screen instead of restarting.
  - Guessing too high sometimes *increased* the score instead of
    decreasing it (a parity-based logic error).
  - The win-score formula had an off-by-one, capping a perfect first
    guess at 80 points instead of 100.
  - The instructions always said "Guess a number between 1 and 100,"
    even on Easy/Hard where the actual range was different.
  - Switching difficulty mid-game didn't regenerate the secret or range,
    so the displayed range and the hidden number could mismatch.

- [ ] Explain what fixes you applied.\
  Removed the per-attempt string conversion of the secret and the
    `except TypeError` fallback in `check_guess` — guess and secret are
    now always compared as plain integers, and hint text now correctly
    matches its outcome ("Too High" → "Go Lower," "Too Low" → "Go Higher").
  - `attempts` now starts at 0 and increments only on valid guesses, so
    "Attempts left" is accurate from the start.
  - "New Game" now resets `status`, `score`, `history`, and the secret,
    and bumps a `game_id` so the guess input also clears.
  - `update_score` always subtracts 5 for "Too High," matching "Too Low."
  - Win scoring changed to `100 - 10 * (attempt_number - 1)` so a
    first-guess win correctly scores 100.
  - The info message now shows the real difficulty range instead of a
    hardcoded 1–100.
  - Added difficulty-change detection that regenerates the secret and
    resets the round when the player switches difficulty mid-game.
  - `parse_guess` now rejects out-of-range input, and invalid guesses no
    longer consume an attempt.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

Assumes Normal difficulty (range 1–100, 8 attempts) and a secret value of 65
(visible via the Developer Debug Info panel — yours will differ per session,
but the behavior pattern below holds for any secret).

1. Game starts. Range: 1–100, Attempts left: 8, Score: 0.
2. User enters a guess of 40 → "Too Low, Go HIGHER!" shown.
   Score updates: 0 − 5 = −5. Attempts left: 7.
3. User enters a guess of 70 → "Too High, Go LOWER!" shown.
   Score updates: −5 − 5 = −10. Attempts left: 6.
4. User enters a guess of 65 (the secret) → "Correct!"
   Score updates: −10 + 80 = 70 (win bonus is 100 − 10 × (attempt_number − 1),
   and this was the 3rd valid guess, so 100 − 20 = 80).
5. Game ends: "You won! The secret was 65. Final score: 70."
   Clicking "New Game 🔁" resets attempts to 8, score to 0, and generates a
   fresh secret in the same range.

