# clear file by name
def clear_file(name):
    f = open(name, "w")
    f.write("")
    f.close()
