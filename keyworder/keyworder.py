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
        self.page = requests.get(self.url)
        self.visible_text = visible_text_from_html(self.page.content)

        self.keyword_collection = []
        self.keyword_count = {}
        self.__count_keywords()
    
    def print_keywords(self, lines=10):
        # Output the top keywords
        print("Top keywords from " + str(self.url))
        print_count = 1
        total_keywords = 0
        print("%4s %5s %15s" % ("Rank", "Freq", "Keyword"))
        for keyword in sorted(self.keyword_count, key=self.keyword_count.get, reverse=True):
            print("%4d %5d %15s" % (print_count, self.keyword_count[keyword], keyword))
            print_count += 1
            total_keywords += self.keyword_count[keyword]
            if (print_count > lines):
                break
        print ("%4d total keywords, %4d unique keywords" % (total_keywords, len(self.keyword_count)))
    
    def set_url(self, new_url):
        self.url = new_url
        self.refresh()
    
    def refresh(self):
        self.page = requests.get(self.url)
        self.visible_text = visible_text_from_html(self.page.content)
        
        self.keyword_collection = []
        self.keyword_count = {}
        self.__count_keywords()
    
    def __count_keywords(self):
        # Build a collection of standalone words through preprocessing the visible_text
        for sentence in self.visible_text:
            self.keyword_collection.extend(filter_string_for_keywords(sentence))
        # Count the occurence of each keyword and store it into a dict
        for keyword in self.keyword_collection:
            if not keyword in self.keyword_count:
                self.keyword_count[keyword] = 1
            else:
                self.keyword_count[keyword] += 1