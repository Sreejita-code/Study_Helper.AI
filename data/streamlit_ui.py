import streamlit as st
from datetime import datetime
import sys
import os

# ✅ Add root folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import task_manager  # Now import works

# ✅ Streamlit Page Config
st.set_page_config(page_title="📋 Study Agent – Task Manager", layout="centered")
st.title("📋 Study Agent – Task Manager")

# ---------------------- Task Input Form ----------------------
with st.form("add_task_form", clear_on_submit=True):
    title = st.text_input("Task Title", "")
    due_time = st.text_input("Due Time (YYYY-MM-DD HH:MM) [optional]", "")
    submitted = st.form_submit_button("➕ Add Task")

    if submitted and title.strip():
        task_manager.add_task(title, due_time.strip() if due_time else None)
        st.success("✅ Task added!")

# ---------------------- List Tasks ----------------------
st.subheader("📝 Your Tasks")
tasks = task_manager.load_tasks()

if not tasks:
    st.info("No tasks yet. Add one above!")
else:
    for task in tasks:
        col1, col2, col3 = st.columns([6, 2, 2])
        status = "✅" if task["done"] else "❌"
        with col1:
            st.write(f"**[{task['id']}] {status} {task['title']}**  \n(Due: {task['due_time'] or 'None'})")
        with col2:
            if not task["done"] and st.button("✔️ Done", key=f"done_{task['id']}"):
                task_manager.mark_done(task["id"])
                st.experimental_rerun()
        with col3:
            if st.button("🗑️ Delete", key=f"del_{task['id']}"):
                task_manager.delete_task(task["id"])
                st.experimental_rerun()
