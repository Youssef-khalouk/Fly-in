
from fly_in_package import Parser, Py_Game, AStarPathfinder


parser = Parser()
parser.set_file("network_of_drones.txt")

if not parser.parse():
    print("Error:", parser.error)


drone_network = parser.get_DroneNetwork()

print(drone_network.start)
print(drone_network.end)
for hub in drone_network.hubs:
    print(hub)
for connection in drone_network.connections:
    print(connection)

a_star = AStarPathfinder(drone_network)


# my_game = Py_Game()
# my_game.set_drone_network(drone_network)

# my_game.run()
