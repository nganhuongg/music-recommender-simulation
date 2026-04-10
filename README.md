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

Real-world recommendation systems usually combine many signals at once. Platforms like Spotify or YouTube learn from large amounts of behavior data such as plays, skips, likes, watch time, repeated listening, and what similar users enjoyed next. They often retrieve a large set of possible candidates, score each item with machine learning models, and then rank the list while balancing relevance, novelty, and variety. In other words, real systems do not just ask whether a song is "good"; they ask whether it is a good fit for a particular person at a particular moment.

This project uses a simpler and more transparent content-based recommender. Instead of learning from the behavior of many users, it recommends songs by comparing the attributes of each song to one user's stated preferences. Each `Song` includes features such as `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The `UserProfile` was expanded beyond genre, mood, and energy to also include `target_tempo_bpm`, `target_valence`, and `target_danceability`. I added these values because genre and mood alone are too coarse: they can separate something like chill lofi from intense rock, but they do not capture finer differences such as cheerful versus melancholy songs, fast versus steady songs, or groove-heavy versus more atmospheric songs.

The workflow is: input a user's taste profile, loop through every song in `songs.csv`, score each song against the profile, sort all songs by score, and return the top `k` results. The scoring rule rewards songs that are closer to the user's preferred values, not just songs with higher numbers. Exact matches on categorical features like genre and mood add bonus points, while numerical features are scored by closeness to the user's target. For example, a song with energy near the user's target energy should score higher than one that is much lower or much higher. This means the system prioritizes interpretable matches: similar vibe first, then the closest overall fit across the remaining features.

![Workflow diagram](images/workflow.png)

The current weighting strategy is designed so that numeric vibe features lead and categorical labels refine the result. A reasonable starting point is `energy = 3.0`, `tempo_bpm = 2.5`, `danceability = 2.0`, `genre = 2.0`, `mood = 2.0`, `valence = 1.5`, and `acousticness = 1.5`. `Energy` and `tempo_bpm` are weighted the most because they strongly separate low-key tracks from intense ones in this dataset. `Danceability` also matters because it helps identify whether a song feels groove-driven or more reflective. `Genre` and `mood` still matter, but they are not given overwhelming weight because the dataset has many one-off labels, and exact matches would otherwise dominate too much. `Valence` and `acousticness` are useful secondary signals that help describe emotional tone and sonic texture.

This system also has clear biases. Because `energy` and `tempo_bpm` have the largest weights, the recommender may over-prioritize the overall intensity of a song and underrate songs that match the user's genre or emotional taste in a subtler way. Exact genre and mood matching can also be brittle because many labels appear only once, which may make the system treat similar songs as different just because they use different tags. The model does not understand lyrics, cultural context, language, or changing mood over time, and it assumes that a user's taste can be summarized by a small fixed profile. That makes the system easy to explain, but less flexible and potentially less fair than a richer real-world recommender.

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

## Example Results

These screenshots show sample terminal output from the recommender after scoring songs, sorting them by total score, and returning the top matches.

![Recommendation result 1](images/result1.png)

![Recommendation result 2](images/result2.png)

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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

