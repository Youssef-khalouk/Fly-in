
from fly_in_package import Parser, Py_Game


parser = Parser()
parser.set_file("network_of_drones.txt")

if not parser.parse():
    print("Error:", parser.error)

drone_network = parser.get_DroneNetwork()

my_game = Py_Game()
my_game.set_drone_network(drone_network)

my_game.run()
