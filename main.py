from collections import Counter

# Get the list of passwords from the file
def get_list():
 data = []
 with open("passwords.txt") as fname:
    lines = fname.readlines()
    for line in lines:
        data.append(line.strip('\n'))
 return data

# Get the prefix for each password and return two list: List of prefix and list of password without prefix
def get_prefix(password_list):
    list_prefix = []
    list_password_without_prefix = []
    for password in password_list:
        prefix = ""
        for letter in password:
            if letter.isalpha() is False:
              prefix = prefix + letter
            else:
              break

        if prefix == password:
            prefix = ""
        #print("Password is {} and prefix is {}".format(password,prefix))

        password_without_prefix = password[ len(prefix) : len(password)]
        
        list_password_without_prefix.append(password_without_prefix)
        list_prefix.append(prefix)
    
    return list_prefix, list_password_without_prefix;

# Get the suffix for each password and return two list: List of suffix and list of basewords
def get_suffix(password_list):
    list_suffix = []
    list_baseword = []
    for password in password_list:
        suffix = ""
        password_reverse = password[::-1]
     
        for letter in password_reverse:
            if letter.isalpha() is False:
              suffix = suffix + letter
            else:
              break
               
        if suffix == password_reverse:
            suffix = ""
        
        suffix_reverse = suffix[::-1]
        #print("Password is {} and suffix is {}".format(password,suffix))
        password_without_suffix = password[ 0 : len(password)-len(suffix_reverse)]
        list_baseword.append(password_without_suffix)
        list_suffix.append(suffix_reverse)
    
    return list_suffix, list_baseword;

def shift_pattern(baseword_list):
    list_shift = []
    for baseword in baseword_list:
        shift = []
        shift_negative = []
        cont = -1
        cont_r = -1
        length = len(baseword)
        for index in range(0, length):
           letter = baseword[index]
           
           if letter.isupper(): 
             if index < length // 2:
                shift.append(index)
             else:
                 shift.append(index-length)
                 cont_r -= 1
                 
        list_shift.append(shift)

    return list_shift

def get_probability(frequency,length):
    list_probabilities = []

    for index in frequency:
        result = frequency[index] / length
        list_probabilities.append(result)

    return list_probabilities

def get_frequency(list, length):
    frequency={} 

    for i in list:
        frequency[i]=list.count(i)
    
 
    return get_probability(frequency, length)

def get_frequency_shift(list_s, length):
    list_probabilities = []
    list_copy = dict(Counter(tuple(x) for x in list_s))
    
    return get_probability(list_copy,length)
     

def main():
    list = get_list()
    length = len(list)
    list_prefix, list_without_prefix = get_prefix(list)
    list_suffix, list_baseword = get_suffix(list_without_prefix)
    list_shift = shift_pattern(list_baseword)
    
    # 4D MODEL
    print("Prefix list",list_prefix)
    print("Base word list",list_baseword)
    print("Suffix list", list_suffix)
    print("shift pattern list", list_shift)
    
    # List of probabilities
    list_prob_prefix =  get_frequency(list_prefix, length)
    list_prob_basew = get_frequency(list_baseword, length)
    list_prob_suffix= get_frequency(list_suffix, length)
    list_prob_shift = get_frequency_shift(list_shift, length)

    print("                           ")
    print("Probability table     ")
    print("                           ")
    print("Probabiliies from prefix",list_prob_prefix)
    print("Probabilities from base words",list_prob_basew)
    print("Probabilities from suffix",list_prob_suffix)
    print("Probabilities from shift",list_prob_shift)

if __name__ == "__main__":
    main()