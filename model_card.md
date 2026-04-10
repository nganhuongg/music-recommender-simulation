# Model Card: Music Recommender Simulation

## 1. Model Name

**CLI VibeMatch 1.0**

---

## 2. Goal / Task

The goal of this recommender is to suggest songs from a small catalog that best match a user's stated preferences. It does this by comparing the features of each song to a user taste profile, computing a score for each song, and ranking the songs from best match to worst match. The model is trying to answer a narrow question: "Given this user profile, which songs in this dataset are the closest fit?"

This is not a prediction model for long-term behavior, popularity, or what a large audience will like. It is a small recommendation simulation focused on matching one user's stated taste to one song at a time.

---

## 3. Intended Use and Non-Intended Use

This recommender is intended for classroom exploration and learning. It is designed to help explain how recommendation systems can turn user preferences and item features into ranked outputs. It is useful for demonstrating ideas like content-based filtering, weighted scoring, ranking rules, explanation generation, and bias in recommendation systems.

It is not intended for real users or production use. It should not be used for commercial streaming recommendations, high-stakes decision making, or any setting where fairness, diversity, or real user satisfaction must be measured carefully. It should also not be treated as a full model of a person's music taste, because it only uses a small handcrafted dataset and a limited set of features.

---

## 4. Data Used

The model uses a dataset stored in `data/songs.csv` with **35 songs**. The dataset began as a small starter file and was expanded with 25 additional songs to create more variety in genres, moods, and audio characteristics. Each song has the following features:

- `id`
- `title`
- `artist`
- `genre`
- `mood`
- `energy`
- `tempo_bpm`
- `valence`
- `danceability`
- `acousticness`

The dataset covers a wide range of genres such as `pop`, `lofi`, `rock`, `ambient`, `jazz`, `synthwave`, `hip hop`, `r&b`, `folk`, `classical`, `edm`, `reggae`, `metal`, `country`, `latin`, `house`, `techno`, `dream pop`, `soul`, `funk`, `blues`, `punk`, `k-pop`, `afrobeat`, `trip hop`, `orchestral`, `bossa nova`, `drum and bass`, `city pop`, `americana`, and `post-rock`. It also includes many moods such as `happy`, `chill`, `intense`, `romantic`, `serene`, `playful`, `groovy`, `melancholic`, `bright`, and `cinematic`.

The main limits of the dataset are that it is still very small and uneven. Many genres and moods appear only once, which makes exact label matching brittle. The data also does not include lyrics, language, release year, artist popularity, user listening history, skip behavior, or any collaborative filtering signals.

---

## 5. Algorithm Summary

This recommender uses a **content-based scoring rule**. Each song is compared directly to a user's profile. The user profile stores:

- favorite genre
- favorite mood
- target energy
- target tempo
- target valence
- target danceability
- whether the user prefers acoustic songs

The model gives bonus points when a song matches the user's preferred `genre` and `mood`. For the numeric features, it rewards songs that are **close** to the user's target instead of simply rewarding high values or low values. For example, if the user's target energy is `0.8`, then a song with energy `0.82` should score higher than a song with energy `0.4` or `0.95`, because it is closer to the target.

The current scoring weights are:

- `energy = 3.0`
- `tempo_bpm = 2.5`
- `danceability = 2.0`
- `genre = 2.0`
- `mood = 2.0`
- `valence = 1.5`
- `acousticness = 1.5`

After every song gets a score, the system sorts the songs by score from highest to lowest and returns the top `k` matches. It also generates a short explanation for each recommendation, such as "matches your preferred genre" or "tempo is close to your target."

Compared to the starter version, the model was improved by adding more user profile features, expanding the dataset, and implementing weighted numeric closeness instead of a very basic placeholder approach.

---

## 6. Observed Behavior / Biases

One pattern I observed is that the recommender works well when the categorical labels and numeric features point in the same direction. For example, a user who likes `pop`, `happy`, high energy, and high danceability tends to receive upbeat pop and dance-oriented tracks near the top, which feels intuitive.

A major limitation is that the model is sensitive to whichever feature has the highest weight, especially `energy`. In one experiment, I doubled the importance of `energy` and cut the importance of `genre` in half. This caused the lower-ranked results to shift toward songs that matched intensity better, even when they were less genre-consistent. That means the model can over-prioritize one dimension of taste and recommend songs that are mathematically close but stylistically less natural.

The dataset also creates imbalance. Many genres and moods only appear once, so some users get weaker genre or mood matching than others simply because the dataset is sparse. The model also cannot understand lyrics, language, artist background, cultural meaning, or changing listening context. Because of that, it may favor users whose taste fits the available tags and numeric ranges more neatly than users with more complex or mixed preferences.

---

## 7. Evaluation Process

I tested the system by running it with several different user profiles and checking whether the top recommendations made sense. I used a normal sample profile in `main.py` and then several edge-case or adversarial profiles to see how the scoring logic behaved under unusual conditions.

The edge-case profiles included:

- a contradictory profile: `lofi` and `chill`, but also very high energy, very high tempo, high valence, and high danceability
- a sparse-match profile: `classical` and `aggressive` together, with very low energy and very low danceability
- a mood-trap profile: `edm` but `chill`, while the numeric targets still strongly favored energetic dance music
- an acoustic-conflict profile: `folk`, `playful`, high energy, high danceability, and `likes_acoustic = True`

These profiles helped test whether the recommender would be "tricked" by conflicting preferences or produce unexpected results. I also ran a weight experiment where I changed `energy` from `3.0` to `6.0` and `genre` from `2.0` to `1.0`. With the original weights, the sample profile produced `Sunrise City`, `Rooftop Lights`, `Gym Hero`, `Velvet Sunrise`, and `Pulse District` in the top five. After the weight shift, the top five became `Sunrise City`, `Rooftop Lights`, `Gym Hero`, `Velvet Sunrise`, and `Midtown Strut`. That comparison showed that the model is quite sensitive to the scoring design.

I also visually checked the CLI output and used the explanation strings to see why songs were being ranked the way they were. This helped confirm that the ranking changes came from the scoring logic I intended, not from accidental bugs.

---

## 8. Strengths

The system is good at broad vibe matching. It can clearly separate calm acoustic styles from intense, fast, and dance-oriented styles. It also does a good job when the user's profile describes a coherent taste pattern, because the genre, mood, and numeric features reinforce each other.

Another strength is transparency. The scoring logic is simple enough to explain clearly, and the CLI output shows the final score and the reasons behind each recommendation. That makes it easier to understand, debug, and reflect on than a more opaque machine learning system.

---

## 9. Limitations and Risks

The biggest limitation is oversensitivity to feature weights. If one feature becomes too important, the model may drift away from intuitive recommendations and start overfitting to that one signal. This happened in my energy-weight experiment, where the model became more intensity-driven and less genre-aware.

The model also works on a tiny handcrafted catalog, so it cannot capture the real complexity of music recommendation. It does not know anything about lyrics, culture, time of day, repeated listening, novelty, artist popularity, or collaborative patterns across many users. Because the dataset is small and uneven, some users are effectively better represented than others, which can create unfairness or weak coverage for certain tastes.

---

## 10. Ideas for Improvement

If I kept developing this project, I would make these improvements:

1. Add support for multiple favorite genres and moods instead of just one, so the profile can represent mixed taste better.
2. Add diversity rules so the top recommendations are not all clustered around the same narrow vibe.
3. Add richer features such as lyric themes, softer genre similarity, or tolerance ranges for numeric targets instead of exact one-point targets.

---

## 11. Personal Reflection

My biggest learning moment was realizing how much influence simple engineering choices have on recommendations. I expected the dataset to matter most, but I learned that the scoring weights themselves can reshape the ranking very quickly. Changing one weight made the model behave differently in a way that was immediately visible, which helped me understand how much recommendation systems depend on design choices rather than just raw data.

Using AI tools helped me move faster when brainstorming scoring rules, designing edge-case profiles, and improving documentation. They were especially useful for turning rough ideas into clear explanations and for suggesting test cases I might not have thought of right away. At the same time, I had to double-check anything that touched the actual implementation or documented results, because an explanation can sound reasonable while still not matching the real code or the real output I captured.

What surprised me most was that a simple algorithm could still feel like a recommender. Even without machine learning or user-history data, the combination of feature matching, weighted scoring, ranking, and short explanations already feels personalized. If I extended this project further, I would next try softer genre similarity, multiple preferred moods, and a diversity-aware reranking step so the results feel both accurate and less repetitive.
