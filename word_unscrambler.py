#!python3
import json
from collections import Counter

with open("/home/miles/workspace/words_dictionary.json", "r") as f:
    words_dict = json.load(f)


count = 0
items = Counter()

scrambled = str(input("enter a word: "))
target = scrambled


def show_word_with_increment(target, start, inc):
    head = target[:start]
    tail = target[start:]
    return list(head)+[tail[(i+inc) % (len(tail))] for i in range(len(tail))]


def handle_word(target, start, recurse=False):
    global count
    for i in range(0, len(target)-start):
        handle_word(show_word_with_increment(
            target, start, i), start+1, recurse=True)
    if start == len(target):
        count += 1
        items[str(target)] += 1
        if(''.join(target) in words_dict):
            print("match!: "+''.join(target))


handle_word(target, 0)
print("permutations attempted>  {}".format(count))
