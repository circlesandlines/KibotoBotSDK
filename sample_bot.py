
"""
	This is a basic usage example
"""

import KibotoBot

config = {
	"kiboto_server_hostname": "localhost",
	"kiboto_server_port": 9090,
	"bot_hostname": "localhost",
	"bot_port": 9091,
	"game_id": "sample_game",
	"session_id": "1",
	"player_id": "P1"
}

def bot_brain(event_data, player_id, game_id):
	""" your bot logic goes here.
	be sure to follow game specific formatting """

	reply = {}

	# ...

	return reply


mybot = KibotoBot(logic_method=bot_brain)
mybot.start()
