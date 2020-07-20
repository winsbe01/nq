import spotipy
import spotipy.util as sutil
from threading import Thread

from config import NqConfig
from player import SongStatus
from local_player import LocalPlayer
from local_library import LocalLibrary
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
		ret = lines.pop(0).strip('\n').split(';;')
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
		fmt = "{0};;{1};;{2};;{3};;{4}\n"
		SpotifyLibrary(self.spotipy, fmt)

	def refresh_local_library(self):
		fmt = "{0};;{1};;{2};;{3};;{4}\n"
		LocalLibrary(fmt, self.config.local_library)

	def status(self):
		return self.current_track

	def pause(self):
		self.player.stop()

	def next(self):
		self.player.skip()
	
	def play(self):
		#self.next_track, queue = self.get_queue()
		self.is_playing = True

		if self.current_track is None:
			self.current_track, self.queue = self.get_queue()
			self.write_queue(self.queue)

		while True:
			if self.player is None:
				if self.current_track[1] == "LOCAL":
					self.player = LocalPlayer(self.current_track[2])
				elif self.current_track[1] == "SPOTIFY":
					self.player = SpotifyPlayer(self.current_track[2], self.spotipy, self.config.spotify_device)
				else:
					raise Exception("bad track type!")

			self.player.reset()
			status = SongStatus()
			pthread = Thread(target=self.player.play(status))
			pthread.start()
			pthread.join()
		
			if status.name == "stopped":
				self.is_playing = False
				break
			elif status.name in ("skipped", "done"):
				self.current_track, self.queue = self.get_queue()
				self.write_queue(self.queue)
				self.player = None
