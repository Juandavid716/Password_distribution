
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
        print(password)
        password_without_suffix = password[ 0 : len(password)-len(suffix_reverse)]
        list_baseword.append(password_without_suffix)
        list_suffix.append(suffix_reverse)
    
    return list_suffix, list_baseword;

def main():
    list = get_list()
    list_prefix, list_without_prefix = get_prefix(list)
    list_sufix, list_baseword = get_suffix(list_without_prefix)
    print("Lista de prefijos",list_prefix)
    print("Lista de base words",list_baseword)
    print("Lista de sufijos", list_sufix)

if __name__ == "__main__":
    main()