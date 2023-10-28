import streamlit as st
import json
import hashlib

st.set_page_config(layout="wide")

if 'clicked_buttons' not in st.session_state:
    st.session_state['clicked_buttons'] = []


def sha256_hash(input_value): return hashlib.sha256(
    input_value.encode('utf-8')).hexdigest()[:8]


def clicked(col_cont):
    print(col_cont)
    if (col_cont in st.session_state['clicked_buttons']):
        return ":green[Add Patch]"
    else:
        return "Add Patch"


def isAdded(file_name):
    if (file_name in st.session_state['clicked_buttons']):
        return False
    else:
        return True


with open('diffs.json', encoding="utf-8") as diff_file:
    diffs = json.load(diff_file)

with st.sidebar:
    st.title("Par A..B usando Git Diff")
    selected_branch = st.radio("---", [branches for branches in diffs.keys()])

st.title(f"Difereças entre [{selected_branch.split('_')[0]}] vs [{selected_branch.split('_')[1]}]",
         anchor="center", help="o patch exibido é uma representação das diferenças entre a branch A e a branch B")

for files in diffs[selected_branch]:
    col_content, col_bring, col_remove = st.columns([0.8, 0.1, 0.1])
    file_hash = sha256_hash(str(diffs[selected_branch][files]))

    with col_content:
        with st.expander(files):
            for line in diffs[selected_branch][files]:
                if (line.startswith('-')):
                    st.markdown(
                        f":red[{line}]", help="linhas que comecam com --- mostram o que existe na branch (A) e nao na branch (B).")
                elif (line.startswith('+')):
                    st.markdown(
                        f":green[{line}]", help="linhas que comecam com +++ mostram o que existe na branch (B) e nao na branch (A).")
                elif (line.startswith('@')):
                    st.markdown(
                        f":blue[{line}]", help="linhas que comecam com @@ sao cabecalhos de contexto para mostrar onde as mudancas ocorrem no arquivo")
                else:
                    st.markdown(f"{line}")

    with col_bring:
        add_patch = st.button(label=clicked(file_hash), key=f"{file_hash}")
        
        if (add_patch):
            if f"{file_hash}" not in st.session_state['clicked_buttons']:
                patch = ""
                st.toast(f"Patch criado para {selected_branch}")
                st.session_state['clicked_buttons'].append(f"{file_hash}")
                for line in diffs[selected_branch][files]:
                    print(f"{patch}")
                    patch += f"{line}\n"
                with open(f"patches/{selected_branch}.patch", 'w', encoding="utf-8") as file:
                    file.write(patch)
                st.rerun()
            else:
                st.toast(f"Patch ja existe {selected_branch}")

    with col_remove:
        remove_patch = st.button(
            "Remove Patch", file_hash[::-1], disabled=isAdded(file_hash))

        if (remove_patch):
            st.toast(f"Patch removido para {selected_branch}")

            with open(f"patches/{selected_branch}.patch", 'r') as file:
                existing_patches = file.readlines()

            lines_to_remove = diffs[selected_branch][files]

            filtered_patches = [
                line for line in existing_patches if line not in lines_to_remove]

            with open(f"patches/{selected_branch}.patch", 'w') as file:
                file.writelines(filtered_patches)

            st.session_state['clicked_buttons'].remove(file_hash)
            st.rerun()
