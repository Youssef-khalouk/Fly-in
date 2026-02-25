class Hub:
    def __init__(self, name, x, y, zone="normal", color=None, max_drones=1):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.zone = zone
        self.color = color
        self.max_drones = int(max_drones)


class Connection:
    def __init__(self, hub1, hub2, max_link_capacity=1):
        self.hub1 = hub1
        self.hub2 = hub2
        self.max_link_capacity = int(max_link_capacity)


class DroneNetwork:
    def __init__(self):
        self.nb_drones = 0
        self.hubs = {}
        self.connections = []
        self.start = None
        self.end = None
