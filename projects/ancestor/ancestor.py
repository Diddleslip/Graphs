class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Init a cache
cache = {}
def earliest_ancestor(ancestors, starting_node):

    
    # Add tuples to cache
    for i in ancestors:
        if i[0] not in cache:
            cache[i[0]] = set()
            cache[i[0]].add(i[1])
        else:
            cache[i[0]].add(i[1])
    # -------------------------------- Set up for graph
      
    s = Stack()

    visited = set()
    arrayList = list()

    s.push([starting_node])

    while s.size() > 0:
        path = s.pop()
        arrayList.append(path)

        v = path[-1]

        if v not in visited:
            ### We don't have anything for if it's oldest node possible
            visited.add(v)

            for next_vert in get_ancestors(v):
                newPath = list(path)
                newPath.append(next_vert)
                s.push(newPath)

    biggestIndex = (0, 0) # Index, Item(Values)
    for index, item in enumerate(arrayList):
        if len(item) > biggestIndex[1]:
            biggestIndex = (index, len(item))
        elif len(item) == biggestIndex[1]:
            # If last item is smaller than last biggestIndex, replace biggestIndex
            if item[-1] < arrayList[biggestIndex[0]][-1]:
                biggestIndex = (index, len(item))

    if len(arrayList) > 1:
        return arrayList[biggestIndex[0]][-1]
    else:
        return -1

def get_ancestors(v):
    parents = list()

    for key, value in cache.items():
        for secondVal in value:
            if v == secondVal:
                parents.append(key)

    return parents

# ------------ For testing
# test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
# print(earliest_ancestor(test_ancestors, 3))