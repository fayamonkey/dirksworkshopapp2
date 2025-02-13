import streamlit as st
import json
import uuid

# File operations
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            # Add UUIDs to old tasks without IDs
            for task in tasks:
                if 'id' not in task:
                    task['id'] = str(uuid.uuid4())
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# App UI
st.title("✅ To-Do List Manager")

# Add new task
with st.form("new_task"):
    task_input = st.text_input("Add a new task:", placeholder="Enter task...")
    if st.form_submit_button("Add Task") and task_input:
        st.session_state.tasks.append({
            "id": str(uuid.uuid4()),
            "name": task_input.strip(),
            "completed": False
        })
        save_tasks(st.session_state.tasks)

# Display tasks
if not st.session_state.tasks:
    st.info("No tasks yet! Add one above ☝️")
else:
    for task in st.session_state.tasks:
        cols = st.columns([6, 1.5, 1.5])
        with cols[0]:
            if task['completed']:
                st.markdown(f"<del>{task['name']}</del>", unsafe_allow_html=True)
            else:
                st.write(task['name'])
        
        with cols[1]:
            if st.button("✅", key=f"complete_{task['id']}"):
                task['completed'] = not task['completed']
                save_tasks(st.session_state.tasks)
                st.experimental_rerun()
        
        with cols[2]:
            if st.button("🗑️", key=f"delete_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                save_tasks(st.session_state.tasks)
                st.experimental_rerun()
