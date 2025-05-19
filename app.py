
import streamlit as st
import PyPDF2
import pandas as pd
import json
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

st.set_page_config(page_title="AI Contract Risk & Flowdown BOT", layout="wide")

# Load risk rules
with open("risk_rules.json") as f:
    risk_rules = json.load(f)

# Load company flowdown rules
with open("flowdown_rules.json") as f:
    flowdown_rules = json.load(f)

def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() or "" for page in pdf_reader.pages])
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return ""

def evaluate_risks(text, rules):
    risk_items = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        for category in rules:
            for keyword in rules[category]["keywords"]:
                if re.search(keyword, sentence, re.IGNORECASE):
                    risk_items.append({
                        "Category": category,
                        "Keyword": keyword,
                        "Context": sentence.strip(),
                        "Risk Level": rules[category]["level"]
                    })
    return pd.DataFrame(risk_items)

def generate_flowdown(text, rules):
    flowdown_items = []
    for clause in rules:
        for keyword in rules[clause]["triggers"]:
            if re.search(keyword, text, re.IGNORECASE):
                flowdown_items.append({
                    "Clause": clause,
                    "Trigger": keyword,
                    "Flowdown Text": rules[clause]["flowdown_text"]
                })
                break
    return pd.DataFrame(flowdown_items)

st.title("🤖 AI Contract Risk & Flowdown BOT")
st.write("Upload a contract to receive a risk review and recommended flowdown clauses.")

uploaded_file = st.file_uploader("Upload contract (PDF or TXT)", type=["txt", "pdf"])

if uploaded_file:
    contract_text = extract_text(uploaded_file)
    st.subheader("📄 Extracted Contract Text")
    st.text_area("Contract Preview", contract_text[:3000], height=300)

    st.subheader("⚠️ Risk Analysis")
    result_df = evaluate_risks(contract_text, risk_rules)
    if not result_df.empty:
        st.dataframe(result_df)
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Risk Report CSV", csv, "risk_report.csv", "text/csv")
    else:
        st.success("No significant risks found based on current rules.")

    st.subheader("📜 Recommended Flowdown Clauses")
    flowdown_df = generate_flowdown(contract_text, flowdown_rules)
    if not flowdown_df.empty:
        st.dataframe(flowdown_df)
        csv = flowdown_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Flowdown Table CSV", csv, "flowdown_clauses.csv", "text/csv")
    else:
        st.success("No applicable flowdown clauses detected based on current rules.")
