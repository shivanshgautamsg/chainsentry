import requests
import os
import json

def fetch_npm_package(pkg_name):
    url = f"https://registry.npmjs.org/{pkg_name}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        latest = data.get("dist-tags", {}).get("latest")
        if latest and latest in data["versions"]:
            meta = data["versions"][latest]
            return {
                "name": pkg_name,
                "version": latest,
                "maintainers": data.get("maintainers", []),
                "dependencies": meta.get("dependencies", {}),
                "description": meta.get("description", "")
            }
    return None

if __name__ == "__main__":
    os.makedirs("data/raw/npm", exist_ok=True)
    packages = ["express", "lodash", "axios"]
    for pkg in packages:
        data = fetch_npm_package(pkg)
        if data:
            with open(f"data/raw/npm/{pkg}.json", "w") as f:
                json.dump(data, f, indent=2)
