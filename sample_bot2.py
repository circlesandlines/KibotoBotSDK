
from KibotoBotSDK import kibotobot
import random

smalltalk_cache = [
	'hey',
	'sup',
	'how you doin?',
	'i\'m good, how\'r you?',
	'meh, could be better, how\'s the wife?',
	'she\'s up to no good I tells yah',
	'feeding the velociraptors again eh?',
	'you know it bob',
	'hah!',
	'the weather',
	'yup'
]

def bot_brain(event_data, player_id, game_id):
	""" your bot logic goes here.
	be sure to follow game specific formatting """

	print event_data

	reply = {'action': smalltalk_cache[random.randint(0, 9)], 'name': 'Enemy'}

	return reply

# The Bot object defaults to local mode (shown below)
# if you want to run a bot locally and don't care about hostnames or ports,
# you can initialize like so instead:
#   mybot = bot.Bot(logic_method=bot_brain, game_id="yourgamehere")
mybot = kibotobot.Bot(kiboto_server_hostname="http://localhost",
		kiboto_server_port=9090,
		bot_hostname="http://localhost",
		bot_port=9092,
		logic_method=bot_brain,
		game_id="sample_game",
		session_id="test_session",
		player_id="Enemy")

if __name__=="__main__":
	mybot.start()
