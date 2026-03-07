
from fly_in_package import Parser, Py_Game, AStarPathfinder

parser = Parser()
parser.set_file("network_of_drones.txt")
parser.set_file("maps\maps\hard\\03_ultimate_challenge.txt")

if not parser.parse():
    print("Error:", parser.error)


drone_network = parser.get_DroneNetwork()

a_star = AStarPathfinder(drone_network)

all_paths = a_star.plan_paths_for_all_drones()


# print(drone_network.start)
# print(drone_network.end)
for hub in drone_network.hubs:
    print(hub)

# print("\nconnections:")
# for connection in drone_network.connections:
#     print(connection)

# print("\npaths:")
# for path in all_paths:
#     print(path)

index = 0
all_done = False
turns = -1
while not all_done:
    turns += 1
    all_done = True
    drone = 0
    index += 1
    for path in all_paths:
        drone += 1
        if len(path) > index:
            if path[index] != "wait":
                print(f"D{drone}-{path[index]} ", end="")
            all_done = False
    
    print("")

print("total turns:", turns)

 
my_game = Py_Game()

my_game.set_drone_network(drone_network)
my_game.set_drones_path(all_paths)

my_game.run()
