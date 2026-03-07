
from fly_in_package import Parser, Py_Game, AStarPathfinder

if __name__ == "__main__":
    parser = Parser()
    # parser.set_file("network_of_drones.txt")
    # parser.set_file("maps/challenger/01_the_impossible_dream.txt")
    parser.set_file("maps/hard/03_ultimate_challenge.txt")

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
