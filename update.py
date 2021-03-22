from database import create_connection
from main import get_prefix
from main import get_suffix
from main import shift_pattern
from main import get_133t_transformation
from main import get_list
from collections import Counter

#STEPS
#1- Get data
#2 - Get dimensions
#3 - Get frequency
#4 - Get probability with new formula
#5 - update list on database
def get_repeated(list_x):
    frequency={} 
    for i in list_x:
        frequency[i]=list_x.count(i)
    
    return  frequency


def update_data(file):
    con = create_connection(r'./databases/test.db')
    cur = con.cursor() 

    data = get_list(file)

    list_prefix, list_without_prefix = get_prefix(data)
    list_suffix, list_baseword = get_suffix(list_without_prefix)
    list_shift = shift_pattern(list_baseword)
    list_133t, list_baseword = get_133t_transformation(list_baseword)

    # INSERT OR IGNORE INTO prefix_table (name, age) VALUES ('Karen', 34)
    # UPDATE my_table SET age = 34 WHERE name='Karen'

    #Frequencies
    prefix = get_repeated(list_prefix)
    suffix = get_repeated(list_suffix)
    bw = get_repeated(list_baseword)
    shift= dict(Counter(tuple(x) for x in list_shift))
    t133 = dict(Counter(tuple(x) for x in list_133t))

    pr = 1
    num = 0.00717213114754

    cur.execute("INSERT OR IGNORE INTO prefix_table (dimension, probability) VALUES (?, ?)",(pr,num))
    cur.execute(" UPDATE prefix_table SET probability = ? WHERE dimension =?",(num,pr))
    con.commit()
    # for p in prefix:
    #     print(p)
    #     print(prefix[p])
    # print(prefix)
    # print(suffix)
    # print(bw)
    # print(shift)
    # print(t133)


if __name__ == "__main__":
    update_data("passwords.txt")
    


