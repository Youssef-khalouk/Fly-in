
class DroneNetwork:
    def __init__(self):
        self.nb_drones = 0
        self.hubs = {}
        self.connections = []
        self.start = None
        self.end = None


class Parser:

    def __init__(self, file: str | None = None) -> None:
        self.file = file
        self.nb_drones = 0
        self.start: dict = {}
        self.end: dict = {}
        self.hubs: list[dict] = []
        self.connections: list[tuple] = []
        self.error: str = "no error"
        self.__hubs_names: list[str] = []

    def parse(self) -> bool:
        if not self.file:
            self.error = "there is no file to open!"
            return None
        try:
            with open(self.file, "r") as file:
                lines: list[str] = file.readlines()
                oky = self.__validate_content_and_order(lines)
                if not oky:
                    return False
                for line in lines:
                    if line.startswith("#"):
                        continue
                    if line.endswith("\n"):
                        line = line[0:-1]
                    if line.startswith("nb_drones:"):
                        if not self.__parse_nb_drones(line):
                            return False

                    elif line.startswith("start_hub:"):
                        if not self.__parse_start_end_hub(line, "start"):
                            return False

                    elif line.startswith("end_hub:"):
                        if not self.__parse_start_end_hub(line, "end"):
                            return False

                    elif line.startswith("hub:"):
                        if not self.__parse_hub(line):
                            return False

                    elif line.startswith("connection:"):
                        if not self.__parse_connection(line):
                            return False
                    elif line.strip():
                        self.error = f"unknown line '{line}'"
                        return False

        except (FileNotFoundError, Exception) as e:
            self.error = str(e)
            return False
        return True

    def __validate_content_and_order(self, lines: list[str]) -> bool:
        if not any(line.startswith("nb_drones") for line in lines):
            self.error = "config file should have 'nb_drones' paramter."
            return False
        if not any(line.startswith("start_hub") for line in lines):
            self.error = "config file should have 'start_hub' parameter."
            return False
        if not any(line.startswith("end_hub") for line in lines):
            self.error = "config file should have 'end_hub' parameter."
            return False
        order = "none"
        for line in lines:
            if line.startswith("start_hub:"):
                if order != "none":
                    self.error = "the start_hub should be in the "
                    self.error += "toop of file after nb_drones."
                    return False
            elif line.startswith("end_hub:"):
                if order != "none":
                    self.error = "the end_hub should be in the "
                    self.error += "toop of file after start_hub."
                    return False
            elif line.startswith("hub:"):
                if order == "connection":
                    self.error = f"wrong order for hub line: {line}"
                    return False
                order = "hub"
                continue
            elif line.startswith("connection:"):
                order = "connection"
        return True

    def __parse_nb_drones(self, line: str) -> bool:
        lwords = line.split(":")
        if len(lwords) != 2:
            self.error = "there is an error in number or drones!"
            return False
        value = lwords[1].replace("\n", "")
        value = value.replace(" ", "")

        if not value:
            self.error = "there is an error in number of drones!"
            return False
        try:
            self.nb_drones = int(value)
        except Exception:
            self.error = "the number of drones is not int!"
            return False
        return True

    def __parse_start_end_hub(self, line: str, hub: str) -> bool:
        lwords = line.split()
        self.__hubs_names.append(lwords[1])
        dc = self.start
        if hub == "end":
            dc = self.end
        dc.update({
            "name": lwords[1],
            "zone": "normal",
            "color": "none",
            "max_drones": 1})

        try:
            dc["x"] = int(lwords[2])
        except Exception:
            self.error = f"the x cordinet should be int, in line '{line}'"
            return False
        try:
            dc["y"] = int(lwords[3])
        except Exception:
            self.error = f"the y cordinet should be int, in line '{line}'"
            return False

        if not self.__parse_zone_metadata(" ".join(lwords[4:]), line, dc):
            return False
        return True

    def __parse_hub(self, line: str) -> bool:

        lwords = line.split()
        self.__hubs_names.append(lwords[1])
        dc: dict = {"name": lwords[1],
                    "zone": "normal",
                    "color": "none",
                    "max_drones": 1}
        try:
            dc["x"] = int(lwords[2])
        except Exception:
            self.error = f"the x cordinet in should be int, in line '{line}'"
            return False
        try:
            dc["y"] = int(lwords[3])
        except Exception:
            self.error = f"the y cordinet should be int, in line '{line}'"
            return False

        if len(lwords) > 4:
            if not self.__parse_zone_metadata(" ".join(lwords[4:]), line, dc):
                return False
        self.hubs.append(dc)
        return True

    def __parse_connection(self, line: str) -> bool:
        lwords = line.split()
        if len(lwords) < 2:
            self.error = f"no parameters in line -> '{line}'"
            return False
        connection = lwords[1].split("-")
        if len(connection) != 2:
            self.error = f"the connection '{connection}' "
            self.error += f"is not valid in line '{line}'"
            return False
        dc = {"max_link_capacity": 1}
        if len(lwords) > 2:
            if not self.__parse_zone_metadata(" ".join(lwords[2:]), line, dc):
                return False

        if connection[0] not in self.__hubs_names:
            self.error = f"the hub '{connection[0]}' doesn't exist in hubs."
            return False
        if connection[1] not in self.__hubs_names:
            self.error = f"the hub '{connection[1]}' doesn't exist in hubs."
            return False
        self.connections.append((connection[0], connection[1], dc))
        return True

    def __parse_zone_metadata(self, data: str, line: str, dc: dict) -> bool:
        start = data.find("[")
        end = data.find("]")
        if start != -1 and end != -1 and end > start:
            the_else = data[end + 1:].strip()
            if the_else:
                self.error = f"unknown '{the_else}' in line -> '{line}'"
                return False
            data = data[start + 1:end]
        else:
            self.error = f"messing square brackets in line '{line}'"
            return False

        tags = data.split()
        for tag in tags:
            key_value = tag.split("=")
            if len(key_value) != 2:
                self.error = f"there is error in this metadata line ->'{line}'"
                return False
            if key_value[0] == "":
                self.error = f"messing key name in this line -> '{line}'"
                return False
            if key_value[1] == "":
                self.error = "messing value for this key"
                self.error += f" '{key_value[0]}' in this line -> '{line}'"
                return False
            if (
                    key_value[0] == "max_drones"
                    or key_value[0] == "max_link_capacity"):
                try:
                    num = int(key_value[1])
                    if num <= 0:
                        self.error = f"the key {key_value[0]}={num},"
                        self.error += " should be positive and more then 0."
                        return False
                    dc[key_value[0]] = num
                except Exception as e:
                    self.error = str(e) + f" in line -> {line}"
                    return False
            else:
                dc[key_value[0]] = key_value[1]
        return True

    def set_file(self, file: str) -> None:
        self.file = file

    def get_error(self):
        return self.error

    def get_DroneNetwork(self) -> DroneNetwork:
        drone_network = DroneNetwork()
        drone_network.nb_drones = self.nb_drones
        drone_network.hubs = self.hubs
        drone_network.connections = self.connections
        drone_network.start = self.start
        drone_network.end = self.end
        return drone_network
