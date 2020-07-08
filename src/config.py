from configparser import ConfigParser
from pathlib import Path

class NqConfig:

	DEFAULT_CONFIG = "~/.config/nq/server.config"

	def __init__(self):
		config = ConfigParser()
		config.read(Path(NqConfig.DEFAULT_CONFIG).expanduser())

		# get spotify stuff
		self.spotify_username = config['spotify']['username']
		self.spotify_client_id = config['spotify']['client_id']
		self.spotify_client_secret = config['spotify']['client_secret']
		self.spotify_device = config['spotify']['device']

		self.spotify_scopes = 'user-library-read user-read-currently-playing user-modify-playback-state'
		self.spotify_redirect_url = 'https://localhost'

		# get general stuff
		self.local_library = Path(config['general']['local_library']).expanduser()
		self.queuefile = Path(config['general']['queuefile']).expanduser()

