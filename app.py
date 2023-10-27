import streamlit as st
import json
import hashlib

st.set_page_config(layout="wide")

if 'clicked_buttons' not in st.session_state: st.session_state['clicked_buttons'] = []

sha256_hash = lambda input_value: hashlib.sha256(input_value.encode('utf-8')).hexdigest()[:8]

def clicked(col_cont):
    if(col_cont in st.session_state['clicked_buttons']):
        return ":green[Add Patch]"
    else:
        return "Add Patch"

with open('diffs.json', encoding="utf-8") as diff_file:
    diffs = json.load(diff_file)

with st.sidebar:
    st.title("Par A..B usando Git Diff")
    selected_branch = st.radio("---", [branches for branches in diffs.keys()])

st.title(f"Difereças entre [{selected_branch.split('_')[0]}] vs [{selected_branch.split('_')[1]}]", anchor="center", help="o patch exibido é uma representação das diferenças entre a branch A e a branch B")
for files in diffs[selected_branch]:
    col_content, col_bring = st.columns([0.9, 0.1])
    file_hash = sha256_hash(str(diffs[selected_branch][files]))
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
        add_patch = st.button(label=clicked(file_hash), key=f"{file_hash}")
        patch = ""
        if (add_patch):
            if f"{file_hash}" not in st.session_state['clicked_buttons']:
                st.toast(f"Patch criado para {selected_branch}")
                st.session_state['clicked_buttons'].append(f"{file_hash}")
                for line in diffs[selected_branch][files]:
                    patch += f"{line}\n"
                with open(f"patches/{selected_branch}.patch", 'a') as file:
                    file.write(patch)
                st.rerun()
            else:
                st.toast(f"Patch já existe {selected_branch}")
