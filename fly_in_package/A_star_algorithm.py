import heapq
import math
from .file_parser import DroneNetwork

class AStarPathfinder:
    def __init__(self, drone_network: DroneNetwork):
        self.network = drone_network


    def heuristic(self, a: str, b: str) -> float:
        pass

    def get_cost(self, node: str) -> float:
        pass

    def find_path(self, start: str, goal: str) -> list[str] | None:
        pass

    def plan_paths_for_all_drones(self) -> list[list[str]]:
        pass