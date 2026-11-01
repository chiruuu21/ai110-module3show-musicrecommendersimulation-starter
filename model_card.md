# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal:** VibeMatch suggests the top 5 songs from a small catalog that best fit a user's taste. The user describes their taste with a favorite genre, a favorite mood, and target levels for energy, tempo, and positivity (valence).

**Assumptions about the user:**

- They can describe their taste with one genre and one mood.
- They type labels exactly as the catalog does (lowercase, e.g. "pop").
- Their taste doesn't change. There is no listening history.

**Intended use:** classroom exploration. It's meant for learning how recommenders turn data into rankings and where they can go wrong.

**Not intended for:**

- Real users or a real music app. The catalog is only 20 songs.
- Users whose taste isn't in the catalog, such as sad, angry, or dark music. The system will quietly recommend upbeat songs instead.
- Any decision that matters, such as ranking artists for pay or promotion. The scores reflect our hand-picked weights, not real listener data.

---

## 3. How the Model Works  

Every song gets a score. Higher score = better match. The top 5 scores are recommended.

- **Genre match:** +1 point if the song's genre is exactly the user's favorite.
- **Mood match:** +1 point if the song's mood is exactly the user's favorite.
- **Energy:** up to +3 points. The closer the song's energy is to what the user wants, the more points it gets.
- **Tempo:** up to +1 point for being close to the user's preferred speed (BPM).
- **Valence (positivity):** up to +1 point for being close to how happy or sad the user wants the music to sound.

The best possible score is 7.

**Changes from the starter logic:** the starter weights were genre +2 and energy ×1.5. In testing, genre was too strong. A loud "intense" pop song beat a truly happy song for a "Happy Pop" listener. So I halved genre (2 → 1) and doubled energy (1.5 → 3). Now the system cares more about how a song *sounds* than what it's *labeled*.

---

## 4. Data  

- **Size:** 20 songs in `data/songs.csv`. I did not add or remove any.
- **Features per song:** genre, mood, energy, tempo (BPM), valence, danceability, acousticness. Only the first five are used in scoring.
- **Genres:** 15 different ones (pop, lofi, rock, metal, jazz, edm, ambient, classical, and more). Most genres have only 1 song. Lofi has the most with 3.
- **Moods:** 14 different ones (happy, chill, intense, calm, romantic, etc.).
- **What's missing:**
  - There are no sad, angry, or melancholy songs. Every song's valence is 0.42 or higher.
  - Very few songs have medium energy.
  - There are no lyrics, languages, or regional music styles.

---

## 5. Strengths  

- **Clear, opposite tastes work well.** Chill Lofi and Deep Intense Rock got completely different lists, and both felt right: quiet study music for one, loud fast songs for the other.
- **The #1 pick is usually spot on.** For all 3 normal profiles, the top song matched the genre, the mood, and the numbers (*Sunrise City*, *Library Rain*, *Storm Runner*).
- **Reasonable fallbacks.** When the genre didn't exist (k-pop), it still found happy, upbeat pop songs.
- **Easy to explain.** Every recommendation comes with reasons, such as "Genre match, Energy similarity: 0.97," so you can see exactly why a song was picked.

---

## 6. Limitations and Bias 

**Main weakness: the system cannot serve listeners who want sad or dark music.** Every song in the catalog has a valence (positivity) of 0.42 or higher, and none of the 14 moods is "sad," "melancholy," or "angry." When I tested a "Sad but Hyped" profile (mood: sad, valence: 0.2), the mood bonus never fired and the best valence match was only 0.78, so the system fell back on recommending upbeat songs like *Gym Hero* and *Sunrise City*. This creates a filter bubble: a user with darker taste is quietly pushed toward happy music, and the scores never warn them that nothing in the catalog actually fits.

**Other limitations found during testing:**

- **Exact text matching:** "indie pop" gets no credit for being close to "pop," and "Pop" (capitalized) matches nothing, so small labeling differences remove the genre and mood bonuses entirely.
- **One song per genre:** 12 of the 15 genres have only one song, so a genre match often points to a single track. After that the list fills with whatever matches on energy.
- **Mid-energy gap:** only 3 songs fall between 0.45 and 0.74 energy. Since energy is now the heaviest weight (3.0), users who want medium-energy music get weaker matches than users at either extreme.
- **Ignored features:** danceability, acousticness, and the 'likes acoustic' preference are loaded but never used in scoring.
- **No input checks:** values outside 0–1 (e.g. energy 1.5) produce negative similarity scores without any error.

---

## 7. Evaluation  

### Profiles tested

I tested 8 user profiles. The full top-5 output for each is in the README.

- **3 normal profiles:** High-Energy Pop, Chill Lofi, Deep Intense Rock.
- **5 "trick" profiles** designed to break the scoring:
  - **Sad but Hyped:** wants sad music with high energy (conflicting preferences).
  - **Peaceful Metalhead:** wants metal that is also calm and slow.
  - **Ghost Genre:** asks for k-pop, which isn't in the catalog.
  - **Capitalized Pop:** the same as High-Energy Pop but typed as "Pop" and "Happy".
  - **Out of Range:** impossible values like energy 1.5 and tempo 300.

For each one I checked whether the top 5 "felt" right for that listener. I also re-ran everything after the weight experiment (genre 2.0 → 1.0, energy 1.5 → 3.0) to see what changed.

### What surprised me

- **Gym Hero showed up everywhere.** It was in the top 5 for 6 of the 8 profiles. In plain terms: the system gives points for "sounds similar" (energy, tempo, positivity) and bonus points for "same genre." Gym Hero is loud, upbeat, and labeled pop, so it collects a little bit of credit from almost everyone. For a "Happy Pop" listener it even beat a genuinely happy song (*Rooftop Lights*) because the genre bonus counted for more than the mood bonus. *Rooftop Lights* is labeled "indie pop," and the computer doesn't know that's close to "pop."
- **Typing "Pop" instead of "pop" broke the results.** The computer treats them as completely different words, so the user lost every genre and mood bonus.
- **The only metal song disappeared for the metal fan.** After the weight change, Peaceful Metalhead got no metal at all, because energy now matters more than genre.

### Comparing pairs of profiles

- **High-Energy Pop vs. Chill Lofi:** The two lists share no songs. Pop gets loud, fast songs (all energy 0.76+), while Lofi gets quiet, slow study music (*Library Rain*, *Midnight Coding*). This makes sense: they asked for opposite energy levels, and energy is the biggest factor.
- **Chill Lofi vs. Deep Intense Rock:** Again no overlap. Rock gets songs at 125–160 BPM, Lofi gets songs at 60–90 BPM. This is the clearest proof the system can tell "relaxing" apart from "intense."
- **High-Energy Pop vs. Deep Intense Rock:** These *do* overlap: *Gym Hero* and *Neon Nights* appear in both. Both users want high energy, and those songs are high energy, so they fit either one. The #1 spot still differs (*Sunrise City* vs. *Storm Runner*) because genre and mood break the tie.
- **High-Energy Pop vs. Sad but Hyped:** Same genre and energy, but the "sad" user gets *Gym Hero* at #1 instead of *Sunrise City*. There are no sad songs, so the mood request is ignored. *Gym Hero* wins only because it's slightly less cheerful. The output is "valid" by the math but doesn't really give this person what they asked for.
- **High-Energy Pop vs. Capitalized Pop:** These profiles are identical except for capital letters, yet the results changed a lot. Synthwave and hip hop songs tied with pop songs because no bonuses fired. This shows the system is fragile about how labels are typed.
- **High-Energy Pop vs. Ghost Genre (k-pop):** With no k-pop available, the system fell back on "happy" + energy and picked *Sunrise City* and *Rooftop Lights* (nearly tied). That is a reasonable fallback, close to what a k-pop fan might enjoy.
- **Deep Intense Rock vs. Peaceful Metalhead:** Rock gets loud, intense songs, while the Metalhead gets calm folk, classical, and ambient (*Golden Hour*, *Starlit Dreams*). This shows the system now listens to *how music sounds* over *what it's labeled*. Before the weight change, the loud metal song *Firestorm* ranked #2 for this calm listener.
- **Deep Intense Rock vs. Out of Range:** Both want loud music, but Out of Range scores are very low (most under 2 out of 7) and some parts go negative. Only *Electric Rush* stands out, because it matches the genre and mood. The system doesn't reject impossible inputs; it just quietly gives worse results.

### Tests

The two unit tests in `tests/test_recommender.py` pass (`pytest` from the project root). They check that a pop/happy user gets the pop/happy song first and that explanations are non-empty.

---

## 8. Future Work  

1. **Smarter label matching.** Ignore capital letters, and give partial credit for related genres (e.g. "indie pop" counts as close to "pop"). This would fix the Capitalized Pop and Rooftop Lights problems.
2. **A bigger, more balanced catalog.** Add sad, dark, and medium-energy songs, with several songs per genre, so every type of listener has real matches.
3. **More variety in the top 5.** Limit how often one song (like *Gym Hero*) or one genre can appear. Use the unused features (acousticness, danceability) so the system can tell similar-energy songs apart.

Also worth adding: input checks that reject impossible values (energy above 1, negative tempo), and a warning when no song is a good match.

---

## 9. Personal Reflection  

**Biggest learning moment:** The "Gym Hero" thing. I expected a happy pop fan to get happy songs. Instead an intense gym song kept showing up near the top, just because it was labeled "pop" and was loud. That's when it clicked: the weights *are* the opinions of the system. Change one number and the whole list changes.

**How AI tools helped (and when I had to double-check):** AI was great for speed. It came up with the "trick" profiles, broke down the scores song by song, and applied the weight change in a minute. But I still had to check its work. It said the tests passed, but when I ran `pytest` myself I got an import error it had missed. It had run the tests in a different way. Also, the weight change it suggested fixed one problem but created another: energy started to dominate everything. So "AI says it works" isn't the same as "it works." I had to run things myself and look at the results.

**What surprised me:** How little it takes to feel like a real recommender. It's just adding up a few points: +1 for genre, +1 for mood, plus some "how close is the energy" math. But the Chill Lofi list honestly looked like a real study playlist. It also surprised me how easy it is to break. Typing "Pop" with a capital P wrecked the results.

**What I'd try next:** Add sad and medium-energy songs to the catalog so more people get real matches. Make genre matching smarter, so "indie pop" counts as close to "pop." Stop one song from showing up in every list. It also made me realize that apps like Spotify probably have the same problems at a much bigger scale. If the data is missing something, those users just quietly get worse recommendations.
