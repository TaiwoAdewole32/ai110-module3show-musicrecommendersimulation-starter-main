import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Stores songs (the catalog of Song objects to recommend from) on the instance."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k Song objects for user (a UserProfile); currently a placeholder returning the first k songs unscored."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a str explaining why song was recommended to user; currently a placeholder string."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

_FLOAT_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness", "speechiness")

def load_songs(csv_path: str) -> List[Dict]:
    """Reads csv_path (path to the songs CSV) and returns a List[Dict] of songs with numeric fields as float, id as int, and explicit as bool."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in _FLOAT_FIELDS:
                row[field] = float(row[field])
            row["explicit"] = row["explicit"].strip().lower() == "true"
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores song against user_prefs on a 10-point tiered scale (genre/mood/energy/acousticness/valence) and returns a (score, reasons) tuple."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += 3
        reasons.append(f"genre match ({song['genre']}, +3.0)")

    if song["mood"] == user_prefs["mood"]:
        score += 3
        reasons.append(f"mood match ({song['mood']}, +3.0)")

    energy_gap = abs(user_prefs["energy"] - song["energy"])
    energy_pts = 2 * (1 - energy_gap)
    score += energy_pts
    reasons.append(f"energy close to target ({song['energy']:.2f} vs {user_prefs['energy']:.2f}, +{energy_pts:.1f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acousticness_pts = 1.5 * (song["acousticness"] if likes_acoustic else 1 - song["acousticness"])
    score += acousticness_pts
    if likes_acoustic:
        reasons.append(f"acoustic-leaning ({song['acousticness']:.2f} acousticness, +{acousticness_pts:.1f})")
    else:
        reasons.append(f"energetic production ({1 - song['acousticness']:.2f} non-acoustic, +{acousticness_pts:.1f})")

    target_valence = user_prefs.get("target_valence", song["valence"])
    valence_pts = 0.5 * (1 - abs(target_valence - song["valence"]))
    score += valence_pts
    reasons.append(f"valence close to target ({song['valence']:.2f}, +{valence_pts:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song in songs against user_prefs and returns the top k as (song, score, explanation) tuples, sorted highest score first."""
    scored = sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda item: item[1],
        reverse=True,
    )
    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
