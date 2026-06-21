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
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
