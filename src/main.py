"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

# Adversarial / edge-case profiles for stress-testing score_song and
# recommend_songs. Each targets a specific way the scoring logic could
# be tricked, blow up, or silently do the wrong thing.
ADVERSARIAL_PROFILES = [
    (
        "Baseline (sanity check)",
        {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    ),
    (
        "Conflicting energy vs. mood (high-energy but wants sad)",
        {"genre": "pop", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
    ),
    (
        "Conflicting acoustic preference vs. energy (wants both loud AND acoustic)",
        {"genre": "rock", "mood": "intense", "energy": 1.0, "likes_acoustic": True},
    ),
    (
        "Out-of-range energy (> 1.0) -- does the gap math stay sane?",
        {"genre": "pop", "mood": "happy", "energy": 1.8, "likes_acoustic": False},
    ),
    (
        "Out-of-range energy (negative) -- can this produce a negative or >2 pt swing?",
        {"genre": "pop", "mood": "happy", "energy": -0.5, "likes_acoustic": False},
    ),
    (
        "No genre/mood in catalog at all -- forces score to rely only on continuous fields",
        {"genre": "opera", "mood": "furious", "energy": 0.5, "likes_acoustic": False},
    ),
    (
        "Case/whitespace mismatch on an otherwise valid genre (exact-match brittleness)",
        {"genre": "Pop", "mood": " happy", "energy": 0.8, "likes_acoustic": False},
    ),
    (
        "Missing optional keys entirely -- exercises the .get() defaults",
        {"genre": "lofi", "mood": "chill", "energy": 0.4},
    ),
    (
        "target_valence conflicts with mood (sad mood, but demands max valence)",
        {
            "genre": "alternative hip-hop",
            "mood": "sad",
            "energy": 0.3,
            "likes_acoustic": False,
            "target_valence": 1.0,
        },
    ),
    (
        "Everything mismatched -- worst-case floor score",
        {"genre": "polka", "mood": "furious", "energy": 0.0, "likes_acoustic": True},
    ),
]


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in ADVERSARIAL_PROFILES:
        print("=" * 70)
        print(f"Profile: {label}")
        print(f"Prefs:   {user_prefs}")
        print("=" * 70)

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
