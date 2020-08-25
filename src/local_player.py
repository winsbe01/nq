from mpg123 import Mpg123, Out123
import logging

from player import Player

nqlog = logging.getLogger("nq")

class LocalPlayer(Player):

	def __init__(self, loc):
		super().__init__(loc)
		self.setup_mp3()

	def setup_mp3(self):
		self.mp3 = Mpg123(self.loc)
		self.mpgout = Out123()
		self.frames = self.mp3.iter_frames(self.mpgout.start)

	def play(self, status):
		nqlog.info("playing local track")
		while True:
			if self.stopped:
				nqlog.debug("stopping local track")
				status.name = "stopped"
				break
			elif self.skipped:
				nqlog.debug("skipping local track")
				status.name = "skipped"
				break
			try:
				self.mpgout.play(next(self.frames))
			except self.mp3.DecodeException as de:
				nqlog.warning("mpg123 error: " + str(de))
				pass
			except StopIteration:
				nqlog.info("finishing local track")
				self.stopped = True
				status.name = "done"
				break
