
# TODO
#  we're going to request parameters by command line
from scipy.stats import ks_2samp
import random

characterMap = {' ': 0, 'a': 1, 'c': 3, 'b': 2,
                'e': 5, 'd': 4, 'g': 7, 'f': 6,
                'i': 9, 'h': 8, 'k': 11, 'j': 10,
                'm': 13, 'l': 12, 'o': 15, 'n': 14,
                'q': 17, 'p': 16, 's': 19, 'r': 18,
                'u': 21, 't': 20, 'w': 23, 'v': 22,
                'y': 25, 'x': 24, 'z': 26}

def num_to_char(val):
    for key,value in characterMap.items():
        if val==value:
            return key

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
            # cipher= m[m_pointer] + k[j] mod 26
            j = (m_pointer % t) #+ 1
            # convert characters to numbers
            plain_text_num = characterMap[plain_text[m_pointer]]
            key_num = characterMap[key[j]]
            cipher_num = (plain_text_num + key_num) % 26
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
    for pt in pt_set:
        max_val = 0
        print("Plaintext index:" + str(pt_index))
        # for all possible key lengths
        for t in range(1, 26):  # if t=4 cafe
            freq_match_count = 0
            # for all the letters of the key
            for j in range(0, t):  # j = 0,1,2,3   p= bbbbccccd
                                                 # k= cafecafec
                                                 # c= fcrggxryzw
                ct_str = ""  # build the cipher that is potentially encrypted with that letter
                for i in range(j, len(ct), t):
                    ct_str += ct[i]

                pred_pt = ""  # and all the letters of the plaintext encrypted by the same letter of the key
                for i in range(j, len(pt), t):
                    pred_pt += pt[i]
                # compare that they match. I think here it will Fail because of the random vals
                #freq_cipher=freq_distributor(ct_str)
                #freq_pt= freq_distributor(pred_pt)
                if comparator(list(ct_str),list(pred_pt)):
                    freq_match_count += 1
            max_val = max(max_val, freq_match_count)

        print("max value: " + str(max_val))
        if max_val > max_freq_plaintext:
            max_freq_plaintext = max_val
            #our_guess = pt
            our_guess = pt_index

        pt_index += 1
    return our_guess


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
    p_random = 0.05  # can change this later
    t = 6
    key = generate_random_key(t)
    print(key)

    #TODO
    #generate multiple CTs per key and plaintext

    # for testing purposes, pass in only plaintext 0:
    cipher = encryption(plaintext_set1[0], key, p_random)
    print(cipher)

    our_guess_pt = decryption(cipher, plaintext_set1)
    print("Our plaintext guess is:", str(our_guess_pt))

    # Index of coincidence in python:
    """
    def getIOC(text):
	letterCounts = []
    # we already did this part:
	# Loop through each letter in the alphabet - count number of times it appears
	for i in range(len(alph)):
		count = 0
		for j in text:
			if j == alph[i]:
				count += 1
		letterCounts.append(count)
    # ------------------- this would go inside of comparator function: 
	# Loop through all letter counts, applying the calculation (the sigma part)
	total = 0
	for i in range(len(letterCounts)):
		ni = letterCounts[i]
		total += ni * (ni - 1)

	N = countLetters(text)
	c = 26.0 # Number of letters in the alphabet
	total = float(total) / ((N * (N - 1)))
	return total
    """