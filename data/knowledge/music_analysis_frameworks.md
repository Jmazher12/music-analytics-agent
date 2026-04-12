# Music Analysis Frameworks

## Analyzing Track Popularity

### Key Factors
Popularity on Spotify correlates with several audio features. Research and analysis have shown:
- Danceability and energy have a moderate positive correlation with popularity
- Extremely high or low instrumentalness tends to correlate with lower popularity
- Explicit tracks sometimes have slightly higher popularity in genres like hip-hop and pop
- Duration extremes (very short or very long tracks) tend to be less popular
- Acousticness has a slight negative correlation with popularity in most modern genres

### Approach
When analyzing what makes tracks popular, consider:
1. Compare audio features of top tracks (popularity > 80) vs. average tracks within the same genre
2. Look at feature distributions rather than single values
3. Consider that popularity is time-dependent and reflects recent listening trends
4. Genre context matters — a "high energy" jazz track differs from a "high energy" metal track

## Comparing Genres

### Feature Profiles
Each genre has a characteristic "fingerprint" of audio features. To compare genres:
1. Calculate mean and standard deviation of each feature per genre
2. Identify the features with the largest differences between genres
3. Use normalized values to compare features on different scales
4. Consider overlap — many genres share similar feature ranges

### Useful Comparisons
- Energy vs. Valence: Maps the emotional landscape of genres (high energy + high valence = happy/party music, high energy + low valence = angry/intense music)
- Danceability vs. Tempo: Shows rhythmic character (some genres are danceable at low tempos, others need high tempos)
- Acousticness vs. Instrumentalness: Distinguishes production style and vocal presence
- Speechiness vs. Energy: Separates rap/spoken word from sung and instrumental genres

## Trend Analysis

### Cross-Genre Patterns
- The "loudness war": tracks have generally gotten louder over time
- Duration has been decreasing in recent years, possibly due to streaming economics
- Danceability and energy have trended upward in mainstream music
- Genre boundaries are increasingly blurred, with more hybrid styles

### Artist Analysis
When analyzing artists:
1. Look at their feature consistency across tracks (some artists have very consistent sound profiles)
2. Compare their features to genre averages to understand what makes them distinctive
3. Track how their sound has evolved across releases
4. Consider collaboration effects — features may shift when artists collaborate

## Statistical Approaches

### Descriptive Statistics
- Mean, median, and mode of audio features per genre or artist
- Standard deviation to measure consistency/variety
- Min/max to identify outliers or extremes
- Percentiles to understand distributions

### Comparative Analysis
- Group by genre, artist, or popularity tier and compare distributions
- Use ranking and sorting to find top/bottom tracks by any feature
- Cross-tabulation of categorical variables (genre, key, mode, time signature)
- Correlation analysis between features to find relationships

### Common SQL Patterns for Music Analysis
- GROUP BY track_genre with aggregate functions (AVG, COUNT, MIN, MAX)
- WHERE clauses to filter by popularity, genre, or feature ranges
- ORDER BY to rank tracks or genres
- HAVING to filter groups (e.g., genres with more than N tracks)
- Subqueries to compare individual tracks against genre averages