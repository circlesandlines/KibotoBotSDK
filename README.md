# KibotoBotSDK
Create a competitive bot to be used in games that support Kiboto

## Status
The Kiboto Bot SDK is currently in a pre-release state. Stay tuned to get installation instructions environment setup usage documentation

## TODO for 1.0 release
- [x] search for session based on config
- [x] listen for game events and execute the bot logic
- [ ] solidify alternate workflows
- [ ] add formal tests
- [ ] formal documentation

## Requirements
- python 2.7, 3.2, 3.3, and 3.4
- setuptools
- tornado
- requests
- running Kiboto server to connect to

## Installation

Clone the repo
```
git clone git@github.com:circlesandlines/KibotoBotSDK.git
cd KibotoBotSDK
```

The package can be installed with setuptools:
```
python setup.py install
```

## Basic usage example
```python
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
#	mybot = bot.Bot(logic_method=bot_brain, game_id="yourgamehere")
# or if using the sample game, only supply the logic method:
#	mybot = bot.Bot(logic_method=bot_brain)
mybot = kibotobot.Bot(kiboto_server_hostname="http://localhost",
		kiboto_server_port=9090,
		bot_hostname="http://localhost",
		bot_port=9091,
		logic_method=bot_brain,
		game_id="sample_game",
		session_id="1",
		player_id="P1")

if __name__=="__main__":
	mybot.start()
```

## Kiboto Server
https://github.com/circlesandlines/Kiboto
