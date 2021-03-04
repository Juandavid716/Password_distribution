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

# Get shift pattern from basewords
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

# Get probability from lists of dimensions (prefix, baseword, suffix)
def get_probability(frequency,length):
    list_probabilities = []

    for index in frequency:
        result = frequency[index] / length
        list_probabilities.append(result)

    return list_probabilities

# Count every time an element appear

def get_frequency(list, length):
    frequency={} 

    for i in list:
        frequency[i]=list.count(i)
    
 
    return get_probability(frequency, length)

#Get probability from lists shift pattern dimension
def get_frequency_shift(list_s, length):
    list_probabilities = []
    list_copy = dict(Counter(tuple(x) for x in list_s))
    
    return get_probability(list_copy,length)
     
def transform_133t(word):
    index_133t=[]
    if "0" in word:
        word=word.replace("0","o")
        index_133t.append(1)
    if "1" in word:
        word=word.replace("1","i")
        index_133t.append(12)
    elif "!" in word:
        word=word.replace("!","i")
        index_133t.append(13)
    if "@" in word:
        word=word.replace("@","a")
        index_133t.append(2)
    elif "4" in word:
        word=word.replace("4","a")
        index_133t.append(3)
    if "3" in word:
        word=word.replace("3","e")
        index_133t.append(6)
    if "$" in word:
        word=word.replace("$","s")
        index_133t.append(4)
    elif "5" in word:
        word=word.replace("5","s")
        index_133t.append(5)
    if "2" in word:
        word=word.replace("2","z")
        index_133t.append(11)
    if "%" in word:
        word=word.replace("%","x")
        index_133t.append(14)
    if "7" in word:
        word=word.replace("7","t")
        index_133t.append(10)
    elif "+" in word:
        word=word.replace("+","t")
        index_133t.append(9)
    if "9" in word:
        word=word.replace("9","g")
        index_133t.append(8)
    elif "6" in word:
        word=word.replace("6","g")
        index_133t.append(7)
    return word,str(list(sorted(index_133t)))

# Get basewords and 133_t transformations
def get_133t_transformation(list_baseword):
    list_133t = []
    list_new_basewords = []
    for baseword in list_baseword:
       baseword_transfomed, list_index = transform_133t(baseword)
       list_133t.append(list_index)
       list_new_basewords.append(baseword_transfomed.lower())
    return list_133t, list_new_basewords


def main():
    list = get_list()
    length = len(list)
    list_prefix, list_without_prefix = get_prefix(list)
    list_suffix, list_baseword = get_suffix(list_without_prefix)
    list_shift = shift_pattern(list_baseword)
    # 5D MODEL
    list_133t, list_baseword = get_133t_transformation(list_baseword)
    print("Prefix list",list_prefix)
    print("Base word list",list_baseword)
    print("Suffix list", list_suffix)
    print("shift pattern list", list_shift)
    print("133t list",list_133t)

    # List of probabilities
    list_prob_prefix =  get_frequency(list_prefix, length)
    list_prob_basew = get_frequency(list_baseword, length)
    list_prob_suffix= get_frequency(list_suffix, length)
    list_prob_shift = get_frequency_shift(list_shift, length)
    list_prob_133t =  get_frequency_shift(list_133t, length)

    print("                           ")
    print("Probability table     ")
    print("                           ")
    print("Probabiliies from prefix",list_prob_prefix)
    print("Probabilities from base words",list_prob_basew)
    print("Probabilities from suffix",list_prob_suffix)
    print("Probabilities from shift",list_prob_shift)
    print("Probabiliies from 133t transformation", list_prob_133t)


if __name__ == "__main__":
    main()
    