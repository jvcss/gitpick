import streamlit as st
import json

st.set_page_config(layout="wide")

with open('diffs.json', encoding="utf-8") as diff_file:
    diffs = json.load(diff_file)

with st.sidebar:
    st.title("O par A..B do Diff")
    selected_branch = st.radio("---", [branches for branches in diffs.keys()])

st.title(f"Difereças entre [{selected_branch.split('_')[0]}] vs [{selected_branch.split('_')[1]}]", anchor="center", help="o patch exibido é uma representação das diferenças entre a branch A e a branch B")
for files in diffs[selected_branch]:
    col_content, col_bring = st.columns([0.9, 0.1])
    with col_content:
        with st.expander(files):
            for line in diffs[selected_branch][files]:
                if(line.startswith('-')):
                    st.markdown(f":red[{line}]", help="linhas que começam com --- mostram o que existe na branch (A) e não na branch (B).")
                elif(line.startswith('+')):
                    st.markdown(f":green[{line}]", help="linhas que começam com +++ mostram o que existe na branch (B) e não na branch (A).")
                elif(line.startswith('@')):
                    st.markdown(f":blue[{line}]", help="linhas que começam com @@ são cabeçalhos de contexto para mostrar onde as mudanças ocorrem no arquivo")
                else:
                    st.markdown(f"{line}")
    with col_bring:
        add_patch = st.button(label="Add Patch", key=f"{col_content}")
        patch = ""
        if (add_patch):
            for line in diffs[selected_branch][files]:
                patch += line
            with open(f"{selected_branch}.patch", 'a') as file:
                file.write(patch)
            st.toast(f"Patch criado para {selected_branch}")
