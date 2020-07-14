from mpg123 import Mpg123, Out123
from player import Player


class LocalPlayer(Player):

	def __init__(self, loc):
		super().__init__(loc)
		self.setup_mp3()

	def setup_mp3(self):
		self.mp3 = Mpg123(self.loc)
		self.mpgout = Out123()
		self.frames = self.mp3.iter_frames(self.mpgout.start)

	def play(self, status):
		while True:
			if self.stopped:
				status.name = "stopped"
				break
			elif self.skipped:
				status.name = "skipped"
				break
			try:
				self.mpgout.play(next(self.frames))
			except self.mp3.DecodeException as de:
				print(str(de))
				pass
			except StopIteration:
				self.stopped = True
				status.name = "done"
				break
