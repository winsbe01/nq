import spotipy
import spotipy.util as sutil
from threading import Thread

from config import NqConfig
from player import SongStatus
from local_player import LocalPlayer
from spotify_player import SpotifyPlayer
from spotify_library import SpotifyLibrary


class NqManager:

	def __init__(self):
		self.is_playing = False
		self.is_started = False
		self.player = None
		self.config = NqConfig()
		self.spotipy = self.spotify_authorize()
		self.current_track = None

	def write_queue(self, queue):
		with open(self.config.queuefile, 'w') as fil:
			fil.writelines(queue)

	def get_queue(self):
		print(self.config.queuefile)
		with open(self.config.queuefile, 'r') as fil:
			lines = fil.readlines()
			print(lines)
		if not lines:
			return None
		ret = lines.pop(0).strip('\n').split(maxsplit=1)
		return ret, lines

	def spotify_authorize(self):

        # try and get a token
		token = sutil.prompt_for_user_token(
			self.config.spotify_username,
			self.config.spotify_scopes,
			self.config.spotify_client_id,
			self.config.spotify_client_secret,
			self.config.spotify_redirect_url)

		# if we get one, return a spotify object
		if token:
			print("my spotify is authorized")
			return spotipy.Spotify(auth=token)
		else:
			print("no token :(")
			return None

	def refresh_spotify_library(self):
		fmt = "{0};;{1};;{2};;{3};;{4};;{5}\n"
		SpotifyLibrary(self.spotipy, fmt)

	def pause(self):
		self.player.stop()
	
	def play(self):
		#self.next_track, queue = self.get_queue()
		if self.current_track is None:
			self.current_track, self.queue = self.get_queue()
			self.write_queue(self.queue)
		while True:
			#self.write_queue(queue)

			if self.player is None:
				print("player is None")
				if self.current_track[0] == "LOCAL":
					self.player = LocalPlayer(self.current_track[1])
				elif self.current_track[0] == "SPOTIFY":
					self.player = SpotifyPlayer(self.current_track[1], self.spotipy, self.config.spotify_device)
				else:
					raise Exception("bad track type!")

			self.player.reset()
			status = SongStatus()
			pthread = Thread(target=self.player.play(status))
			pthread.start()
			pthread.join()
		
			if status.name != "done":
				break
			else:
				self.current_track, self.queue = self.get_queue()
				self.write_queue(self.queue)
				self.player = None
