import re
from .stop_words import NLTK_stop_words

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