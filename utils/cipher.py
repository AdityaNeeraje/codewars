def cipher(l):
    s = ""
    if type(l) is list:
        for item in l:
            if item != " ":
                s += chr(int(item) + 63)
            else:
                s += " "
        return s
    else:
        if l != " ":
            return chr(int(l) + 63)
        else:
            return " "