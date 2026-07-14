# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

FireSimulator 1.0 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

FireSimulator 1.0 recommends songs based on a listener’s preferences. It tries to find songs that match the user’s genre, mood, energy level, and acoustic preference. It then ranks the songs from strongest to weakest match.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The model gives every song a score. Songs receive points when their genre and mood match the user's preferences. Songs also receive points when their energy and  acousticness are close to what the user want. Valance is used as a small purposeful tie breaker. The system also awards points for popularity and release year (direction-aware, so a user can ask for mainstream/recent or niche/classic songs), for overlap between the user's favorite mood tags and a song's mood tags, and for exact matches on preferred listening activity (e.g. studying, partying) and song structure (e.g. verse-chorus, storytelling). The system sorts the songs by score and returns the highest ranked options.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The dataset contains 20 songs. The genres that are represented are pop, lofi, rock, afrobeats, hip-hop and trap.I added 10 more songs and also added more categories to rate songs such as speechiness and explicit. There are parts of musical taste missing in the dataset such as lyrical depth.
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The model gives reasonable results when the user's preferences such as people who listen to pop, hip-hop, and lofi are represented well in the data set. Happy pop users usually receive energetic pop songs. Chill lofi users usually receive calmer songs such as Midnight Coding and Library Rain. Happy hip-hop usually receive matching songs such as Headlines. The scoring system also gives partial credit when energy and acousticness are lcose instead of requiring an exact match.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One weakness I discovered is that the recommender relies on exact matches for genre and mood. During testing, small differences such as capitalization or extra spaces caused valid preferences to receive no matching points. The small and uneven dataset also gives users who prefer less-represented genres fewer strong recommendations. As a result, the system may favor popular genres and fail to recognize songs that still fit the user’s overall taste.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested the recommender with several different user profiles. These included a Happy Pop listener, a listener who wanted sad pop with high energy, a listener who wanted intense rock that was also acoustic, and a Chill Lofi listener. I also tested edge cases, including energy values outside the normal 0.0 to 1.0 range, genres and moods that were not in the catalog, preferences with different capitalization or extra spaces, and a profile with a missing acoustic preference.

Happy Pop Compared with High-Energy Sad Pop
Happy Pop ranked Sunrise City first because it matched the genre, mood, and energy target. High-Energy Sad Pop ranked Gym Hero first because its pop genre and high energy outweighed its mood mismatch.

Happy Pop Compared with Intense Acoustic Rock
Happy Pop favored energetic pop songs such as Sunrise City and Gym Hero. Intense Acoustic Rock ranked Storm Runner first because it matched rock, intense, and high energy, even though it was not very acoustic.

High-Energy Sad Pop Compared with Intense Acoustic Rock
Gym Hero performed well for High-Energy Sad Pop because it matched pop and high energy. Storm Runner ranked higher for Intense Acoustic Rock because it matched both the requested genre and mood.

Very High Energy Compared with Negative Energy
Both invalid energy profiles still ranked Sunrise City first because its genre and mood matches remained strong. This showed that the system does not properly validate energy values outside the 0.0 to 1.0 range.

Missing Categories Compared with Formatting Errors
The opera and furious profile received weak matches because those categories were absent from the dataset. The formatting profile also lost matching points because capitalization and extra spaces prevented exact genre and mood matches.

Chill Lofi Compared with Happy Pop
Chill Lofi favored calmer songs such as Midnight Coding and Library Rain. Happy Pop preferred higher-energy tracks because its genre, mood, and energy targets were different.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would clean user inputs by removing extra spaces and ignoring capitalization. I wwould add more songs from different genres, moods, cultures, and artists. I would also validate energy values and include features such as tempo, danceability, listening history, and user feedback.
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned that recommender systems turn user preferences into scores that can be used to rank items. I also learned that small choices in feature weights can greatly change the final recommendations. The most surprising result was that a song could rank highly even when it did not match the requested mood. This project showed me how bias can appear when a dataset is small or uneven.
