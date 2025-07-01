import streamlit as st
import json
import plotly.express as px
import os
# Utility to load JSON files
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

st.set_page_config(page_title="ChainSentry Dashboard", layout="wide")
st.title("🛡️ ChainSentry Threat Intelligence Dashboard")
cve_data = load_json("models/cve_risks.json")


# Load data
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

trust_scores = load_json("models/maintainer_scores.json")
dep_risks = load_json("models/dependency_risks.json")

# Section 1: Maintainer Trust Score
st.header("👤 Maintainer Trust Scores")
if trust_scores:
    df = [{"maintainer": k, "trust": v} for k, v in trust_scores.items()]
    fig = px.bar(df, x="maintainer", y="trust", color="trust", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No maintainer score data found.")

# Section 2: Dependency Risk Warnings
st.header("⚠️ Package Risk Reports")
if dep_risks:
    for pkg in dep_risks:
        with st.expander(f"{pkg['package']} ({pkg['platform']})"):
            st.write(f"🔗 Dependencies: {pkg['num_dependencies']}")
            if pkg["issues"]:
                for issue in pkg["issues"]:
                    st.error(f"🧨 {issue}")
            else:
                st.success("✅ No suspicious issues found.")
else:
    st.info("No dependency risk data found.")
# Section 3: Known CVEs from NVD API
st.header("💣 Known Vulnerabilities (CVE Data)")

if cve_data:
    for item in cve_data:
        with st.expander(f"{item['package']} ({item['platform']}) – {len(item['cves'])} vulnerabilities"):
            for cve in item["cves"]:
                color = "red" if cve["score"] >= 7 else "orange" if cve["score"] >= 4 else "green"
                st.markdown(f"""
                <div style="padding:10px;margin-bottom:10px;border:1px solid #ddd;border-radius:10px;background-color:#f9f9f9">
                    <b style="color:{color.upper()};">CVE:</b> <code>{cve['id']}</code>  
                    <br><b>Description:</b> {cve['desc'][:200]}...
                    <br><b>MITRE Weakness:</b> {cve['mitre'] or 'N/A'}
                    <br><b>Severity:</b> <span style="color:{color};"><b>{cve['score']}</b></span>
                </div>
                """, unsafe_allow_html=True)
else:
    st.success("✅ No CVEs detected for known packages.")

