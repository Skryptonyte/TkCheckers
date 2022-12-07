

def length(l):
    count = 0
    for i in l:
        count += 1
    return count

def NumberToName(player):
    if (player == 1):
        return "Black"
    else:
        return "Red"