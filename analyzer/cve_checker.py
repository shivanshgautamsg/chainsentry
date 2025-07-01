import os
import json
import requests
from dotenv import load_dotenv
from time import sleep

load_dotenv()
API_KEY = os.getenv("NVD_API_KEY")

headers = {"apiKey": API_KEY}
base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def check_cves_for_package(pkg_name):
    params = {"keywordSearch": pkg_name, "resultsPerPage": "5"}
    try:
        r = requests.get(base_url, headers=headers, params=params)
        if r.status_code == 200:
            data = r.json()
            if data.get("vulnerabilities"):
                return [
                    {
                        "id": vuln["cve"]["id"],
                        "score": vuln["cve"].get("metrics", {}).get("cvssMetricV31", [{}])[0]
                            .get("cvssData", {}).get("baseScore", 0),
                        "desc": vuln["cve"]["descriptions"][0]["value"],
                        "mitre": vuln["cve"].get("weaknesses", [{}])[0]
                            .get("description", [{}])[0].get("value", "")
                    }
                    for vuln in data["vulnerabilities"]
                ]
    except:
        pass
    return []

def run_cve_scan():
    with open("models/dependency_risks.json") as f:
        packages = json.load(f)

    results = []
    for pkg in packages:
        name = pkg["package"]
        print(f"Checking CVEs for {name}...")
        cves = check_cves_for_package(name)
        sleep(1)  # avoid rate-limiting
        if cves:
            results.append({
                "package": name,
                "platform": pkg["platform"],
                "cves": cves
            })

    with open("models/cve_risks.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_cve_scan()
