import re
import requests
import sys
from preprocess import text_from_html
from filter import preprocess

if __name__ == "__main__":
	DEFAULT_URL = "https://stackoverflow.com"
	URL = sys.argv[1] if (len(sys.argv) > 1) else DEFAULT_URL
	words_to_print = 10

	page = requests.get(URL)
	visible_text = text_from_html(page.content)

    # Build a collection of standalone words through preprocessing the visible_text
	word_collection = []
	for sentence in visible_text:
		word_collection.extend(preprocess(sentence))

	# Count the occurence of each word and store it into a dict
	word_count = {}
	for word in word_collection:
		if not word in word_count:
			word_count[word] = 1
		else:
			word_count[word] += 1

	# Output the top words_to_print
	printed_words_count = 0
	for word in sorted(word_count, key=word_count.get, reverse=True):
		print(word, word_count[word])
		printed_words_count += 1
		if (printed_words_count >= words_to_print):
			break