import json
import os

def normalize_pypi(path):
    data = json.load(open(path))
    return {
        "name": data["name"],
        "version": data["version"],
        "platform": "pypi",
        "dependencies": data["requires"],
        "maintainers": [data["author"]],
        "description": data["summary"]
    }

def normalize_npm(path):
    data = json.load(open(path))
    return {
        "name": data["name"],
        "version": data["version"],
        "platform": "npm",
        "dependencies": list(data["dependencies"].keys()),
        "maintainers": [m["name"] for m in data["maintainers"]],
        "description": data["description"]
    }

if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)

    for path in os.listdir("data/raw/pypi"):
        full = f"data/raw/pypi/{path}"
        norm = normalize_pypi(full)
        json.dump(norm, open(f"data/processed/{norm['name']}_pypi.json", "w"), indent=2)

    for path in os.listdir("data/raw/npm"):
        full = f"data/raw/npm/{path}"
        norm = normalize_npm(full)
        json.dump(norm, open(f"data/processed/{norm['name']}_npm.json", "w"), indent=2)
