import re
import requests
import sys
from .preprocess import visible_text_from_html
from .filter import filter_string_for_keywords

class Keyworder:
    """
    Keyworder class.
    """
    def __init__(self, url="https://stackoverflow.com"):
        self.url = url
        self.page = requests.get(url)
        self.visible_text = visible_text_from_html(self.page.content)

        # Build a collection of standalone words through preprocessing the visible_text
        self.keyword_collection = []
        for sentence in self.visible_text:
            self.keyword_collection.extend(filter_string_for_keywords(sentence))

        # Count the occurence of each keyword and store it into a dict
        self.keyword_count = {}
        for keyword in self.keyword_collection:
            if not keyword in self.keyword_count:
                self.keyword_count[keyword] = 1
            else:
                self.keyword_count[keyword] += 1
    
    def print_keywords(self, num=10):
        # Output the top keywords
        print(str(len(self.keyword_count)) + " visible unique keywords in " + str(self.url))
        print_count = 0
        for keyword in sorted(self.keyword_count, key=self.keyword_count.get, reverse=True):
            print(print_count, self.keyword_count[keyword], keyword)
            print_count += 1
            if (print_count >= num):
                break