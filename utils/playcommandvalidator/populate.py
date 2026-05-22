import json
import logging
import time

logging.basicConfig(level=logging.WARNING)

def main():
  file_path = "./apis/playcommands.json"
  logging.debug("Loading file")
  with open(file_path, 'r') as file:
    data = json.load(file)
  logging.debug("Loaded file")

  commandsList = []

  for game in data["gameData"]:
    for mode in game["modes"]:
      if "modeName" not in mode:
        logging.warn(f"No modeName found for `{mode}`")
      
      elif "identifier" in mode and mode["identifier"] != None:
        currID = mode["identifier"]
        logging.debug(f"Identifier `{currID}` for `{mode["modeName"]}`")
        if(currID in commandsList):
          logging.warn(f"Found duplicate identifier {currID}")
        commandsList.append(currID)

      else:
        logging.debug(f"No Identifier found for `{mode["modeName"]}`")

  commandsList = sorted(commandsList)
  data["commandsRaw"] = commandsList
  current_time = int(time.time())
  data["lastUpdated"] = current_time

  response = input(f"Generated {len(commandsList)} identifiers. Input `push` to merge list with source.\n")
  if response == "push":
    with open(file_path, 'w') as file:
      json.dump(data, file)
    logging.debug(f"Pushed {len(commandsList)} identifiers.")

if __name__ == '__main__':
    main()
