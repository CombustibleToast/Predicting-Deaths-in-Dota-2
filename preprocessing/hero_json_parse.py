import json

file = open("heroes.json")
raw = json.load(file)

role_indexes = {}
i = 0
for _, data in raw.items():
	for role in data["roles"]:
		if role not in role_indexes:
			role_indexes[role] = i
			i += 1

print("role mapping:", role_indexes)

mapping = {}
for _, data in raw.items():
	# print(data)

	parsed_name = data["name"].removeprefix("npc_dota_hero_").replace("_", "")
	# print(parsed_name)

	id = data["id"]
	# print(id)

	# roles = data["roles"] # raw roles as strings
	roles = [role_indexes[x] for x in data["roles"]] # roles as indexes
	# print(roles)

	# Map
	mapping[parsed_name] = {"id": id, "roles": roles}

	# Only do 1 entry for now
	# break

# print(json.dumps(raw))
output_file = open("heroes_parsed.json", "w")
json.dump(mapping, output_file, indent=4)