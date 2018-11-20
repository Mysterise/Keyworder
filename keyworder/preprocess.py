import re
from .stop_words import NLTK_stop_words
from bs4 import BeautifulSoup
from bs4.element import Comment

def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False

def separate_words(text):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.

    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('(?u)\W+')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        # leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words

def validate_url(url):
    """ 
    Validates url for requests.
    From https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return re.match(regex, url) is not None

def tag_visible(element):
    """ 
    Helper function for visible_text_from_html to determine if an element is considered visible. 
    From https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def visible_text_from_html(body):
    """ Returns a list of all visible text given the html body. """
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    # Trim visible_texts off empty strings and return as a list rather than as a filter iterable.
    return list(filter(None, [t.strip() for t in visible_texts])) 

def build_stop_word_regex(stop_word_list):
    """ Builds a regular expression which will match all words in the given stop_word_list. """
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = r'\b' + word + r'(?![\w-])'
        stop_word_regex_list.append(word_regex)
    return re.compile('(?u)' + '|'.join(stop_word_regex_list), re.IGNORECASE)

def generate_candidate_keywords_from_regex(sentence_list, regex, min_characters=1, max_words=10):
    """ Generates a list of keywords given regex as delimiters. """
    keyword_list = []
    for s in sentence_list:
        temp = re.sub(regex, '|', s.strip())
        phrases = temp.split('|')
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != '' and len(phrase) >= min_characters and len(phrase.split()) <= max_words:
                keyword_list.append(phrase)
    return keyword_list

def filter_string_for_keywords(string, stop_words=NLTK_stop_words):
    """
    Filter a string to extract only keywords.
        - removing stop words
        - stripping/adding punctuation
        - changing case
        - word find/replace
    RETURN: the preprocessed string in list form.
    """

    filtered_string = string.lower()

    # Removing noise
    filtered_string = re.sub(r"<[^>]*>", "", filtered_string)     # Removing any HTML tags
    filtered_string = re.sub(r"\d+", "", filtered_string)         # Removing all digits
    filtered_string = re.sub(r"\"", "", filtered_string)          # Replacing apostrophe with null
    filtered_string = re.sub(r"\W", " ", filtered_string)         # Removing all non alpha-numeric words
    filtered_string = re.sub(r"\s+", " ", filtered_string)        # Trimming multiple whitespaces

    # Removing noise words
    filtered_string_list = filtered_string.split()
    final_filtered_string_list = [word for word in filtered_string_list if word not in stop_words]
    # filtered_string = " ".join(final_filtered_string_list)

    # print(final_filtered_string_list)
    return final_filtered_string_list