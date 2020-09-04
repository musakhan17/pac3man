import random
import glob
import sys

"""
Markov Babbler

After being trained on text from various authors, can
'babble', or generate random walks, and produce text that
vaguely sounds like the author.
"""


class Babbler:
    def __init__(self, n, seed=None):
        """
        n is the length of an n-gram for state.
        seed is the seed for a random number generation. If none given use the default.
        """
        self.n = n
        if seed != None:
            random.seed(seed)
        # TODO: your code goes here
        self.ngram_map = {}
        self.ngram2 = []
        self.starters = []
        self.stoppers = []

    def add_sentence(self, sentence):
        """
        Process the given sentence.
        The sentence is a string separated by spaces. Break it into
        words using split(). Convert each word to lowercase using lower().
        Then start processing n-grams and updating your states.
        Remember to track starters (i.e. n-grams that being sentences),
        stoppers (i.e. n-grams that end a sentence), and that
        stoppers (i.e. n-grams that end a sentence), and that
        any n-grams that stops a sentence should be followed by the
        special symbol 'EOL' in the state transition table. 'EOL' is short
        for 'end of line', and since it is capitalized and all of the
        text from the book is lower-case, it will be unambiguous.
        """
        self.ngram2 = sentence.lower()
        self.ngram2 = sentence.split()
        letter_list = self.ngram2[0:self.n]
        x = ' '.join(letter_list)

        for i in self.ngram2[self.n:]:
            if x in self.ngram_map:
                self.ngram_map[x].append(i)
            else:
                self.ngram_map[x] = [i]
            letter_list.pop(0)
            letter_list.append(i)
            x = ' '.join(letter_list)

        if x in self.ngram_map:
            self.ngram_map[x].append('EOL')
        else:
            self.ngram_map[x] = ['EOL']

        self.stoppers.append(' '.join(self.ngram2[len(self.ngram2) - self.n:]))
        self.starters.append(' '.join(self.ngram2[0:self.n]))

    def add_file(self, filename):
        """
        This method done for you. It just calls your add_sentence() method
        for each line of an input file. We are assuming that the input data
        has already been pre-processed so that each sentence is on a separate line.
        """
        for line in [line.rstrip().lower() for line in open(filename, errors='ignore').readlines()]:
            self.add_sentence(line)

    def get_starters(self):
        """
        Return a list of all of the n-grams that start any sentence we've seen.
        The resulting list may contain duplicates, because one n-gram may start
        multiple sentences.
        """
        return self.starters

    def get_stoppers(self):
        """
        Return a list of all the n-grams that stop any sentence we've seen.
        The resulting value may contain duplicates, because one n-gram may stop
        multiple sentences.
        """
        return self.stoppers

    def get_successors(self, ngram):
        """
        Return a list of words that may follow a given n-gram.
        The resulting list may contain duplicates, because each
        n-gram may be followed by different words. For example,
        suppose an author has the following sentences:
        'the dog dances quickly'
        'the dog dances with the cat'
        'the dog dances with me'

        If n=3, then the n-gram 'the dog dances' is followed by
        'quickly' one time, and 'with' two times.

        If the given state never occurs, return an empty list.
        """
        if self.ngram2 not in self.ngram_map:
            return []
        else:
            return self.ngram_map[ngram]

    def get_all_ngrams(self):
        """
        Return all the possible n-grams, or n-word sequences, that we have seen
        across all sentences.

        Probably a one-line method.
        """
        return self.ngram_map.keys()

    def has_successor(self, ngram):
        """
        Return True if the given ngram has at least one possible successor
        word, and False if it does not. This is another way of asking
        if we have ever seen a given ngram, because ngrams with no successor
        words must not have occurred in the training sentences.
        """
        if ngram in self.ngram_map:
            return True
        else:
            return False

    def get_random_successor(self, ngram):
        """
        Given an n-gram, randomly pick from the possible words
        that could follow that n-gram. The randomness should take into
        account how likely a word is to follow the given n-gram.
        For example, if n=3 and we train on these three sentences:
        'the dog dances quickly'
        'the dog dances with the cat'
        'the dog dances with me'

        and we call get_random_next_word() for the state 'the dog dances',
        we should get 'quickly' about 1/3 of the time, and 'with' 2/3 of the time.
        """

        temp_list = self.get_successors(ngram)
        weight = 1
        temp_map = {}

        for i in temp_list:
            if i not in temp_map:
                temp_map[i] = 1
            else:
                temp_map[i] = temp_map[i] + 1

        for j in temp_map.values():
            weight = weight + j

        x = random.randint(1, weight)
        check = True
        while check:
            for k in temp_map.keys():
                if temp_map[k] <= 0:
                    return k
                else:
                    temp_map[k] = temp_map[k] - x

    def babble(self):
        """
        Generate a random sentence using the following algorithm:

        1: Pick a starter ngram. This is the current ngram, and also
        the current sentence so far.
        Suppose the starter ngram is 'a b c'

        2: Choose a successor word based on the current ngram.
        3: If the successor word is 'EOL', then return the current sentence.
        4: Otherwise, add the word to the end of the sentence
        (meaning sentence is now 'a b c d')
        5: Also add the word to the end of the current ngram, and
        remove the first word from the current ngram.
        This produces 'b c d' for our example.
        6: Repeat step #2 until you generate 'EOL'.

        ngram_start = random.choice(self.get_starters())
        letters = ngram_start
        successor = self.get_random_successor(ngram_start)
        while successor is not 'EOL':
            successor += ' ' + successor
            letters_list2 = ngram_start.split()
            letters_list2.pop(0)
            letters_list2.append(successor)
            ngram_start = ' '.join(letters_list2)
            successor = self.get_random_successor(ngram_start)
        return letters
        """

        ngram_start = random.choice(self.get_starters())
        sentence = ngram_start
        successor = self.get_random_successor(ngram_start)
        while successor != 'EOL':
            sentence += ' ' + successor
            letters_list2 = ngram_start.split()
            letters_list2.pop(0)
            letters_list2.append(successor)
            ngram_start = ' '.join(letters_list2)
            successor = self.get_random_successor(ngram_start)
        return sentence


def main(n=2, filename='tests/test3.txt', num_sentences=40):
    """
    Simple test driver.
    """

    print(filename)
    babbler = Babbler(n)
    babbler.add_file(filename)

    print(f'num starters {len(babbler.get_starters())}')
    print(f'num ngrams {len(babbler.get_all_ngrams())}')
    print(f'num stoppers {len(babbler.get_stoppers())}')
    for _ in range(num_sentences):
        print(babbler.babble())


if __name__ == '__main__':
    # remove the first parameter, which should be babbler.py, the name of the script
    sys.argv.pop(0)
    n = 3
    filename = 'tests/test3.txt'
    num_sentences = 5
    if len(sys.argv) > 0:
        n = int(sys.argv.pop(0))
    if len(sys.argv) > 0:
        filename = sys.argv.pop(0)
    if len(sys.argv) > 0:
        num_sentences = int(sys.argv.pop(0))
    main(n, filename, num_sentences)
