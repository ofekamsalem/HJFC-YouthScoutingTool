from update_player_attributes import modify_player_attributes


players = (modify_player_attributes())
print([(p.player_name, p.player_id) for p in players])
