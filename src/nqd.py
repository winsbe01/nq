import socketserver 
from threading import Thread

from manager import NqManager

class NqHandler(socketserver.StreamRequestHandler):

	def handle(self):
		str_data = self.rfile.readline().strip().decode("utf-8")
		if str_data == "play":
			Thread(target=mgr.play).start()
		elif str_data == "pause":
			mgr.pause()
		elif str_data == "next":
			mgr.next()
			if not mgr.is_playing:
				Thread(target=mgr.play).start()
		elif str_data == "toggle":
			if mgr.is_playing:
				mgr.pause()
			else:
				Thread(target=mgr.play).start()
		elif str_data == "status":
			self.wfile.write(mgr.status()[0].encode())
		elif str_data == "spotify_refresh":
			Thread(target=mgr.refresh_spotify_library).start()
			self.wfile.write(b"spotify refresh started...\n")
		elif str_data == "local_refresh":
			Thread(target=mgr.refresh_local_library).start()
			self.wfile.write(b"local refresh started...\n")
		else:
			self.wfile.write("unrecognized command: {}\n".format(str_data).encode())


if __name__ == "__main__":
	mgr = NqManager()
	PORT = 55555
	with socketserver.TCPServer(("", PORT), NqHandler) as httpd:
		print("serving...")
		httpd.serve_forever()
