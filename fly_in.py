import sys
from fly_in_package import Parser, Py_Game, AStarPathfinder

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("mesing config file : python3 fly_in.py <config.txt>")
        sys.exit(1)

    parser = Parser()
    parser.set_file(sys.argv[1])

    if not parser.parse():
        print("Error:", parser.get_error())
        exit(1)

    drone_network = parser.get_DroneNetwork()

    a_star = AStarPathfinder(drone_network)
    all_paths = a_star.plan_paths_for_all_drones()
    if not all_paths:
        print("error: there is no valid path!")
        exit(1)
    a_star.print_moves()

    my_game = Py_Game()
    my_game.set_drone_network(drone_network)
    my_game.set_drones_path(all_paths)
    my_game.run()
