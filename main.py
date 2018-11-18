import re
import requests
import sys
from bs4 import BeautifulSoup
from bs4.element import Comment

DEFAULT_URL = "https://stackoverflow.com"
URL = sys.argv[1] if (len(sys.argv) > 1) else DEFAULT_URL
WORDS_TO_PRINT = 10

noise_words = set({'ourselves', 'hers', 'between', 'yourself', 'again',
				  'there', 'about', 'once', 'during', 'out', 'very', 'having',
				  'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its',
				  'yours', 'such', 'into', 'of', 'most', 'itself', 'other',
				  'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
				  'each', 'the', 'themselves', 'below', 'are', 'we',
				  'these', 'your', 'his', 'through', 'don', 'me', 'were',
				  'her', 'more', 'himself', 'this', 'down', 'should', 'our',
				  'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had',
				  'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them',
				  'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
				  'yourselves', 'then', 'that', 'because', 'what', 'over',
				  'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
				  'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
				  'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being',
				  'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it',
				  'how', 'further', 'was', 'here', 'than'})

def preprocess(string):
	"""
	Apply preprocessing to a single string. 
		- removing stop words
		- stripping/adding punctuation
		- changing case
		- word find/replace
	RETURN: the preprocessed string in list form.
	"""
	processed_string = string

	# # Removing neutral conjunctions 
	# processed_string = re.sub(r'\b(the|is|a|and|or|of|for|are)\b', "", processed_string)

	# Removing noise
	processed_string = re.sub(r'<[^>]*>', "", processed_string)     # Removing any HTML tags
	#processed_string = re.sub(r'[\d]{2,}', "", processed_string)    # Removing 2 or more consequent digits
	processed_string = re.sub(r'\'', "", processed_string)          # Replacing apostrophe with null
	processed_string = re.sub(r'\W', " ", processed_string)         # Removing all non alpha-numeric words
	processed_string = re.sub(r'\s+', " ", processed_string)        # Trimming multiple whitespaces

	processed_string = processed_string.lower()
	
	# Removing noise words
	processed_string_list = processed_string.split()
	final_processed_string_list = [word for word in processed_string_list if word not in noise_words]
	# processed_string = ' '.join(final_processed_string_list)

	# print(final_processed_string_list)
	return final_processed_string_list


# From https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Grab visible text from an html body
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    # Trim visible_texts off empty strings and return as a list rather than as a filter iterable.
    return list(filter(None, [t.strip() for t in visible_texts])) 

if __name__ == "__main__":
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

    printed_words_count = 0
    for word in sorted(word_count, key=word_count.get, reverse=True):
        print(word, word_count[word])
        printed_words_count += 1
        if (printed_words_count >= WORDS_TO_PRINT):
            break