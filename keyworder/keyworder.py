import os
import re
import requests
import sys
from .preprocess import (separate_words, validate_url, visible_text_from_html, build_stop_word_regex, generate_candidate_keywords_from_regex)
from nltk.tokenize import sent_tokenize

def nltk_stoplist():
    from .stoplists import nltk_stoplist
    return nltk_stoplist.words()


class Keyworder:
    """
    Keyworder class.
    """

    test = "Criteria of compatibility of a system of linear Diophantine equations, strict inequations, \
            and nonstrict inequations are considered. Upper bounds for components of a minimal set \
            of solutions and algorithms of construction of minimal generating sets of solutions for all \
            types of systems are given. These criteria and the corresponding algorithms for \
            constructing a minimal supporting set of solutions can be used in solving all the \
            considered types of systems and systems of mixed types."

    def __init__(self, stop_words):
        # Checks if stop_words is given as a list or text file string
        # try:
        #     if isinstance(stop_words, list):
        self.stop_words = stop_words
        #     else if (os.path.isfile(stop_words)):
        #         self.stop_words = open(stop_words).read().splitlines()
        #     else: 
        #         raise TypeError("Provided stop_words type not supported. \
        #                         stop_words should be either a list or filepath.")
        # except TypeError as error:
        #     print(error)
    
    def extract_keywords_from_url(self, url):
        """
        Given a url source, extracts keywords from visible text in the url using the defined stop_words.

        @param url String of the url to be scraped
        @return list List of sentences
        """
        try:
            if not validate_url(url):
                raise ValueError()
        except ValueError:
            print("Invalid URL '" + url + "'")
            return None

        self.source = url
        page = requests.get(url)
        visible_text = visible_text_from_html(page.content)
        regex = build_stop_word_regex(self.stop_words)
        candidate_keywords = generate_candidate_keywords_from_regex(visible_text, regex) 
        return candidate_keywords
    
    def extract_keywords_from_text(self, text):
        regex = build_stop_word_regex(self.stop_words)
        candidate_keywords = generate_candidate_keywords_from_regex(sent_tokenize(text), regex) 
        return candidate_keywords

    def calculate_word_scores(self, candidate_keywords):
        word_frequency = {}
        word_degree = {}
        for keyword in candidate_keywords:
            word_list = separate_words(keyword)
            word_list_length = len(word_list)
            word_list_degree = word_list_length - 1
            for word in word_list:
                word_frequency.setdefault(word, 0)
                word_frequency[word] += 1
                word_degree.setdefault(word, 0)
                word_degree[word] += word_list_degree
        for item in word_frequency:
            word_degree[item] = word_degree[item] + word_frequency[item]

        # Calculate Word scores = deg(w)/frew(w)
        word_scores = {}
        for item in word_frequency:
            word_scores.setdefault(item, 0)
            word_scores[item] = word_degree[item] / (word_frequency[item] * 1.0)
        return word_scores

    def generate_candidate_keyword_scores(self, candidate_keywords, word_scores, min_frequency=1):
        candidate_keyword_scores = {}
        for keyword in candidate_keywords:
            if candidate_keywords.count(keyword) >= min_frequency:
                candidate_keyword_scores.setdefault(keyword, 0)
                word_list = separate_words(keyword)
                candidate_score = 0
                for word in word_list:
                    candidate_score += word_scores[word]
                candidate_keyword_scores[keyword] = candidate_score
        return candidate_keyword_scores

    def top_keyword_scores(self, candidate_keywords, num=10, min_frequency=1):
        word_scores = self.calculate_word_scores(candidate_keywords)
        keyword_scores = self.generate_candidate_keyword_scores(candidate_keywords, word_scores, min_frequency)

        count = 1
        top_keyword_scores_list = []
        for keyword in sorted(keyword_scores, key=keyword_scores.get, reverse=True):
            top_keyword_scores_list.append((keyword_scores[keyword], keyword))
            count += 1
            if (count >= num): break
        return top_keyword_scores_list
        
    def top_freq_keywords(self, keyword_list, lines=10, log=False):
        # Output the top keywords
        keyword_count = self.__count_keywords(keyword_list)
        if (log):
            print("Top keywords from " + self.source)
            print("%4s %5s %15s" % ("Rank", "Freq", "Keyword"))

        print_count = 1
        total_keywords = 0
        for keyword in sorted(keyword_count, key=keyword_count.get, reverse=True):
            if(log): print("%4d %5d %15s" % (print_count, keyword_count[keyword], keyword))
            
            print_count += 1
            total_keywords += keyword_count[keyword]
            if (print_count > lines): break

        if (log): print("%5d total keywords, %5d unique keywords" % (total_keywords, len(keyword_count)))
    
    def __count_keywords(self, keyword_list):
        # Count the occurence of each keyword and store it into a dict
        keyword_count = {}
        for keyword in keyword_list:
            if not keyword in keyword_count:
                keyword_count[keyword] = 1
            else:
                keyword_count[keyword] += 1
        return keyword_count

    # def set_url(self, new_url):
    #     self.url = new_url
    #     self.refresh()
    
    # def refresh(self):
    #     self.page = requests.get(self.url)
    #     self.visible_text = visible_text_from_html(self.page.content)
        
    #     self.keyword_collection = []
    #     keyword_count = {}
    #     self.__count_keywords()