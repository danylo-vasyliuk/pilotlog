import json
from pprint import pprint


with open("import - pilotlog_mcc.json") as f:
    a = f.read()


a = a.replace('\\"', '"')
a = json.loads(a)

# aircraft = next(filter(lambda i: i["table"] == "Aircraft", a))
# flight = next(filter(lambda i: i["table"] == "Flight", a))
#
# pprint(aircraft)
# pprint(flight)
s = set()

for i in a:
    s.add(i["table"])

print(s)
with open("test_data.json", "w") as f:
    json.dump(a, f, indent=4)
