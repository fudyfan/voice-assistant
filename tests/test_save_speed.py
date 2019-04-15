import json
import io

print("open file\n")
with open('test_speed.json', 'r') as speedFile:
    results = json.load(speedFile)
    print("results from file\n")
    print(results)

speed = results["speed"]
print("speed from json: %d\n" % (speed))

print("manually set speed to 4")
speed = 4

print("opening file to write")
with open('test_speed.json', 'w') as speedFile_:
    speedFile_.write(json.dumps({'speed':speed}, indent=4))

print("check save file")