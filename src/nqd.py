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
			Thread(target=mgr.play).start()
		elif str_data == "toggle":
			mgr.toggle()
		elif str_data == "spotify_refresh":
			Thread(target=mgr.refresh_spotify_library).start()
			self.wfile.write(b"spotify refresh started...\n")
		else:
			print("unrecognized command: " + str_data)


if __name__ == "__main__":
	mgr = NqManager()
	PORT = 55555
	with socketserver.TCPServer(("", PORT), NqHandler) as httpd:
		print("serving...")
		httpd.serve_forever()
