# Encryption algorithm based on pseudocode given in project statement
# TODO
#  we're going to request parameters by command line
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

# Encryption scheme
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
        c_pointer +=1

    return cipher_text

def generate_random_key(key_length):
    key=""
    for i in range(key_length):
        key += num_to_char(random.randint(0, 26))
    return key

def decryption1()


if __name__ == '__main__':
    p_random = 0.05  # can change this later


    plaintext_set1=[]
    # open the dictionary 1 text file
    with open('dict_1.txt', 'rb') as file:
        lines = [line.rstrip() for line in file]

    for p in lines:
        #print(p)
        p=str(p, 'UTF-8')
        if not (p.find('Candidate') !=-1 or p.find('Test') !=-1): # check that line is not empty
            if p.strip():
            #print(p)
                plaintext_set1.append(p)

    # for plaintext in plaintext_set1:
    #     print(plaintext)

    # print(len(plaintext_set1))

    # For testing purposes, we generate a key of length t
    t=7
    key = generate_random_key(t)
    print(key)

    #TODO
    #generate multiple CTs per key and plaintext

    result = encryption(plaintext_set1[0], key, p_random)
    print(result)