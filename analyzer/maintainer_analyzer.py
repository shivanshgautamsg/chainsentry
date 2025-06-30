import os
import json
import pandas as pd
from sklearn.ensemble import IsolationForest

def extract_commits(repo_json_path):
    data = json.load(open(repo_json_path))
    commits = data["commits"]
    timestamps = [commit["commit"]["committer"]["date"] for commit in commits]
    authors = [commit["commit"]["committer"]["name"] for commit in commits]
    return list(zip(authors, timestamps))

def build_trust_scores():
    scores = {}
    github_dir = "data/raw/github"

    for file in os.listdir(github_dir):
        full_path = os.path.join(github_dir, file)
        commit_data = extract_commits(full_path)

        df = pd.DataFrame(commit_data, columns=["author", "timestamp"])
        if df.empty:
            continue

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["hour"] = df["timestamp"].dt.hour

        for author in df["author"].unique():
            author_df = df[df["author"] == author]
            activity_by_hour = author_df["hour"].value_counts().sort_index()

            # Pad hours
            for h in range(24):
                if h not in activity_by_hour:
                    activity_by_hour[h] = 0
            activity_by_hour = activity_by_hour.sort_index()

            # Outlier detection
            model = IsolationForest(contamination=0.15)
            values = activity_by_hour.values.reshape(-1, 1)
            model.fit(values)
            score = model.decision_function(values).mean()
            trust = max(0, min(1, 1 + score))  # Scale to [0, 1]
            scores[author] = round(trust, 3)

    os.makedirs("models", exist_ok=True)
    with open("models/maintainer_scores.json", "w") as f:
        json.dump(scores, f, indent=2)

if __name__ == "__main__":
    build_trust_scores()
