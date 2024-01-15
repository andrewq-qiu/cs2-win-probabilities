<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="assets/percent-icon.png" alt="Logo" width="120" height="120" style="background-color: white">

<h3 align="center">cs2-win-probabilities</h3>
  <p align="center">
    Predicting live win probabilities in a CS2 round
    <br />
    <br />
    <br />
  </p>
</div>

## About

##### What's CS2?

[Counter-Strike 2](https://www.counter-strike.net/cs2) (CS2) is a tactical first-person shooter game where two teams compete against each other in a bomb planting and defusal situation over a series of rounds. CS2 is renowned both for its high skill and complex strategy. Correspondingly, it is one of the world's leading eSports games, with a net prize pool of over $180M. With such high stakes, understanding the optimal choice in different situations is invaluable. 

#### My Project: Solving a Subproblem

My project focuses on a critical aspect of CS2 gameplay: decision-making in the final moments of a round. Often, teams face a strategic dilemma of whether to "save" their weaponry by avoiding conflict and preserving resources for future rounds, especially when the odds of achieving the primary objective seem low.

My project attempts to uncover the optimal choice by modelling the win probability of a round, given its current state (player health, positions, weaponry, and state of the objective). This has applications in CS2 gameplay analytics and live broadcasting. Notably, Blast.tv provides a [similar](https://blast.tv/article/blast-fall-final-2023-innovations) tool which displays win probabilities during a match's broadcast. This project also provides significant steps towards building an open-source version of such a tool.

## Technologies

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 

**Libraries:** Pytorch, Numpy, Jupyter, Selenium, BeautifulSoup

## Motivation and Learning Outcomes

This project was inspired by [Blast.tv's AI round prediction graphic](https://blast.tv/article/blast-fall-final-2023-innovations) on their CS2 competitive broadcasts. Through this project, I wanted to achieve a few key learning outcomes:
* Approach a publicly unexplored ML problem from scratch
* Evaluate neural networks vs. more traditional Bayesian modelling
* Extract a useful and reasonably sized dataset from a large and difficult data source

## Getting Started

### Project Structure

This project is presented alongside an article [TODO]().

#### Directory structure
- `scripts` - scripts for downloading and processing data
- `notebooks` - Jupyter notebooks at various stages of experimentation

This project was written and tested with Python 3.9. Scraping code was built around https://hltv.org/ (last tested in Jan 2023).

Begin by setting up the required requirements:

```
pip install -r requirements.txt
```

#### Dataset creation

A SQL database file containing the final processed data can be retrieved here: [TODO](). Alternatively, you can scrape raw data from HLTV and process it via a sequence of scripts.

To download the demos used, 

```
chmod u+x scripts/download_demos.sh
scripts/download_demos.sh
```
