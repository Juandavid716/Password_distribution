from collections import Counter
from database import create_connection
from create_tables import create_table
from Esrank import get_L1_L2
import numpy as np 
from rank import transform_133t
from rank import rank_estimation
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

#Get probability order by desc
def get_probability_sorted(name_list):
    list = []
    for row in name_list:
        list.append(float(row[1]))
    
    return list


# Count every time an element appear

def get_frequency(list, length):
    frequency={} 
    dimensions = []

    # Count number of times that a prefix is repeated
    for i in list:
        frequency[i]=list.count(i)
    
    
    for key in frequency.keys():
        dimensions.append(key)

    return dimensions, get_probability(frequency, length)

#Get probability from lists shift pattern dimension
def get_frequency_shift(list_s, length, num):
    list_probabilities = []
    list_copy = dict(Counter(tuple(x) for x in list_s))
    dimensions = []

    for key in list_copy.keys():

        if num == 0:
            values = "["+','.join(str(v) for v in key)+"]"
        else:
            values = "".join(str(x) for x in key)
            ''.join(map(str,values))
        dimensions.append(values)

    return dimensions, get_probability(list_copy,length)



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
    #Connection
    con = create_connection(r'./databases/test.db')
    cur = con.cursor() 
    
    #Create tables
    create_table("prefix_table", cur)
    create_table("suffix_table", cur)
    create_table("baseword_table", cur)
    create_table("shift_table", cur)
    create_table("table_133t", cur)

    # Get lists
    list = get_list()
    length = len(list)
    list_prefix, list_without_prefix = get_prefix(list)
    list_suffix, list_baseword = get_suffix(list_without_prefix)
    list_shift = shift_pattern(list_baseword)
    list_133t, list_baseword = get_133t_transformation(list_baseword)

    # # 5D MODEL
    # print("Prefix list",list_prefix)
    # print("Base word list",list_baseword)
    # print("Suffix list", list_suffix)
    # print("shift pattern list", list_shift)
    # print("133t list",list_133t)

    # List of probabilities
    list_prefix, list_prob_prefix =  get_frequency(list_prefix, length)
    list_baseword, list_prob_basew = get_frequency(list_baseword, length)
    list_suffix, list_prob_suffix= get_frequency(list_suffix, length)
    list_shift, list_prob_shift = get_frequency_shift(list_shift, length,0)
    list_133t, list_prob_133t =  get_frequency_shift(list_133t, length,1)
    
    # Insertions list on database 
    cur.executemany("""INSERT INTO  prefix_table (dimension,probability) VALUES (?,?)""", zip(list_prefix,list_prob_prefix))
    cur.executemany("""INSERT INTO  suffix_table (dimension,probability) VALUES (?,?)""", zip(list_suffix,list_prob_suffix))
    cur.executemany("""INSERT INTO  baseword_table (dimension,probability) VALUES (?,?)""", zip(list_baseword,list_prob_basew))
    cur.executemany("""INSERT INTO  shift_table (dimension,probability) VALUES (?,?)""", zip(list_shift,list_prob_shift))
    cur.executemany("""INSERT INTO  table_133t (dimension,probability) VALUES (?,?)""", zip(list_133t,list_prob_133t))
    con.commit()

    # Get probabilities sorted by highest probability
    prefix_probabilities = cur.execute("SELECT * FROM prefix_table ORDER BY probability DESC ").fetchall()
    suffix_probabilities = cur.execute("SELECT * FROM suffix_table ORDER BY probability DESC ").fetchall()
    baseword_probabilities = cur.execute("SELECT * FROM baseword_table ORDER BY probability DESC ").fetchall()
    shift_probabilities = cur.execute("SELECT * FROM shift_table ORDER BY probability DESC ").fetchall()
    t133_probabilities = cur.execute("SELECT * FROM table_133t ORDER BY probability DESC ").fetchall()

    P1 = get_probability_sorted(prefix_probabilities)
    P2 = get_probability_sorted(suffix_probabilities)
    P3 = get_probability_sorted(baseword_probabilities)
    P4 = get_probability_sorted(shift_probabilities)
    P5 = get_probability_sorted(t133_probabilities)

    # P = List of lists 
    P = [P1,P2,P3,P4,P5]
    #print(P)

    gamma=1.09
    dimensiones=5
    b=5
    p=P1[4]*P2[2]*P3[2]*P4[2]*P5[6]
    L=get_L1_L2(P,dimensiones, gamma,b,p )

    numbits=np.ceil(np.log2(sum(L)/2))
    print("With an enumeration of", int(2**(numbits)), " candidates passwords is possible to recover this password ")
  
    L = rank_estimation("@isaliiana123",con)
    if L == -5:
        print("None")
    else:
      numbits=np.ceil(np.log2(L))
      print("Numbit is", ((numbits)))

    # print("                           ")
    # print("Probability table     ")
    # print("                           ")
    # print("Probabiliies from prefix",list_prob_prefix)
    # print("Probabilities from base words",list_prob_basew)
    # print("Probabilities from suffix",list_prob_suffix)
    # print("Probabilities from shift",list_prob_shift)
    # print("Probabiliies from 133t transformation", list_prob_133t)


if __name__ == "__main__":
    main()
    