from util import Stack, Queue

def earliest_ancestor(ancestors, starting_node):

    crest = {}
    for p in ancestors:
        if p[1] not in crest:
            crest[p[1]] = []
        if p[0] not in crest:
            crest[p[0]] = []
        crest[p[1]].append(p[0])

    # def find_parents(node):
    #     parents = []
    #     for person in ancestors:
    #         if person[-1] == node:
    #             parents.append(person[0])
    #     return parents

    fam = Queue()
    fam.enqueue([starting_node])
    longest = []

    while fam.size() > 0:
        path = fam.dequeue()
        person = path[-1]

        for parent in crest[person]:
            new_path = list(path)
            new_path.append(parent)
            fam.enqueue(new_path)
            if len(new_path) > len(longest) or len(new_path) == len(longest) and new_path[-1] < longest[-1]:
                longest = new_path
    if not longest:
        return -1
    return longest[-1]