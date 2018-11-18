from bs4 import BeautifulSoup
from bs4.element import Comment

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
