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

- Genre and mood together contribute up to 4.5 of the model's 13.5 available points, or about 33%. These features use exact matching, while energy and acousticness contribute up to 5 points using gradient scoring. Because energy is weighted more heavily than genre, a song with a closer energy level can outrank a same-genre song with a weaker energy match. Mood is still worth 3 points, so a mood mismatch can significantly affect the ranking.
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

```
Profile Prefs: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

Top Recommendations

1. Sunrise City

Artist: Neon Echo
Score: 10.55

Reasons:
Genre match: pop, +1.5
Mood match: happy, +3.0
Energy close to target: 0.82 vs. 0.80, +3.4
Energetic production: 0.82 non-acoustic, +1.2
Valence close to target: 0.84, +0.5
Popularity mainstream fit: 78, +0.4
Release year recency fit: 2023, +0.5

2. Boys Don't Cry

Artist: Lil Tecca
Score: 8.81

Reasons:
Mood match: happy, +3.0
Energy close to target: 0.87 vs. 0.80, +3.3
Energetic production: 0.92 non-acoustic, +1.4
Valence close to target: 0.35, +0.5
Popularity mainstream fit: 69, +0.3
Release year recency fit: 2019, +0.3

3. Headlines

Artist: Drake
Score: 8.72

Reasons:
Mood match: happy, +3.0
Energy exactly matches the target: 0.80 vs. 0.80, +3.5
Energetic production: 0.88 non-acoustic, +1.3
Valence close to target: 0.42, +0.5
Popularity mainstream fit: 80, +0.4
Release year recency fit: 2011, +0.0

4. Rooftop Lights

Artist: Indigo Parade
Score: 8.66

Reasons:
Mood match: happy, +3.0
Energy close to target: 0.76 vs. 0.80, +3.4
Energetic production: 0.65 non-acoustic, +1.0
Valence close to target: 0.81, +0.5
Popularity mainstream fit: 66, +0.3
Release year recency fit: 2023, +0.5

5. Necessari

Artist: Kizz Daniel
Score: 8.39

Reasons:
Mood match: happy, +3.0
Energy close to target: 0.65 vs. 0.80, +3.0
Energetic production: 0.80 non-acoustic, +1.2
Valence close to target: 0.80, +0.5
Popularity mainstream fit: 60, +0.3
Release year recency fit: 2021, +0.4
```

## Sample Output with Diverse Profiles
# Profile 1: Happy Pop Listener
```
Preferences:
Genre: pop
Mood: happy
Target energy: 0.8
Likes acoustic music: No

Top recommendations:

1. Sunrise City by Neon Echo
   Score: 10.55
   Reasons: genre match, mood match, close energy level,
   energetic production, popularity fit, and recent release.

2. Boys Don't Cry by Lil Tecca
   Score: 8.81
   Reasons: mood match, close energy level, energetic
   production, and popularity fit.

3. Headlines by Drake
   Score: 8.72
   Reasons: mood match, exact energy match, energetic
   production, and popularity fit.

4. Rooftop Lights by Indigo Parade
   Score: 8.66
   Reasons: mood match, close energy level, energetic
   production, and recent release.

5. Necessari by Kizz Daniel
   Score: 8.39
   Reasons: mood match, close energy level, energetic
   production, and release-year fit.

Sunrise City ranked first because it matched the listener's genre, mood, and energy preferences. The remaining songs matched the happy mood and high-energy preference but did not match every requested feature.
```

# Profile 2: High-Energy Sad Pop Listener
```
Preferences:
Genre: pop
Mood: sad
Target energy: 0.9
Likes acoustic music: No

Top recommendations:

1. Gym Hero by Max Pulse
   Score: 7.63
   Reasons: genre match, close energy level, energetic
   production, popularity fit, and recent release.

2. Hope by XXXTentacion
   Score: 7.17
   Reasons: mood match, partial energy match, popularity
   fit, and release-year fit.

3. Sunrise City by Neon Echo
   Score: 6.34
   Reasons: genre match, close energy level, and energetic
   production. A genre diversity penalty of -1.0 was applied.

4. Storm Runner by Voltline
   Score: 5.96
   Reasons: nearly exact energy match, energetic
   production, and popularity fit.

5. Boys Don't Cry by Lil Tecca
   Score: 5.95
   Reasons: close energy level, energetic production,
   popularity fit, and release-year fit.

Gym Hero ranked first because its pop genre and high energy outweighed its mood mismatch. Hope matched the requested sad mood, but its lower energy caused it to rank second. Sunrise City received a diversity penalty because pop had already appeared in the selected recommendations.
```
# Profile 3: Niche and Classic Lofi Listener
```
Preferences:
Genre: lofi
Mood: chill
Target energy: 0.4
Likes acoustic music: Yes
Prefers popular music: No
Prefers recent music: No
Favorite mood tags: nostalgic, introspective
Preferred activity: studying
Preferred structure: instrumental build

Top recommendations:

1. Midnight Coding by LoRoom
   Score: 12.30
   Reasons: genre match, mood match, close energy level,
   acoustic fit, niche popularity fit, mood-tag overlap,
   studying activity match, and instrumental-build match.

2. Library Rain by Paper Lanterns
   Score: 11.00
   Reasons: genre match, mood match, close energy level,
   acoustic fit, niche popularity fit, mood-tag overlap,
   studying activity match, and instrumental-build match.
   A genre diversity penalty of -1.0 was applied.

3. Spacewalk Thoughts by Orbit Bloom
   Score: 9.99
   Reasons: mood match, close energy level, acoustic fit,
   niche popularity fit, mood-tag overlap, and
   instrumental-build match.

4. Yukon by Justin Bieber
   Score: 7.87
   Reasons: mood match, close energy level, niche
   popularity fit, classic-release fit, and mood-tag overlap.

5. Coffee Shop Stories by Slow Stereo
   Score: 6.26
   Reasons: close energy level, strong acoustic fit,
   niche popularity fit, classic-release fit, and
   nostalgic mood-tag overlap.
```
**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I tested how changing the feature weights affected the recommendation order. I reduced the genre weight to 1.5 points and increased energy to 3.5 points, which allowed a song with a strong energy match to rank above a song that only matched the requested genre. I also added popularity, release year, mood tags, listening activity, and song structure to make recommendations more specific.

I ran the recommender with several different user profiles, including a Happy Pop listener, a High-Energy Sad Pop listener, an Intense Acoustic Rock listener, and a Niche and Classic Lofi listener. The results changed based on each profile. High-energy users received more energetic songs, while the lofi profile favored calmer and more acoustic songs. I also tested invalid energy values, missing preferences, unknown genres, capitalization differences, and extra spaces to identify weaknesses in the scoring logic.

Finally, I tested the diversity penalty. When an artist or genre had already appeared in the selected results, later songs from the same artist received a 2-point penalty and repeated genres received a 1-point penalty. This allowed other relevant artists and genres to appear in the top recommendations instead of allowing one category to dominate the list.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.


The recommender uses a small catalog of only 20 songs, so it cannot represent the full range of artists, genres, cultures, moods, or listening preferences. Users who prefer an underrepresented genre may receive weaker recommendations than users whose preferences are common in the dataset. The system also relies on exact text matches for categories such as genre, mood, listening activity, and song structure. Capitalization, spelling mistakes, or extra spaces can prevent a valid preference from receiving matching points. The labels are manually assigned and subjective, so two similar songs may be placed in different categories.
---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

The biggest learning moment during this project was that changes in values when ranking songs can drastically change the outcome of how a song is rank. The designing of a point-based system is something that has to be strategically done in order to accurately match a user's needs. Using AI was helpful when implementing the methods in recommender.py and in creation of normal and edge test profiles. I needed to doubl-check the AI all the time especially when it came to creating test profiles to make sure it was in the boundaries that I wanted. 

I was surprised that simple algorithms could feel personalized by simply adding points for matching genre, mood, energy, and acoustic preferences. Even without machine learning, ranking songs by weighted scores made the recommendations change in ways that matched different user profiles. If I extended this project I would add more categories to make the song recommendation be more targeted and more songs to the catalog. I would also add more protections for ambiguous values and would suggest to the user that certain fields are required. 

