def cong(x,y):
    return x+y
    
def print_list(the_list,level):
    for item in the_list:
        if isinstance(item,list):
            print_list(item,level+1)
        else :
            for num in range(level):
                print("\t",end='')
            print(item)