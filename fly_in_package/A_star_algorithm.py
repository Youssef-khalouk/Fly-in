import heapq
from .file_parser import DroneNetwork

# heuristic is the distance to the goal


class AStarPathfinder:
    def __init__(self, drone_network: DroneNetwork):
        self.network = drone_network
        self.hubs = {h["name"]: h for h in drone_network.hubs}
        self.start = drone_network.start
        self.end = drone_network.end
        self.all_paths = []

        self.graph = {}
        for a, b, data in drone_network.connections:
            if a not in self.graph:
                self.graph[a] = []
            if b not in self.graph:
                self.graph[b] = []
            self.graph[a].append((b, data))
            self.graph[b].append((a, data))

    def __hub_at_time(self, path: list[str], t: int) -> str:
        if not path:
            return ""
        t = min(t, len(path) - 1)
        while t > 0 and path[t] in ("wait", "connection"):
            t -= 1
        return path[t]

    def __link_at_time(self, path: list[str], pos: int) -> str:
        if len(path) <= pos:
            return ""
        next_hub = path[pos]
        pos -= 1
        while pos > 0 and path[pos] in ("wait", "connection"):
            pos -= 1
        return f"{path[pos]}-{next_hub}"

    def __movement_cost(self, curent_hub: str, next_hub: str,
                        pos: int, data: dict) -> tuple[int, int]:
        bonus = 0
        the_hub = self.hubs.get(next_hub)
        if not the_hub:
            return 1, 0

        zone = the_hub.get("zone")
        if zone == "blocked":
            return -1, 0
        if zone == "restricted":
            return -3, 0
        if zone == "priority":
            bonus += 1

        # check the max drones in the hub
        count = 0
        for path in self.all_paths:
            other_hub = self.__hub_at_time(path, pos)
            if other_hub == next_hub:
                count += 1
        if count >= the_hub["max_drones"]:
            return -2, 0

        # check the max_link_capacity
        count = 0
        curent_link = f"{curent_hub}-{next_hub}"
        for path in self.all_paths:
            if curent_link == self.__link_at_time(path, pos):
                count += 1
        if count >= data["max_link_capacity"]:
            return -2, 0

        return 1, bonus

    def find_path(self) -> list[str] | None:
        heap = []
        heapq.heappush(heap, (0, 0, self.start["name"], [self.start["name"]]))
        visited = set()
        last_hub = ""
        while heap:
            h, _, hub, path = heapq.heappop(heap)

            if hub == self.end["name"]:
                return path
            state = (hub, len(path))
            if state not in visited:
                visited.add((hub, len(path)))
                for next_h, data in self.graph.get(hub, []):
                    if next_h == last_hub:
                        continue
                    cost, bonus = self.__movement_cost(hub, next_h, len(path), data)
                    if cost == -1:
                        continue
                    elif cost == -2:
                        heapq.heappush(heap, (h+1, bonus, hub, path+["wait"]))
                        last_hub = hub
                    elif cost == -3:
                        heapq.heappush(heap, (h+2, bonus, next_h, path+["connection", next_h]))
                        last_hub = hub
                    elif cost >= 0:
                        heapq.heappush(heap, (h+cost, bonus, next_h, path+[next_h]))
                        last_hub = hub

        return None

    def plan_paths_for_all_drones(self) -> list[list[str]]:
        self.all_paths = []
        for i in range(self.network.nb_drones):
            path = self.find_path()
            if path:
                self.all_paths.append(path)
        return self.all_paths
