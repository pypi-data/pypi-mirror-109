"""This is the 'nester.py' module and it provides one \
function called print_list() which prints lists may or\
 may not include nested lists."""

def print_list(list_name, indent=False ,level=0):
    """This function takes one positional argument called
    'lst',which is any Python list (of - possibly - nested list).
    Each data item in the provided list is (recursively) printed
    to the screen on it's own line"""
    for each in list_name:
        if isinstance(each,list):
            print_list(each,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end="")
            print(each)
            

