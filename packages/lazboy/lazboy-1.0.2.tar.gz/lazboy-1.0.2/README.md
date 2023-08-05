# La-Z-Boy

[![Join the chat at https://gitter.im/La-Z-Boy/Lobby](https://badges.gitter.im/La-Z-Boy/Lobby.svg)](https://gitter.im/La-Z-Boy/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

The end result of extreme boredom and the sufferings after watching some really low-rated movies on TV.

This script is really helpful when you want to know the the Movies that are to be telecasted on TV
along with their `"Timing"` and `"IMDb Rating"`, so you never miss out a good watch right when you sit
on your La-Z-Boy.


Check demo version at [Heroku App](https://protected-cove-85139.herokuapp.com/) (Use channels like Movies-Now, Star-Movies, etc.)

### Dependencies
-----------------

Install all the dependencies using `pip install -r requirements.txt` before using the script.

   * BeautifulSoup
   * mechanize
   * tabulate
   * fpdf

### Usage
-----------------

**Run the program:**

    $ python main.py [channel name]


    `channel name` : Name of the movie channel

**Example:**

    $ python main.py star movies


**Output:**

    Movie: Dawn of the Planet of the Apes  Time: 21:00 - 23:45  Rating: 7.6


And it's done! You have the name of the movie, timings and most importantly, the IMDb rating for the movie
right in front of you on the Terminal.

### Contribute

Have any suggestions? Please feel free to report as issues/pull requests.
