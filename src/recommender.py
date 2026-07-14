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
_INT_FIELDS = ("popularity", "release_year")

def load_songs(csv_path: str) -> List[Dict]:
    """Reads csv_path (path to the songs CSV) and returns a List[Dict] of songs with numeric fields as float, id/popularity/release_year as int, and explicit as bool."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in _FLOAT_FIELDS:
                row[field] = float(row[field])
            for field in _INT_FIELDS:
                row[field] = int(row[field])
            row["explicit"] = row["explicit"].strip().lower() == "true"
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict, catalog_year_range: Optional[Tuple[int, int]] = None) -> Tuple[float, List[str]]:
    """Scores song against user_prefs on a 10-point tiered scale (genre/mood/energy/acousticness/valence) and returns a (score, reasons) tuple."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        genre_pts = 1.5
        score += genre_pts
        reasons.append(f"genre match ({song['genre']}, +{genre_pts:.1f})")

    if song["mood"] == user_prefs["mood"]:
        mood_pts = 3
        score += mood_pts
        reasons.append(f"mood match ({song['mood']}, +{mood_pts:.1f})")

    energy_gap = min(abs(user_prefs["energy"] - song["energy"]), 1.0)
    energy_pts = 3.5 * (1 - energy_gap)
    score += energy_pts
    reasons.append(f"energy close to target ({song['energy']:.2f} vs {user_prefs['energy']:.2f}, {energy_pts:+.1f})")

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

    prefers_popular = user_prefs.get("prefers_popular", True)
    popularity_pts = 0.5 * (song["popularity"] / 100 if prefers_popular else 1 - song["popularity"] / 100)
    score += popularity_pts
    reasons.append(f"popularity {'mainstream' if prefers_popular else 'niche'} fit ({song['popularity']}, +{popularity_pts:.1f})")

    prefers_recent = user_prefs.get("prefers_recent", True)
    min_year, max_year = catalog_year_range or (song["release_year"], song["release_year"])
    year_span = max(max_year - min_year, 1)
    recency = (song["release_year"] - min_year) / year_span
    recency_pts = 0.5 * (recency if prefers_recent else 1 - recency)
    score += recency_pts
    reasons.append(f"release year {'recency' if prefers_recent else 'classic'} fit ({song['release_year']}, +{recency_pts:.1f})")

    song_tags = {t.strip() for t in song.get("mood_tags", "").split(";") if t.strip()}
    requested_mood_tags = user_prefs.get("favorite_mood_tags")
    if requested_mood_tags:
        requested_tags = {requested_mood_tags} if isinstance(requested_mood_tags, str) else set(requested_mood_tags)
        overlap = requested_tags & song_tags
        if overlap:
            tag_pts = 1.0 * (len(overlap) / len(requested_tags))
            score += tag_pts
            reasons.append(f"mood tag overlap ({', '.join(sorted(overlap))}, +{tag_pts:.1f})")

    preferred_activity = user_prefs.get("preferred_activity")
    if preferred_activity and preferred_activity == song.get("listening_activity"):
        score += 0.5
        reasons.append(f"listening activity match ({song['listening_activity']}, +0.5)")

    preferred_structure = user_prefs.get("preferred_structure")
    if preferred_structure and preferred_structure == song.get("song_structure"):
        score += 1.0
        reasons.append(f"song structure match ({song['song_structure']}, +1.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song in songs against user_prefs and returns the top k as (song, score, explanation) tuples, sorted highest score first."""
    years = [song["release_year"] for song in songs]
    catalog_year_range = (min(years), max(years)) if years else None
    scored = sorted(
        ((song, *score_song(user_prefs, song, catalog_year_range)) for song in songs),
        key=lambda item: item[1],
        reverse=True,
    )
    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
