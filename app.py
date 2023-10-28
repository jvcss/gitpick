import streamlit as st
import json
import hashlib
from enum import Enum

class FileConf(Enum):
    READ = 1
    WRITE = 2
    JSON = 3
    LINES = 4

st.set_page_config(layout="wide")

if 'clicked_buttons' not in st.session_state:
    st.session_state['clicked_buttons'] = []

def sha256_hash(input_value): return hashlib.sha256(
    input_value.encode('utf-8')).hexdigest()[:5]

def clicked(col_cont):
    print("file path hash: "+col_cont)
    if (col_cont in st.session_state['clicked_buttons']):
        return ":green[Add Patch]"
    else:
        return "Add Patch"

def isAdded(file_name):
    if (file_name in st.session_state['clicked_buttons']):
        return False
    else:
        return True

def read_write(rw:FileConf, file, formatConf='', content=''):
    if rw == FileConf.READ:
        if formatConf == FileConf.LINES:
            print('return lines')
            out = ""
            with open(file, 'r', encoding="utf-8") as fl:
                out = fl.readlines()
            return out

        elif formatConf == FileConf.JSON:
            out = ""
            print("return json")
            with open(file, encoding="utf-8") as f:
                out = json.load(f)
            return out
    elif rw == FileConf.WRITE:
        if formatConf == FileConf.LINES:
            print('write LINES')
            with open(file, 'w', encoding="utf-8") as file:
                file.write(content)
            
        else:
            with open(file, 'w', encoding="utf-8") as file:
                print('write content')
                file.write(content)
        
def filter_lines(actual_lines, lines_to_remove):
    lines_to_remove_set = set(lines_to_remove)
    filtered_lines = [line.rstrip('\n') for line in actual_lines if line.rstrip('\n') not in lines_to_remove_set]
    filtered_string = '\n'.join(filtered_lines)
    return filtered_string

diffs = read_write(FileConf.READ, 'diffs.json', FileConf.JSON)

with st.sidebar:
    st.title("Par A..B usando Git Diff")
    selected_branch = st.radio("---", [branches for branches in diffs.keys()])

st.title(f"Difereças entre [{selected_branch.split('_')[0]}] vs [{selected_branch.split('_')[1]}]",
         anchor="center", help="The displayed patch is a representation of the differences between branch A and branch B")

for files in diffs[selected_branch]:
    col_content, col_bring, col_remove = st.columns([0.8, 0.1, 0.1])
    file_hash = sha256_hash(str(diffs[selected_branch][files]))

    with col_content:
        with st.expander(files):
            for line in diffs[selected_branch][files]:
                if (line.startswith('-')):
                    st.markdown(
                        f":red[{line}]", help="Lines starting with --- show what exists in branch (A) and not in branch (B)")
                elif (line.startswith('+')):
                    st.markdown(
                        f":green[{line}]", help="Lines starting with +++ show what exists in branch (B) and not in branch (A)")
                elif (line.startswith('@')):
                    st.markdown(
                        f":blue[{line}]", help="Lines starting with @@ are context headers to show where the changes occur in the file")
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
                    patch += f"{line}\n"
                read_write(FileConf.WRITE, f"patches/{selected_branch}.patch", content=patch)
                st.rerun()
            else:
                st.toast(f"Patch ja existe {selected_branch}")

    with col_remove:
        remove_patch = st.button(
            "Remove Patch", file_hash[::-1], disabled=isAdded(file_hash))

        if (remove_patch):
            st.toast(f"Patch removido para {selected_branch}")

            existing_patches = read_write(
                FileConf.READ, f"patches/{selected_branch}.patch", FileConf.LINES)

            lines_to_remove = diffs[selected_branch][files]

            filtered_patches = filter_lines(existing_patches, lines_to_remove)

            read_write(FileConf.WRITE, f"patches/{selected_branch}.patch", FileConf.LINES, content=filtered_patches)

            st.session_state['clicked_buttons'].remove(file_hash)
            st.rerun()
