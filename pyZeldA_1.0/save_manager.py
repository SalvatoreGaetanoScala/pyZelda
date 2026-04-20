import json
import os
from settings import BASE_DIR

SAVES_DIR = os.path.join(BASE_DIR, "saves")

class SaveManager:
    def __init__(self):
        if not os.path.exists(SAVES_DIR):
            os.makedirs(SAVES_DIR)

    def get_slot_path(self, slot_id):
        return os.path.join(SAVES_DIR, f"save_slot_{slot_id}.json")

    def save_game(self, slot_id, game_data):
        """Salva i dati nel file slot specificato."""
        path = self.get_slot_path(slot_id)
        try:
            with open(path, 'w') as f:
                json.dump(game_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")
            return False

    def load_game(self, slot_id):
        """Carica i dati dal file slot."""
        path = self.get_slot_path(slot_id)
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Errore nel caricamento: {e}")
            return None

    def delete_save(self, slot_id):
        """Elimina il file di salvataggio dello slot specificato."""
        path = self.get_slot_path(slot_id)
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except Exception as e:
                print(f"Errore eliminazione save: {e}")
                return False
        return False

    def get_slots_info(self):
        """Restituisce una lista di 3 elementi con le info sommarie per i menu."""
        slots = []
        for i in range(3):
            data = self.load_game(i)
            if data:
                slots.append({
                    "empty": False,
                    "name": data.get("player_name", "Eroe"),
                    "level": data.get("level", 1),
                    "play_time": data.get("play_time", 0)
                })
            else:
                slots.append({"empty": True})
        return slots