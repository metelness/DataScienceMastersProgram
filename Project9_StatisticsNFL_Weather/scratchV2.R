setwd("C:\\Users\\adamp\\OneDrive\\Desktop\\a_StatsR\\Final")
df_stadiums <- read.csv('nfl_stadiums.csv')
spreadspoke_scores <- read.csv('spreadspoke_scores.csv')
df_teams <- read.csv('nfl_teams.csv')

library(sqldf)
library(tidyverse)

# pull in stadium data
df_stadiums <- sqldf("SELECT DISTINCT
                        stadium_name
                        ,stadium_weather_type
                        ,stadium_open
                      FROM
                        df_stadiums
                      ")
# remove white space and special characters from stadium names to join further downstream 
df_stadiums$stad_pkey <- str_replace_all(df_stadiums$stadium_name, "[^[:alnum:]]", " ")
df_stadiums$stad_pkey <- gsub("[[:space:]]", "", df_stadiums$stad_pkey)

# designate an SKEY for a unique identifier further downstream
df_main <- sqldf("SELECT 
                    schedule_date||team_home AS SKEY
                    ,schedule_week
                    ,schedule_date
                    ,team_home
                    ,team_away
                    ,spread_favorite
                    ,over_under_line
                    ,team_favorite_id
                    ,score_home
                    ,score_away
                    ,over_under_line
                    ,weather_temperature
                    ,weather_wind_mph
                    ,weather_humidity
                    ,stadium
                  FROM
                    spreadspoke_scores
                  WHERE
                     schedule_season > 1980
                    /*AND lower(schedule_week) NOT IN ('wildcard','division','conference','superbowl')*/
                  ")

# remove white space and special characters from stadium names to join further downstream 
df_main$stad_fkey <- str_replace_all(df_main$stadium, "[^[:alnum:]]", " ")
df_main$stad_fkey <- gsub("[[:space:]]", "", df_main$stad_fkey)

# add a foreign key for the teams table
df_main$fav_fkey <- str_replace_all(df_main$team_favorite_id, "[^[:alnum:]]", " ")
df_main$fav_fkey <- gsub("[[:space:]]", "", df_main$fav_fkey)

# pull in required fields from the team table
df_teams <-  sqldf("SELECT
                      team_id
                      ,team_name
                    FROM 
                      df_teams
                    WHERE 
                      team_division IS NOT NULL AND team_division <> ''
                      AND team_name <> 'San Diego Chargers'
                  ")
# add primary key to the teams table
df_teams$fav_pkey <- str_replace_all(df_teams$team_id, "[^[:alnum:]]", " ")
df_teams$fav_pkey <- gsub("[[:space:]]", "", df_teams$fav_pkey)

#combine all three tables remove dome home games
df_final <- sqldf("SELECT
                      a.*, b.*,c.*
                    FROM 
                      df_main a
                    LEFT JOIN 
                      df_stadiums b ON a.stad_fkey = b.stad_pkey
                    LEFT JOIN
                      df_teams c ON a.fav_fkey= c.fav_pkey
                    where stadium_weather_type <>'dome'
                     ")
# had to remove null divisions further upstream and had to remove San Diego Chargers and keep LA Chargers
checkDups <- sqldf("SELECT
                      COUNT(SKEY) as CNT
                      ,SKEY
                   FROM
                   df_final
                   GROUP BY SKEY
                   HAVING COUNT(SKEY) > 1")

# calculate the actual over under, and identify the winning team, losing team, and their scores
winningTeam <- sqldf(' SELECT
                          a.SKEY
                          ,a.schedule_date
                          ,a.team_home
                          ,a.team_away
                          ,a.spread_favorite
                          ,CASE WHEN winningTeam = favTeam THEN 1 ELSE 0 END AS favWon
                          ,favTeam,winningTeam,winningTeamScore,losingTeamScore
                          ,a.over_under_line
                          ,winningTeamScore + losingTeamScore AS actualOverUnder
                          FROM 
                            df_final a
                          INNER JOIN
                              (SELECT
                                SKEY
                                ,team_home
                                ,schedule_date
                                ,CASE WHEN score_home > score_away THEN team_home 
                                     WHEN score_away > score_home THEN team_away
                                     ELSE "tie" END AS winningTeam
                                ,CASE WHEN score_home > score_away THEN score_home 
                                     WHEN score_away > score_home THEN score_away
                                     ELSE 0 END AS winningTeamScore
                                ,CASE WHEN score_home > score_away THEN score_away 
                                     WHEN score_away > score_home THEN score_home
                                     ELSE 0 END AS losingTeamScore
                                ,over_under_line
                                ,team_name as favTeam
                              FROM 
                                df_final a
                              ) scores ON a.SKEY = scores.SKEY 
                         ')
                    
# create a calculated field to show who won and the final point spread outcome
spreadCorrect1 <- sqldf('
                       SELECT
                        SKEY
                        ,schedule_date
                        ,team_home
                        ,team_away
                        ,favTeam
                        ,winningTeam
                        ,winningTeamScore
                        ,losingTeamScore
                        ,spread_favorite
                        ,actualOverUnder
                        ,over_under_line
                        ,CASE WHEN favWon = 1 THEN losingTeamScore - winningTeamScore 
                            WHEN favWon = 0 THEN  winningTeamScore - losingTeamScore
                            ELSE spread_favorite end as actualSpread
                        ,CASE WHEN favTeam = winningTeam THEN 1 ELSE 0 END AS favTeamWon
                       FROM 
                        winningTeam
                       ')

# create a calculated field to show how off was the Over Under and spread
df_final <- sqldf('SELECT
                        b.*
                        ,a.favTeam
                        ,a.winningTeam
                        ,a.winningTeamScore
                        ,a.losingTeamScore
                        ,a.actualSpread
                        ,CASE WHEN a.actualSpread > 0 THEN 1 ELSE 0
                          END AS upsetInd
                        ,CASE WHEN a.favTeamWon = 1 THEN (abs(a.actualSpread) - abs(a.spread_favorite))/abs(a.spread_favorite)
                              ELSE (abs(a.actualSpread) - (a.spread_favorite))/(a.spread_favorite)
                               END*100 prcntSprdOff
                        ,a.actualOverUnder
                        ,((abs(a.actualOverUnder) - abs(a.over_under_line))/abs(a.over_under_line))*100 as  prcntOvrUndrOff
                       FROM 
                        spreadCorrect1 a
                      INNER JOIN df_final b ON a.SKEY = b.SKEY
                       ')
# caclulate the respective z scores
df_final$zSprdOff <- (df_final$prcntSprdOff-mean(df_final$prcntSprdOff, na.rm=TRUE))/sd(df_final$prcntSprdOff, na.rm=TRUE)
df_final$zOvrUndOff <- (df_final$prcntOvrUndrOff-mean(df_final$prcntOvrUndrOff, na.rm=TRUE))/sd(df_final$prcntOvrUndrOff, na.rm=TRUE)

# bring in some weather variables to indicate the severity of the weather
# cold season is defined as any games played in the last three weeks of the regular season
# cold severity is binned accordingly
# z score outliers are named
df_final <- sqldf("SELECT DISTINCT 
                    1 as ind
                    ,1 as ind2
                    ,a.*
                    ,CASE WHEN schedule_week < 14 THEN 0 ELSE 1 END AS coldSeason  
                    ,CASE WHEN weather_temperature > 20 and weather_temperature <= 32 THEN 'coldLVL1'
                          WHEN weather_temperature > 10 and weather_temperature < 20  THEN 'coldLVL2'
                          WHEN weather_temperature <= 10 THEN 'coldLVL3'
                          ELSE 'coldLVL0'
                              END AS coldDayLvl
                    ,CASE WHEN favTeam = winningTeam THEN 1 ELSE 0 END AS favTeamWon
                    ,CASE WHEN team_home = winningTeam THEN 1 ELSE 0 END AS homeTeamWon
                    ,CASE WHEN abs(zSprdOff) >= 1.96 THEN 1 ELSE 0 END AS zSprdOffIndicator
                    ,CASE WHEN abs(zOvrUndOff) >= 1.96 THEN 1 ELSE 0 END AS zOvrUndOffIndicator
                  FROM
                    df_final a
                   ")
# view a distribution of how off the spread and over under were
ggplot(df_final, aes(prcntSprdOff)) + 
  geom_histogram(aes(y = ..density..), colour = "red", fill = "red", alpha = 0.75,binwidth = 3 ) + 
  ggtitle("NFL seasons 1980 - 2017 How Off was the Spread?") +
  labs(x = "% spread was off dist", y = "Density") + 
  stat_function(fun = dnorm, args = 
                  list(mean = mean(df_final$prcntSprdOff), sd = 
                         sd(df_final$prcntSprdOff)),colour = "black", size = 2)

ggplot(df_final, aes(prcntOvrUndrOff)) + 
  geom_histogram(aes(y = ..density..), colour = "red", fill = "red", alpha = 0.75,binwidth = 3 ) + 
  ggtitle("NFL seasons 1980 - 2017 How Off was the Over/Under?") +
  labs(x = "% Over/Under was off dist", y = "Density") + 
  stat_function(fun = dnorm, args = 
                  list(mean = mean(df_final$prcntOvrUndrOff), sd = 
                         sd(df_final$prcntOvrUndrOff)),colour = "black", size = 2)

# remove NA values
df_final <- na.omit(df_final)

# pivot the categorical variables
df_final <- df_final %>% spread(stadium_weather_type, 1)
df_final <- df_final %>% spread(coldDayLvl, 1)

# replace the NA's in the new columns with 0's
df_final[is.na(df_final)] <- 0

df_coldTeam2 <- sqldf("
                    SELECT
                      team_home
                      ,count(SKEY) as gamesPlayed
                      ,sum(coldLvl1)AS sumCold1 
                      ,sum(coldLvl2)AS sumCold2
                      ,sum(coldLvl3)AS sumCold3
                    FROM 
                      df_final
                    WHERE coldSeason = 1
                    GROUP BY 1")


# cold teams are teams that have more cold level 1,2,3 games above the average in any category 
# played more than a single season
df_coldTeam1 <- sqldf("
                  SELECT DISTINCT 
                    team_home as coldTeamName
                    ,1 as coldTeamInd
                  FROM
                    df_coldTeam2 a
                  ,(
                    SELECT 
                      avg(sumCold1) AS avgCold1 
                      ,avg(sumCold2) AS avgCold2
                      ,avg(sumCold3) AS avgCold3
                    FROM 
                      df_coldTeam2
                    ) c1
                    WHERE CASE WHEN sumCold1 > avgCold1 or sumCold2 > avgCold2 or sumCold3 > avgCold3 THEN 1 ELSE 0
                      END = 1 and gamesPlayed > 20 
                   ")


# indicator for the cold teams
df_final <- sqldf("
                  SELECT 
                    a.*
                    ,CASE WHEN coldTeamInd is null then 0 else 1 END as coldTeamHomeInd
                  FROM  
                    df_final a 
                  left join 
                    df_coldTeam1 b on b.coldTeamName = a.team_home
                  ")
# indicator for the warm teams 
df_warmTeams <- sqldf("
                    
                    SELECT DISTINCT 
                      team_home as warmTeamName
                      ,1 as warmTeamInd
                    FROM 
                      df_final
                    WHERE team_home not in (SELECT DISTINCT coldTeamName FROM df_coldTeam1)
                  ")
# combine the two
df_final <- sqldf("
                  SELECT 
                    a.*
                    ,CASE WHEN warmTeamInd is null then 0 else 1 END as warmTeamAwayInd
                  FROM  
                    df_final a 
                  left join 
                    df_warmTeams b on warmTeamName = a.team_away
                  ")

# Calculate the windchill
df_final$windChill <- 35.74 + .6251 * df_final$weather_temperature - 
  35.75 * df_final$weather_wind_mph^.16 + .4275 * 
  df_final$weather_temperature * df_final$weather_wind_mph^.16

df_final <- sqldf("SELECT 
                    1 as Kind
                    ,SKEY
                    ,schedule_week
                    ,schedule_date
                    ,team_home
                    ,team_away
                    ,team_favorite_id
                    ,favTeam
                    ,favTeamWon
                    ,winningTeam
                    ,homeTeamWon
                    ,coldSeason
                    ,coldLVL0
                    ,coldLVL1
                    ,coldLVL2
                    ,coldLVL3
                    ,coldTeamHomeInd
                    ,warmTeamAwayInd
                    ,cold
                    ,moderate
                    ,warm
                    ,zSprdOffIndicator
                    ,zOvrUndOffIndicator
                    ,score_home
                    ,score_away
                    ,stadium_open
                    ,winningTeamScore
                    ,losingTeamScore
                    ,over_under_line
                    ,actualOverUnder
                    ,spread_favorite
                    ,actualSpread
                    ,weather_temperature
                    ,weather_wind_mph
                    ,windChill
                    ,weather_humidity
                    ,prcntSprdOff
                    ,prcntOvrUndrOff
                  FROM 
                    df_final
                
                  ")

# k-means cluster variables based on weather patterns
set.seed(123)
weatherK <- df_final[,33:34]
library(cluster)    # clustering algorithms
library(factoextra) # clustering algorithms & visualization
weatherK <- na.omit(weatherK)
# convert all the columns to numeric
weatherK <- sapply( weatherK, as.numeric)
weatherK <- scale(weatherK)
weatherK <- data.frame(weatherK)

k2 <- kmeans(weatherK, centers = 3, nstart = 25)
# plot
fviz_cluster(k2, geom = "point", data = weatherK) + ggtitle("k = 2")

# find the optimal number of clusters for the K-means cluster algorithm above
fviz_nbclust(weatherK, kmeans, method = "wss")
fviz_nbclust(weatherK, kmeans, method = "silhouette")
# add the clusters to the data frame
df_final$cluster <- k2$cluster

# split apart clusters into separate columns
df_final <- df_final %>% spread(cluster, 1)

# replace the NA's in the new columns with 0's
df_final[is.na(df_final)] <- 0
df_final$cluster <- k2$cluster
#convert to numeric 
df_final$`1` <- sapply(df_final$`1`, as.numeric)
df_final$`2` <- sapply(df_final$`2`, as.numeric)
df_final$`3` <- sapply(df_final$`3`, as.numeric)


# plot shows a somewhat linear relationship to the spread being off related to weather_temps
scatter <- df_final[,33:37]
scatter <- na.omit(scatter)
# convert all the columns to numeric
scatter <- sapply( scatter, as.numeric)
scatter <- scale(scatter)
scatter <- data.frame(scatter)
pairs(scatter, pch = 19)
# after viewing the scater plot, there appears to be some linearity between the variables 
#   in their current state

ggplot(df_final, aes(weather_temperature)) + 
  geom_histogram(aes(y = ..density..), colour = "white", fill = "royalblue4", alpha = 0.75,binwidth = 3 ) + 
  ggtitle("Spread Outliers Temp ALL") +
  labs(x = "Temprature", y = "Density") + 
  stat_function(fun = dnorm, args = 
                  list(mean = mean(df_final$weather_temperature), sd = 
                         sd(df_final$weather_temperature)),colour = "black", size = 2)

# there are teams with very hot game days and cold game days in the last weeks of the season
#   as illuastrated by the histogram density plot. Also, the data are left skewed with some heavy outliers

# controlling for instances where there are total outliers in either the spread or over/under and 
#   controlling for teams that are from warm climates
#   and adding an indicator for games that were played in cold weather
# we get a potential correlation and statisitical significance of R^2 related to the two dependant variables
upper.panel <- function(x, y){
  points(x,y, pch = 19, col=c("red", "green3","blue")[df_final$cluster])
  r <- round(cor(x, y), digits = 2)
  txt <- paste0("R = ", r)
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(0, 1, 0, 1))
  text(0.5, 0.9, txt)
}
pairs(df_final[,32:37], lower.panel = NULL, 
      upper.panel = upper.panel)
pairs(df_final[,32:37], lower.panel = NULL, 
      upper.panel = upper.panel)

# multi linear regression
lm.spread <- lm(prcntSprdOff ~ weather_wind_mph  + windChill, data = df_final, na.action = na.exclude)
summary(lm.spread)

lm.overunder <- lm(prcntOvrUndrOff ~ weather_wind_mph  + windChill, data = df_final, na.action = na.exclude)
summary(lm.overunder)

ggplot(data = df_final, mapping=aes(x = weather_wind_mph, y = prcntOvrUndrOff)) + 
  geom_point(aes(color = cluster)) + geom_smooth(aes(group = 1), method = "lm", se = FALSE, linetype = 2) +
  geom_jitter()

ggplot(data = df_final, mapping=aes(x = windChill, y = prcntSprdOff)) + 
  geom_point(aes(color = cluster)) + geom_smooth(aes(group = 1), method = "lm", se = FALSE, linetype = 2) +
  geom_jitter()

# While there is a linear relationship, and the weather variables are a factor in the model's prediction according
  # the p-value's significance, the overall R^2 is minimal .005, which means .5% of the variance in the 
  # over/under score is a result of the weather variables Windchill and weather_wind_mph. Even less is the spread 
  # where .1% of the variance is explained bu the weather variables. 
# produce logistic regression of coldTeamUpset related with only weather factors

Train <- createDataPartition(df_final$homeTeamWon, p = 0.8, list = FALSE)
training <- df_final[ Train, ]
testing <- df_final[ -Train, ]

homeTeamWon <- glm(formula = training$homeTeamWon ~ training$windChill
                     , family = binomial(), data = training)
summary(homeTeamWon)
res <- predict(homeTeamWon, testing, type = "response")
res <- predict(homeTeamWon, training, type = "response")

confmatrix <- table(Actual_Value = training$homeTeamWon, Predicted_Value = res > .5)
confmatrix


roc_obj <- roc(training$homeTeamWon, res)
auc(roc_obj)
TPR = rev(roc_obj$sensitivities)
FPR = rev(1 - roc_obj$specificities)
labels = roc_obj$homeTeamWon
scores = roc_obj$res

plot(roc(training$homeTeamWon, res, direction = "<"), print.auc = TRUE,
     col = "red", lwd = 3, main = "ROC for Home Team Winning")

#### Z - score predictions
Train <- createDataPartition(df_final$zOvrUndOffIndicator, p = 0.8, list = FALSE)
training <- df_final[ Train, ]
testing <- df_final[ -Train, ]

z.zOvrUndOffIndicator <- glm(formula = training$zOvrUndOffIndicator ~ training$windChill
                   , family = binomial(), data = training)
summary(z.zOvrUndOffIndicator)
res <- predict(z.zOvrUndOffIndicator, testing, type = "response")
res <- predict(z.zOvrUndOffIndicator, training, type = "response")

confmatrix <- table(Actual_Value = training$zOvrUndOffIndicator, Predicted_Value = res > .5)
confmatrix


roc_obj <- roc(training$zOvrUndOffIndicator, res)
auc(roc_obj)
TPR = rev(roc_obj$sensitivities)
FPR = rev(1 - roc_obj$specificities)
labels = roc_obj$zOvrUndOffIndicator
scores = roc_obj$res

plot(roc(training$zOvrUndOffIndicator, res, direction = "<"), print.auc = TRUE,
     col = "red", lwd = 3, main = "ROC for Home Team Winning")



Train <- createDataPartition(df_final$zSprdOffIndicator, p = 0.8, list = FALSE)
training <- df_final[ Train, ]
testing <- df_final[ -Train, ]

z.zSprdOffIndicator <- glm(formula = training$zSprdOffIndicator ~ training$windChill
                             , family = binomial(), data = training)
summary(z.zSprdOffIndicator)
res <- predict(z.zSprdOffIndicator, testing, type = "response")
res <- predict(z.zSprdOffIndicator, training, type = "response")

confmatrix <- table(Actual_Value = training$zOvrUndOffIndicator, Predicted_Value = res > .5)
confmatrix


roc_obj <- roc(training$zSprdOffIndicator, res)
auc(roc_obj)
TPR = rev(roc_obj$sensitivities)
FPR = rev(1 - roc_obj$specificities)
labels = roc_obj$zSprdOffIndicator
scores = roc_obj$res

plot(roc(training$zSprdOffIndicator, res, direction = "<"), print.auc = TRUE,
     col = "red", lwd = 3, main = "ROC for Home Team Winning")