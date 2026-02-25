

class Parser:

    def __init__(self, file: str | None = None) -> None:
        self.file = file
        self.nb_drones = 0
        self.start: dict = {}
        self.end: dict = {}
        self.hubs: list[dict] = []
        self.error: str = ""

    def parse(self) -> bool:
        if not self.file:
            self.error = "there is no file to open!"
            return None
        try:
            with open(self.file, "r") as file:
                lines: list[str] = file.readlines()
                for line in lines:
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
                        if not self.__parse_hub(line):
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
            self.error = f"the x cordinet in should be int, in line '{line}'"
            return False
        try:
            dc["y"] = int(lwords[3])
        except Exception:
            self.error = f"the y cordinet should be int, in line '{line}'"
            return False

        color = lwords[4]
        if color.startswith("[") and color.endswith("]"):
            try:
                color_name, value = color.split("=")
                if color_name == "[color":
                    dc["color"] = value[0:-1]
                else:
                    nm = color_name[1:]
                    self.error = f"the key '{nm}' is not valid for color, in line '{line}'"
                    return False
            except Exception:
                self.error = f"color section is not well, in line '{line}'"
                return False
        else:
            self.error = f"messing parantheses, in line '{line}'"
            return False

        return True

    def __parse_hub(self, line: str) -> bool:
        # hub: roof1 3 4 [zone=restricted color=red]

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

        s = lwords[4] + lwords[5]

        if s.startswith("[") and s.endswith("]"):
            keys = s[1:-1].split(" ")

            try:
                color_name, value = s.split("")
                if color_name == "[color":
                    dc["color"] = value[0:-1]
                else:
                    nm = color_name[1:]
                    self.error = f"the key '{nm}' is not valid for color, in line '{line}'"
                    return False
            except Exception:
                self.error = f"color section is not well, in line '{line}'"
                return False
        else:
            self.error = f"messing parantheses, in line '{line}'"
            return False

        self.hubs.append(dc)

        return True

    def __parse_connection(self, line: str) -> bool:
        return True

    def set_file(self, file: str) -> None:
        self.file = file
