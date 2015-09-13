
from KibotoBotSDK import kibotobot

def bot_brain(event_data, player_id, game_id):
	""" your bot logic goes here.
	be sure to follow game specific formatting """

	reply = {}

	# ...

	return reply

# The Bot object defaults to local mode (shown below)
# if you want to run a bot locally and don't care about hostnames or ports,
# you can initialize like so instead:
#   mybot = bot.Bot(logic_method=bot_brain, game_id="yourgamehere")
# or if using the sample game, only supply the logic method:
#   mybot = bot.Bot(logic_method=bot_brain)
mybot = kibotobot.Bot(kiboto_server_hostname="http://localhost",
		kiboto_server_port=9090,
		bot_hostname="http://localhost",
		bot_port=9092,
		logic_method=bot_brain,
		game_id="sample_game",
		session_id="1",
		player_id="P2")
mybot.start()
