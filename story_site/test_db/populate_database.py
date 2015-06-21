import json    

with open("countriesToCities2.json", "rb") as source:
    contents = json.load(source)


query = "INSERT story_site_country (`name`) VALUES ('None');\n"
for country in contents:
    if not country=="":
        query += "INSERT story_site_country (`name`) VALUES ('"+country+"');\n"

        for city in contents[country]:
            print city

with open("countriesDump.sql", "w") as dest:
    dest.write(query.encode('utf-8'))




