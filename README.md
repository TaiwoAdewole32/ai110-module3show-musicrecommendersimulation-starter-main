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
| Genre | 3 | binary - exact match or 0 |
| Mood | 3 | binary - exact match or 0 |
| Energy | 2 | gradient - `2 * (1 - abs(target_energy - song.energy))` |
| Acousticness | 1.5 | gradient, direction-aware on `likes_acoustic` |
| Valence | 0.5 | gradient tie-breaker |

Genre and mood are categorical, so they're scored binary - a song either is or isn't the right genre/mood. Energy and acousticness are continuous 0-1 floats, so they're scored on a gradient instead, giving partial credit for "close enough" matches rather than an all-or-nothing cutoff. Valence isn't an explicit `UserProfile` preference, so it only contributes a small tie-breaking amount.
### Potential Biases

- Genre + mood together are worth 6 of the 10 points (60%) and are all-or-nothing, while energy and acousticness (3.5 pts combined) are gradient-scored. This means the system over-prioritizes genre/mood labels over "feel": a song that's a near-perfect energy/acousticness vibe match but tagged with a slightly different genre can rank below a same-genre song with a worse energy fit.
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



