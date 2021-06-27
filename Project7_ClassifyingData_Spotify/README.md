# ClassifyingData using Spotify's API on the band Alcest

This program classifies text in a variety of ways using data from Spotify's API on the artist Alcest. 

The project was supposed to meet the following criteria:
- Display the same analysis using 3 different charts (ex. A bar chart, a line chart and a pie chart)
- Use appropriate, complete, professional labeling
- Rank your charts from most effective to least effective.

Summary of findings: 
The data utilized for the bar, line, and pie charts is from the artist Alcest and is an average of song metrics by album. The data used for the scatter plot is at the song level and is not averaged. Metrics are defined and derived by Spotify.

The pie chart displays the percentage of each album’s position on the pie chart. It doesn't offer any real context to what the data means. For example, is the chart indicating that Kodama has 16.3% beats per minute? The data here is better represented in its raw form. This is the least productive chart to represent this data.

The bar chart displays the data in a much more appealing way. However, the visual seems to indicate a ranking rather than a disparity over time. Bar charts are great for displaying stack rankings, but with this dataset, it appears to be a performance-based measure rather than progression over time. This is the second least productive chart to represent this data.

The line graph displays some interesting findings about the progression of the musical styles of Alcest over the years and is the preferred measurement for this metric. It shows the progression of slower paced (lower beats per minute) on their early albums, to a sharp spike in beats per minute on their third release, and then falls back under an average of 120 beats per minute for their latter two releases. This is the second most productive chart to represent this data.

Finally, a fourth chart was displayed to visualize the correlation between variables. This chart shows the valence, which “measures musical positiveness conveyed by a track”, compared to the energy, which represents a “perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.” This dataset uses data at a more granular level (song level) to include more datapoints. There appears to be a linear correlation to the valence (positiveness) of a song and the amount energy in a song. Which makes logical sense as low energy songs would tend to be less dynamic in sound range, lower tempo, and lower perceived loudness.  This is the least most productive chart to represent this data.
