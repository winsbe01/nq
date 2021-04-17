import socketserver 
from threading import Thread
import logging

from manager import NqManager
from log import NqLog

nqlog = logging.getLogger("nq")

class NqHandler(socketserver.StreamRequestHandler):

	def handle(self):
		str_data = self.rfile.readline().strip().decode("utf-8")
		if str_data == "play":
			nqlog.info("user ->	`play`")
			Thread(target=mgr.play).start()
		elif str_data == "pause":
			nqlog.info("user ->	`pause`")
			mgr.pause()
		elif str_data == "next":
			nqlog.info("user -> `next`")
			mgr.next()
			if not mgr.is_playing:
				Thread(target=mgr.play).start()
		elif str_data == "toggle":
			nqlog.info("user ->	`toggle`")
			if mgr.is_playing:
				mgr.pause()
			else:
				Thread(target=mgr.play).start()
		elif str_data == "status":
			nqlog.info("user ->	`status`")
			if mgr.status():
				self.wfile.write(mgr.status()[0].encode())
			else:
				self.wfile.write(b"")
		elif str_data == "spotify_refresh":
			nqlog.info("user -> `refresh spotify`")
			Thread(target=mgr.refresh_spotify_library).start()
			self.wfile.write(b"spotify refresh started...\n")
		elif str_data == "local_refresh":
			nqlog.info("user -> `refresh local`")
			Thread(target=mgr.refresh_local_library).start()
			self.wfile.write(b"local refresh started...\n")
		else:
			self.wfile.write("unrecognized command: {}\n".format(str_data).encode())


if __name__ == "__main__":
	NqLog().setup()
	mgr = NqManager()
	PORT = 55555
	with socketserver.TCPServer(("", PORT), NqHandler) as httpd:
		nqlog.info("====== START NQD SERVER ======")
		httpd.serve_forever()
