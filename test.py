import heapq

graph = {
    "hub": ["roof1", "corridorA"],
    "roof1": ["roof2"],
    "roof2": ["goal"],
    "corridorA": ["tunnelB"],
    "tunnelB": ["goal"],
    "goal": []
}

# Simple heuristic: straight-line guess (0 for unweighted)
heuristic = {
    "hub": 2,
    "roof1": 1,
    "roof2": 2,
    "corridorA": 1,
    "tunnelB": 1,
    "goal": 0
}

def a_star(graph, start, goal):
    queue = []
    heapq.heappush(queue, (0 + heuristic[start], 0, start, [start]))
    visited = set()

    while queue:
        f, g, node, path = heapq.heappop(queue)
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                g_new = g + 1  # edge cost = 1
                f_new = g_new + heuristic[neighbor]
                heapq.heappush(queue, (f_new, g_new, neighbor, path + [neighbor]))

print(a_star(graph, "hub", "goal"))



def a_star_no_heap(graph, start, goal):
    # Each element: (node, path_so_far, g_cost)
    open_list = [(start, [start], 0)]
    visited = set()
    mylist = []
    while open_list:
        # Find the node with the lowest f = g + h
        current_index = 0
        current_f = open_list[0][2] + heuristic[open_list[0][0]]
        for i, (node, path, g) in enumerate(open_list):
            f = g + heuristic[node]
            if f < current_f:
                current_index = i
                current_f = f

        mylist.append(open_list[current_index])
        node, path, g = open_list.pop(current_index)

        if node == goal:
            for i in mylist:
                print(i)
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                open_list.append((neighbor, path + [neighbor], g + 1))  # edge cost = 1

# Test
print(a_star_no_heap(graph, "hub", "goal"))