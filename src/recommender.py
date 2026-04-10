from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
    target_tempo_bpm: float
    target_valence: float
    target_danceability: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric_fields = {
        "id": int,
        "energy": float,
        "tempo_bpm": float,
        "valence": float,
        "danceability": float,
        "acousticness": float,
    }

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        songs = []
        for row in reader:
            song = dict(row)
            for field, caster in numeric_fields.items():
                song[field] = caster(song[field])
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a weighted match score and explanation reasons for one song."""
    weights = {
        "genre": 2.0,
        "mood": 2.0,
        "energy": 3.0,
        "tempo_bpm": 2.5,
        "danceability": 2.0,
        "valence": 1.5,
        "acousticness": 1.5,
    }

    reasons: List[str] = []
    score = 0.0

    if user_prefs.get("genre") == song.get("genre"):
        score += weights["genre"]
        reasons.append("matches your preferred genre")

    if user_prefs.get("mood") == song.get("mood"):
        score += weights["mood"]
        reasons.append("matches your preferred mood")

    def closeness(candidate: float, target: float, value_range: float) -> float:
        distance = abs(candidate - target)
        normalized = distance / value_range
        return max(0.0, 1.0 - normalized)

    energy_match = closeness(song["energy"], user_prefs["energy"], 1.0)
    score += weights["energy"] * energy_match
    if energy_match >= 0.8:
        reasons.append("energy is close to your target")

    tempo_match = closeness(song["tempo_bpm"], user_prefs["tempo_bpm"], 116.0)
    score += weights["tempo_bpm"] * tempo_match
    if tempo_match >= 0.8:
        reasons.append("tempo is close to your target")

    danceability_match = closeness(song["danceability"], user_prefs["danceability"], 1.0)
    score += weights["danceability"] * danceability_match
    if danceability_match >= 0.8:
        reasons.append("danceability is close to your target")

    valence_match = closeness(song["valence"], user_prefs["valence"], 1.0)
    score += weights["valence"] * valence_match
    if valence_match >= 0.8:
        reasons.append("valence is close to your target")

    target_acousticness = 1.0 if user_prefs.get("likes_acoustic") else 0.0
    acousticness_match = closeness(song["acousticness"], target_acousticness, 1.0)
    score += weights["acousticness"] * acousticness_match
    if acousticness_match >= 0.8:
        reasons.append("acousticness fits your preference")

    if not reasons:
        reasons.append("has the closest overall feature match")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank the results, and return the top-k matches."""
    scored_songs: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
