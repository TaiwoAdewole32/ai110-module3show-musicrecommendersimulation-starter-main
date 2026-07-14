# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

I asked the Claude Code to expand songs.csv by adding popularity, release year, detailed mood tags, listening activity, and song structure for each song. I also asked it to update recommender.py so these new attributes contribute weighted points to each song’s recommendation score.

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

Act as an AI Engineer, In song.csv add these attributes: to given set of songs: song popularity from 0 - 100, release year, detailed mood tags (e.g., "nostalgic," "aggressive," "euphoric"),  listening activity which is the situation the song fits best, such as studying, exercising, driving, relaxing, partying, or sleeping, and song structure which is the arrangement of the song, such as verse-chorus, storytelling, freestyle, instrumental build, or progressive.

Update the scoring logic in recommender.py so scoring accounts for the new attributes which are popularity, mood_tags, listening_activity, song_structure, and release year. Popularity should add +0.5 points, mood_tags +1 point, listening_activity +0.5 points, song structure +1 points, release year +0.5.

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

The agent edited songs.csv, recommender.py, main.py, README.md, and model_card.md. It added the five new song attributes, created scoring logic for popularity, release year, mood tags, listening activity, and song structure, and added a test profile that used all five preferences.

The agent ran commands to list the repository files, search for existing attributes, read the code and documentation, load the updated CSV, run pytest, and execute the recommendation program. The final test command reported that all 2 tests passed, and the program output confirmed that the new scoring rules produced recommendation scores and explanations correctly.

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I manually reviewed the new song attributes to make sure the values matched did not severely alter the main attributes. I also checked the scoring weights and recommendation explanations, then verified the system by running the tests and reviewing the CLI output.


---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
