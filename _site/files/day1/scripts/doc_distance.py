#!/usr/bin/python
# docdist8.py - treat whole file as a single "line"
#
# Original version by Erik D. Demaine on January 31, 2011,
# based on code by Ronald L. Rivest (see docdist[1-7].py).
#
# Usage:
#    docdist8.py filename1 filename2
#     
# This program computes the "distance" between two text files
# as the angle between their word frequency vectors (in radians).
#
# For each input file, a word-frequency vector is computed as follows:
#    (1) the specified file is read in
#    (2) it is converted into a list of alphanumeric "words"
#        Here a "word" is a sequence of consecutive alphanumeric
#        characters.  Non-alphanumeric characters are treated as blanks.
#        Case is not significant.
#    (3) for each word, its frequency of occurrence is determined
#    (4) the word/frequency lists are sorted into order alphabetically
#
# The "distance" between two vectors is the angle between them.
# If x = (x1, x2, ..., xn) is the first vector (xi = freq of word i)
# and y = (y1, y2, ..., yn) is the second vector,
# then the angle between them is defined as:
#    d(x,y) = arccos(inner_product(x,y) / (norm(x)*norm(y)))
# where:
#    inner_product(x,y) = x1*y1 + x2*y2 + ... xn*yn
#    norm(x) = sqrt(inner_product(x,x))



# NB # the script is from an MIT course on Algorithms:
# https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/lecture-notes/)
# some modifications were done to support Arabic and work with Python 3
# (MGR, July 2018)



import math
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

import string
import re
import sys

##################################
# Operation 0: clean Arabic ######
##################################

# deNoise(text) deletes short vowels from Arabic text
def deNoise(text):
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return(text)

def normalizeArabicLight(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("[يى]ء", "ئ", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("(ؤ)", "ء", text)
    text = re.sub("(ئ)", "ء", text)
    #text = re.sub("(ء)", "", text)
    #text = re.sub("(ة)", "ه", text)
    return(text)


##################################
# Operation 1: read a text file ##
##################################
def read_file(filename):
    """ 
    Read the text file with the given filename;
    return a list of the lines of text in the file.
    """
    try:
        f = open(filename, 'r', encoding="utf8")
        text = f.read()
        text = deNoise(text)
        text = normalizeArabicLight(text)
        return(text)
    except IOError:
        print("Error opening or reading input file: ",filename)
        sys.exit()

#################################################
# Operation 2: split the text lines into words ##
#################################################

# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
##translation_table = string.maketrans(string.punctuation+string.uppercase,
##                                     " "*len(string.punctuation)+string.lowercase)

def get_words_from_line_list(text):
    """
    Parse the given text into words.
    Return list of all words found.
    """
    #text = text.translate(translation_table)
    word_list = re.findall(r"\w+", text)
    #print(word_list[-50:])
    return word_list

##############################################
# Operation 3: count frequency of each word ##
##############################################
def count_frequency(word_list):
    """
    Return a dictionary mapping words to frequency.
    """
    D = {}
    for new_word in word_list:
        if new_word in D:
            D[new_word] = D[new_word]+1
        else:
            D[new_word] = 1
    return D

#############################################
## compute word frequencies for input file ##
#############################################
def word_frequencies_for_file(filename):
    """
    Return dictionary of (word,frequency) pairs for the given file.
    """

    line_list = read_file(filename)
    word_list = get_words_from_line_list(line_list)
    freq_mapping = count_frequency(word_list)

    print("File",filename,":",len(line_list),"lines,",len(word_list),"words,", len(freq_mapping),"distinct words")

    return freq_mapping

def inner_product(D1,D2):
    """
    Inner product between two vectors, where vectors
    are represented as dictionaries of (word,freq) pairs.

    Example: inner_product({"and":3,"of":2,"the":5},
                           {"and":4,"in":1,"of":1,"this":2}) = 14.0 
    """
    sum = 0.0
    for key in D1:
        if key in D2:
            sum += D1[key] * D2[key]
    return sum

def vector_angle(D1,D2):
    """
    The input is a list of (word,freq) pairs, sorted alphabetically.

    Return the angle between these two vectors.
    """
    numerator = inner_product(D1,D2)
    denominator = math.sqrt(inner_product(D1,D1)*inner_product(D2,D2))
    return math.acos(numerator/denominator)

def main():
    if len(sys.argv) != 3:
        print("Usage: docdist8.py filename_1 filename_2")
    else:
        filename_1 = sys.argv[1]
        filename_2 = sys.argv[2]
        sorted_word_list_1 = word_frequencies_for_file(filename_1)
        sorted_word_list_2 = word_frequencies_for_file(filename_2)
        distance = vector_angle(sorted_word_list_1,sorted_word_list_2)
        print("The distance between the documents is: %0.6f (radians)" % distance)
        print("NB: 0.0 - full match; 1.0 - completely different.")

##if __name__ == "__main__":
##    import profile
##    profile.run("main()")

    
main()



