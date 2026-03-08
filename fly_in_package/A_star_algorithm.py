import heapq
from .file_parser import DroneNetwork

# heuristic is the distance to the goal


class AStarPathfinder:
    def __init__(self, drone_network: DroneNetwork):
        self.network = drone_network

        self.hubs = {h["name"]: h for h in drone_network.hubs}
        self.start = drone_network.start
        self.end = drone_network.end
        self.hubs[self.start["name"]] = self.start
        self.hubs[self.end["name"]] = self.end

        self.all_paths = []

        self.graph = {}
        for a, b, data in drone_network.connections:
            if a not in self.graph:
                self.graph[a] = []
            if b not in self.graph:
                self.graph[b] = []
            self.graph[a].append((b, data))
            self.graph[b].append((a, data))

        self.hub_reservations = {}
        self.link_reservations = {}

    def __register_path(self, path):
        for pos in range(len(path)):
            hub = self.__hub_at_time(path, pos)
            if hub:
                hub_at_time = (hub, pos)
                reserations = self.hub_reservations.get(hub_at_time, 0)
                self.hub_reservations[hub_at_time] = reserations + 1
            link = self.__link_at_time(path, pos)
            if link:
                lint_at_time = (link, pos)
                reserations = self.link_reservations.get(lint_at_time, 0)
                self.link_reservations[lint_at_time] = reserations + 1

    def __heuristic(self, hub: str) -> int:
        hx = self.hubs[hub]["x"]
        hy = self.hubs[hub]["y"]
        gx = self.end["x"]
        gy = self.end["y"]

        # manhattan distance
        return abs(hx - gx) + abs(hy - gy)

    def __hub_at_time(self, path: list[str], t: int) -> str:
        if not path:
            return ""
        t = min(t, len(path) - 1)
        if path[t] == "connection":
            return path[t+1]
        while t > 0 and path[t] == "wait":
            t -= 1
        return path[t]

    def __link_at_time(self, path: list[str], pos: int) -> str:
        if len(path) <= pos or pos < 0:
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
            return 2, 0

        # check the max drones in the hub
        drones_in_hub = self.hub_reservations.get((next_hub, pos), 0)
        if drones_in_hub >= the_hub["max_drones"]:
            return -2, 0
        # ckeck the max link capacity
        link = f"{curent_hub}-{next_hub}"
        drones_in_link = self.link_reservations.get((link, pos), 0)
        if drones_in_link >= data["max_link_capacity"]:
            return -2, 0

        zone = the_hub.get("zone")

        if zone == "restricted":
            return -3, 0

        if zone == "blocked":
            return -1, 0

        if zone == "priority":
            bonus += 1

        return 1, bonus

    def find_path(self) -> list[str] | None:
        heap = []
        name = self.start["name"]
        heapq.heappush(heap, (0, 0, 0, name, [name], None))
        vesited = set()
        while heap:
            g, _, _, hub, path, parent = heapq.heappop(heap)

            if hub == self.end["name"]:
                self.__register_path(path)
                return path

            state = (hub, len(path), parent)
            if state in vesited:
                continue

            vesited.add(state)
            for next_h, data in self.graph.get(hub, []):
                if next_h == parent:
                    continue
                cost, bonus = self.__movement_cost(
                                    hub, next_h, len(path), data)
                heur = self.__heuristic(next_h)
                node = ()
                if cost == -1:
                    continue
                elif cost == -2:
                    if next_h == self.end["name"]:
                        return []
                    node = (g+1, -1, heur, hub, path+["wait"], parent)
                elif cost == -3:
                    array = ["connection", next_h]
                    node = (g+2, 0, heur, next_h, path + array, hub)
                elif cost >= 0:
                    node = (g+cost, -bonus, heur, next_h, path+[next_h], hub)
                else:
                    continue
                heapq.heappush(heap, node)

        return None

    def plan_paths_for_all_drones(self) -> list[list[str]]:
        self.all_paths = []
        for i in range(self.network.nb_drones):
            path = self.find_path()
            if path:
                self.all_paths.append(path)
        return self.all_paths

    def print_moves(self) -> None:
        if not self.all_paths:
            return
        index = 0
        all_done = False
        turns = -1
        while not all_done:
            turns += 1
            all_done = True
            drone = 0
            index += 1
            for path in self.all_paths:
                drone += 1
                if len(path) > index:
                    if path[index] != "wait":
                        print(f"D{drone}-{path[index]} ", end="")
                    all_done = False
            print("")

        print("total turns:", turns)
