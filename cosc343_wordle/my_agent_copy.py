__author__ = "Shay Stevens"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "stesh969@student.otago.ac.nz"

import operator
import numpy as np

def checkMultipleLetters(word):
   for letter in word:
      if word.count(letter) > 1:
         return True
   return False

def mostUniqueWord(dictionary, correct_letters, partial_letters):
   words_score = {}

   for word in dictionary:
      score = 0
      for letter in correct_letters:
         if word.count(letter) > 0:
            score += word.count(letter)

      for letter in partial_letters:
         if word.count(letter) > 0 and letter not in correct_letters:
            score += word.count(letter)

      words_score.update({word: score})

   unique_word = min(words_score, key=lambda k: words_score[k])

   while checkMultipleLetters(unique_word) and len(words_score) > 1:
      del words_score[unique_word]
      unique_word = min(words_score, key=lambda k: words_score[k])

   return unique_word



def bestWord(dictionary, word_length):
   frequency_dictionary = {}
   for word in dictionary:
      for letter in word:
         frequency_dictionary = letterDictionary(frequency_dictionary, letter)

   best_letters = list(dict(sorted(frequency_dictionary.items(), key=operator.itemgetter(1), reverse=True)[:word_length]).keys())
   word_score = {}

   for word in dictionary:
      score = 0
      for i in range(0, len(best_letters)):
         if best_letters[i] in word:
            score += word_length - i

      word_score.update({word: score})

   best_word = list(dict(sorted(word_score.items(), key=operator.itemgetter(1), reverse=True)[:1]).keys())[0]

   return best_word


def letterDictionary(letter_dictionary, letter):
   count = 1
   if letter_dictionary.get(letter) != None:
      count = letter_dictionary.get(letter) + 1
      letter_dictionary.update({letter: count})
   else:
      letter_dictionary.update({letter: count})

   return letter_dictionary


def letterDictionaryIndexes(letter_dictionary, letter, index):
   if letter_dictionary.get(letter) != None:
      indexArray = letter_dictionary.get(letter)
      indexArray.append(index)
      letter_dictionary.update({letter: indexArray})
   else:
      indexArray = []
      indexArray.append(index)
      letter_dictionary.update({letter: indexArray})

   return letter_dictionary


def removeCorrect(words_to_remove, word, correct_letters_keys, correct_letters_index):
   for key in correct_letters_keys:
      indexes = correct_letters_index.get(key)
      for index in indexes:
         if key != word[index] and word not in words_to_remove:
            words_to_remove.append(word)

   return words_to_remove


def removePartial(words_to_remove, word, partial_letters, partial_letters_keys, partial_letters_index):
   for key in partial_letters_keys:
      if partial_letters.get(key) > word.count(key) and word not in words_to_remove:
         words_to_remove.append(word)

      indexes = partial_letters_index.get(key)
      for index in indexes:
         if key == word[index] and word not in words_to_remove:
            words_to_remove.append(word)

   return words_to_remove

def removeIncorrect(words_to_remove, word, incorrect_letters_keys, correct_letters_keys, partial_letters_keys, incorrect_letters_index):
   for key in incorrect_letters_keys:
      if key in word and key not in correct_letters_keys and key not in partial_letters_keys and word not in words_to_remove:
         words_to_remove.append(word)

      indexes = incorrect_letters_index.get(key)
      for index in indexes:
         if key == word[index] and word not in words_to_remove:
            words_to_remove.append(word)

   return words_to_remove


def findCorrectKeys(letter_indexes, letter_states, letters):
   correct_letters_index = {}

   for i in range(len(letter_states)):
      if letter_states[i] == 1:
         correct_letters_index = letterDictionaryIndexes(correct_letters_index, letters[letter_indexes[i]], i)


   return correct_letters_index


def findPartialKeys(letter_indexes, letter_states, letters):
   partial_letters_index = {}

   for i in range(len(letter_states)):
      if letter_states[i] == -1:
         partial_letters_index = letterDictionaryIndexes(partial_letters_index, letters[letter_indexes[i]], i)

   return partial_letters_index

def removeNonMatchingEasy(dictionary, correct_letters, partial_letters):
   # words to remove array
   words_to_remove = []

   correct_letters_keys = list(correct_letters)
   partial_letters_keys = list(partial_letters)

   for word in dictionary:
      if(len(correct_letters_keys) > 0):
         words_to_remove = removeCorrect(words_to_remove, word, correct_letters_keys, correct_letters)

      if(len(partial_letters_keys) > 0):
         words_to_remove = removePartial(words_to_remove, word, partial_letters, partial_letters_keys, partial_letters)

   for word in words_to_remove:
      dictionary.remove(word)

   return dictionary

def removeWordsEasy(dictionary, letter_indexes, letter_states, letters):
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
         if (len(incorrect_letters_keys) > 0):
            words_to_remove = removeIncorrect(words_to_remove, word, incorrect_letters_keys, correct_letters_keys,
                                              partial_letters_keys, incorrect_letters_index)

      for word in words_to_remove:
         dictionary.remove(word)

      return dictionary

def removeWords(dictionary, letter_indexes, letter_states, letters):
   # Dictionaries that contain the letter and the number of times it appears in the word
   incorrect_letters = {}
   partial_letters = {}
   correct_letters = {}

   # Dictionaries that contain the letter and it's indexes in the word
   correct_letters_index = {}
   partial_letters_index = {}
   incorrect_letters_index = {}

   #words to remove array
   words_to_remove = []

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

   for word in dictionary:
      if(len(correct_letters_keys) > 0):
         words_to_remove = removeCorrect(words_to_remove, word, correct_letters_keys, correct_letters_index)

      if(len(incorrect_letters_keys) > 0):
         words_to_remove = removeIncorrect(words_to_remove, word, incorrect_letters_keys, correct_letters_keys, partial_letters_keys, incorrect_letters_index)

      if(len(partial_letters_keys) > 0):
         words_to_remove = removePartial(words_to_remove, word, partial_letters, partial_letters_keys, partial_letters_index)

   for word in words_to_remove:
      dictionary.remove(word)

   return dictionary


class WordleAgent():
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

   roundDictionary: list
   correct_letters: dict = {}
   partial_letters: dict = {}

   def __init__(self, dictionary,letters,word_length,num_guesses,mode):
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

      partial_letters = findPartialKeys(letter_indexes, letter_states, self.letters)
      correct_letters = findCorrectKeys(letter_indexes, letter_states, self.letters)

      if 0 < guess_counter < self.num_guesses:
         self.roundDictionary = removeWords(self.roundDictionary, letter_indexes, letter_states, self.letters)

      elif guess_counter == 0:
         self.roundDictionary = self.dictionary.copy()

      # Randomly pick an index from the entire dictionary
      if len(self.roundDictionary) > 1 and guess_counter == 0:
         guess = mostUniqueWord(self.roundDictionary, self.correct_letters, self.partial_letters)
         #guess = bestWord(self.roundDictionary, self.word_length)

      elif len(self.roundDictionary) > 1 and guess_counter > 0:
         guess = bestWord(self.roundDictionary, self.word_length)
         #guess = mostUniqueWord(self.roundDictionary, self.correct_letters, self.partial_letters)

      else:
         guess = self.roundDictionary[0]

      """elif len(self.roundDictionary) > 1:
         word_index = np.random.randint(0, len(self.roundDictionary))
         guess = self.roundDictionary[word_index]"""
      return guess
