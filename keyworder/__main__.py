import re
import requests
import sys
from .keyworder import Keyworder

def main():
	URL = sys.argv[1] if (len(sys.argv) > 1) else DEFAULT_URL
	words_to_print = 10

	kw = Keyworder(URL)
	kw.print_keywords(words_to_print)

if __name__ == "__main__":
	main()