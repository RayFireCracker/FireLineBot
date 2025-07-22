import json
import os

MEMORY_PATH = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {"interactions": [], "evolution": {}}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def update_memory(memory, user_id, message):
    memory.setdefault("interactions", []).append({"user_id": user_id, "message": message})
    if user_id not in memory["evolution"]:
        memory["evolution"][user_id] = {"traits": {"engaged": True}, "history": []}
    memory["evolution"][user_id]["history"].append(message)
    return memory
