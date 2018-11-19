import re
import requests
import sys
from .keyworder import Keyworder

def main():
	URL = None
	words_to_print = 10

	if (len(sys.argv) > 1):
		 URL = sys.argv[1] 
	if (len(sys.argv) > 2):
		words_to_print = sys.argv[2]

	kw = Keyworder(URL)
	kw.print_keywords(words_to_print)

if __name__ == "__main__":
	main()