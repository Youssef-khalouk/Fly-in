import heapq

graph = {
    "hub": ["roof1", "corridorA", "mahta"],
    "roof1": ["roof2"],
    "roof2": ["torot", "lhdim"],
    "corridorA": ["tunnelB"],
    "tunnelB": ["torot"],
    "mahta": ["tunnelB", "torot"],
    "torot": ["goal"],
    "lhdim": ["goal"],
    "goal": []
}

cost = {
    "hub": 2,
    "roof1": 1,
    "roof2": 2,
    "corridorA": 1,
    "tunnelB": 1,
    "torot": 4,
    "mahta": 2,
    "goal": 1,
    "lhdim": 4
}


def greedy_best_first_heap(graph, start, goal):
    heap = []
    heapq.heappush(heap, (cost[start], start, [start]))
    visited = set()

    while heap:
        # print("====")
        # for i in heap:
        #     print(i)
        # print("======")
        h, node, path = heapq.heappop(heap)

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                heapq.heappush(heap, (cost[neighbor] + h, neighbor, path + [neighbor]))


# Test
print(greedy_best_first_heap(graph, "hub", "goal"))
