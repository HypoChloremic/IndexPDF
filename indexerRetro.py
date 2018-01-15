# IndexerRetro is a simple CLE script used to index unique words from specific
# pages of a pdf document.
# 2017 Ali Rassolie (cc)


import subprocess
import PyPDF2
import os
from collections import Counter
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--parent", nargs=1, help="Absolute path to the file parent")
ap.add_argument("-f", "--file", nargs=1, help="Name of pdf")
ap.add_argument("-o", "--output", nargs=1, help="Name of output")
args = ap.parse_args()


class IndexerRetro:
	def __init__(self):
		print(f"[IndexerRetro] Initializing")

	def index(self, parent, path, out, delimiter=r"\\"):
		print(f"{parent}{delimiter}{path}")
		p = f"{parent}{delimiter}{path}"
		with open(p, "rb") as data:
			numpages = PyPDF2.PdfFileReader(data).numPages

		index = {}
		for i in range(1, numpages):
			text = self.getData(p, i)
			
			if text: 
				count = Counter(text.split())
				for k in iter(count):
					try: 
						index[k].append(i)
					except KeyError as e:
						index[k] = [i]
				print(f"[Indexer] Page {i}/{numpages}")
			else: 
				print(f"[Indexer] Page {i}/{numpages} <Nothing returned>")

		with open(f"{parent}{delimiter}{out}.txt", "a", encoding="utf8") as file: 
			for i in iter(index):
				file.write(f"{i}: {index[i]}\n")


	def getData(self, filename, page):
	    try:
	        content = subprocess.check_output(["pdftotext", '-enc', 'UTF-8', "-f",f"{page-1}", "-l", f"{page}",f"{filename}", "-"])
	    except subprocess.CalledProcessError as e:
	        print('Skipping {} (pdftotext returned status {})'.format(filename, e.returncode))
	        return None
	    return content.decode('utf-8')

process = IndexerRetro()
process.index(path=args.file[0], parent=args.parent[0], out=args.output[0])

