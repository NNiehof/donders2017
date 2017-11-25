"""Class that checks whether user input is in the first n most commonly used
words from a given word count list.
"""

import pandas as pd
import re

textfile = "Resources/it_50k.txt"
storytext = "Resources/casino murder Italian.txt"


class WordFilter:
    """Word filter class.
    Parameters
    ----------
    n_words : int
        Include first n_words from word list in the filter
    wordcount : str
        Textfile with word count
    """
    def __init__(self, n_words=10000, wordcount=textfile):
        self.wordlist = pd.read_csv(wordcount, sep=" ", header=None,
                                    encoding="ISO-8859-1", nrows=n_words,
                                    usecols=[0], squeeze=True)

        # read in text narrative
        with open(storytext, 'r', encoding="ISO-8859-1") as story:
            for line in story:
                # keep only alphanumeric and diacritic characters
                line = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚàèìòùÀÈÌÒÙâêîôÂÊÎÔãõÃÕçÇ ]', ' ', line)
                line.encode("ISO-8859-1")
                storywords = pd.Series(list(filter(None, line.split(" "))))
                # skip lines with only whitespace
                if not storywords.empty:
                    self.wordlist = pd.concat([self.wordlist, storywords],
                                              axis=0, ignore_index=True)

        self.student_words = None

    def filter_text(self, user_input):
        """
        Parameters
        ----------
        user_input : str
            String of words to check for presence in word list

        Returns
        -------
        None or tuple
            None if all user input was present in the word list. Return a tuple
            with (index, word) of the first word not present in the list.
        """
        self.student_words = user_input.split()
        for ind_w, word in enumerate(self.student_words):
            if self.wordlist.str.contains(word).any():
                pass
            else:
                return (ind_w, word)
        return None


if __name__ == "__main__":
    filt = WordFilter()
    excl_words = filt.filter_text("che la appeltaart")
    print(excl_words)
    print(filt.wordlist)
