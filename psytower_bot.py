
from KibotoBotSDK import kibotobot
import random

actions = {
	"Attack": {
		'id': 1,
		'applied_to': "enemy"
	},
	"Guard": {
		'id': 2,
		'applied_to': "self"
	},
	"Dual Attack": {
		'id': 3,
		'applied_to': "enemy"
	},
	"Double Attack": {
		'id': 4,
		'applied_to': "enemy"
	},
	"Triple Attack": {
		'id': 5,
		'applied_to': "enemy"
	},
	"Wait": {
		'id': 7,
		'applied_to': "self"
	},
	"Heal": {
		'id': 8,
		'applied_to': "self" #NOTE heal can be applied to others too.
	},
	"Fire": {
		'id': 9,
		'applied_to': "enemy"
	},
	"Spark": {
		'id': 10,
		'applied_to': "enemy"
	}
}

enemies = [
	'Psy Punk',
	'Warlord',
	'EnerWitch'
]

def bot_brain(event_data, player_id, game_id):
	""" A randomized Psy Tower bot. So far it only works for a
	party and enemy troop size of one. """

        print event_data

	# choose an action randomly. ideally this will be smarter AI :P
	player_actions = {
		'Lou': actions[random.choice(list(actions.keys()))],
		'Jack': actions[random.choice(list(actions.keys()))],
		'Jane': actions[random.choice(list(actions.keys()))]
	}

	# if attack, choose one of the enemies at random
	for player in player_actions:
		if player_actions[player]['applied_to'] == 'enemy':
			player_actions[player]['applied_to'] = random.choice(enemies)

        reply = {'action': player_actions, 'name': "GoodGuy"}

	return reply

# The Bot object defaults to local mode (shown below)
# if you want to run a bot locally and don't care about hostnames or ports,
# you can initialize like so instead:
#   mybot = bot.Bot(logic_method=bot_brain, game_id="yourgamehere")
mybot = kibotobot.Bot(kiboto_server_hostname="http://localhost",
		kiboto_server_port=9090,
		bot_hostname="http://localhost",
		bot_port=9091,
		logic_method=bot_brain,
		game_id="sample_game",
		session_id="test_session",
		player_id="GoodGuy")

if __name__=="__main__":
	mybot.start()
