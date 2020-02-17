def getFatherIndex(union,index):
    if union[index] == index:
        return index
    else:
        return getFatherIndex(union,union[index])