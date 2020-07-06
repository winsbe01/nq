from time import sleep, time
from player import Player


class SpotifyPlayer(Player):

	def __init__(self, loc, sp, dev):
		super().__init__(loc)
		self.sp = sp
		self.sp.transfer_playback(dev, force_play=False)
		self.cur_ms = 0
		self.init_song_info()

	def init_song_info(self):
		self.remaining_ms = self.sp.track(self.loc)['duration_ms']

	def get_system_ms(self):
		return int(round(time() * 1000))

	def play(self, status):
		i = [self.loc]
		self.sp.start_playback(uris=i, position_ms=self.cur_ms)
		self.end_time = self.get_system_ms() + self.remaining_ms
		while True:
			if self.stopped:
				self.sp.pause_playback()
				self.cur_ms = self.sp.currently_playing()['progress_ms']
				self.remaining_ms = self.remaining_ms - self.cur_ms
				status.name = "stopped"
				break
			elif self.end_time < self.get_system_ms():
				if not self.sp.currently_playing()['is_playing']:
					status.name = "done"
					break
			else:
				sleep(1)
