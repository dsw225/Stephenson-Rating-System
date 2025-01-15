# Stephenson Rating System Python Implementation

This python library implements the Stephenson rating system for estimating the relative skill level of players in two-player games such as chess. It extends the Glicko method by including a second parameter controlling player deviation across time, a bonus parameter, and a neighbourhood parameter.

This idea stemmed from reading a paper from Mark Glickman comparing Elo, Glicko, Glicko-2 and the Stephenson model in [competitive womens beach volleyball found here](http://www.glicko.net/research/volleyball-FINAL.pdf), in which the Stephenson Model has a lower misclassification rate than the other models. However, when I went to use it on my own project (in which I'm currently testing a Glicko-2 Modified System based off of this repository), I couldn't find any python implementation, so I decided to create my own.

Compared to the [R implentation by Alec Stephenson and Jeff Sonas found here,](https://cran.r-project.org/web/packages/PlayerRatings/index.html) there are a few slight differences. My specific application of this rating system doesn't have an average period between games, so I adjusted the t factor which is usually the number of periods since the player last competed. However in this implementation the t factor is a ratio of (days since last competed) / (time period). While this is different it allows for an easier application of irregular playing rates. Beyond that this application differs as it only computes individual ratings and scores and does not have any methods to parse an entire dataset, however one could do so easily as shown in the test files.

In the docs you can find [ChessRatings.pdf](https://github.com/dsw225/Stephenson-Rating-System/blob/main/docs/ChessRatings.pdf) which explains how the Stephenson System works, [steph.Rd](https://github.com/dsw225/Stephenson-Rating-System/blob/main/docs/steph.Rd) which explains base arguments, [glicko.pdf](https://github.com/dsw225/Stephenson-Rating-System/blob/main/docs/glicko.pdf) which the stephenson system is built off of, [AFLRatings.pdf](https://github.com/dsw225/Stephenson-Rating-System/blob/main/docs/AFLRatings.pdf) which is helpful in understanding the Stephenson System, [PlayerRatings.pdf](https://github.com/dsw225/Stephenson-Rating-System/blob/main/docs/PlayerRatings.pdf) which is the R documentation of the Stephenson System among others, and finally [Glickmans volleyball paper](https://github.com/dsw225/Stephenson-Rating-System/blob/main/docs/volleyball-FINAL.pdf) mentioned earlier.

The data file included is the aflodds data included in the R package to make sure that the results of each method worked the same.

## Usage

The steps to compute ratings are as follows:

#### Step One:

<img src="https://github.com/dsw225/Stephenson-Rating-System/blob/main/imgs/Step1.png?raw=true" alt="alt text" width="550">

Which we can accomplish using:

```python
player_one.updateVar(match_date)
```

Where player one is an instance of a stephenson rating, and match_date is the current match date.

#### Step Two:

<img src="https://github.com/dsw225/Stephenson-Rating-System/blob/main/imgs/Step2.png?raw=true" alt="alt text" width="550">

Which we can accomplish using:

```python
player_one.newVarRating(player_two, match_score, 1)
```

Where player_one and player_two are instances of a stephenson ratings, and match_score is the outcome. (0 for Loss, 1 for Win, .5 for Tie, or if you have fractional results). The following number is the player advantage bonus (1) - ie home team or white in chess. If the gamma parameter isn't changed this is irrelevant.

When updating two players at once it is important to remember that the players rating will change so you must create a clone of the rating before it is updated for another player:

```python
   player_one_clone = copy.deepcopy(player_one)

   player_one.newVarRating(player_two, match_score, 1) #pone is 1 for home team - since default gamma is 0 this is irrelevant
   player_two.newVarRating(player_one_clone, (1 - match_score), 0) 
```

#### Predictions

<img src="https://github.com/dsw225/Stephenson-Rating-System/blob/main/imgs/Prediction.png?raw=true" alt="alt text" width="550">

To get a prediction score we can accomplish this by:

```python
prediction = player_one.expectedScore(player_two)
```

Where player_one and player_two are instances of a stephenson ratings, and prediction is the probability of player_one winning.

#### R/Python Function

This python library is based off of the R library by [Alec Stephenson and Jeff Sonas](https://cran.r-project.org/web/packages/PlayerRatings/index.html), so the following also apply to this library:

<img src="https://github.com/dsw225/Stephenson-Rating-System/blob/main/imgs/RFunction.png?raw=true" alt="alt text" width="550">

## Contributing

Pull requests are welcome. For any changes, please open an issue first
to discuss what you would like to change.
