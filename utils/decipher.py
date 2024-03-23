def decipher(s):
    if len(s) > 1:
        l = []
        for ch in s:
            if ch == " ":
                l.append(" ")
            else:
                l.append(ord(ch) - 63)
        return l
    else:
        if s != " ":
            return ord(s) - 63
        else:
            return " "