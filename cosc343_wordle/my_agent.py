__author__ = "Shay Stevens"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "stesh969@student.otago.ac.nz"

# import operator module
import operator

import numpy as np


def checkMultipleLetters(word):
    """
    Checks if a word contains multiple of the same letter.

    Parameters
    ----------
    word - The word (String) that is being checked

    Returns
    -------
    True if the word contains multiple of the same letter else false
    """
    for letter in word:
        if word.count(letter) > 1:
            return True
    return False


def mostUniqueWord(dictionary, correct_letters, partial_letters):
    """
    * This function is no longer used
    Finds the unique word within a given dictionary, correct letters and partial letters.

    Parameters
    ----------
    dictionary - Dictionary list to find the unique word from
    correct_letters - Correct letters list from previous guesses
    partial_letters - Partial letters list from previous guesses

    Returns
    -------
    A string of the unique word
    """

    # A dictionary that holds every word and score for that word
    words_score = {}

    for word in dictionary:
        score = 0

        # If a correct letter is in the word add the number of times it appears x2 to score
        for letter in correct_letters:
            if word.count(letter) > 0:
                score += word.count(letter) * 2

        # If a partial letter is in the word and not in correct letter list add the number of times it appears to score
        for letter in partial_letters:
            if word.count(letter) > 0 and letter not in correct_letters:
                score += word.count(letter)

        # Update the scores
        words_score.update({word: score})

    # Get the unique word (The word with the minimum score)
    unique_word = min(words_score, key=lambda k: words_score[k])

    # If the unique word contains multiple of the same letter get the next unique word
    while checkMultipleLetters(unique_word) and len(words_score) > 1:
        del words_score[unique_word]
        unique_word = min(words_score, key=lambda k: words_score[k])

    return unique_word


def bestWord(dictionary, word_length):
    """
    Finds the word with the highest frequency within a given dictionary with a word length.

    Parameters
    ----------
    dictionary - Dictionary list to find the best word from
    word_length - The length of the words inside the dictionary (int)

    Returns
    -------
    Returns a string of the best word
    """

    # Dictionary to hold every letter and frequency for that letter
    frequency_dictionary = {}

    for word in dictionary:
        for letter in word:
            frequency_dictionary = letterDictionary(frequency_dictionary, letter)

    # List of length word length that contains the letters with the highest frequency
    best_letters = list(
        dict(sorted(frequency_dictionary.items(), key=operator.itemgetter(1), reverse=True)[:word_length]).keys())

    # Dictionary that holds the score for every word with respect to the top letter frequencies
    word_score = {}

    for word in dictionary:
        score = 0
        for i in range(0, len(best_letters)):
            if best_letters[i] in word:
                score += 1  # word_length - i

        word_score.update({word: score})

    # Best word string is the word with the top score
    best_word = max(word_score, key=lambda k: word_score[k])

    return best_word


def letterDictionary(letter_dictionary, letter):
    """
    This function takes a dictionary and a letter and updates the dictionary and returns the updated dictionary.

    Parameters
    ----------
    letter_dictionary - The dictionary that needs to be updated
    letter - The letter (Char) that will be used to update the dictionary

    Returns
    -------
    The updated dictionary
    """

    count = 1
    if letter_dictionary.get(letter) is not None:
        # Update the dictionary with the previous value + 1
        count = letter_dictionary.get(letter) + 1
        letter_dictionary.update({letter: count})
    else:
        # Update the dictionary with the new value
        letter_dictionary.update({letter: count})

    return letter_dictionary


def letterDictionaryIndexes(letter_dictionary, letter, index):
    """
    Function that updates an index dictionary with a given letter and index and returns the updated dictionary.

    Parameters
    ----------
    letter_dictionary - Dictionary that contains letters and their indexes
    letter - Letter (Char) that will be used to update the dictionary
    index - Index (int) that will be used to update the dictionary

    Returns
    -------
    The updated index dictionary
    """
    if letter_dictionary.get(letter) is not None:
        # If letter is inside the dictionary update the value already in there with the new value
        index_array = letter_dictionary.get(letter)
        index_array.append(index)
        letter_dictionary.update({letter: index_array})
    else:
        # If the letter is not in the dictionary update the dictionary with the new value
        index_array = [index]
        letter_dictionary.update({letter: index_array})

    return letter_dictionary


def removeCorrect(words_to_remove, word, correct_letters_keys, correct_letters_index):
    """
    Function that will check if the word contains the correct letters in the correct position if not it is added to the
    words to remove.

    Parameters
    ----------
    words_to_remove - List of the words that will be used to remove words from dictionary
    word - The word (String) that needs to be checked
    correct_letters_keys - List of correct letters
    correct_letters_index - Dictionary of letters and indexes

    Returns
    -------
    words_to_remove with or without the new word
    """
    for key in correct_letters_keys:
        indexes = correct_letters_index.get(key)
        for index in indexes:
            if key != word[index] and word not in words_to_remove:
                words_to_remove.append(word)

    return words_to_remove


def removePartial(words_to_remove, word, partial_letters, partial_letters_keys, partial_letters_index):
    """
    Function that will check if the word contains the partial letters in the word and that they are not in the same
    position as the previous guess.

    Parameters
    ----------
    words_to_remove - List of the words that will be used to remove words from dictionary
    word - The word (String) that needs to be checked
    partial_letters - Dictionary of how many times the partial letter is in the word
    partial_letters_keys - List of every partial letter
    partial_letters_index - Dictionary of the partial letters and it's indexes

    Returns
    -------
    words_to_remove with or without the new word
    """
    for key in partial_letters_keys:
        if partial_letters.get(key) > word.count(key) and word not in words_to_remove:
            words_to_remove.append(word)

        indexes = partial_letters_index.get(key)
        for index in indexes:
            if key == word[index] and word not in words_to_remove:
                words_to_remove.append(word)

    return words_to_remove


def removeIncorrect(words_to_remove, word, incorrect_letters_keys, correct_letters_keys, partial_letters_keys,
                    incorrect_letters_index):
    """
    Function that will check that the word does not contain any incorrect letters that aren't in the correct/partial
    list or in the same position.

    Parameters
    ----------
    words_to_remove - List of the words that will be used to remove words from dictionary
    word - The word (String) that needs to be checked
    incorrect_letters_keys - List of the incorrect letters (letters with state 0)
    correct_letters_keys - List of the correct letters
    partial_letters_keys - List of the partial letters
    incorrect_letters_index - Dictionary of the incorrect letters and their indexes

    Returns
    -------
    words_to_remove with or without the new word
    """

    for key in incorrect_letters_keys:
        if key in word and key not in correct_letters_keys and key not in partial_letters_keys and word not in \
                words_to_remove:
            words_to_remove.append(word)

        indexes = incorrect_letters_index.get(key)
        for index in indexes:
            if key == word[index] and word not in words_to_remove:
                words_to_remove.append(word)

    return words_to_remove


def findCorrectKeys(letter_indexes, letter_states, letters):
    """
    Function that returns a dictionary of the correct letters and their indexes
    Parameters
    ----------
    letter_indexes - letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;

    letter_states - letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).

    letters - Letters available for the game

    Returns
    -------
    A dictionary of the correct letters and their indexes
    """

    correct_letters_index = {}

    for i in range(len(letter_states)):
        if letter_states[i] == 1:
            correct_letters_index = letterDictionaryIndexes(correct_letters_index, letters[letter_indexes[i]], i)

    return correct_letters_index


def findPartialKeys(letter_indexes, letter_states, letters):
    """
    Function that returns a dictionary of the partial letters and their indexes

    Parameters
    ----------
    letter_indexes - letter_indexes is a list of indexes of letters from self.letters corresponding to
                        the previous guess, a list of -1's on guess 0;

    letter_states - letter_states is a list of the same length as letter_indexes, providing feedback about the
                        previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                        letter was not found in the solution), -1 (the correspond letter is found in the
                        solution, but not in that spot), 1 (the corresponding letter is found in the solution
                        in that spot).

    letters - Letters available for the game

    Returns
    -------
    A dictionary of the partial letters and their indexes
    """

    partial_letters_index = {}

    for i in range(len(letter_states)):
        if letter_states[i] == -1:
            partial_letters_index = letterDictionaryIndexes(partial_letters_index, letters[letter_indexes[i]], i)

    return partial_letters_index


def removeNonMatchingEasy(dictionary, correct_letters, partial_letters):
    """
    This function is no longer used but was used for my easy mode implementation
    Parameters
    ----------
    dictionary
    correct_letters
    partial_letters

    Returns
    -------

    """
    # words to remove array
    words_to_remove = []

    correct_letters_keys = list(correct_letters)
    partial_letters_keys = list(partial_letters)

    for word in dictionary:
        if len(correct_letters_keys) > 0:
            words_to_remove = removeCorrect(words_to_remove, word, correct_letters_keys, correct_letters)

        if len(partial_letters_keys) > 0:
            words_to_remove = removePartial(words_to_remove, word, partial_letters, partial_letters_keys,
                                            partial_letters)

    for word in words_to_remove:
        dictionary.remove(word)

    return dictionary


def removeWordsEasy(dictionary, letter_indexes, letter_states, letters):
    """
    This function is no longer used but was used for my easy mode implementation
    Parameters
    ----------
    dictionary
    letter_indexes
    letter_states
    letters

    Returns
    -------

    """
    # Dictionaries that contain the letter and the number of times it appears in the word
    incorrect_letters = {}

    # Dictionaries that contain the letter and it's indexes in the word
    incorrect_letters_index = {}

    # words to remove array
    words_to_remove = []

    for i in range(len(letter_states)):
        if letter_states[i] == 0:
            incorrect_letters = letterDictionary(incorrect_letters, letters[letter_indexes[i]])
            incorrect_letters_index = letterDictionaryIndexes(incorrect_letters_index, letters[letter_indexes[i]], i)

        # Keys of each dictionary
        correct_letters_keys = list(findCorrectKeys(letter_indexes, letter_states, letters))
        partial_letters_keys = list(findPartialKeys(letter_indexes, letter_states, letters))
        incorrect_letters_keys = list(incorrect_letters)

        for word in dictionary:
            if len(incorrect_letters_keys) > 0:
                words_to_remove = removeIncorrect(words_to_remove, word, incorrect_letters_keys, correct_letters_keys,
                                                  partial_letters_keys, incorrect_letters_index)

        for word in words_to_remove:
            dictionary.remove(word)

        return dictionary


def removeWords(dictionary, letter_indexes, letter_states, letters):
    """
    Function that returns the dictionary with all the words removed that aren't possible solutions for the game.

    Parameters
    ----------
    dictionary - Dictionary list of words for the round that need to be checked

    letter_indexes - letter_indexes is a list of indexes of letters from self.letters corresponding to
                        the previous guess, a list of -1's on guess 0;

    letter_states - letter_states is a list of the same length as letter_indexes, providing feedback about the
                        previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                        letter was not found in the solution), -1 (the correspond letter is found in the
                        solution, but not in that spot), 1 (the corresponding letter is found in the solution
                        in that spot).

    letters - Letters available for the game

    Returns
    -------
    The updated dictionary list that only contains the possible words
    """
    # Dictionaries that contain the letter and the number of times it appears in the word
    incorrect_letters = {}
    partial_letters = {}
    correct_letters = {}

    # Dictionaries that contain the letter and it's indexes in the word
    correct_letters_index = {}
    partial_letters_index = {}
    incorrect_letters_index = {}

    # words to remove array
    words_to_remove = []

    # Add values to the letter dictionaries and letter index dictionaries
    for i in range(len(letter_states)):
        if letter_states[i] == 1:
            correct_letters = letterDictionary(correct_letters, letters[letter_indexes[i]])
            correct_letters_index = letterDictionaryIndexes(correct_letters_index, letters[letter_indexes[i]], i)

        elif letter_states[i] == -1:
            partial_letters = letterDictionary(partial_letters, letters[letter_indexes[i]])
            partial_letters_index = letterDictionaryIndexes(partial_letters_index, letters[letter_indexes[i]], i)

        else:
            incorrect_letters = letterDictionary(incorrect_letters, letters[letter_indexes[i]])
            incorrect_letters_index = letterDictionaryIndexes(incorrect_letters_index, letters[letter_indexes[i]], i)

    # Keys of each dictionary
    correct_letters_keys = list(correct_letters)
    partial_letters_keys = list(partial_letters)
    incorrect_letters_keys = list(incorrect_letters)

    # Add words that aren't possible to words_to_remove array
    for word in dictionary:
        if len(incorrect_letters_keys) > 0:
            words_to_remove = removeIncorrect(words_to_remove, word, incorrect_letters_keys, correct_letters_keys,
                                              partial_letters_keys, incorrect_letters_index)

        if len(correct_letters_keys) > 0:
            words_to_remove = removeCorrect(words_to_remove, word, correct_letters_keys, correct_letters_index)

        if len(partial_letters_keys) > 0:
            words_to_remove = removePartial(words_to_remove, word, partial_letters, partial_letters_keys,
                                            partial_letters_index)

    # Remove words in dictionary that are in words_to_remove array
    dictionary = list(filter(lambda word: word not in words_to_remove, dictionary))

    return dictionary


class WordleAgent:
    """
          A class that encapsulates the code dictating the
          behaviour of the Wordle playing agent

          ...

          Attributes
          ----------
          dictionary : list
              a list of valid words for the game
          letters : list
              a list containing valid characters in the game
          word_length : int
              the number of letters per guess word
          num_guesses : int
              the max. number of guesses per game
          mode: str
              indicates whether the game is played in 'easy' or 'hard' mode

          Methods
          -------
          AgentFunction(percepts)
              Returns the next word guess given state of the game in percepts
          """

    # list of words for the round
    roundDictionary: list

    # dictionary containing the correct letters and index
    correct_letters: dict = {}

    # dictionary containing the partial letters and index
    partial_letters: dict = {}

    def __init__(self, dictionary, letters, word_length, num_guesses, mode):
        """
      :param dictionary: a list of valid words for the game
      :param letters: a list containing valid characters in the game
      :param word_length: the number of letters per guess word
      :param num_guesses: the max. number of guesses per game
      :param mode: indicates whether the game is played in 'easy' or 'hard' mode
      """

        self.dictionary = dictionary
        self.letters = letters
        self.word_length = word_length
        self.num_guesses = num_guesses
        self.mode = mode

    def AgentFunction(self, percepts):
        """Returns the next word guess given state of the game in percepts

      :param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
               guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
               letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;
               letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).
      :return: string - a word from self.dictionary that is the next guess
      """
        # Extract three different parts of percepts.
        guess_counter, letter_indexes, letter_states = percepts

        self.partial_letters = findPartialKeys(letter_indexes, letter_states, self.letters)
        self.correct_letters = findCorrectKeys(letter_indexes, letter_states, self.letters)

        if guess_counter == 0:
            # Make a copy of the dictionary and set it to the dictionary for the round
            self.roundDictionary = self.dictionary.copy()
        else:
            # Update the round dictionary with only the possible words
            self.roundDictionary = removeWords(self.roundDictionary, letter_indexes, letter_states, self.letters)

        '''if len(self.roundDictionary) > 1 and guess_counter == 0:
            guess = mostUniqueWord(self.roundDictionary, self.correct_letters, self.partial_letters)
        elif len(self.roundDictionary) > 1 and guess_counter > 0:
            guess = bestWord(self.roundDictionary, self.word_length)
        else:
            guess = self.roundDictionary[0]'''

        if len(self.roundDictionary) > 1 and len(self.correct_letters) + len(self.partial_letters) \
                < self.word_length - 1:
            guess = bestWord(self.roundDictionary, self.word_length)
        else:
            word_index = np.random.randint(0, len(self.roundDictionary))
            guess = self.roundDictionary[word_index]

        return guess
