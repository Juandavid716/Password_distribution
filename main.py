
# Get the list of passwords from the file
def get_list():
 data = []
 with open("passwords.txt") as fname:
    lines = fname.readlines()
    for line in lines:
        data.append(line.strip('\n'))
 return data

# Get the prefix for each password and return password without prefix
def get_prefix(password_list):
    list_prefix = []
    list_password_without_prefix = []
    for password in password_list:
        prefix = ""
        for letter in password:
            if letter.isdigit():
              prefix = prefix + letter
            else:
              break

        if prefix == password:
            prefix = ""
        #print("Password is {} and prefix is {}".format(password,prefix))

        password_without_prefix = password.replace(prefix,'')
        list_password_without_prefix.append(password_without_prefix)
        list_prefix.append(prefix)
    
    return list_prefix, list_password_without_prefix;

        

def main():
    list = get_list()
    list_prefix, list_without_prefix = get_prefix(list)

if __name__ == "__main__":
    main()