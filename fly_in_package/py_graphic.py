from .file_parser import DroneNetwork
import pygame
from typing import Any
import math
import random


class Hub:
    def __init__(self, name: str, x: int, y: int, color: tuple, zone: str):
        self.name = name
        self.SU = 1
        self.size = 90
        self.x = x
        self.y = y
        self.color = color
        self.zone = zone
        self.hub_surface = self.__get_hub_surface()

    def scall(self, su: float) -> None:
        self.SU = su
        self.hub_surface = self.__get_hub_surface()

    def __get_hub_surface(self, size: int = 90) -> pygame.Surface:
        scaled_size = int(size * self.SU)

        big_surface = pygame.Surface(
            (scaled_size * 4, scaled_size * 4), pygame.SRCALPHA)

        center = scaled_size * 2
        outer_radius = scaled_size * 2
        inner_radius = int(scaled_size * 1.5)

        pygame.draw.circle(big_surface, self.color,
                           (center, center), outer_radius)

        pygame.draw.circle(big_surface, (255, 255, 255),
                           (center, center), inner_radius, 4)

        # -------- DRAW H --------
        h_height = scaled_size
        h_width = scaled_size * 0.6
        thickness = int(5 * self.SU)

        left_x = center - h_width // 2
        right_x = center + h_width // 2
        top_y = center - h_height // 2
        bottom_y = center + h_height // 2
        mid_y = center

        pygame.draw.line(big_surface, (255, 255, 255), (left_x, top_y),
                         (left_x, bottom_y), thickness)

        pygame.draw.line(big_surface, (255, 255, 255), (right_x, top_y),
                         (right_x, bottom_y), thickness)

        pygame.draw.line(big_surface, (255, 255, 255), (left_x, mid_y),
                         (right_x, mid_y), thickness)

        return pygame.transform.smoothscale(big_surface, (scaled_size,
                                                          scaled_size))


class Drone:
    def __init__(self, drone_image, x: int = 0, y: int = 0):
        # deferent place for every drone in the hub
        self.place = random.randint(10, 40)
        self.x = x + self.place
        self.y = y + self.place
        self.zone = "normal"
        self.drone_image = drone_image
        self.SU = 1
        self.drone_angle = 0
        self.rotated_drone = self.drone_image
        self.drone = self.__get_drone()
        self.__rotate_drone(0)
        self.speed = 4
        self.path: tuple[tuple[int] | str] | str = []
        self.which_hub = 0
        self.old_num = -1

        self.mv_x = 0
        self.mv_y = 0

        self.segment_start_x = 0
        self.segment_start_y = 0
        self.segment_total_distance = 0

    def set_path(self, path: list[tuple | str]) -> None:
        self.path = []
        for p in path:
            if isinstance(p, tuple):
                self.path.append((p[0] + self.place, p[1] + self.place, p[2]))
            else:
                self.path.append(p)
        self.x, self.y, h = self.path[0]

    def update(self) -> None:
        if not self.path:
            return
        if self.which_hub >= len(self.path):
            return

        wait = False

        i = self.which_hub
        while self.path[i] == "wait":
            i += 1
            wait = True
        target_x, target_y, zone = self.path[i]

        if self.which_hub != self.old_num:
            self.mv_x = self.x
            self.mv_y = self.y
            self.old_num = self.which_hub
            angle_radians = math.atan2(target_x-self.mv_x, target_y-self.mv_y)
            angle_degrees = math.degrees(angle_radians)
            self.__rotate_drone(angle_degrees)

            self.segment_start_x = self.mv_x
            self.segment_start_y = self.mv_y
            dx = target_x - self.mv_x
            dy = target_y - self.mv_y
            self.segment_total_distance = math.sqrt(dx*dx + dy*dy)

        dx = target_x - self.mv_x
        dy = target_y - self.mv_y

        distance = math.sqrt(dx*dx + dy*dy)

        # update progress
        traveled = self.segment_total_distance - distance
        if self.segment_total_distance == 0:
            progress = 0
        else:
            progress = traveled / self.segment_total_distance
        progress = max(0, min(1, progress))  # clamp 0..1
        # smooth speed
        if zone == "restricted":
            current_speed = (self.speed/2) * 4 * progress * (1 - progress)
        else:
            current_speed = self.speed * 4 * progress * (1 - progress)
        # minimum speed so it doesn't freeze at start
        current_speed = max(current_speed, 0.5)

        if not wait:
            scale = 50 + 20 * math.sin(math.pi * progress)
            self.drone = self.__get_drone(scale)

        if distance > current_speed:
            self.mv_x += (dx / distance) * current_speed
            self.mv_y += (dy / distance) * current_speed
            if not wait:
                self.x = self.mv_x
                self.y = self.mv_y
        else:
            self.which_hub += 1
            self.mv_x = target_x
            self.mv_y = target_y
            if not wait:
                self.x = target_x
                self.y = target_y
                self.zone = zone

    def get_position(self):
        return (self.x, self.y)

    def get_drone(self):
        return self.drone

    def scall(self, su: float) -> None:
        self.SU = su
        self.drone = self.__get_drone()

    def __get_drone(self, size: int = 50):
        size = int(size * self.SU) + 1
        return pygame.transform.smoothscale(self.rotated_drone, (size, size))

    def __rotate_drone(self, angle: int) -> None:
        if angle == self.drone_angle:
            return
        self.drone_angle = angle

        rotated = pygame.transform.rotate(self.drone_image, self.drone_angle)
        original_width, original_height = self.drone_image.get_size()
        rotated_width, rotated_height = rotated.get_size()
        crop_rect = pygame.Rect(
            (rotated_width - original_width) // 2,
            (rotated_height - original_height) // 2,
            original_width,
            original_height
        )
        self.rotated_drone = rotated.subsurface(crop_rect).copy()
        self.drone = self.__get_drone()


class Py_Game:
    def __init__(self):
        self.width = 1000
        self.height = 800
        # grad unit
        self.GU = 100
        # scall unit
        self.SU = 1.0
        self.canvas_x = 0
        self.canvas_y = 0
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fly_in")
        self.drone_image = pygame.image.load("images/drone.png"
                                             ).convert_alpha()
        self.ground_image = pygame.image.load("images/ground.png"
                                              ).convert_alpha()
        self.hubs: list[Hub] = []
        self.connections: list[tuple] = []
        self.ground = self.__scall_image(self.ground_image)
        self.font = pygame.font.SysFont(None, int(self.SU * 30))

        self.drones = []

    def __scall_image(self, image, size: int = 200) -> pygame.surface:
        size = int(size * self.SU) + 1
        return pygame.transform.smoothscale(image, (size, size))

    def set_drone_network(self, network: DroneNetwork) -> None:
        for hub in network.hubs:
            self.hubs.append(Hub(
                hub["name"],
                hub["x"] * self.GU,
                hub["y"] * self.GU,
                self.___get_color(hub["color"]),
                hub["zone"]))

        self.hubs.append(Hub(
            network.start["name"],
            network.start["x"] * self.GU,
            network.start["y"] * self.GU,
            self.___get_color(network.start["color"]),
            hub["zone"]))
        self.hubs.append(Hub(
            network.end["name"],
            network.end["x"] * self.GU,
            network.end["y"] * self.GU,
            self.___get_color(network.end["color"]),
            hub["zone"]))

        for connection in network.connections:
            if connection[0] == network.start["name"]:
                x1, y1 = network.start["x"], network.start["y"]
            if connection[0] == network.end["name"]:
                x1, y1 = network.end["x"], network.end["y"]
            else:
                x1, y1 = next(([h["x"], h["y"]]
                               for h in network.hubs
                               if h["name"] == connection[0]), [0, 0])

            if connection[1] == network.start["name"]:
                x2, y2 = network.start["x"], network.start["y"]
            if connection[1] == network.end["name"]:
                x2, y2 = network.end["x"], network.end["y"]
            else:
                x2, y2 = next(([h["x"], h["y"]]
                               for h in network.hubs
                               if h["name"] == connection[1]), [0, 0])

            self.connections.append((x1 * self.GU, y1 * self.GU,
                                     x2 * self.GU, y2 * self.GU))

        x = network.start["x"] * self.GU
        y = network.start["y"] * self.GU
        for _ in range(network.nb_drones):
            self.drones.append(Drone(self.drone_image, x, y))

    def set_drones_path(self, paths: list[str]) -> None:
        for i, path in enumerate(paths):
            if not path:
                continue
            drone_path = []
            for name in path:
                if name == "wait":
                    drone_path.append("wait")
                # connection is not passing but the code is detecting
                # where is the restrected hubs
                # if name == "connection":
                #     drone_path.append("connection")
                else:
                    for hub in self.hubs:
                        if hub.name == name:
                            drone_path.append((hub.x, hub.y, hub.zone))
                            break
            self.drones[i].set_path(drone_path.copy())

    def run(self) -> None:
        clock = pygame.time.Clock()

        while self.running:
            self.__check_keys(pygame.key.get_pressed())
            self.__check_events()
            self.__check_mouse_button()

            for x in range(int(self.width/(200 * self.SU)) + 2):
                for y in range(int(self.height/(200 * self.SU)) + 2):
                    self.screen.blit(self.ground, (
                        (self.canvas_x % (200*self.SU)) + ((x-1)*200*self.SU),
                        (self.canvas_y % (200*self.SU)) + ((y-1)*200*self.SU)))
            for connection in self.connections:
                pygame.draw.aaline(
                    self.screen,
                    (255, 255, 255),
                    (
                        ((connection[0] + 45)*self.SU)+self.canvas_x,
                        ((connection[1] + 45)*self.SU)+self.canvas_y
                    ), (
                        ((connection[2] + 45)*self.SU)+self.canvas_x,
                        ((connection[3] + 45)*self.SU)+self.canvas_y
                    )
                )
            for hub in self.hubs:
                self.screen.blit(hub.hub_surface, (
                    self.canvas_x + (hub.x*self.SU),
                    self.canvas_y + (hub.y*self.SU)
                ))
                # -------- DRAW TEXT --------
                t_surface = self.font.render(hub.name, True, (255, 255, 255))
                self.screen.blit(t_surface, (
                    self.canvas_x + ((hub.x) * self.SU),
                    self.canvas_y + ((hub.y + self.GU) * self.SU)
                ))
            for drone in self.drones:
                drone.update()
                self.screen.blit(drone.get_drone(), (
                    self.canvas_x + (drone.x*self.SU),
                    self.canvas_y + (drone.y*self.SU)
                ))

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def __check_keys(self, keys: Any) -> None:
        if keys[pygame.K_UP]:
            self.canvas_y -= 5

        if keys[pygame.K_DOWN]:
            self.canvas_y += 5

        if keys[pygame.K_LEFT]:
            self.canvas_x -= 5

        if keys[pygame.K_RIGHT]:
            self.canvas_x += 5

        if keys[pygame.K_a]:
            self.__scall_elements(.03)
        if keys[pygame.K_s]:
            self.__scall_elements(-.03)

    def __check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEWHEEL:
                self.__scall_elements(event.y * 0.4)

    def __scall_elements(self, scall_size: int) -> None:
        old_scale = self.SU
        self.SU += scall_size
        self.SU = max(0.1, min(self.SU, 4))
        scale_ratio = self.SU / old_scale
        self.font = pygame.font.SysFont(None, int(self.SU * 30))
        screen_center_x = self.screen.get_width() / 2
        screen_center_y = self.screen.get_height() / 2
        self.canvas_x = screen_center_x - (
            (screen_center_x - self.canvas_x) * scale_ratio)
        self.canvas_y = screen_center_y - (
            (screen_center_y - self.canvas_y) * scale_ratio)
        self.ground = self.__scall_image(self.ground_image)
        for drone in self.drones:
            drone.scall(self.SU)
        for hub in self.hubs:
            hub.scall(self.SU)

    def __check_mouse_button(self) -> None:
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            dx, dy = pygame.mouse.get_rel()
            self.canvas_x += dx
            self.canvas_y += dy
        else:
            pygame.mouse.get_rel()

    @staticmethod
    def ___get_color(color_name: str) -> tuple:
        colors = {
            # Basic
            "white": (255, 255, 255), "black": (0, 0, 0),
            "red": (255, 0, 0), "green": (0, 255, 0),
            "blue": (0, 0, 255), "yellow": (255, 255, 0),
            "cyan": (0, 255, 255), "magenta": (255, 0, 255),
            "gray": (128, 128, 128),

            # Extended
            "dark_gray": (64, 64, 64), "light_gray": (192, 192, 192),
            "orange": (255, 165, 0), "dark_orange": (255, 140, 0),
            "purple": (128, 0, 128), "violet": (238, 130, 238),
            "pink": (255, 192, 203), "hot_pink": (255, 105, 180),
            "brown": (139, 69, 19), "maroon": (128, 0, 0),
            "lime": (50, 205, 50), "dark_green": (0, 100, 0),
            "navy": (0, 0, 128), "sky_blue": (135, 206, 235),
            "teal": (0, 128, 128), "turquoise": (64, 224, 208),
            "gold": (255, 215, 0), "silver": (192, 192, 192),
            "beige": (245, 245, 220), "coral": (255, 127, 80),
            "salmon": (250, 128, 114), "indigo": (75, 0, 130),
            "olive": (128, 128, 0), "chocolate": (210, 105, 30),
            "crimson": (220, 20, 60), "khaki": (240, 230, 140),
            "lavender": (230, 230, 250),
        }
        return colors.get(color_name.lower(), (255, 255, 255))
