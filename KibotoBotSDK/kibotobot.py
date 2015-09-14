"""
	get all sessions from server
	pick ones with empty string as value to session key.


	Workflow:

	configure the game you want to play
	optional: configure the session
	optional: configure the player
	configure the kiboto server host and port

	start it up
	grab all sessions from kiboto server and search for the configured criteria
	request to connect to session (send bots hostname and port)
	when complete and session confirmed,
	immediately turn on ioloop and start listening for game events
	broadcast 'bot ready' message on ping when everything started and state complete

"""
import tornado.ioloop
from tornado.httpserver import HTTPServer
import tornado.web
from tornado.netutil import bind_sockets
from tornado.process import fork_processes
import json
import requests
import urllib

class NoSessionAvailableException(Exception): pass
class NoBotBrainException(Exception): pass
class KibotoServerConnectionError(Exception): pass

class BotEventHandler(tornado.web.RequestHandler):
	def initialize(self, bot_logic, player_id, game_id):
		self.bot_logic = bot_logic
		self.player_id = player_id
		self.game_id = game_id

	@tornado.web.asynchronous
	def post(self):
		message = json.loads(self.request.body)
		reply = self.bot_logic(message['event'], self.player_id, self.game_id)
		print reply
		self.write(json.dumps(reply))
		self.finish()

	@tornado.web.asynchronous
	def ping(self):
		""" send a 200 on ping. this is so the clients know the bot is ready :)"""
		self.send_error(200)
		

class Bot:
	def __init__(self, kiboto_server_hostname="localhost", kiboto_server_port=9090, bot_hostname="localhost", bot_port=9091, logic_method=None, game_id="sample_game", session_id="1", player_id=""):

		if not logic_method:
			raise NoBotBrainException("Bot's logic method not specified")

		# bot config
		self.bot_logic = logic_method
		self.bot_endpoint = bot_hostname + ':' + str(bot_port) + '/event'
		self.bot_port = bot_port
		self.game_id = game_id
		self.session_id = session_id
		self.player_id = player_id

		self.session_key = ':'.join([game_id, session_id, player_id]).rstrip(':').rstrip(':')
		# NOTE 2 rstrips just in case session id and player id not specified

		# kiboto server connection config
		self.kiboto_subscription_url = kiboto_server_hostname + ':' + str(kiboto_server_port) + '/subscribe'
		self.kiboto_sessions_url = kiboto_server_hostname + ':' + str(kiboto_server_port) + '/get_sessions'

	def join_session(self, bot_endpoint):
		"""find a session and connect. this part is all synchronous code. only start async once bot starts listening"""

		# get all active sessions
		try:
			sessions_request = requests.get(self.kiboto_sessions_url)
		except Exception as e:
			raise KibotoServerConnectionError(str(e))

		if sessions_request.status_code != 200:
			raise KibotoServerConnectionError("connection not successful: " + str(sessions_request.status_code))

		sessions = json.loads(sessions_request.text)
		print 'sessions available: ', sessions
		print 'searching for: ', self.session_key
		print 'bot endpoint: ', bot_endpoint

		if not sessions:
			print "sessions empty?", sessions

		session_chosen = False
		for active_session_key, active_bot_endpoint in sessions.iteritems():
			# does the configured session have a match in the actual
			# on-going session data?
			# eg. find   "sample_game:1:P1" or
			# look for specific session in the game:
			# "sample_game:1"
			# or any session in the game:
			# "sample_game"
			# will check substring
			# pick the first match and try to reserve it
			if self.session_key in active_session_key:
				# if no bot has been set to the player session
				# try to reserve it.
				if active_bot_endpoint == "empty":
					params = {
						# NOTE: we use k here instead of self.session_key
						# because self.session_key could have vaues missing
						'session_key': active_session_key,
						'hostname': bot_endpoint
					}
					query = self.kiboto_subscription_url + '?' + urllib.urlencode(params)
					print "query = ", query
					success = requests.get(query)
					if success.status_code == 200:
						session_chosen = True
						# don't try to connect to others if already connected to one!
						break
				elif active_bot_endpoint == bot_endpoint:
					# if the bot crashed and is trying to re-connect,
					# let it do so. check if the set endpoint is our own
					session_chosen = True
					break

		if not session_chosen:
			raise NoSessionAvailableException('The session does not exist: ' + self.session_key)

	def start(self):
		"""Start up a tornado web server and use the logic method as the request handler"""

		# find a session and join it
		self.join_session(self.bot_endpoint)

		# configure the bot event handler and the user supplied logic
		bot_server_app = tornado.web.Application([
			(r"/event", BotEventHandler, dict(	bot_logic=self.bot_logic,
								player_id=self.player_id,
								game_id=self.game_id ))
			])

		# start 'er up
		sockets = bind_sockets(self.bot_port)
		print "Bot is listening d[-_-]b"
		fork_processes(None)
		server = HTTPServer(bot_server_app)
		server.add_sockets(sockets)

		# start listening
		tornado.ioloop.IOLoop.instance().start()
