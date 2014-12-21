# Kyle Vickers
# HW6
# Main File
# CS671

import string
import collections
import string
import cipher
from string import maketrans
from collections import defaultdict

alpha_lc = string.ascii_lowercase
alpha_uc = string.ascii_uppercase


def encode(message, shift=13):
    ''' Shifts all letters in messages by shift steps
    Able to use any additional datastructures or functions.
    If no value is given to shift, it defaults to 13.
    Does not change spacing, punctuation, or non-alpha chars.
    Handles negative shifts, they are valid inputs.
    Raises ValueError for shift values above 26 or below -26.
    '''
    if shift < -26 or shift > 26:
        raise ValueError("Shift is outside of bounds")
    if shift == 0 or len(message) == 0:
        return message

    return message.translate(
        maketrans(string.ascii_lowercase + string.ascii_uppercase,
                            (''.join((string.ascii_lowercase[(shift % len(string.ascii_lowercase)):] +
                                      string.ascii_lowercase[:(shift % len(string.ascii_lowercase))])) +
                             ''.join((string.ascii_uppercase[(shift % len(string.ascii_uppercase)):] +
                                      string.ascii_uppercase[:(shift % len(string.ascii_uppercase))])))))


def tryShifts(message):
    ''' Returns a generator for finding the next logical shift
    Tries the possible shifts by most likely to least likely,
    using letter frequency in the coded message, and the ordering
    above. it should provide decoded messages lazily, returning
    a generator that gives the next most likely one each time
    '''
    mc_eng_chars_lc = list("etaoinshrdlucmfwypvbgkqjxz")
    mc_eng_chars_uc = list("etaoinshrdlucmfwypvbgkqjxz".upper())
    mc_mes_chars = commonLetters(message)
    for ei in range(len(mc_eng_chars_lc)):
        shift_amt = getShiftAmt(
            mc_eng_chars_lc, mc_eng_chars_uc, mc_mes_chars, ei, 0)
        yield cipher.encode(message, shift_amt)


def commonLetters(s):
    ''' Returns list of letters found in string s with most frequent first '''
    c = collections.Counter(getLetters(s))
    return [a for a, b in c.most_common(len(c))]


def getLetters(s):
    ''' Returns string containing just the letters it originally had '''
    in_table = string.maketrans("", "")
    out_table = in_table.translate(in_table, string.letters)
    return s.translate(in_table, out_table)


def getShiftAmt(eng_chars_lc, eng_chars_uc, mes_chars, eI, mI):
    ''' Returns the shift amount in the alphabet between two letters
    If the mes character is uppercase it checks upper case alpha
    If the mes character is lowercase it checks lower case alpha
    '''
    if mes_chars[mI].isupper():
        eng_index = alpha_uc.index(eng_chars_uc[eI])
        mes_index = alpha_uc.index(mes_chars[mI])
    else:
        eng_index = alpha_lc.index(eng_chars_lc[eI])
        mes_index = alpha_lc.index(mes_chars[mI])
    return eng_index - mes_index


class Trie:

    ''' Uses a trie to help our program quickly accept
    or reject potential words in our proposed decodings.
    In its most basic form, it must have add and __contains__.
    In addition, for any whole word, the tree should keep track
    of the number of times that word was seen in valid
    decodings. '''

    def __init__(self):
        self.value = 1
        self.size = 0
        self.children = dict()
        self.parent = None
        self.value = None
        self.words = []
        self.cnt = 0
        self.depth = 0

    def add(self, vals):
        if vals == '':
            return
        if vals[0] in self.children:
            self.children[vals[0]].add(vals[1:])
        else:
            newtrie = Trie()
            newtrie.value = [vals[0]]
            newtrie.parent = None
            self.children[vals[0]] = newtrie
            newtrie.add(vals[1:])

    def printAllChildren(self):
        if not self.children:
            return
        for x in self.children:
            print self.children[x]

    def getToAll(self):
        if not self.children:
            return

        print self
        for it in self.children:
            self.children[it].getToAll()

    def __str__(self):
        ret = ret + "count %d " % self.count
        return ret

    def __contains__(self, vals):
        if len(vals) == 0:
            return True
        if not vals[0] in self.children:
            return False

        return self.children[vals[0]].__contains__(vals[1:])

    def update(self, vals):
        if len(vals) == 0:
            self.cnt += 1
            return
        try:
            return self.children[vals[0]].update(vals[1:])
        except KeyError:
            return

    def count(self, vals):
        if len(vals) == 0:
            return self.cnt
        return self.children[vals[0]].count(vals[1:])


def decode(message, dictfilename):
    ''' Uses tryshifts and a dictionary to get potential decodings for message
    Then checks using a trie built from the list of dictionarywords stored in
    the file 'dictfilename' whether the number of real words in the possible
    decoded message is above half the total number of words in the message.
    Once such a decoding is found, the function should return the decoded
    message and the trie used for it as a tuple, never generating the later
    possible decodings. Make sure to update the word counts in the trie
    before returning.
    '''
    msg_word_count = len(message.split())
    msg_gen = tryShifts(message)

    tri = Trie()
    dict_file = open(dictfilename, 'r')
    for line in dict_file:
        tri.add(line.rstrip('\n'))
                #maybe should use strip for both head and tail of line

    for x in range(0, 26):
        msg_words = next(msg_gen).split(' ')
        cnt_passed = 0
        for cur_word in msg_words:
            if cur_word in tri:
                cnt_passed += 1
        if cnt_passed > msg_word_count / 2:
            for update_word in msg_words:
                tri.update(update_word.strip(string.punctuation))
            return (' '.join(msg_words), tri)

# decoded = decode( "hello this is a message of words", "dictionary.txt" )
# print decoded
# NLandPUNC = "\nand enterprises of great pitch and moment,\nwith this regard their currents turn awry,\nand lose the name of action."
# out_message, out_trie = decode(NLandPUNC, "dictionary.txt")
# print out_message
