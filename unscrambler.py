#!python3
import json
from collections import Counter
import os.path
import urllib.request
import time

DICTIONARY_FILENAME = "words_dictionary.json"
DICTIONARY_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"


count = 0
items = Counter()
words_dict = None
matches = []
digested_dictionary = {}


def load_dictionary():
    global words_dict
    if not os.path.isfile(DICTIONARY_FILENAME):
        try:
            urllib.request.urlretrieve(DICTIONARY_URL, DICTIONARY_FILENAME)
        except Exception as e:
            print('Unable to download dictionary!')
            raise e
    with open(DICTIONARY_FILENAME, "r") as f:
        words_dict = json.load(f)


def digest_word(word):
    return ''.join(sorted(word))


def generate_digest_dictionary():

    if not words_dict:
        load_dictionary()
    digested_dictionary = {}
    results = {}
    longest = 1
    temp_dict = {}
    for word in words_dict:
        digested = digest_word(word)
        res = digested_dictionary.get(digested, [])
        res.append(word)
        digested_dictionary[digested] = res
        if len(res) >= longest:
            longest = len(res)
            # print(res)
        if results.get(len(word), {}).get('anagrams_count', 0) < len(res):
            temp_dict = dict(anagrams_count=len(res),
                             anagrams=res)
            results[len(word)] = temp_dict
    for item, val in results.items():
        if val['anagrams_count'] > 1:
            print("{}, {}".format(item, val))
    return digested_dictionary


def show_word_with_increment(target, start, inc):
    head = target[:start]
    tail = target[start:]
    return list(head)+[tail[(i+inc) % (len(tail))] for i in range(len(tail))]


def handle_word(target, start, verbose=False):
    global count

    for i in range(0, len(target)-start):
        handle_word(show_word_with_increment(
            target, start, i), start+1)
    if start == len(target):
        count += 1
        items[str(target)] += 1
        if(''.join(target) in words_dict):
            global matches
            if verbose:
                print("match!: "+''.join(target))
            matches.append(''.join(target))


def _solve_anagram(target):
    global matches
    matches = []
    handle_word(target, 0)
    return matches.copy()


def _solve_anagram_quick(target, dig_dict=generate_digest_dictionary()):
    return dig_dict[digest_word(target)]


def _check_for_word_subset(a, b):
    # Return true, XXXX if a is sub of b, XXXX, true if b is sub of a
    a = list(a)
    b = list(b)
    only_a_has = []
    only_b_has = []
    for char in a:

        if char in b:
            del b[b.index(char)]
        else:
            only_a_has.append(char)
    only_b_has = b
    return len(only_a_has) == 0, len(only_b_has) == 0


def _solve_anagram_quick_including_subsets(
        target, dig_dict=generate_digest_dictionary()):
    all_anagrams = []
    dig_target = digest_word(target)
    for word, agrams in dig_dict.items():
        if _check_for_word_subset(word, dig_target)[0]:
            all_anagrams += agrams

    return all_anagrams


print(_solve_anagram_quick_including_subsets("eohll"))


def solve_anagram():
    load_dictionary()
    target = str(input("enter a word: "))
    start_time = time.time()
    handle_word(target, 0)
    end_time = time.time()
    print("{} permutations attempted against a dictionary of {} words".format(
        count, len(words_dict)))
    print("Took {} seconds".format(end_time-start_time))
    print("{} matches found".format(len(matches)))
    for match in matches:
        print(" - {}".format(match))


def find_most_common_anagram_brute_force(min_length=3):
    results = {}

    load_dictionary()
    total_words = len(words_dict)

    for i, word in enumerate(words_dict):
        print("\r {}, word {}  of {} ".format(word, i, total_words))
        if len(word) > min_length:
            res = _solve_anagram(word)
            if len(res) > 2:
                print(res)
                if results.get(len(word), {}).get('anagrams_count', 0) > len(res):
                    temp_dict = dict(anagrams_count=len(res),
                                     anagrams=res, word=word)
                    results[len(word)] = temp_dict
                    print(temp_dict)

    print(results)


# solve_anagram()
# find_most_common_anagram()
# generate_digest_dictionary()
# print(_solve_anagram_quick("sbcsiea"))
