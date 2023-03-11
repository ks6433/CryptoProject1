#!/usr/bin/env python
# coding: utf-8
#  we're going to request parameters by command line
from scipy.stats import ks_2samp
import random
import numpy as np

characterMap = {' ': 0, 'a': 1, 'c': 3, 'b': 2,
                'e': 5, 'd': 4, 'g': 7, 'f': 6,
                'i': 9, 'h': 8, 'k': 11, 'j': 10,
                'm': 13, 'l': 12, 'o': 15, 'n': 14,
                'q': 17, 'p': 16, 's': 19, 'r': 18,
                'u': 21, 't': 20, 'w': 23, 'v': 22,
                'y': 25, 'x': 24, 'z': 26}

        
def num_to_char(val):
    return list(characterMap.keys())[list(characterMap.values()).index(val)]
# when probability is =0:
# p=blue  2 12 21 5
# k=cafe  3 1  6  5
# c=emaj  5 13 1 10

# Encryption algorithm based on pseudocode given in project statement
def encryption(plain_text, key, p_random):
    c_pointer = 0
    m_pointer = 0
    num_rand_char = 0
    cipher_text = []
    t = len(key)
    # iterate over all letters of PT and be able to calculate the next value
    while m_pointer < len(plain_text): # TODO change to a c_pointer <= L + num_rand_char
        coin_val = random.randint(0,1)
        if coin_val >= p_random:
            # cipher= m[m_pointer] + k[j] mod 27
            j = (m_pointer % t) #+ 1
            # convert characters to numbers
            plain_text_num = characterMap[plain_text[m_pointer]]
            key_num = characterMap[key[j]]
            cipher_num = (plain_text_num + key_num) % 27
            # convert number to character
            cipher= num_to_char(cipher_num)
            cipher_text.append(cipher)
            m_pointer += 1
        else:
            # set ciphertext to be a random char
            random_num = random.randint(0,26)
            random_char=num_to_char(random_num)
            cipher_text.append(random_char)
            num_rand_char += 1
        c_pointer += 1
        
    abc = ""
    #print(abc.join(cipher_text))
    return cipher_text

def generate_random_key(key_length):
    key=""
    for i in range(key_length):
        key += num_to_char(random.randint(0, 26))
    return key

def comparator(a, b):
    result = ks_2samp(a, b)
    # print(result.pvalue)
    if result.pvalue >= 0.05:
        return True # the two distributions are significantly identical
    else:
        return False # the two distributions are not significantly identical


def freq_distributor(ct):
    distribution_list = [0 for i in range(len(characterMap))]
    for i in ct:
        distribution_list[characterMap[i]] += 1
    return distribution_list



def decryption(ct, pt_set):
    our_guess = ""
    max_freq_plaintext = 0
    pt_index = 0
    # iterate over all potential plaintexts (there are 5 of them)
    min_var = 9999 # This is the minimum variance between plaintext and ciphertext
    for pt in pt_set:
        lenn = len(pt) if len(pt) < len(ct) else len(ct)
        sum_var = 9999 # sum of variances
        for t in range(1, 26):  # if t=4 cafe
            bins = []
            for j in range(0, t):
                diffs = [] # shift in plaintext characters
                for i in range(j, lenn, t):
                    diff = characterMap[ct[i]] - characterMap[pt[i]]
                    diffs.append(diff)
                bins.append(np.std(diffs)) #gives a measure of the constancy of shift across all the j's
            var = np.sum(bins)
            sum_var = var if var < sum_var else sum_var
        if sum_var < min_var:
            min_var = sum_var
            guess = pt_index
        
        pt_index += 1
        
    return guess

if __name__ == '__main__':
    # read the dictionary input file
    plaintext_set1 = []
    # open the dictionary 1 text file
    with open('dict_1.txt', 'rb') as file:
        lines = [line.rstrip() for line in file]

    for p in lines:
        #print(p)
        p = str(p, 'UTF-8')
        if not (p.find('Candidate') !=-1 or p.find('Test') !=-1): # check that line is not empty
            if p.strip():
            # print(p)
                plaintext_set1.append(p)

    # For testing purposes, we generate a key of length t
    p_random = 0.00  # can change this later
    t = 6
    key = generate_random_key(t)
    #print(key)

    #TODO
    #generate multiple CTs per key and plaintext

    # for testing purposes, pass in only plaintext 0:
    #cipher = encryption(plaintext_set1[4], key, p_random)
    #print(cipher)
    
    print("Enter you cipher")
    cipher_new = input()
    cipher = [symbol for symbol in cipher_new]
    
    our_guess_pt = decryption(cipher, plaintext_set1)
    print("Our plaintext guess is:", str(our_guess_pt))

   



