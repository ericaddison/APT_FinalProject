import random


colors_policy = {'name': 'colors_policy',
                 'names': ['Mr. Blue', 'Mr. Black', 'Mr. Red', 'Mr. White', 'Mr. Green']
                 }


def get_name(conv, policy):
    """Generate a random name for the given conversation from the given policy"""
    aliases = conv.get_aliases()
    names = policy['names']
    random.shuffle(names)
    ind = 0
    nameind = 1
    name = names[ind]
    while name in aliases:
        name = names[ind%len(names)]
        if ind > len(names):
            name += nameind
            nameind += 1
    return name
