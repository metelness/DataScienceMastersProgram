# Analysis of my Spotify Listening Habits

This was a fun project. The purpose was to extract data that wasn't preestablished (i.e. Kaggle).

I went to Spotify’s developer website to obtain and access token so I could obtain data through their API. 

I established metrics I wanted to wrangle based on the documentation provided by Spotify. I was able to establish my own metadata based on Spotify’s documentation to the variables I would produce in my dataset. 

I had to iterate over the playlists and then within that iteration, applied an additional iteration over the tracks. This will make future pulls significantly easier and optimal for frequent use, as the key values are already parsed and ready for extraction. 

Finally, I came away with two tables, one with my playlist data and basic data on the tracks and the other containing the audio analysis for each track.

The exploratory analysis was conducted for my own knowledge. I simply wanted to see the distribution of some of the variables within my dataset. 
