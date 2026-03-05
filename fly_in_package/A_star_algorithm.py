import heapq
# import math
from .file_parser import DroneNetwork

# heuristic is the distance to the goal


class AStarPathfinder:
    def __init__(self, drone_network: DroneNetwork):
        self.network = drone_network
        self.connections = drone_network.connections
        self.hubs = {h["name"]: h for h in drone_network.hubs}
        self.start = drone_network.start
        self.end = drone_network.end
        self.all_paths = []

    def movement_cost(self, next_hub: str, pos: int) -> float:
        h = 2
        the_hub = self.hubs.get(next_hub)
        if not the_hub:
            return -1
        # for path in self.all_paths:
        #     if path[pos] == next_hub:
        #         return -10
        if the_hub.get("zone") == "blocked":
            return -1
        if the_hub.get("zone") == "restricted":
            h += 1
        if the_hub.get("zone") == "priority":
            h -= 1
        return h

    def find_path(self) -> list[str] | None:
        heap = []
        heapq.heappush(heap, (0, self.start["name"], [self.start["name"]]))
        vesited = set()

        while heap:
            # print("\n=============")
            # for hub in heap:
            #     print(hub)

            h, hub, path = heapq.heappop(heap)

            if hub == self.end["name"]:
                return path

            if hub not in vesited:
                vesited.add(hub)
                for i in self.connections:
                    if i[0] == hub:
                        m_cost = h + self.movement_cost(i[1], len(path))
                        if m_cost >= 0:
                            heapq.heappush(heap, (m_cost, i[1], path + [i[1]]))
                            break
                        # elif m_cost == -10:



        return None

    def plan_paths_for_all_drones(self) -> list[list[str]]:
        self.all_paths = []
        for i in range(self.network.nb_drones):
            self.all_paths.append(self.find_path())
        return self.all_paths
