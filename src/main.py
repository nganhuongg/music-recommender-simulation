"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
    "genre": "folk",
    "mood": "playful",
    "energy": 0.85,
    "tempo_bpm": 128,
    "valence": 0.88,
    "danceability": 0.90,
    "likes_acoustic": True,
    }


    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nUser profile:\n")
    print(f"  Genre: {user_prefs['genre']}")
    print(f"  Mood: {user_prefs['mood']}")
    print(f"  Target energy: {user_prefs['energy']:.2f}")
    print(f"  Target tempo: {user_prefs['tempo_bpm']:.0f} BPM")
    print(f"  Target valence: {user_prefs['valence']:.2f}")
    print(f"  Target danceability: {user_prefs['danceability']:.2f}")
    print(f"  Likes acoustic: {user_prefs['likes_acoustic']}")

    print("\nTop recommendations:\n")
    divider = "-" * 72
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [reason.strip() for reason in explanation.split(",") if reason.strip()]

        print(divider)
        print(f"{index}. {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Final Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
    print(divider)


if __name__ == "__main__":
    main()
