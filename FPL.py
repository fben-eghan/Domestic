import pandas as pd
import requests
import json
from sklearn.linear_model import LinearRegression

class FPLPlayer:
    def __init__(self, id, name, team, position, cost, total_points):
        self.id = id
        self.name = name
        self.team = team
        self.position = position
        self.cost = cost
        self.total_points = total_points

class FPLTeam:
    def __init__(self, budget, num_players):
        self.budget = budget
        self.num_players = num_players
        self.players = []
        self.positions = {'GKP': 0, 'DEF': 0, 'MID': 0, 'FWD': 0}

    def add_player(self, player):
        if len(self.players) < self.num_players and self.budget >= player.cost and self.positions[player.position] < 5:
            self.players.append(player)
            self.budget -= player.cost
            self.positions[player.position] += 1
            print(f"Added {player.name} ({player.position}) to the team.")
        elif len(self.players) == self.num_players:
            print("Team is already full.")
        elif self.budget < player.cost:
            print(f"Not enough budget to add {player.name} ({player.position}).")
        else:
            print(f"Position limit reached for {player.position} players.")

    def get_team_points(self):
        total_points = sum([player.total_points for player in self.players])
        return total_points

# Fetch real-time player data from FPL API
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
response = requests.get(url)
data = json.loads(response.text)
elements = pd.DataFrame(data['elements'])
teams = pd.DataFrame(data['teams'])

# Data cleaning
elements = elements[['id', 'web_name', 'team', 'element_type', 'now_cost', 'total_points']]
elements['position'] = elements.element_type.map({1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'})
elements['team'] = elements.team.map(teams.set_index('id').name)
elements = elements.drop('element_type', axis=1)

# Get historical data for each player
for i, row in elements.iterrows():
    player_id = row['id']
    history_url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
    history_response = requests.get(history_url)
    history_data = json.loads(history_response.text)
    history = pd.DataFrame(history_data['history'])
    history = history[['total_points']]
    history['total_points'] = history['total_points'].astype(int)

    # Use historical data to train a linear regression model and predict future points
    X = history.index.values.reshape(-1, 1)
    y = history['total_points']
    model = LinearRegression()
    model.fit(X, y)
    next_game_points = int(model.predict([[history.index[-1] + 1]]))

    # Create FPLPlayer object and add it to the FPLTeam object
    player = FPLPlayer(
        id=row['id'],
        name=row['web_name'],
        team=row['team'],
        position=row['position'],
        cost=row['now_cost'],
        total_points=next_game_points
    )
    team.add_player(player)
