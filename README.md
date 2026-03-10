*This project has been created as part of the 42 curriculum by ykhalouk.*

# Description

This project implements a multi-drone pathfinding simulator using A* search on a user-defined network of hubs and connections. It reads a configuration file describing start/end hubs, intermediate hubs, and connections, then plans collision-aware routes for multiple drones while respecting hub capacities, link capacities, and zone restrictions.

The program includes both a command-line solver and a real-time graphical visualization using pygame. The goal is to demonstrate multi-agent path planning and visualize drone movement in a simplified airspace.

# Instructions

## Requirements

- Python 3.14 (tested)
- `pygame` 

## Setup

1. Create and activate a virtual environment (optional):

```sh
python -m venv my_env
source my_env\lib\activate
```

2. Install dependencies:

```sh
python -m pip install pygame
```

## Running the project

### Command-line solver

From the repository root:

```sh
python fly_in.py <path_to_map_file>
```

Example:

```sh
python fly_in.py maps/network_of_drones.txt
```

### Graphical visualization

Run the same command; the program will display a pygame window showing the drones moving along their planned paths.

# Algorithm & Implementation

The pathfinder uses **A\\*** search to compute a path from the start hub to the end hub. Key implementation details:

- **Heuristic**: Manhattan distance between current hub and goal.
- **State**: Includes hub, time step (path length), and parent hub to prevent immediate backtracking.
- **Reservations**: The algorithm reserves hubs and links per time-step to avoid collisions between multiple drones.
- **Zone effects**:
  - `restricted`: prohibits traversal and slows movement in visualization.
  - `blocked`: disallows traversal.
  - `priority`: gives a small bonus in cost to prefer those hubs.
- **Multi-drone planning**: The solver iterates for each drone, reusing reservations so later drones avoid earlier drone paths.

# Visual Representation

The pygame GUI shows:

- **Hubs** as circles with an "H" icon, scaled based on zoom level.
- **Connections** as lines between hubs.
- **Drones** as rotating sprites that move smoothly along computed paths.
- **Zoom & Pan**: Use arrow keys to pan the view and `A`/`S` keys to zoom in/out.
- **Hub labels**: Toggle via `H` key.

These visual features make it easier to understand the path planning decisions and observe drone interactions over time.

# Resources

- A* Search algorithm: https://en.wikipedia.org/wiki/A*_search_algorithm
- Pygame documentation: https://www.pygame.org/docs/


# Movement Mathematics

### polynomial esaing
$f(t) = 3t^2 - 2t^3$

or

$f(t)=t^2(3−2t)$

    for step in range(21):
        progress = step / 20   # 0.0 -> 1.0
        ease = 3*progress**2 - 2*progress**3
        value = start + ((end - start) * ease)


### cosine easing

$f(t)=0.5−0.5cos(πt)$

same as:

$f(t) = \frac{1 - \cos(\pi t)}{2}$

    for step in range(21):
        progress = step / 20
        ease = .5 - (.5 * math.cos(math.pi * progress))
        value = start + ((end - start) * ease)


## calcualte distence 
  $d = √((x₂ − x₁)² + (y₂ − y₁)²)$

    x1, y1 = 2, 3
    x2, y2 = 6, 7

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    print(distance)
