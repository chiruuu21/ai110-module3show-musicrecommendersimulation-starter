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

Real-world recommendation systems, like those used by Spotify or YouTube, have huge data on different customer bases around the world which they leverage in their algorithm. These systems often combine collaborative filtering (using patterns from other users' behavior) and content-based filtering (matching item attributes to user preferences), and are frequently enhanced with deep learning models . Our version will focus on a content-based approach, prioritizing simplicity and transparency. 

Explain your design in plain language.

Our app is designed to suggest tracks aligning with individual tastes, our music recommender system evaluates song attributes against user preferences. Each Song in our system is represented by features such as genre, mood, energy, tempo (BPM), valence, and danceability, while the UserProfile stores preferences for these attributes, including preferred genre, mood, energy, tempo, and valence. The Recommender computes a relevance score for each song by comparing its attributes to the user's preferences, using a combination of similarity measures for numerical features and exact matches for categorical features. Songs are then ranked based on their scores, and the top matches are recommended to the user.


Finalized Algorithm Recipe
Genre Match: +2.0 points if the song's genre matches the user's preferred genre.
Mood Match: +1.0 point if the song's mood matches the user's preferred mood.
Energy Similarity: Add 1.5 * (1.0 - abs(song_energy - user_energy)).
Tempo Similarity: Add 1.0 * (1.0 - abs(song_tempo - user_tempo) / max_tempo).
Valence Similarity: Add 1.0 * (1.0 - abs(song_valence - user_valence)).

Potential Biases
Over-Prioritization of Genre
Numerical Feature Scaling
User Preference Dependence
Dataset Bias:

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



