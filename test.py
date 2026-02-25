from fly_in_package.file_parser import Parser


parser = Parser()
parser.set_file("network_of_drones.txt")

if not parser.parse():
    print("Error:", parser.error)

print(str(parser.nb_drones))
print(str(parser.start))
print(str(parser.end))
print(str(parser.hubs))
# print(str())
