import io
import numpy as np
import pandas
import csv

def test():
	bytes = 'lol\txd☯\nlaskjdf\tkj'.encode('UTF-8')
	# bio = io.BytesIO(bytes.decode('UTF-8'))
	# lst = tuple(item for item in bytes.decode('UTF-8').split('\n'))
	# print(lst)
	# nparr = np.genfromtxt(io.BytesIO(bytes), delimiter='\t', dtype=str)
	nparr = csv.reader(io.StringIO(bytes.decode('UTF-8')), delimiter='\t')
	# nparr = pandas.read_csv(io.BytesIO(bytes), delimiter='\t', dtype=str)
	# print(nparr)
	print(nparr)
	for row in nparr:
		print(', '.join(row))

test()