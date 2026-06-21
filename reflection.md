# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
A number-guessing game with a difficulty selector in the    sidebar, a text box to enter a guess, and a "Developer Debug Info" panel that, when opened, shows the secret number right there on the screen.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  1. The debug panel reveals the secret answer before you even guess.
  2. The hints are backwards on every other guess (e.g., guessing 9 when the answer is 10 says "too high").
  3. The attempts left counter is off by one from the very first guess.
  4. Clicking "New Game" after winning or losing doesn't actually restart the game. It just loops back to the "game over" screen.
  5. The instructions always say "guess between 1 and 100," even on Easy or Hard difficulty where the range is different.
  6. There is no range limit. Even if i enter -9 it says go lower and doesn't show an error for wrong input. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input              | Expected Behavior         | Actual Behavior                  | Console Output / Error |
|--------------------|---------------------------|----------------------------------|------------------------|
| 10                 | secret = 8 so, "GO LOWER!"|"GO HIGHER!"                      | None                   |
| New Game           | Game resets to a new one  |"Game over / You already won"     | None                   |
| page load (Normal) | Attempts left: 8          | Attempts left: 7"(No guess made) | None                   |
| -9                 | Error message wrong input | "Go LOWER!"                      | None
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
While troubleshooting an issue where game hints were displaying in reverse, Claude correctly identified that the logic in the check_guess function was inverted and suggested swapping the hint logic to resolve the bug.

I applied the suggested changes to the check_guess function, ran the application locally, and manually tested several inputs to confirm that the hints were now accurate and intuitive.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I asked AI to fix the score formula and then add a comment it directly added a fixed comment stating the score for guessing the first time is 100 and then for every guess 10 is subtracted from the score. 

When I ran `app.py` i realised that the code was not fixed instead only a comment was added. 


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I ran a manual test to verify the behavior of the game's hint delivery system using specific boundary inputs.   The bug has been solved as it no longer showed flipped hints. 

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
This test revealed that hints were completely inverted (e.g., giving a "higher" hint when the guess was already too high). After that was fixed, the hints were helpful to get closer to the secret number. 

- Did AI help you design or understand any tests? How?
The AI helped me to track the bug down. It pointed the lines where the error existed and it suggesting a fix by Fixing the swapped hint messages in both the normal and except paths. 


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit re-runs the whole script every time you click something, like
a button or a checkbox. So normal variables don't remember anything —
they reset each time. `session_state` is the only thing that remembers
values between clicks, like the secret number, score, and attempts. I
saw this in the "New Game" bug — it forgot to reset one value, so the
game got stuck. In short: Streamlit forgets everything except what you
put in session_state.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
Test the bug with real examples before trusting a
fix. The first "fix" for the hints only changed the text, not the real
problem. I only caught it because I checked it against actual examples.

- What is one thing you would do differently next time you work with AI on a coding task?
Write the test cases first, before asking for the fix. That would catch a half-fixed bug faster.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
Code that looks fixed isn't
always actually fixed. Now I check examples myself instead of trusting
the comments saying "FIXED."  