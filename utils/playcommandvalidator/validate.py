import os

import requests
import logging
import json

logging.basicConfig(level=logging.WARNING)  # Set logging level to DEBUG for detailed logs

def main():
    logging.debug("Starting...")
    try:
        resource_response = requests.get("https://api.hypixel.net/v2/resources/games")
        
        if resource_response.status_code != 200:
            logging.error("Failed to load API data.")
            return
        
        resource = resource_response.json()
        file_path = "./apis/playcommands.json"
        with open(file_path, 'r') as file:
            games = json.load(file)
        
        if not resource["success"] or not games["success"]:
            logging.error("API request not successful.")
            return
        
        gameIDs = []
        modeIDs = {}
        
        for gameObject in games["gameData"]:
            gameID = gameObject.get("game", "")
            if not gameID:
                logging.warning(f"Invalid game ID in play commands: {gameObject}")
                continue
            
            gameIDs.append(gameID)
            modes = gameObject.get("modes", [])
            for mode in modes:
                if mode.get("modeName", "") == "":
                    logging.warning(f"Invalid mode name (id) in play commands for game '{gameID}': {mode}")
                    continue
                if mode.get("name", "") == "":
                    logging.warning(f"Missing mode coloquial name in play commands for game '{gameID}': {mode}")
                    continue
                if mode.get("identifier", "") == "":
                    if not mode.get("requirements", {}).get("unavailable", False):
                        logging.warning(f"Missing mode identifier (playcommand) in play commands for game '{gameID}': {mode}")
                        continue
                modeIDs.setdefault(gameID, {})[mode.get("modeName", "")] = mode.get("name", "")
            modeIDs[gameID] = {y.get("modeName", ""): y.get("name", "") for y in modes}
        
        logging.debug(f"Loaded game IDs: {gameIDs}")
        logging.debug(f"Loaded mode IDs: {modeIDs}")
        
        for game in resource["games"]:
            if game not in gameIDs:
                logging.warning(f"Game '{game}' in resource but not in play commands.")
                continue
            
            resource_modes = resource["games"][game].get("modeNames", {})
            logging.debug(f"Checking modes for game '{game}': {resource_modes}")
            
            for mode in resource_modes:
                if mode not in modeIDs.get(game, {}):
                    logging.warning(f"Mode '{mode}' in resource but not found in play commands for game '{game}'.")
                else:
                    expected_name = resource["games"][game]["modeNames"][mode]
                    actual_name = modeIDs[game][mode]
                    if actual_name != expected_name:
                        logging.warning(f"Mismatched names for mode '{mode}' in game '{game}': actual='{actual_name}', expected='{expected_name}'")
        
        logging.debug("Ending...")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")

if __name__ == '__main__':
    main()
