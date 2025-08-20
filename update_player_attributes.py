from parse_game import parse_games

def modify_player_attributes() -> list:
    res = []
    team = parse_games()
    team.calc_minutes_percentage_for_each_player()
    team.calc_minutes_rotation_location_for_each_player()
    for player in team.team_players.values():
            if 25 <= player.minutes_percentage <= 50 and 12 <= player.minutes_rotation <= 18 and player.has_played_under_90_minutes_in_last_3_games() and player.in_squad_last_3_games() and player.not_started_in_last_3_games():
                res.append(player) 
    return res

