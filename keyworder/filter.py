import re
from stop_words import NLTK_stop_words

def preprocess(string, stop_words=NLTK_stop_words):
    """
    Apply preprocessing to a single string. 
        - removing stop words
        - stripping/adding punctuation
        - changing case
        - word find/replace
    RETURN: the preprocessed string in list form.
    """

    processed_string = string.lower()

    # Removing noise
    processed_string = re.sub(r"<[^>]*>", "", processed_string)     # Removing any HTML tags
    processed_string = re.sub(r"\d+", "", processed_string)         # Removing all digits
    processed_string = re.sub(r"\"", "", processed_string)          # Replacing apostrophe with null
    processed_string = re.sub(r"\W", " ", processed_string)         # Removing all non alpha-numeric words
    processed_string = re.sub(r"\s+", " ", processed_string)        # Trimming multiple whitespaces

    # Removing noise words
    processed_string_list = processed_string.split()
    final_processed_string_list = [word for word in processed_string_list if word not in stop_words]
    # processed_string = " ".join(final_processed_string_list)

    # print(final_processed_string_list)
    return final_processed_string_list