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
- `Song` fields used in scoring: `genre`, `mood`, `energy`, `acousticness`, `popularity`, `release_year`, `mood_tags`, `listening_activity`, `song_structure` (optionally `valence` as a tie-breaker). Stored-but-unused-in-scoring: `id`, `title`, `artist`, `tempo_bpm`, `danceability` (excluded per the earlier feature analysis - collinear with energy, free text, or bias risk).
- `UserProfile`/`user_prefs` fields used in scoring: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`, `prefers_popular`, `prefers_recent`, `favorite_mood_tags`, `preferred_activity`, `preferred_structure` - each maps 1:1 to one of the `Song` fields above.

### The Algorithm Recipe (finalized weights)

`score_song` (in `src/recommender.py`) scores every song on a 13.5-point tiered-additive scale:

| Feature | Max pts | Scoring shape |
|---|---|---|
| Genre | 1.5 | binary - exact match or 0 |
| Mood | 3 | binary - exact match or 0 |
| Energy | 3.5 | gradient - `3.5 * (1 - abs(target_energy - song.energy))` |
| Acousticness | 1.5 | gradient, direction-aware on `likes_acoustic` |
| Valence | 0.5 | gradient tie-breaker |
| Popularity | 0.5 | gradient, direction-aware on `prefers_popular` (default `True`) |
| Release year | 0.5 | gradient, direction-aware on `prefers_recent` (default `True`), normalized against the catalog's min/max `release_year` |
| Mood tags | 1 | partial credit - fraction of `favorite_mood_tags` found in the song's `mood_tags` |
| Listening activity | 0.5 | binary - exact match against `preferred_activity`, or 0 |
| Song structure | 1 | binary - exact match against `preferred_structure`, or 0 |

Genre, mood, listening activity, and song structure are categorical, so they're scored binary - a song either is or isn't the right match. Energy, acousticness, popularity, and release year are continuous, so they're scored on a gradient instead, giving partial credit for "close enough" matches rather than an all-or-nothing cutoff. Mood tags sit in between: multiple tags can be requested, and the song earns a proportional share of the point for however many it actually has. Valence isn't an explicit `UserProfile` preference, so it only contributes a small tie-breaking amount.
### Potential Biases

- Genre + mood together are worth 4.5 of the 10 points (45%) and are all-or-nothing, while energy and acousticness (5 pts combined) are gradient-scored. Genre was deliberately de-weighted and energy up-weighted relative to an earlier version of this scale, so "feel" (energy fit) can now outweigh an exact genre match: a song with a much closer energy fit can out-rank a same-genre song that's further from the target energy. Mood is still binary and still worth as much as energy at its max, so a mood mismatch remains costly.
- Genre and mood labels in the catalog are coarse and somewhat subjective (e.g. the `afrobeats` / `pop` / `dance pop` boundaries), so a binary match/no-match cutoff can penalize genuinely well-fitting songs over a labeling technicality rather than an actual taste mismatch.
- With only 20 songs and uneven genre representation in `data/songs.csv`, users whose favorite genre has few catalog entries get a much smaller pool of "full-credit" matches than users who like well-represented genres like pop.
- `prefers_popular` and `prefers_recent` both default to `True` when a `user_prefs` profile doesn't set them, so every recommendation run has a built-in mainstream/recency bias unless a profile explicitly opts out - niche or catalog/classic listeners are scored against the grain by default.

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

Sunrise City - Score: 10.55
Because: genre match (pop, +1.5); mood match (happy, +3.0); energy close to target (0.82 vs 0.80, +3.4); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5); popularity mainstream fit (78, +0.4); release year recency fit (2023, +0.5)

Boys Don't Cry - Score: 8.81
Because: mood match (happy, +3.0); energy close to target (0.87 vs 0.80, +3.3); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.35, +0.5); popularity mainstream fit (69, +0.3); release year recency fit (2019, +0.3)

Headlines - Score: 8.72
Because: mood match (happy, +3.0); energy close to target (0.80 vs 0.80, +3.5); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.42, +0.5); popularity mainstream fit (80, +0.4); release year recency fit (2011, +0.0)

Rooftop Lights - Score: 8.66
Because: mood match (happy, +3.0); energy close to target (0.76 vs 0.80, +3.4); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.81, +0.5); popularity mainstream fit (66, +0.3); release year recency fit (2023, +0.5)

Necessari - Score: 8.39
Because: mood match (happy, +3.0); energy close to target (0.65 vs 0.80, +3.0); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.80, +0.5); popularity mainstream fit (60, +0.3); release year recency fit (2021, +0.4)

## Sample Output with Diverse Profiles
Profile: Baseline (sanity check)
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 10.55
Because: genre match (pop, +1.5); mood match (happy, +3.0); energy close to target (0.82 vs 0.80, +3.4); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5); popularity mainstream fit (78, +0.4); release year recency fit (2023, +0.5)

Boys Don't Cry - Score: 8.81
Because: mood match (happy, +3.0); energy close to target (0.87 vs 0.80, +3.3); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.35, +0.5); popularity mainstream fit (69, +0.3); release year recency fit (2019, +0.3)

Headlines - Score: 8.72
Because: mood match (happy, +3.0); energy close to target (0.80 vs 0.80, +3.5); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.42, +0.5); popularity mainstream fit (80, +0.4); release year recency fit (2011, +0.0)

Rooftop Lights - Score: 8.66
Because: mood match (happy, +3.0); energy close to target (0.76 vs 0.80, +3.4); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.81, +0.5); popularity mainstream fit (66, +0.3); release year recency fit (2023, +0.5)

Necessari - Score: 8.39
Because: mood match (happy, +3.0); energy close to target (0.65 vs 0.80, +3.0); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.80, +0.5); popularity mainstream fit (60, +0.3); release year recency fit (2021, +0.4)

Profile: Conflicting energy vs. mood (high-energy but wants sad)
Prefs:   {'genre': 'pop', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}

Top recommendations:

Gym Hero - Score: 7.63
Because: genre match (pop, +1.5); energy close to target (0.93 vs 0.90, +3.4); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.77, +0.5); popularity mainstream fit (70, +0.3); release year recency fit (2022, +0.5)

Sunrise City - Score: 7.34
Because: genre match (pop, +1.5); energy close to target (0.82 vs 0.90, +3.2); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5); popularity mainstream fit (78, +0.4); release year recency fit (2023, +0.5)

Hope - Score: 7.17
Because: mood match (sad, +3.0); energy close to target (0.57 vs 0.90, +2.3); energetic production (0.45 non-acoustic, +0.7); valence close to target (0.20, +0.5); popularity mainstream fit (71, +0.4); release year recency fit (2018, +0.3)

Storm Runner - Score: 5.96
Because: energy close to target (0.91 vs 0.90, +3.5); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.48, +0.5); popularity mainstream fit (62, +0.3); release year recency fit (2019, +0.3)

Boys Don't Cry - Score: 5.95
Because: energy close to target (0.87 vs 0.90, +3.4); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.35, +0.5); popularity mainstream fit (69, +0.3); release year recency fit (2019, +0.3)

Profile: Conflicting acoustic preference vs. energy (wants both loud AND acoustic)
Prefs:   {'genre': 'rock', 'mood': 'intense', 'energy': 1.0, 'likes_acoustic': True}

Top recommendations:

Storm Runner - Score: 8.98
Because: genre match (rock, +1.5); mood match (intense, +3.0); energy close to target (0.91 vs 1.00, +3.2); acoustic-leaning (0.10 acousticness, +0.2); valence close to target (0.48, +0.5); popularity mainstream fit (62, +0.3); release year recency fit (2019, +0.3)

Gym Hero - Score: 7.64
Because: mood match (intense, +3.0); energy close to target (0.93 vs 1.00, +3.3); acoustic-leaning (0.05 acousticness, +0.1); valence close to target (0.77, +0.5); popularity mainstream fit (70, +0.3); release year recency fit (2022, +0.5)

Sunrise City - Score: 4.53
Because: energy close to target (0.82 vs 1.00, +2.9); acoustic-leaning (0.18 acousticness, +0.3); valence close to target (0.84, +0.5); popularity mainstream fit (78, +0.4); release year recency fit (2023, +0.5)

Rooftop Lights - Score: 4.51
Because: energy close to target (0.76 vs 1.00, +2.7); acoustic-leaning (0.35 acousticness, +0.5); valence close to target (0.81, +0.5); popularity mainstream fit (66, +0.3); release year recency fit (2023, +0.5)

Beauty and a Beat - Score: 4.35
Because: energy close to target (0.95 vs 1.00, +3.3); acoustic-leaning (0.05 acousticness, +0.1); valence close to target (0.82, +0.5); popularity mainstream fit (82, +0.4); release year recency fit (2012, +0.0)

Profile: Out-of-range energy (> 1.0) -- does the gap math stay sane?
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 1.8, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 7.19
Because: genre match (pop, +1.5); mood match (happy, +3.0); energy close to target (0.82 vs 1.80, +0.1); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5); popularity mainstream fit (78, +0.4); release year recency fit (2023, +0.5)

Beauty and a Beat - Score: 5.90
Because: mood match (happy, +3.0); energy close to target (0.95 vs 1.80, +0.5); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.82, +0.5); popularity mainstream fit (82, +0.4); release year recency fit (2012, +0.0)

Boys Don't Cry - Score: 5.80
Because: mood match (happy, +3.0); energy close to target (0.87 vs 1.80, +0.2); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.35, +0.5); popularity mainstream fit (69, +0.3); release year recency fit (2019, +0.3)

MMS - Score: 5.63
Because: mood match (happy, +3.0); energy close to target (0.50 vs 1.80, +0.0); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.5); popularity mainstream fit (65, +0.3); release year recency fit (2022, +0.5)

Necessari - Score: 5.42
Because: mood match (happy, +3.0); energy close to target (0.65 vs 1.80, +0.0); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.80, +0.5); popularity mainstream fit (60, +0.3); release year recency fit (2021, +0.4)

Profile: Out-of-range energy (negative) -- can this produce a negative or >2 pt swing?
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': -0.5, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 7.12
Because: genre match (pop, +1.5); mood match (happy, +3.0); energy close to target (0.82 vs -0.50, +0.0); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5); popularity mainstream fit (78, +0.4); release year recency fit (2023, +0.5)

MMS - Score: 5.63
Because: mood match (happy, +3.0); energy close to target (0.50 vs -0.50, +0.0); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.5); popularity mainstream fit (65, +0.3); release year recency fit (2022, +0.5)

Boys Don't Cry - Score: 5.56
Because: mood match (happy, +3.0); energy close to target (0.87 vs -0.50, +0.0); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.35, +0.5); popularity mainstream fit (69, +0.3); release year recency fit (2019, +0.3)

Necessari - Score: 5.42
Because: mood match (happy, +3.0); energy close to target (0.65 vs -0.50, +0.0); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.80, +0.5); popularity mainstream fit (60, +0.3); release year recency fit (2021, +0.4)

Beauty and a Beat - Score: 5.38
Because: mood match (happy, +3.0); energy close to target (0.95 vs -0.50, +0.0); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.82, +0.5); popularity mainstream fit (82, +0.4); release year recency fit (2012, +0.0)

Profile: No genre/mood in catalog at all -- forces score to rely only on continuous fields
Prefs:   {'genre': 'opera', 'mood': 'furious', 'energy': 0.5, 'likes_acoustic': False}

Top recommendations:

MMS - Score: 6.13
Because: energy close to target (0.50 vs 0.50, +3.5); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.5); popularity mainstream fit (65, +0.3); release year recency fit (2022, +0.5)

Yukon - Score: 5.64
Because: energy close to target (0.52 vs 0.50, +3.4); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.65, +0.5); popularity mainstream fit (63, +0.3); release year recency fit (2021, +0.4)

Necessari - Score: 5.39
Because: energy close to target (0.65 vs 0.50, +3.0); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.80, +0.5); popularity mainstream fit (60, +0.3); release year recency fit (2021, +0.4)

Trust Issues - Score: 5.37
Because: energy close to target (0.45 vs 0.50, +3.3); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.28, +0.5); popularity mainstream fit (68, +0.3); release year recency fit (2011, +0.0)

Unavailable - Score: 5.24
Because: energy close to target (0.76 vs 0.50, +2.6); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.65, +0.5); popularity mainstream fit (74, +0.4); release year recency fit (2022, +0.5)

Profile: Case/whitespace mismatch on an otherwise valid genre (exact-match brittleness)
Prefs:   {'genre': 'Pop', 'mood': ' happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 6.05
Because: energy close to target (0.82 vs 0.80, +3.4); energetic production (0.82 non-acoustic, +1.2); valence close to target (0.84, +0.5); popularity mainstream fit (78, +0.4); release year recency fit (2023, +0.5)

Unavailable - Score: 6.01
Because: energy close to target (0.76 vs 0.80, +3.4); energetic production (0.88 non-acoustic, +1.3); valence close to target (0.65, +0.5); popularity mainstream fit (74, +0.4); release year recency fit (2022, +0.5)

Starboy - Score: 5.82
Because: energy close to target (0.74 vs 0.80, +3.3); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.55, +0.5); popularity mainstream fit (88, +0.4); release year recency fit (2016, +0.2)

Boys Don't Cry - Score: 5.81
Because: energy close to target (0.87 vs 0.80, +3.3); energetic production (0.92 non-acoustic, +1.4); valence close to target (0.35, +0.5); popularity mainstream fit (69, +0.3); release year recency fit (2019, +0.3)

Gym Hero - Score: 5.78
Because: energy close to target (0.93 vs 0.80, +3.0); energetic production (0.95 non-acoustic, +1.4); valence close to target (0.77, +0.5); popularity mainstream fit (70, +0.3); release year recency fit (2022, +0.5)

Profile: Missing optional keys entirely -- exercises the .get() defaults
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4}

Top recommendations:

Midnight Coding - Score: 9.56
Because: genre match (lofi, +1.5); mood match (chill, +3.0); energy close to target (0.42 vs 0.40, +3.4); energetic production (0.29 non-acoustic, +0.4); valence close to target (0.56, +0.5); popularity mainstream fit (55, +0.3); release year recency fit (2021, +0.4)

Library Rain - Score: 9.15
Because: genre match (lofi, +1.5); mood match (chill, +3.0); energy close to target (0.35 vs 0.40, +3.3); energetic production (0.14 non-acoustic, +0.2); valence close to target (0.60, +0.5); popularity mainstream fit (48, +0.2); release year recency fit (2020, +0.4)

Yukon - Score: 8.29
Because: mood match (chill, +3.0); energy close to target (0.52 vs 0.40, +3.1); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.65, +0.5); popularity mainstream fit (63, +0.3); release year recency fit (2021, +0.4)

Spacewalk Thoughts - Score: 7.17
Because: mood match (chill, +3.0); energy close to target (0.28 vs 0.40, +3.1); energetic production (0.08 non-acoustic, +0.1); valence close to target (0.65, +0.5); popularity mainstream fit (35, +0.2); release year recency fit (2018, +0.3)

Focus Flow - Score: 6.54
Because: genre match (lofi, +1.5); energy close to target (0.40 vs 0.40, +3.5); energetic production (0.22 non-acoustic, +0.3); valence close to target (0.59, +0.5); popularity mainstream fit (50, +0.2); release year recency fit (2022, +0.5)

Profile: target_valence conflicts with mood (sad mood, but demands max valence)
Prefs:   {'genre': 'alternative hip-hop', 'mood': 'sad', 'energy': 0.3, 'likes_acoustic': False, 'target_valence': 1.0}

Top recommendations:

Hope - Score: 8.48
Because: genre match (alternative hip-hop, +1.5); mood match (sad, +3.0); energy close to target (0.57 vs 0.30, +2.6); energetic production (0.45 non-acoustic, +0.7); valence close to target (0.20, +0.1); popularity mainstream fit (71, +0.4); release year recency fit (2018, +0.3)

MMS - Score: 5.27
Because: energy close to target (0.50 vs 0.30, +2.8); energetic production (0.90 non-acoustic, +1.4); valence close to target (0.68, +0.3); popularity mainstream fit (65, +0.3); release year recency fit (2022, +0.5)

Yukon - Score: 4.76
Because: energy close to target (0.52 vs 0.30, +2.7); energetic production (0.65 non-acoustic, +1.0); valence close to target (0.65, +0.3); popularity mainstream fit (63, +0.3); release year recency fit (2021, +0.4)

Trust Issues - Score: 4.66
Because: energy close to target (0.45 vs 0.30, +3.0); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.28, +0.1); popularity mainstream fit (68, +0.3); release year recency fit (2011, +0.0)

Necessari - Score: 4.59
Because: energy close to target (0.65 vs 0.30, +2.3); energetic production (0.80 non-acoustic, +1.2); valence close to target (0.80, +0.4); popularity mainstream fit (60, +0.3); release year recency fit (2021, +0.4)

Profile: Everything mismatched -- worst-case floor score
Prefs:   {'genre': 'polka', 'mood': 'furious', 'energy': 0.0, 'likes_acoustic': True}

Top recommendations:

Spacewalk Thoughts - Score: 4.87
Because: energy close to target (0.28 vs 0.00, +2.5); acoustic-leaning (0.92 acousticness, +1.4); valence close to target (0.65, +0.5); popularity mainstream fit (35, +0.2); release year recency fit (2018, +0.3)

Library Rain - Score: 4.68
Because: energy close to target (0.35 vs 0.00, +2.3); acoustic-leaning (0.86 acousticness, +1.3); valence close to target (0.60, +0.5); popularity mainstream fit (48, +0.2); release year recency fit (2020, +0.4)

Coffee Shop Stories - Score: 4.51
Because: energy close to target (0.37 vs 0.00, +2.2); acoustic-leaning (0.89 acousticness, +1.3); valence close to target (0.71, +0.5); popularity mainstream fit (44, +0.2); release year recency fit (2017, +0.2)

Focus Flow - Score: 4.48
Because: energy close to target (0.40 vs 0.00, +2.1); acoustic-leaning (0.78 acousticness, +1.2); valence close to target (0.59, +0.5); popularity mainstream fit (50, +0.2); release year recency fit (2022, +0.5)

Midnight Coding - Score: 4.29
Because: energy close to target (0.42 vs 0.00, +2.0); acoustic-leaning (0.71 acousticness, +1.1); valence close to target (0.56, +0.5); popularity mainstream fit (55, +0.3); release year recency fit (2021, +0.4)

Profile: Niche/classic listener -- exercises all 5 new attributes
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True, 'prefers_popular': False, 'prefers_recent': False, 'favorite_mood_tags': ['nostalgic', 'introspective'], 'preferred_activity': 'studying', 'preferred_structure': 'instrumental build'}

Top recommendations:

Midnight Coding - Score: 12.30
Because: genre match (lofi, +1.5); mood match (chill, +3.0); energy close to target (0.42 vs 0.40, +3.4); acoustic-leaning (0.71 acousticness, +1.1); valence close to target (0.56, +0.5); popularity niche fit (55, +0.2); release year classic fit (2021, +0.1); mood tag overlap (introspective, nostalgic, +1.0); listening activity match (studying, +0.5); song structure match (instrumental build, +1.0)

Library Rain - Score: 12.00
Because: genre match (lofi, +1.5); mood match (chill, +3.0); energy close to target (0.35 vs 0.40, +3.3); acoustic-leaning (0.86 acousticness, +1.3); valence close to target (0.60, +0.5); popularity niche fit (48, +0.3); release year classic fit (2020, +0.1); mood tag overlap (nostalgic, +0.5); listening activity match (studying, +0.5); song structure match (instrumental build, +1.0)

Spacewalk Thoughts - Score: 9.99
Because: mood match (chill, +3.0); energy close to target (0.28 vs 0.40, +3.1); acoustic-leaning (0.92 acousticness, +1.4); valence close to target (0.65, +0.5); popularity niche fit (35, +0.3); release year classic fit (2018, +0.2); mood tag overlap (introspective, +0.5); song structure match (instrumental build, +1.0)

Focus Flow - Score: 8.96
Because: genre match (lofi, +1.5); energy close to target (0.40 vs 0.40, +3.5); acoustic-leaning (0.78 acousticness, +1.2); valence close to target (0.59, +0.5); popularity niche fit (50, +0.2); release year classic fit (2022, +0.0); mood tag overlap (introspective, +0.5); listening activity match (studying, +0.5); song structure match (instrumental build, +1.0)

Yukon - Score: 7.87
Because: mood match (chill, +3.0); energy close to target (0.52 vs 0.40, +3.1); acoustic-leaning (0.35 acousticness, +0.5); valence close to target (0.65, +0.5); popularity niche fit (63, +0.2); release year classic fit (2021, +0.1); mood tag overlap (nostalgic, +0.5)

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

