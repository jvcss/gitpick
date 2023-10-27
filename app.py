import streamlit as st
import json

st.set_page_config(layout="wide")

with open('diffs.json', encoding="utf-8") as diff_file:
    diffs = json.load(diff_file)

with st.sidebar:
    st.title("O par A..B do Diff")
    selected_branch = st.radio("---", [branches for branches in diffs.keys()])

st.title("Monstra a diferença de A para B", anchor="center")
for files in diffs[selected_branch]:
    with st.expander(files):
        [st.text(line) for line in diffs[selected_branch][files]]
        
