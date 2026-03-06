
from fly_in_package import Parser, Py_Game, AStarPathfinder

parser = Parser()
parser.set_file("network_of_drones.txt")

if not parser.parse():
    print("Error:", parser.error)


drone_network = parser.get_DroneNetwork()

a_star = AStarPathfinder(drone_network)

all_paths = a_star.plan_paths_for_all_drones()


# print(drone_network.start)
# print(drone_network.end)
# for hub in drone_network.hubs:
#     print(hub)

# print("\nconnections:")
# for connection in drone_network.connections:
#     print(connection)

# print("\npaths:")
# for path in all_paths:
#     # print(path)
#     for i in path:
#         if i == "connection":
#             print(path)


my_game = Py_Game()

my_game.set_drone_network(drone_network)
my_game.set_drones_path(all_paths)

my_game.run()
