import os
import json
import re
import math
import string

def entropy(s):
    """Measure the randomness of a string (useful for detecting obfuscated code)"""
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(s)]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob])

def is_typosquat(name, legit_list):
    for legit in legit_list:
        if len(name) >= 4 and abs(len(name) - len(legit)) <= 2:
            if sum(a != b for a, b in zip(name, legit)) <= 2:
                return True
    return False

def analyze_dependency_file(path, platform, legit_libs):
    data = json.load(open(path))
    issues = []

    deps = data.get("dependencies", []) or []
    if platform == "npm":
        deps = deps  # already a list
    elif platform == "pypi" and isinstance(deps, list):
        deps = [x.split(" ")[0] for x in deps if x]  # remove version spec

    for dep in deps:
        if is_typosquat(dep, legit_libs):
            issues.append(f"Possible typosquat: {dep}")

        # Entropy flag for suspicious strings
        if entropy(dep) > 4.5:
            issues.append(f"High entropy dependency name: {dep}")

    return {
        "package": data["name"],
        "platform": platform,
        "issues": issues,
        "num_dependencies": len(deps)
    }

def run_dependency_analysis():
    legit_libs_npm = ["express", "lodash", "axios", "react", "vue"]
    legit_libs_pypi = ["requests", "flask", "pandas", "numpy", "scipy"]

    output = []

    for fname in os.listdir("data/processed"):
        if fname.endswith("_npm.json"):
            result = analyze_dependency_file(f"data/processed/{fname}", "npm", legit_libs_npm)
            output.append(result)
        elif fname.endswith("_pypi.json"):
            result = analyze_dependency_file(f"data/processed/{fname}", "pypi", legit_libs_pypi)
            output.append(result)

    os.makedirs("models", exist_ok=True)
    with open("models/dependency_risks.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    run_dependency_analysis()
