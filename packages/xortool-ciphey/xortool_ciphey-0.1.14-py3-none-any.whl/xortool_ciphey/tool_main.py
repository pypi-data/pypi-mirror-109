#!/usr/bin/env python3

__doc__ = f"""
xortool
  A tool to do some xor analysis:
  - guess the key length (based on count of equal chars)
  - guess the key (base on knowledge of most frequent char)

Usage:
  xortool [-x] [-m MAX-LEN] [-f] [-t CHARSET] [FILE]
  xortool [-x] [-l LEN] [-c CHAR | -b | -o] [-f] [-t CHARSET] [-p PLAIN] [FILE]
  xortool [-x] [-m MAX-LEN| -l LEN] [-c CHAR | -b | -o] [-f] [-t CHARSET] [-p PLAIN] [FILE]
  xortool [-h | --help]
  xortool --version

Options:
  -x --hex                          input is hex-encoded str
  -l LEN, --key-length=LEN          length of the key
  -m MAX-LEN, --max-keylen=MAX-LEN  maximum key length to probe [default: 65]
  -c CHAR, --char=CHAR              most frequent char (one char or hex code)
  -b --brute-chars                  brute force all possible most frequent chars
  -o --brute-printable              same as -b but will only check printable chars
  -f --filter-output                filter outputs based on the charset
  -t CHARSET --text-charset=CHARSET target text character set [default: printable]
  -p PLAIN --known-plaintext=PLAIN  use known plaintext for decoding
  -h --help                         show this help

Notes:
  Text character set:
    * Pre-defined sets: printable, base32, base64
    * Custom sets:
      - a: lowercase chars
      - A: uppercase chars
      - 1: digits
      - !: special chars
      - *: printable chars

Examples:
  xortool file.bin
  xortool -l 11 -c 20 file.bin
  xortool -x -c ' ' file.hex
  xortool -b -f -l 23 -t base64 message.enc
"""

from operator import itemgetter
import os
import string
import sys

from xortool_ciphey.args import (
    parse_parameters,
    ArgError,
)
from xortool_ciphey.charset import CharsetError
from xortool_ciphey.colors import (
    COLORS,
    C_BEST_KEYLEN,
    C_BEST_PROB,
    C_FATAL,
    C_KEY,
    C_RESET,
    C_WARN,
)
from xortool_ciphey.routine import (
    decode_from_hex,
    dexor,
    die,
    load_file,
    mkdir,
    rmdir,
    MkdirError,
)


DIRNAME = 'xortool_out'  # here plaintexts will be placed
PARAMETERS = dict()


class AnalysisError(Exception):
    pass
def parse_char(ch):
    """
    'A' or '\x41' or '0x41' or '41'
    '\x00' or '0x00' or '00'
    """
    if ch is None:
        return None
    if len(ch) == 1:
        return ord(ch)
    if ch[0:2] in ("0x", "\\x"):
        ch = ch[2:]
    if not ch:
        raise ValueError("Empty char")
    if len(ch) > 2:
        raise ValueError("Char can be only a char letter or hex")
    return int(ch, 16)

def api(text = None, config = {"most_frequent_char": " ", "known_key_length": None}):
    if text == None:
        return "Error. No text given."

    PARAMETERS.update(parse_parameters(__doc__))

    ciphertext = text

    PARAMETERS["most_frequent_char"] = parse_char(config["most_frequent_char"])
    try_chars = [PARAMETERS["most_frequent_char"]]

    PARAMETERS["known_key_length"] = config["known_key_length"]

    if not PARAMETERS["known_key_length"]:
        PARAMETERS["known_key_length"] = guess_key_length(ciphertext)
    
    (probable_keys,
         key_char_used) = guess_probable_keys_for_chars(ciphertext, try_chars)

    keys = print_keys(probable_keys)

    plaintext = produce_plaintexts(ciphertext, probable_keys, key_char_used)
    
    return (keys, plaintext)

def main():
    try:
        PARAMETERS.update(parse_parameters(__doc__, __version__))
        ciphertext = get_ciphertext()
        if not PARAMETERS["known_key_length"]:
            PARAMETERS["known_key_length"] = guess_key_length(ciphertext)

        if PARAMETERS["brute_chars"]:
            try_chars = range(256)
        elif PARAMETERS["brute_printable"]:
            try_chars = map(ord, string.printable)
        elif PARAMETERS["most_frequent_char"] is not None:
            try_chars = [PARAMETERS["most_frequent_char"]]
        else:
            die(C_WARN +
                "Most possible char is needed to guess the key!" +
                C_RESET)

        (probable_keys,
         key_char_used) = guess_probable_keys_for_chars(ciphertext, try_chars)

        print_keys(probable_keys)
        produce_plaintexts(ciphertext, probable_keys, key_char_used)

    except AnalysisError as err:
        print(C_FATAL + "[ERROR] Analysis error:\n\t", err, C_RESET)
    except ArgError as err:
        print(C_FATAL + "[ERROR] Bad argument:\n\t", err, C_RESET)
    except CharsetError as err:
        print(C_FATAL + "[ERROR] Bad charset:\n\t", err, C_RESET)
    except IOError as err:
        print(C_FATAL + "[ERROR] Can't load file:\n\t", err, C_RESET)
    except MkdirError as err:
        print(C_FATAL + "[ERROR] Can't create directory:\n\t", err, C_RESET)
    except UnicodeDecodeError as err:
        print(C_FATAL + "[ERROR] Input is not hex:\n\t", err, C_RESET)
    else:
        return
    cleanup()
    sys.exit(1)


# -----------------------------------------------------------------------------
# LOADING CIPHERTEXT
# -----------------------------------------------------------------------------

def get_ciphertext():
    """Load ciphertext from a file or stdin and hex-decode if needed"""
    ciphertext = load_file(PARAMETERS["filename"])
    if PARAMETERS["input_is_hex"]:
        ciphertext = decode_from_hex(ciphertext)
    return ciphertext


# -----------------------------------------------------------------------------
# KEYLENGTH GUESSING SECTION
# -----------------------------------------------------------------------------

def guess_key_length(text):
    """
    Try key lengths from 1 to max_key_length and print local maximums

    Set key_length to the most possible if it's not set by user.
    """
    fitnesses = calculate_fitnesses(text)
    if not fitnesses:
        raise AnalysisError("No candidates for key length found! Too small file?")

    print_fitnesses(fitnesses)
    guess_and_print_divisors(fitnesses)
    return get_max_fitnessed_key_length(fitnesses)


def calculate_fitnesses(text):
    """Calculate fitnesses for each keylen"""
    prev = 0
    pprev = 0
    fitnesses = []
    for key_length in range(1, PARAMETERS["max_key_length"] + 1):
        fitness = count_equals(text, key_length)

        # smaller key-length with nearly the same fitness is preferable
        fitness = (float(fitness) /
                   (PARAMETERS["max_key_length"] + key_length ** 1.5))

        if pprev < prev and prev > fitness:  # local maximum
            fitnesses += [(key_length - 1, prev)]

        pprev = prev
        prev = fitness

    if pprev < prev:
        fitnesses += [(key_length - 1, prev)]

    return fitnesses


def print_fitnesses(fitnesses):
    return 

    # top sorted by fitness, but print sorted by length
    fitnesses.sort(key=itemgetter(1), reverse=True)
    top10 = fitnesses[:10]
    best_fitness = top10[0][1]
    top10.sort(key=itemgetter(0))

    fitness_sum = calculate_fitness_sum(top10)
    fmt = "{C_KEYLEN}{:" + str(len(str(max(i[0] for i in top10)))) + \
            "d}{C_RESET}: {C_PROB}{:5.1f}%{C_RESET}"

    best_colors = COLORS.copy()
    best_colors.update({
        'C_KEYLEN': C_BEST_KEYLEN,
        'C_PROB': C_BEST_PROB,
    })

    for key_length, fitness in top10:
        colors = best_colors if fitness == best_fitness else COLORS
        pct = round(100 * fitness * 1.0 / fitness_sum, 1)


def calculate_fitness_sum(fitnesses):
    return sum([f[1] for f in fitnesses])


def count_equals(text, key_length):
    """Count equal chars count for each offset and sum them"""
    equals_count = 0
    if key_length >= len(text):
        return 0

    for offset in range(key_length):
        chars_count = chars_count_at_offset(text, key_length, offset)
        equals_count += max(chars_count.values()) - 1  # why -1? don't know
    return equals_count


def guess_and_print_divisors(fitnesses):
    """
    Prints common divisors and returns the most common divisor
    """
    divisors_counts = [0] * (PARAMETERS["max_key_length"] + 1)
    for key_length, fitness in fitnesses:
        for number in range(3, key_length + 1):
            if key_length % number == 0:
                divisors_counts[number] += 1
    max_divisors = max(divisors_counts)

    limit = 3
    ret = 2
    fmt = "Key-length can be {C_DIV}{:d}*n{C_RESET}"
    for number, divisors_count in enumerate(divisors_counts):
        if divisors_count == max_divisors:
            ret = number
            limit -= 1
            if limit == 0:
                return ret
    return ret


def get_max_fitnessed_key_length(fitnesses):
    max_fitness = 0
    max_fitnessed_key_length = 0
    for key_length, fitness in fitnesses:
        if fitness > max_fitness:
            max_fitness = fitness
            max_fitnessed_key_length = key_length
    return max_fitnessed_key_length


def chars_count_at_offset(text, key_length, offset):
    chars_count = dict()
    for pos in range(offset, len(text), key_length):
        c = text[pos]
        if c in chars_count:
            chars_count[c] += 1
        else:
            chars_count[c] = 1
    return chars_count


# -----------------------------------------------------------------------------
# KEYS GUESSING SECTION
# -----------------------------------------------------------------------------

def guess_probable_keys_for_chars(text, try_chars):
    """
    Guess keys for list of characters.
    """
    probable_keys = []
    key_char_used = {}

    for c in try_chars:
        keys = guess_keys(text, c)
        for key in keys:
            key_char_used[key] = c
            if key not in probable_keys:
                probable_keys.append(key)

    return probable_keys, key_char_used


def guess_keys(text, most_char):
    """
    Generate all possible keys for key length
    and the most possible char
    """
    key_length = PARAMETERS["known_key_length"]
    key_possible_bytes = [[] for _ in range(key_length)]

    for offset in range(key_length):  # each byte of key<
        chars_count = chars_count_at_offset(text, key_length, offset)
        max_count = max(chars_count.values())
        for char in chars_count:
            if chars_count[char] >= max_count:
                key_possible_bytes[offset].append(char ^ most_char)

    return all_keys(key_possible_bytes)


def all_keys(key_possible_bytes, key_part=(), offset=0):
    """
    Produce all combinations of possible key chars
    """
    keys = []
    if offset >= len(key_possible_bytes):
        return [bytes(key_part)]
    for c in key_possible_bytes[offset]:
        keys += all_keys(key_possible_bytes, key_part + (c,), offset + 1)
    return keys


def print_keys(keys):

    if not keys:
        return {"Keys": "No keys guessed!"}

    possible_keys = {"keys": []}

    fmt = "{C_COUNT}{:d}{C_RESET} possible key(s) of length {C_COUNT}{:d}{C_RESET}:"
    for key in keys[:5]:
        possible_keys["keys"].append(repr(key)[2:-1])
    return possible_keys

# -----------------------------------------------------------------------------
# RETURNS PERCENTAGE OF VALID TEXT CHARS
# -----------------------------------------------------------------------------

def percentage_valid(text):
    x = 0.0
    for c in text:
        if c in PARAMETERS["text_charset"]:
            x += 1
    return x / len(text)


# -----------------------------------------------------------------------------
# PRODUCE OUTPUT
# -----------------------------------------------------------------------------

def produce_plaintexts(ciphertext, keys, key_char_used):
    """
    Produce plaintext variant for each possible key,
    creates csv files with keys, percentage of valid
    characters and used most frequent character
    """

    # this is split up in two files since the
    # key can contain all kinds of characters

    result = {}

    # key repr
    result["fn_key_mapping"] = {}
    fn_key_mapping = result["fn_key_mapping"]

    # char used, percent valid
    result["filename-char_used-perc_valid"] = {}
    fn_perc_mapping = result["filename-char_used-perc_valid"]

    key_mapping = fn_key_mapping
    perc_mapping = fn_perc_mapping

    threshold_valid = 95
    count_valid = 0

    for index, key in enumerate(keys):
        key_index = str(index).rjust(len(str(len(keys) - 1)), "0")
        key_repr = repr(key)
        # file_name = os.path.join(DIRNAME, key_index + ".out")

        dexored = dexor(ciphertext, key)
        # ignore saving file when known plain is provided and output doesn't contain it
        if PARAMETERS["known_plain"] and PARAMETERS["known_plain"] not in dexored:
            continue
        perc = round(100 * percentage_valid(dexored))
        if perc > threshold_valid:
            count_valid += 1
        
        key_mapping[key_index] = key_repr

        # [key_char_used, percentage]
        perc_mapping[key_index] = [key_char_used[key], perc]
        if not PARAMETERS["filter_output"] or \
            (PARAMETERS["filter_output"] and perc > threshold_valid):
            result["Dexored"] = dexored.decode("utf-8")

    if PARAMETERS["known_plain"]:
        # Is this a crib, known plaintext given?
        result["known_plain"] = PARAMETERS["known_plain"].decode('ascii')
    
    result["fn_key_mapping"] = fn_key_mapping
    result["perc_mapping"] = fn_perc_mapping
    return result


def cleanup():
    if os.path.exists(DIRNAME):
        rmdir(DIRNAME)