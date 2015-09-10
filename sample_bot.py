
"""
	This is a basic usage example
"""

from KibotoBotSDK import kibotobot

# below are the default configs that the Bot object initializes to
# if not provided. can switch them here though
# if you want to run a bot locally and don't care about hostnames or ports,
# you can initialize like so:
#	mybot = bot.Bot(logic_method=bot_brain, game_id="yourgamehere")
# or if using the sample game, only supply the logic method:
#	mybot = bot.Bot(logic_method=bot_brain)

config = {
	"kiboto_server_hostname": "http://localhost",
	"kiboto_server_port": 9090,
	"bot_hostname": "http://localhost",
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


mybot = kibotobot.Bot(kiboto_server_hostname=config['kiboto_server_hostname'],
		kiboto_server_port=config['kiboto_server_port'],
		bot_hostname=config['bot_hostname'],
		bot_port=config['bot_port'],
		logic_method=bot_brain,
		game_id=config['game_id'],
		session_id=config['session_id'],
		player_id=config['player_id'])
mybot.start()
