# xboxgamertag
Python module to get data from www.xboxgamertag.com

## Usage
#### Installation
`pip install xboxgamertag`
#### Simple example
```python
from xboxgamertag import gamertag

user = Gamertag('WoolDoughnut310') # My gamertag is WoolDoughnut310, by the way

# Get my amount of gamerscore
print(user.gamerscore)

# If you want to see how many games I have played in total
print(user.total_games_played)
```
