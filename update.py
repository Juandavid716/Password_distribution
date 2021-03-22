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

def update_4D_5D(list_s,  num, name_table, con, total, new_total):
    cur = con.cursor() 
    for key in list_s.keys():
    
        if num == 0:
            p = "["+','.join(str(v) for v in key)+"]"
        else:
            p = "".join(str(x) for x in key)
            ''.join(map(str,p))

        vals = cur.execute("SELECT probability FROM {} WHERE dimension=?".format(name_table), (p, )).fetchone()
        if vals:
            old_probability = vals[0]
      
            new_probability = float(old_probability)* total / (total + new_total) + float(list_s[key]) / (total + new_total)
            print(new_probability)
            cur.execute(" UPDATE {} SET probability = ? WHERE dimension =?".format(name_table),(new_probability,p))
            
            con.commit()
        else:
            new_probability = float(list_s[key]) / (total + new_total)
            print("sino",new_probability)
            cur.execute("INSERT OR IGNORE INTO {} (dimension, probability) VALUES (?, ?)".format(name_table),(p,new_probability))
            con.commit()

def update_dimensions(list_dimension, name_table, con ,total, new_total):
    cur = con.cursor() 
    for p in list_dimension:
        vals = cur.execute("SELECT probability FROM {} WHERE dimension=?".format(name_table), (p, )).fetchone()
        if vals:
            old_probability = vals[0]
            new_probability = float(old_probability)* total / (total + new_total) + float(list_dimension[p]) / (total + new_total)
            cur.execute(" UPDATE {} SET probability = ? WHERE dimension =?".format(name_table),(new_probability,p))
            con.commit()
            print("entro y lo hizo bien", new_probability)
        else:
            new_probability = float(list_dimension[p]) / (total + new_total)
            print(new_probability)
            cur.execute("INSERT OR IGNORE INTO {} (dimension, probability) VALUES (?, ?)".format(name_table),(p,new_probability))
            con.commit()

def update_data(file, total):
    con = create_connection(r'./databases/test.db')
    cur = con.cursor() 

    data = get_list(file)
    new_total = len(data)
    list_prefix, list_without_prefix = get_prefix(data)
    list_suffix, list_baseword = get_suffix(list_without_prefix)
    list_shift = shift_pattern(list_baseword)
    list_133t, list_baseword = get_133t_transformation(list_baseword)

    #Frequencies
    prefix = get_repeated(list_prefix)
    suffix = get_repeated(list_suffix)
    bw = get_repeated(list_baseword)
    shift= dict(Counter(tuple(x) for x in list_shift))
    t133 = dict(Counter(tuple(x) for x in list_133t))

    # Update each dimension with new probability, passing as parameters: original list, name table, connection, length of original dataset -> total, new_total = total + lenngth of new dataset
    update_dimensions(prefix, "prefix_table",con, total, new_total)
    update_dimensions(suffix, "suffix_table",con, total, new_total)
    update_dimensions(bw, "baseword_table",con, total, new_total)
    update_4D_5D(shift,0,"shift_table", con, total, new_total)   
    update_4D_5D(t133,1,"table_133t", con, total, new_total)
    
    # for key in shift.keys():
    #     num=0
    #     if num == 0:
    #         p = "["+','.join(str(v) for v in key)+"]"
    #     else:
    #         p = "".join(str(x) for x in key)
    #         ''.join(map(str,p))

    #     vals = cur.execute("SELECT probability FROM shift_table WHERE dimension=?", (p, )).fetchone()
    #     if vals:
    #         old_probability = vals[0]
      
    #         new_probability = float(old_probability)* total / (total + new_total) + float(shift[key]) / (total + new_total)
    #         print(new_probability)
    #         cur.execute(" UPDATE shift_table SET probability = ? WHERE dimension =?",(new_probability,p))
            
    #         con.commit()
    #     else:
    #         new_probability = float(shift[key]) / (total + new_total)
    #         print("sino",new_probability)
    #         cur.execute("INSERT OR IGNORE INTO shift_table (dimension, probability) VALUES (?, ?)",(p,new_probability))
    #         con.commit()
            
        
    
    
    # cur.execute("INSERT OR IGNORE INTO prefix_table (dimension, probability) VALUES (?, ?)",(pr,num))
    # cur.execute(" UPDATE prefix_table SET probability = ? WHERE dimension =?",(num,pr))
    # con.commit()
    # 
    #     
    # print(prefix)
    # print(suffix)
    # print(bw)
    # print(shift)
    # print(t133)


if __name__ == "__main__":
    update_data("passwords.txt", 999424)
    


