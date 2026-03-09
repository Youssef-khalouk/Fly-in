import sys
from fly_in_package import Parser, Py_Game, AStarPathfinder

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("mesing config file : python3 fly_in.py <config.txt>")
        sys.exit(1)

    parser = Parser()
    parser.set_file(sys.argv[1])
    # parser.set_file("maps/network_of_drones.txt")
    # parser.set_file("maps/impossible_map.txt")
    # parser.set_file("maps/01_the_impossible_dream.txt")

    if not parser.parse():
        print("Error:", parser.error)
        exit(1)

    drone_network = parser.get_DroneNetwork()

    a_star = AStarPathfinder(drone_network)
    all_paths = a_star.plan_paths_for_all_drones()
    a_star.print_moves()

    my_game = Py_Game()
    my_game.set_drone_network(drone_network)
    my_game.set_drones_path(all_paths)
    my_game.run()
