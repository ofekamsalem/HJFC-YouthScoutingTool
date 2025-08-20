from dataclasses import dataclass, field
from player import Player
from game import Game
from typing import List


"""""
methods that I want from Team:
1. return max minutes from all players - done
2. calc rotations status of all players - done
3. calc percentage status of minutes from all players - done
4. add player to players dictionary - done
5. add game to games_list - done
"""

@dataclass
class Team:
    club_name: str
    club_id: str
    team_name: str
    team_id: str
    team_players: dict[str, Player] = field(default_factory=dict)
    games: List[Game] = field(default_factory=list)            


    # add a player to the team's dictionary (key: player_id, value: Player)
    def add_player(self, Player):
        self.team_players[Player.player_id] = Player

    # get the player with the most total minutes
    def max_minutes_of_all_players(self) -> Player:
        top_player = max(self.team_players.values(), key=lambda p: p.total_minutes)
        return top_player

    # add a game to the team's games list
    def add_game(self, game: Game) -> None:
        self.games.append(game)

    # for each player, calculate minutes percentage relative to the top-minutes player
    def calc_minutes_percentage_for_each_player(self) -> None:
        max_minutes_player = self.max_minutes_of_all_players()
        for player in self.team_players.values():
            player.minutes_percentage = 100 * (player.total_minutes / max_minutes_player.total_minutes)
    
    # for each player, calculate minutes percentage relative to the top-minutes player
    def calc_minutes_rotation_location_for_each_player(self) -> None:
        players_sorted_by_minutes = sorted(self.team_players.values(), key=lambda p: p.total_minutes, reverse=True)
        for index, player in enumerate(players_sorted_by_minutes, start=1):
            player.minutes_rotation = index
    
    



    

    




# print(p)

# t = Team("11","aa","aaa")

# t.add_player["1"]

# print(t.team_players)

# team_players: dict
# games_list: list