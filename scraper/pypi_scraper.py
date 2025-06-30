import requests
import json
import os

def fetch_pypi_package(pkg_name):
    url = f"https://pypi.org/pypi/{pkg_name}/json"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return {
            "name": pkg_name,
            "version": data["info"]["version"],
            "author": data["info"]["author"],
            "requires": data["info"]["requires_dist"],
            "summary": data["info"]["summary"],
            "url": data["info"]["project_url"]
        }
    return None

if __name__ == "__main__":
    os.makedirs("data/raw/pypi", exist_ok=True)
    packages = ["requests", "flask", "pandas"]
    for pkg in packages:
        pkg_data = fetch_pypi_package(pkg)
        if pkg_data:
            with open(f"data/raw/pypi/{pkg}.json", "w") as f:
                json.dump(pkg_data, f, indent=2)
