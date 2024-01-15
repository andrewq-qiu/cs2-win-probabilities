# CS2 Win Probabilities

## Introduction

[Counter-Strike 2](https://www.counter-strike.net/cs2) is a tactical first-person shooter game where players are divided into two teams: terrorists and counter-terrorists. The terrorists aim to plant and explode a bomb, while the counter-terrorists act to prevent the bomb planting or disarm the bomb once planted. The game is played in a series of time-limited rounds, where the starting state of each round is determined by weapons saved by survivors of previous rounds and the cumulative in-game economy, which is used to purchase new weapons and equipment. The money awarded to each team is dependent on their performance in previous rounds, and rewards kills and the completion of objectives. 

At each state of the game, certain actions are more optimal than others. For example, towards the end of a round, teams with a disadvantage may choose to purposefully forgo a round as to preserve their weaponry for the next. Determining the optimal actions in different situations is an actively explored problem in the Counter-Strike professional scene. 

This project aims to solve a subproblem:

**Given knowledge of the current state of a round, can we predict the win probability of each team?**

### Approach

This is journaled in my medium article here: TODO

### Code

This project was completed using Python 3.12.0. Packages used are outlined in `requirements.txt`.

#### Directory Structure

* `_data`: Stores the raw and processed data generated from the scripts
* `config`: Various configuration files used in Python scripts
  * `maps.txt`: The list of CS2 maps used in the model
  * `events.txt`: The list of CS2 HLTV events from which data is used
* `run`: Bash scripts with preloaded arguments for invoking Python scripts
* `scripts`: Various Python scripts for data generation and processing
