
# Flappy Bird

Flappy bird mobile application game recreated in python using in-build dependencies. Play with the same feel on desktop. Get highscores and save your recent games as well.

### Features
 - Stores game data and highscores in local database
 - Created using python in-built dependencies

## Installation
**Clone the Repo**

    $ https://github.com/Dhirajjjj/Flappy-bird.git
    $ cd Flappy-bird

**Create and run Virtual enviornment**

    $ python -m venv venv
    $ . \venv\Scripts\activate

**Install dependencies**

    $ pip install -r requirements.txt

**Create local databse**

    $ sqlite3 flappy_test.db
    $ CREATE  TABLE highscore ( user_name STRING, score INTEGER );
    $ CREATE  TABLE user ( user_name STRING, pass_word STRING );

**Start the game**

    $ python flappy.py

## There's more to come

 - Multiplayer mode
 - Global highscores and competitions
 - Various game modes [inverted, blind, ablities]