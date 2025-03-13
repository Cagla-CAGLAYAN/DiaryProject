import streamlit as st
import firebase_admin
from firebase_admin import db, credentials
from datetime import date
from TrainDiary import TrainDiary

current_date = date.today().isoformat()

if 'firebase_initialized' not in st.session_state:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://diaryproject-e7776-default-rtdb.europe-west1.firebasedatabase.app/"})
    st.session_state.firebase_initialized = True

notes_ref = db.reference("/notes/content")
train_diary = TrainDiary()

def st_vertical_space(n):
    for i in range(n):
        st.write(" ")

def get_comments():
    comments_ref = notes_ref
    comments = []
    try:
        data = comments_ref.get()
        if data and isinstance(data, dict) and "Notes" in data:
            comments = data["Notes"]
        elif data is None:
            comments = []
    except Exception as e:
        print(f"Error fetching comments: {e}")
    return comments

def add_note(note_info):
    try:
        data = notes_ref.get() or {}
        notes = data.get("Notes", [])
        notes.append({
            "content": note_info,
            "date": current_date,
            "checked": False
        })
        notes_ref.update({"Notes": notes})
    except Exception as e:
        st.error(f"Error adding note: {e}")


if "GC" not in st.session_state:
    st.session_state["GC"] = get_comments
if "AN" not in st.session_state:
    st.session_state["AN"] = add_note
if "selected_notes" not in st.session_state:
    st.session_state["selected_notes"] = {}  
if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = {}  

GC = st.session_state["GC"]
AN = st.session_state["AN"]

def analyze_and_display(content: str, idx: int):
    with st.container(border=True):
        print(f"{content}")
        try:
            result = train_diary.diary_analyze_sync(content)
            print(f"{result}")
            st.session_state["analysis_results"][idx] = result
        except Exception as e:
            print(f"Error analyzing content at index {idx}: {e}")
 
            st.session_state["analysis_results"][idx] = f"Error analyzing diary: {e}"
            
@st.dialog("Diary Analysis")
def analysis(item):
    st.write(f"{item}")


def main():
    with st.popover("Add Diary"):
        st.markdown("### Add Your Diary Entry")
        note = st.text_input("Note")
        if st.button("Add Note"):
            if note:
                AN(note)
                st.success("Note added successfully!")
                st.rerun()

    with st.container(border=True):
        st_vertical_space(3)
        comments = GC()
        print(f"Fetched comments: {comments}")

        if comments:
            rerun_required = False  

            for i, comment in enumerate(comments):
                col_note, col_check = st.columns([4, 1])

                with col_note:
                    content = comment.get("content", comment) if isinstance(comment, dict) else comment
                    st.write(f"{content}")

                with col_check:
                    selected = st.checkbox("Select", key=f"checkbox_{i}", value=(i in st.session_state["selected_notes"]))

                    if selected and i not in st.session_state["selected_notes"]:
                        print(f"Adding index {i} to selected_notes")
                        st.session_state["selected_notes"][i] = content
                        rerun_required = True  

                    elif not selected and i in st.session_state["selected_notes"]:
                        print(f"Removing index {i} from selected_notes")
                        del st.session_state["selected_notes"][i]
                        if i in st.session_state["analysis_results"]:
                            del st.session_state["analysis_results"][i]
                        rerun_required = True

            if rerun_required:
                st.rerun()
            

            for idx in st.session_state["selected_notes"]:
                if "analysis" not in st.session_state:
                    if idx not in st.session_state["analysis_results"]:
                            analyze_and_display(st.session_state["selected_notes"][idx], idx)
                            analysis(f"{st.session_state['analysis_results'].get(idx, 'Analysis pending...')}")

        else:
            st.write("No diary entries yet. Add one above!")


if __name__ == '__main__':
    main()