# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world music recommenders typically work in three stages: they build numeric representations of users and items (features or learned embeddings), use a fast candidate generation step to narrow a massive catalog down to a manageable shortlist, and then apply a more precise ranking model to order that shortlist for the user. This simulation prioritizes the representation and ranking stages and skips candidate generation entirely, since our catalog is only 20 songs - every song can be scored directly with no need to pre-filter. `Song` and `UserProfile` fields stand in for the "representation" stage: hand-picked features instead of learned embeddings. The weighted scoring formula (the "Algorithm Recipe") stands in for a real ranking model, using explicit feature-match weights instead of a trained ranker.
- `Song` fields used in scoring: `genre`, `mood`, `energy`, `acousticness` (optionally `valence` as a tie-breaker). Stored-but-unused-in-scoring: `id`, `title`, `artist`, `tempo_bpm`, `danceability` (excluded per the earlier feature analysis - collinear with energy, free text, or bias risk).
- `UserProfile` fields used in scoring: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic` - each maps 1:1 to one of the `Song` fields above.

### The Algorithm Recipe (finalized weights)

`score_song` (in `src/recommender.py`) scores every song on a 10-point tiered-additive scale:

| Feature | Max pts | Scoring shape |
|---|---|---|
| Genre | 1.5 | binary - exact match or 0 |
| Mood | 3 | binary - exact match or 0 |
| Energy | 3.5 | gradient - `3.5 * (1 - abs(target_energy - song.energy))` |
| Acousticness | 1.5 | gradient, direction-aware on `likes_acoustic` |
| Valence | 0.5 | gradient tie-breaker |

Genre and mood are categorical, so they're scored binary - a song either is or isn't the right genre/mood. Energy and acousticness are continuous 0-1 floats, so they're scored on a gradient instead, giving partial credit for "close enough" matches rather than an all-or-nothing cutoff. Valence isn't an explicit `UserProfile` preference, so it only contributes a small tie-breaking amount.
### Potential Biases

- Genre + mood together are worth 4.5 of the 10 points (45%) and are all-or-nothing, while energy and acousticness (5 pts combined) are gradient-scored. Genre was deliberately de-weighted and energy up-weighted relative to an earlier version of this scale, so "feel" (energy fit) can now outweigh an exact genre match: a song with a much closer energy fit can out-rank a same-genre song that's further from the target energy. Mood is still binary and still worth as much as energy at its max, so a mood mismatch remains costly.
- Genre and mood labels in the catalog are coarse and somewhat subjective (e.g. the `afrobeats` / `pop` / `dance pop` boundaries), so a binary match/no-match cutoff can penalize genuinely well-fitting songs over a labeling technicality rather than an actual taste mismatch.
- With only 20 songs and uneven genre representation in `data/songs.csv`, users whose favorite genre has few catalog entries get a much smaller pool of "full-credit" matches than users who like well-represented genres like pop.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

Top recommendations:

Sunrise City - Score: 9.69
Because: genre matches (pop); mood matches (happy); energy close to target (0.82 vs 0.80); energetic production (0.82 non-acoustic)

Unavailable - Score: 6.82
Because: mood matches (happy); energy close to target (0.80 vs 0.80); energetic production (0.88 non-acoustic)

Beauty and a Beat - Score: 6.76
Because: mood matches (happy); energy close to target (0.88 vs 0.80); energetic production (0.95 non-acoustic)

MMS - Score: 6.75
Because: mood matches (happy); energy close to target (0.85 vs 0.80); energetic production (0.90 non-acoustic)

Gym Hero - Score: 6.67
Because: genre matches (pop); energy close to target (0.93 vs 0.80); energetic production (0.95 non-acoustic)

## Sample Output with Diverse Profiles
Profile: Baseline (sanity check)
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 9.69
Because: genre match (pop, +3.0); mood match (happy, +3.0); energy close to target (0.82 vs 0.80, +2.0); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5)

Gym Hero - Score: 6.67
Because: genre match (pop, +3.0); energy close to target (0.93 vs 0.80, +1.7); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.77, +0.5)

MMS - Score: 6.65
Because: mood match (happy, +3.0); energy close to target (0.70 vs 0.80, +1.8); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.5)

Beauty and a Beat - Score: 6.62
Because: mood match (happy, +3.0); energy close to target (0.95 vs 0.80, +1.7); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.82, +0.5)

Headlines - Score: 6.62
Because: mood match (happy, +3.0); energy close to target (0.70 vs 0.80, +1.8); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.42, +0.5)

Profile: Conflicting energy vs. mood (high-energy but wants sad)
Prefs:   {'genre': 'pop', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}

Top recommendations:

Gym Hero - Score: 6.86
Because: genre match (pop, +3.0); energy close to target (0.93 vs 0.90, +1.9); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.77, +0.5)

Sunrise City - Score: 6.57
Because: genre match (pop, +3.0); energy close to target (0.82 vs 0.90, +1.8); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5)

Yukon - Score: 5.78
Because: genre match (pop, +3.0); energy close to target (0.55 vs 0.90, +1.3); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.65, +0.5)

Hope - Score: 5.29
Because: mood match (sad, +3.0); energy close to target (0.46 vs 0.90, +1.1); energetic production (0.45 non-acoustic, +0.7); valence close to target (0.20, +0.5)

Storm Runner - Score: 3.83
Because: energy close to target (0.91 vs 0.90, +2.0); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.48, +0.5)

Profile: Conflicting acoustic preference vs. energy (wants both loud AND acoustic)
Prefs:   {'genre': 'rock', 'mood': 'intense', 'energy': 1.0, 'likes_acoustic': True}

Top recommendations:

Storm Runner - Score: 8.47
Because: genre match (rock, +3.0); mood match (intense, +3.0); energy close to target (0.91 vs 1.00, +1.8); acoustic-leaning (0.10 acousticness, +0.2); valence close to target (0.48, +0.5)

Gym Hero - Score: 5.44
Because: mood match (intense, +3.0); energy close to target (0.93 vs 1.00, +1.9); acoustic-leaning (0.05 acousticness, +0.1); valence close to target (0.77, +0.5)

Coffee Shop Stories - Score: 2.58
Because: energy close to target (0.37 vs 1.00, +0.7); acoustic-leaning (0.89 acousticness, +1.3); valence close to target (0.71, +0.5)

Rooftop Lights - Score: 2.54
Because: energy close to target (0.76 vs 1.00, +1.5); acoustic-leaning (0.35 acousticness, +0.5); valence close to target (0.81, +0.5)

Library Rain - Score: 2.49
Because: energy close to target (0.35 vs 1.00, +0.7); acoustic-leaning (0.86 acousticness, +1.3); valence close to target (0.60, +0.5)

Profile: Out-of-range energy (> 1.0) -- does the gap math stay sane?
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 1.8, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 7.77
Because: genre match (pop, +3.0); mood match (happy, +3.0); energy close to target (0.82 vs 1.80, +0.0); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5)

Beauty and a Beat - Score: 5.22
Because: mood match (happy, +3.0); energy close to target (0.95 vs 1.80, +0.3); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.82, +0.5)

Gym Hero - Score: 5.18
Because: genre match (pop, +3.0); energy close to target (0.93 vs 1.80, +0.3); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.77, +0.5)

MMS - Score: 4.85
Because: mood match (happy, +3.0); energy close to target (0.70 vs 1.80, +0.0); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.5)

Headlines - Score: 4.82
Because: mood match (happy, +3.0); energy close to target (0.70 vs 1.80, +0.0); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.42, +0.5)

Profile: Out-of-range energy (negative) -- can this produce a negative or >2 pt swing?
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': -0.5, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 7.73
Because: genre match (pop, +3.0); mood match (happy, +3.0); energy close to target (0.82 vs -0.50, +0.0); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5)

Gym Hero - Score: 4.92
Because: genre match (pop, +3.0); energy close to target (0.93 vs -0.50, +0.0); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.77, +0.5)

Beauty and a Beat - Score: 4.92
Because: mood match (happy, +3.0); energy close to target (0.95 vs -0.50, +0.0); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.82, +0.5)

MMS - Score: 4.85
Because: mood match (happy, +3.0); energy close to target (0.70 vs -0.50, +0.0); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.5)

Headlines - Score: 4.82
Because: mood match (happy, +3.0); energy close to target (0.70 vs -0.50, +0.0); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.42, +0.5)

Profile: No genre/mood in catalog at all -- forces score to rely only on continuous fields
Prefs:   {'genre': 'opera', 'mood': 'furious', 'energy': 0.5, 'likes_acoustic': False}

Top recommendations:

Trust Issues - Score: 3.60
Because: energy close to target (0.45 vs 0.50, +1.9); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.28, +0.5)

MMS - Score: 3.45
Because: energy close to target (0.70 vs 0.50, +1.6); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.5)

Headlines - Score: 3.42
Because: energy close to target (0.70 vs 0.50, +1.6); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.42, +0.5)

Starboy - Score: 3.40
Because: energy close to target (0.74 vs 0.50, +1.5); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.55, +0.5)

Yukon - Score: 3.38
Because: energy close to target (0.55 vs 0.50, +1.9); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.65, +0.5)

Profile: Case/whitespace mismatch on an otherwise valid genre (exact-match brittleness)
Prefs:   {'genre': 'Pop', 'mood': ' happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

Unavailable - Score: 3.82
Because: energy close to target (0.80 vs 0.80, +2.0); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.65, +0.5)

Starboy - Score: 3.76
Because: energy close to target (0.74 vs 0.80, +1.9); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.55, +0.5)

Boys Don't Cry - Score: 3.74
Because: energy close to target (0.87 vs 0.80, +1.9); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.35, +0.5)

Sunrise City - Score: 3.69
Because: energy close to target (0.82 vs 0.80, +2.0); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5)

Gym Hero - Score: 3.67
Because: energy close to target (0.93 vs 0.80, +1.7); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.77, +0.5)

Profile: Missing optional keys entirely -- exercises the .get() defaults
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4}

Top recommendations:

Midnight Coding - Score: 8.89
Because: genre match (lofi, +3.0); mood match (chill, +3.0); energy close to target (0.42 vs 0.40, +2.0); energetic production (0.29 non-acoustic, +0.4); valence close to target (0.56, +0.5)

Library Rain - Score: 8.61
Because: genre match (lofi, +3.0); mood match (chill, +3.0); energy close to target (0.35 vs 0.40, +1.9); energetic production (0.14 non-acoustic, +0.2); valence close to target (0.60, +0.5)

Yukon - Score: 6.18
Because: mood match (chill, +3.0); energy close to target (0.55 vs 0.40, +1.7); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.65, +0.5)

Focus Flow - Score: 5.83
Because: genre match (lofi, +3.0); energy close to target (0.40 vs 0.40, +2.0); energetic production (0.22 non-acoustic, +0.3); valence close to target (0.59, +0.5)

Spacewalk Thoughts - Score: 5.38
Because: mood match (chill, +3.0); energy close to target (0.28 vs 0.40, +1.8); energetic production (0.08 non-acoustic, +0.1); valence close to target (0.65, +0.5)

Profile: target_valence conflicts with mood (sad mood, but demands max valence)
Prefs:   {'genre': 'alternative hip-hop', 'mood': 'sad', 'energy': 0.3, 'likes_acoustic': False, 'target_valence': 1.0}



**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

The biggest learning moment during this project was that changes in values when ranking songs can drastically change the outcome of how a song is rank. The designing of a point-based system is something that has to be strategically done in order to accurately match a user's needs. Using AI was helpful when implementing the methods in recommender.py and in creation of normal and edge test profiles. I needed to doubl-check the AI all the time especially when it came to creating test profiles to make sure it was in the boundaries that I wanted. 

I was surprised that simple algorithms could feel personalized by simply adding points for matching genre, mood, energy, and acoustic preferences. Even without machine learning, ranking songs by weighted scores made the recommendations change in ways that matched different user profiles. If I extended this project I would add more categories to make the song recommendation be more targeted and more songs to the catalog. I would also add more protections for ambiguous values and would suggest to the user that certain fields are required. 

