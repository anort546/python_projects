import json
with open("Practice4/sample-data.json", "r") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':45} {'Speed':10} {'MTU':5}")
print("-" * 80)


for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    dn = attributes["dn"]
    speed = attributes["speed"]
    mtu = attributes["mtu"]

    print(f"{dn:45} {speed:10} {mtu:5}")