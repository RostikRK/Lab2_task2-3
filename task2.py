"""
Data parser
"""
import json
import twitter1
import sys



def reading_dict(path):
    """
    Reads the file and generates data
    >>> ":-)" == ":-("
    False
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def navigation_trough_json(data):
    """
    Navigates the user though the json file
    """
    print("Now starts a navigation trough the twitter timeline json file. To start please select information about which post you want to get. Totally our program normally reads", len(data), "posts. (to change this setting change the variable count in twitter1.py) The numeration is from the newest to oldest.")
    while True:
        try:
            post_num = int(input())
            starting_root = data[post_num-1]
            break
        except IndexError:
            print("There is no such post. Please try again")
    while (isinstance(starting_root, dict) == True) or (isinstance(starting_root, list) == True) and (starting_root != None):
        if type(starting_root)==list:
            if len(starting_root)==1:
                starting_root = starting_root[0]
            else:
                dict_list = []
                for ellem in starting_root:
                    if type(ellem) == dict:
                        dict_list.append(ellem)
                if len(dict_list)>1:
                    print("There another ways where to go: ", "\n".join(dict_list) ," \nPlease choose where to go next.")
                    print('Or in order to quit write (q)')
                    while True:
                        try:
                            next_step = input()
                            if next_step == "q":
                                sys.exit()
                            else:
                                starting_root = starting_root[next_step]
                                break
                        except KeyError:
                            print("You entered not exist next step. Please try again.")
                else:
                    break
        else:
            print("Okey where should we go next: ", "\n".join(starting_root.keys()),"")
            print('Or in order to quit write (q)')
            while True:
                try:
                    next_step = input()
                    if next_step == "q":
                        sys.exit()
                    else:
                        starting_root = starting_root[next_step]
                        break
                except KeyError:
                    print("You entered not exist next step. Please try again.")
    return starting_root


if __name__ == "__main__":
    twitter1.get_timeline_file()
    data = reading_dict("user_timeline.json")
    startint_root = navigation_trough_json(data)
    print(startint_root)
