# DSC550DataMining_TrumpTweets

The goal of this project is to analyze Tweets from the president. There are no political motives and there are no assumptions made about the president. With that disclaimer, below are some hypothesis questions I’d like to answer.
- Does the president have more tweets before he was president (<201611) or after (>201611)?
- What topic did the president tweet about the most and is this topic consistent over time?
- Are there any correlations between the topic and the time of year?
- Are there any correlations between the topic and the number of retweets and favorites?
  - Retweets – somebody retweets the president’s original tweet
  - Favorites – somebody “favorited” (liked) the president’s original tweet
- Is there a linear trajectory of the frequency of retweets and favorites over time?
- Is it possible to determine if President Trump was President at the time of the tweet, based on the topic itself?

Again, there are no political motives for this analysis. It will simply be interesting to apply several subjects learned form this course to unstructured data. These steps include:
- Loading a csv to data frame.
- Cleaning the text data:
  - Remove punctuation
  - Lower case the text
  - Remove anything after @ and # as it’ll be one word and not overly useful
  - Apply stemming and lemmatization
- Vectorize the text with TF-IDF
- Add the topics back to the data frame
- Check the dimensionality of the data frame
- View the distribution with histograms
- See how the data looks over time (Tweets over time)
- Review correlation, specifically with topics
- Use Parallel coordinates to see the relationship between the features.
- Use a percentile feature selection model to find the most relevant features.
- Transform the data that are right skewed to a logarithmic scale utilizing np.log1p. Print the features before and after to show their descriptive statistics
- Converting categorical data to one hot encoding was completed between steps 7 and 8 where I converted the topics to a binary classifier. 
- Training - Split your data into two sets: Training and Testing.
- Evaluation of prediction of whether a Tweet was made prior to or during Trump's presidency using logistic regression.
  - Metrics for the evaluation: 
  - Confusion Matrix - notice how well the model did with all features included. 
  - Precision, Recall & F1 score - all three scores were very high 93+
  - ROC curve - the curve is nearly perfect in predictions.
- I decided to add an additional classifier to see if I could predict Trump's tweets by topic alone. This method wasn't as accurate, but still showed that the topics could make strong predictions on whether Trump was president or not. The F1 score was .73 and .67 respectively. Which means the topics he Tweets about can help to predict a timeline of his Tweets.
- Per the recommendation of a fellow student, I added Kfolds in my model split, but the results yielded zero false positives or false negatives which makes me think I overfit the model even more than before. So, I reverted back to the original. 
