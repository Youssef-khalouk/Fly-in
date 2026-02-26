

class Parser:

    def __init__(self, file: str | None = None) -> None:
        self.file = file
        self.nb_drones = 0
        self.start: dict = {}
        self.end: dict = {}
        self.hubs: list[dict] = []
        self.error: str = "no error"

    def parse(self) -> bool:
        if not self.file:
            self.error = "there is no file to open!"
            return None
        try:
            with open(self.file, "r") as file:
                lines: list[str] = file.readlines()
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

        except (FileNotFoundError, Exception) as e:
            self.error = str(e)
            return False
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

        dc = self.start
        if hub == "end":
            dc = self.end

        dc["name"] = lwords[1]
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

        metadata = self.__parse_zone_metadata(" ".join(lwords[4:]), line)

        if not metadata:
            return False
        dc.update(metadata)
        return True

    def __parse_hub(self, line: str) -> bool:

        lwords = line.split()

        dc = {}

        dc["name"] = lwords[1]
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

        metadata = self.__parse_zone_metadata(" ".join(lwords[4:]), line)

        if not metadata:
            return False
        self.hubs.append(metadata)
        return True

    def __parse_connection(self, line: str) -> bool:
        return True

    def __parse_zone_metadata(self, data: str, line: str = "") -> dict | None:
        if data.startswith("[") and data.endswith("]"):
            data = data[1:-1]
        else:
            self.error = f"messing paranthes in line '{line}'"
            return None
        tags = data.split()
        dc: dict = {"zone": "normal",
                    "color": "none",
                    "max_drones": 1}
        for tag in tags:
            key_value = tag.split("=")
            if len(key_value) != 2:
                self.error = f"there is error in this metadata line ->'{line}'"
                return None
            if key_value[0] == "":
                self.error = f"messing key name in this line -> '{line}'"
                return None
            if key_value[1] == "":
                self.error = "messing value for this key"
                self.error += f" '{key_value[0]}' in this line -> '{line}'"
                return None
            if key_value[0] == "max_drones":
                try:
                    num = int(key_value[1])
                    dc["max_drones"] = num
                except Exception as e:
                    self.error = str(e) + f" in line -> {line}"
                    return None
            else:
                dc[key_value[0]] = key_value[1]
        return dc

    def set_file(self, file: str) -> None:
        self.file = file









parser = Parser()
parser.set_file("network_of_drones.txt")

if not parser.parse():
    print("Error:", parser.error)

print(str(parser.nb_drones))
print(str(parser.start))
print(str(parser.end))
for hub in parser.hubs:
    print(hub)
# print(str())
