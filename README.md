# IDAI202-2505445--Snigdha_Reddy_Guduru

# ⚽ Pitchside: Football Injury and Team Performance Dashboard

**A data-driven exploration of player injuries, recovery, and football team performance.**



<img width="1440" height="900" alt="Screenshot 2026-10-27 at 11 43 59 AM" src="https://github.com/user-attachments/assets/984e3f9d-b642-437c-a4b6-46e6f003529d" />
<img width="1440" height="900" alt="Screenshot 2026-10-27 at 11 44 06 AM" src="https://github.com/user-attachments/assets/ff2489d2-2388-4593-aaeb-1e51ed4ac86a" />
<img width="1440" height="900" alt="Screenshot 2026-10-27 at 11 44 16 AM" src="https://github.com/user-attachments/assets/882f6bbc-cc4b-4ce5-b8d5-d96e8b8422d4" />
<img width="1440" height="900" alt="Screenshot 2026-10-27 at 11 44 23 AM" src="https://github.com/user-attachments/assets/23b5ab24-e449-435f-af82-b9285437044a" />
<img width="1440" height="900" alt="Screenshot 2026-10-27 at 11 44 30 AM" src="https://github.com/user-attachments/assets/33f4e7e6-f8df-4139-8925-d68752b86af7" />
<img width="1440" height="900" alt="Screenshot 2026-10-27 at 11 44 38 AM" src="https://github.com/user-attachments/assets/5a98bbdb-e757-4b6b-ab94-40cd06ea6fd0" />


**Live Dashboard:** [Add your Streamlit app link here]https://idai202-2505445--snigdhareddyguduru-mdyyd9woif8txdq7hca7ni.streamlit.app/Data_Lab

**GitHub Repository:** [View the project](https://github.com/snigdhareddyguduru/IDAI202-2505445--Snigdha_Reddy_Guduru)


## 1. Introduction

Football is often discussed in terms of goals, wins, losses and individual performances. However, one factor that can affect all of these is player availability. An injury can keep a player away from matches for days or even months, and their absence may influence the way a team performs. At the same time, returning from an injury does not necessarily mean that a player immediately returns to their previous level of performance.

This made me curious about how much information we could actually extract from football injury data. Instead of looking at injuries as isolated incidents, I wanted to explore them alongside player ratings, recovery durations and team results.

This led me to develop **Pitchside**, an interactive dashboard that uses Python and data visualisation to explore injury patterns and their possible relationship with player and team performance. The project was developed as part of my CRS Artificial Intelligence coursework for Mathematics for AI-II.

## 2. Problem Statement

Football injury data can contain useful information, but looking at hundreds of records individually makes it difficult to recognise patterns. It is not immediately obvious which clubs experience more recorded injuries, which injury types occur most frequently, how player ratings change after an injury, or whether team goal differences change while a player is absent.

The problem I wanted to address was how to turn this information into something easier to explore and understand. I therefore set out to build a dashboard where users could move beyond individual records and investigate broader patterns through interactive charts, comparisons and filters.

The aim was not to prove that injuries directly cause a team to lose matches. Instead, I wanted to see what the available data could tell us, where interesting patterns appeared, and where the data was not sufficient to draw firm conclusions.

## 3. Research Questions

Before analysing the dataset, I identified the questions I wanted Pitchside to investigate:

1. Which players and clubs have the highest number of recorded injuries in the dataset?
2. Which injury types appear most frequently, and how does injury frequency vary across months and clubs?
3. How do recorded player ratings differ before and after an injury?
4. What patterns can be observed between injury duration and changes in player ratings after returning?
5. How does the team's average goal difference during a player's absence compare with its average goal difference before the injury?
6. Is there any observable relationship between a player's age and the team performance-drop index associated with their absence?

These questions guided my data cleaning, feature engineering, analysis and the visualisations I included in the dashboard.

## 4. The Dataset

I worked with a football injury dataset containing **656 records and 42 original columns**. The dataset included player names, clubs, positions, ages, FIFA ratings, injury information, injury and return dates, player ratings from selected matches, and team goal differences before and during player absences.

I loaded the source data into Python using Pandas and used it as the starting point for my analysis. I then created additional variables from the existing columns so that I could investigate questions that were not directly answered by the raw data.

The dataset was useful because it brought player-level and team-level information together. However, some records were incomplete, and the available match information was limited to the matches recorded around each injury. This affected which comparisons could be made reliably.

## 5. How I Approached the Project

### Data cleaning

The first challenge was making the dataset suitable for analysis. Some missing values were represented by the text `N.A.`, while other fields were already empty. I standardised these missing values and converted the injury and return dates into datetime format. I also converted relevant rating and goal-difference columns into numeric values so that they could be used in calculations and charts.

I then calculated injury duration by finding the difference between the return date and injury date. When a record produced a negative duration, I treated the duration as missing because it was not a valid recovery period. I also noticed a few unusually long durations. Rather than automatically removing them, I retained them for consideration because unusual values are not necessarily incorrect values.

Missing information remained an important part of the project. I chose not to replace every missing value with an estimated one, since doing so could introduce information that was not actually present in the dataset.

### Feature engineering

Cleaning the data was only one part of the process. I also needed to create variables that would help answer my research questions.

I calculated the average player rating across the available recorded matches before an injury and after the player's return. By subtracting the pre-injury average from the post-injury average, I created a **Rating Change** variable. Positive values indicate an increase in the recorded average rating, while negative values indicate a decrease.

For team performance, I calculated the average goal difference before the injury and during the player's absence. I then created the **Team Performance Drop Index**, defined as:

`Average GD Before Injury − Average GD During Absence`

A positive value indicates that the team's average goal difference was lower during the player's absence than before the injury. A negative value indicates that it was higher during the absence.

These calculations allowed me to investigate player and team performance using the same dataset. However, the index is a descriptive comparison, not proof that the absent player caused the difference.

### Exploratory data analysis

Once the additional variables were ready, I used Pandas operations such as `groupby()`, aggregation and `pivot_table()` to compare injury records across players, clubs, injury types and months.

I examined which players and clubs had the most recorded injuries, which injury types appeared most often, and which records had the largest positive Team Performance Drop Index. I also explored rating changes after injuries, recovery durations and differences in team goal difference.

The analysis was iterative. Some comparisons produced useful patterns, while others required more caution because of missing values or the limited number of observations available for certain calculations.

## 6. Building the Dashboard

After completing the initial analysis in Python, I developed Pitchside using Streamlit. I wanted the dashboard to be more than a collection of charts, so I separated it into pages based on the different questions a user might want to investigate.

**Overview** brings the main dataset statistics and key comparisons together in one place. **Player Explorer** allows users to select players and examine their available injury records, ratings and recovery information. **Injury Analysis** focuses on injury frequency, monthly patterns and recovery durations. **Team Performance** explores goal differences before injuries and during player absences. Finally, **Data Lab** allows users to search, filter, sort and inspect the underlying records.

I used Plotly to create interactive visualisations and designed the interface around a dark football-analytics theme with emerald accents. I also separated the code into different files for the application, individual dashboard pages, data loading, analytical functions and styling. This made the project easier to organise and maintain as the dashboard grew.

The final application includes a club injury comparison, injury-type charts, a monthly injury heatmap, a player-rating timeline, an age-versus-performance-drop scatter plot, a comeback leaderboard and additional views for recovery and team performance.

## 7. What I Found

One of the first patterns I noticed was that injury records were not distributed equally across clubs. Newcastle had the highest number of recorded injury entries in this dataset, with 120, followed by Everton with 103 and Manchester United with 101. These figures describe the records available in this dataset; they should not be interpreted as definitive rankings of injury risk across clubs.

Hamstring injuries were the most frequently recorded injury type, appearing 95 times. Knee injuries appeared 57 times and ankle injuries 52 times. This gave me a clearer picture of which injury categories were most common in the data.

I also found that the relationship between injury duration and rating change was almost zero in a simple correlation analysis. The Pearson correlation was approximately **0.01**, based on 364 records with both values available. In other words, the dataset did not show a meaningful linear relationship between the length of an injury and the change in average player rating after returning. This does not mean recovery time is unimportant; it means that injury duration alone did not explain rating changes in this particular analysis.

The Team Performance Drop Index also varied considerably between injury records. Some records showed a lower average goal difference during the player's absence, while others showed an improvement. This reinforced the importance of looking at individual records and avoiding the assumption that every injury has the same effect on a team.

Overall, I found that the dataset was useful for identifying patterns, but the results were more complicated than a simple conclusion that longer injuries always lead to worse performance.

## 8. Conclusion

Building Pitchside helped me explore how data analysis can be used to investigate a real-world problem in football. By cleaning the dataset, creating new variables and comparing player ratings with team goal differences, I was able to turn individual injury records into a more accessible set of insights.

One of the most important findings was that the relationship between injuries and performance cannot be reduced to a single measure. A player may return with a higher or lower rating, and a team's results may improve or decline during that player's absence. These outcomes depend on more than the injury alone, and the patterns in this dataset do not establish cause and effect.

The project also showed me why data visualisation matters. A table of hundreds of records can be difficult to interpret, whereas interactive charts make it easier to compare clubs, investigate individual players and identify patterns worth exploring further.

## 9. Limitations

The biggest limitation was the quality and completeness of the available data. Some injury dates, return dates and player ratings were missing, which meant that not every record could be used in every analysis. The number of valid observations therefore differed between calculations.

The dataset also contained only a limited number of recorded matches before and after injuries. Three available ratings on either side of an injury cannot fully represent a player's long-term performance, and a change in rating may reflect factors other than recovery.

Similarly, the Team Performance Drop Index compares average goal differences across two recorded periods. It does not control for opposition strength, home and away matches, tactics, other unavailable players or changes in team selection. It should therefore be treated as an indicator for further investigation rather than a direct measurement of an injury's causal impact.

Finally, the dataset's coverage may not be equally representative of every club, player or injury. The observed counts cannot automatically be generalised to all professional football.

## 10. What I Would Improve Next

If I continued working on Pitchside, I would try to obtain a larger dataset containing more seasons, more matches and more detailed injury information. I would also include variables such as minutes played, match location, opposition strength, player position and team results across a longer period.

With more complete data, I could investigate whether performance changes persist over time instead of relying only on a few recorded matches. I would also explore statistical methods that account for other factors influencing team results, and compare players who missed matches with suitable comparison periods where possible.

Another improvement would be to add clearer data-quality indicators within the dashboard, so users could see how many records support each chart. This would make the findings easier to interpret and help users understand the uncertainty behind the comparisons.

## 11. Personal Reflection

When I started this project, I thought most of the work would be about analysing the dataset and creating graphs. I soon realised that getting the data into a form I could actually use was a major part of the process. Missing values, inconsistent entries and date problems meant that I had to check my assumptions before moving on to the analysis.

Building the dashboard was another learning experience. I had to organise the code across multiple files, make the different pages work together and deal with errors that did not always have an obvious solution. Deploying the application also required me to understand how the local project, GitHub repository, dependencies and hosting platform connected with one another.

What I found most useful was seeing how a calculation could become something a user could interact with and interpret. At the same time, I learnt that a chart can make a pattern look convincing without necessarily explaining why it exists. Understanding the limitations of the data was just as important as producing the visualisations.

If I were to do the project again, I would spend more time planning the data-quality checks and defining exactly what each performance measure could and could not tell me before building the dashboard. Overall, Pitchside gave me practical experience with the full process, from preparing a dataset and analysing it to developing and deploying an interactive application.

## 12. Project Information

**Project:** Pitchside — Football Injury and Team Performance Dashboard  
**Course:** Mathematics for AI-II  
**Programme:** Career-related Studies (CRS), Artificial Intelligence  
**Assessment:** Summative Assessment — Developing User-Centred Dashboards to Solve Real-World Problems  
**Student:** Snigdha Reddy Guduru  
**School:** Udgam School for Children

## Technologies Used

Python · Pandas · Streamlit · Plotly · Matplotlib · Seaborn · Git · GitHub · Streamlit Community Cloud
