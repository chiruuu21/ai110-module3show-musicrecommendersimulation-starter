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
cd src && python main.py
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Run from the `src/` folder with `python3 main.py`. Each profile shows the top 5 results.

Output below uses the updated weights from the Step 3 experiment (genre 1.0, energy 3.0, max score 7.0).

### Standard Profiles

**High-Energy Pop**

```
=== Profile: High-Energy Pop ===
Prefs: {'preferred_genre': 'pop', 'preferred_mood': 'happy', 'target_energy': 0.85, 'target_tempo': 125, 'target_valence': 0.8}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Sunrise City           pop         happy        6.83  
2   Rooftop Lights         indie pop   happy        5.71  
3   Gym Hero               pop         intense      5.69  
4   Neon Nights            synthwave   energetic    4.76  
5   Urban Vibes            hip hop     confident    4.73  

Top pick explanation: Score: 6.83. Reasons: Genre match, Mood match, Energy similarity: 0.97, Tempo similarity: 0.96, Valence similarity: 0.96
```

**Chill Lofi**

```
=== Profile: Chill Lofi ===
Prefs: {'preferred_genre': 'lofi', 'preferred_mood': 'chill', 'target_energy': 0.35, 'target_tempo': 75, 'target_valence': 0.6}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Library Rain           lofi        chill        6.99  
2   Midnight Coding        lofi        chill        6.74  
3   Focus Flow             lofi        focused      5.81  
4   Spacewalk Thoughts     ambient     chill        5.67  
5   Coffee Shop Stories    jazz        relaxed      4.75  

Top pick explanation: Score: 6.99. Reasons: Genre match, Mood match, Energy similarity: 1.00, Tempo similarity: 0.98, Valence similarity: 1.00
```

**Deep Intense Rock**

```
=== Profile: Deep Intense Rock ===
Prefs: {'preferred_genre': 'rock', 'preferred_mood': 'intense', 'target_energy': 0.92, 'target_tempo': 150, 'target_valence': 0.45}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Storm Runner           rock        intense      6.93  
2   Firestorm              metal       intense      5.83  
3   Gym Hero               pop         intense      5.56  
4   Electric Rush          edm         party        4.64  
5   Neon Nights            synthwave   energetic    4.55  

Top pick explanation: Score: 6.93. Reasons: Genre match, Mood match, Energy similarity: 0.99, Tempo similarity: 0.99, Valence similarity: 0.97
```

### Adversarial / Edge-Case Profiles

These profiles were designed to try to "trick" the scoring logic.

**Sad but Hyped**

```
=== Profile: Sad but Hyped ===
Prefs: {'preferred_genre': 'pop', 'preferred_mood': 'sad', 'target_energy': 0.9, 'target_tempo': 130, 'target_valence': 0.2}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Gym Hero               pop         intense      5.33  
2   Sunrise City           pop         happy        5.06  
3   Storm Runner           rock        intense      4.58  
4   Firestorm              metal       intense      4.48  
5   Neon Nights            synthwave   energetic    4.46  

Top pick explanation: Score: 5.33. Reasons: Genre match, Energy similarity: 0.97, Tempo similarity: 0.99, Valence similarity: 0.43
```

**Peaceful Metalhead**

```
=== Profile: Peaceful Metalhead ===
Prefs: {'preferred_genre': 'metal', 'preferred_mood': 'peaceful', 'target_energy': 0.1, 'target_tempo': 60, 'target_valence': 0.9}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Golden Hour            folk        peaceful     4.58  
2   Starlit Dreams         classical   romantic     4.47  
3   Spacewalk Thoughts     ambient     chill        4.21  
4   Ocean Breeze           ambient     calm         4.20  
5   Library Rain           lofi        chill        3.89  

Top pick explanation: Score: 4.58. Reasons: Mood match, Energy similarity: 0.62, Tempo similarity: 0.84, Valence similarity: 0.88
```

**Ghost Genre (k-pop)**

```
=== Profile: Ghost Genre (k-pop) ===
Prefs: {'preferred_genre': 'k-pop', 'preferred_mood': 'happy', 'target_energy': 0.8, 'target_tempo': 120, 'target_valence': 0.8}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Sunrise City           pop         happy        5.89  
2   Rooftop Lights         indie pop   happy        5.85  
3   Deep Dive              techno      focused      4.70  
4   Urban Vibes            hip hop     confident    4.67  
5   Neon Nights            synthwave   energetic    4.59  

Top pick explanation: Score: 5.89. Reasons: Mood match, Energy similarity: 0.98, Tempo similarity: 0.99, Valence similarity: 0.96
```

**Capitalized Pop**

```
=== Profile: Capitalized Pop ===
Prefs: {'preferred_genre': 'Pop', 'preferred_mood': 'Happy', 'target_energy': 0.85, 'target_tempo': 125, 'target_valence': 0.8}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Sunrise City           pop         happy        4.83  
2   Neon Nights            synthwave   energetic    4.76  
3   Urban Vibes            hip hop     confident    4.73  
4   Rooftop Lights         indie pop   happy        4.71  
5   Gym Hero               pop         intense      4.69  

Top pick explanation: Score: 4.83. Reasons: Energy similarity: 0.97, Tempo similarity: 0.96, Valence similarity: 0.96
```

**Out of Range**

```
=== Profile: Out of Range ===
Prefs: {'preferred_genre': 'edm', 'preferred_mood': 'party', 'target_energy': 1.5, 'target_tempo': 300, 'target_valence': -0.5}

#   Title                  Genre       Mood         Score 
----------------------------------------------------------
1   Electric Rush          edm         party        3.20  
2   Firestorm              metal       intense      1.73  
3   Storm Runner           rock        intense      1.51  
4   Gym Hero               pop         intense      1.18  
5   Neon Nights            synthwave   energetic    1.11  

Top pick explanation: Score: 3.20. Reasons: Genre match, Mood match, Energy similarity: 0.42, Tempo similarity: 0.14, Valence similarity: -0.20
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



