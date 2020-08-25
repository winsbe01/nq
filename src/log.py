import logging

class NqLog:
	def setup(self):
		nqlog = logging.getLogger("nq")
		nqlog.setLevel(logging.DEBUG)

		console = logging.StreamHandler()
		console.setLevel(logging.DEBUG)

		formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
		console.setFormatter(formatter)

		nqlog.addHandler(console)
