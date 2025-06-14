import streamlit as st
from datetime import datetime
import sys
import os

# ✅ Fix file path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import task_manager, leetcode_agent

# ✅ Page config
st.set_page_config(page_title="📚 Study Agent", layout="centered")

# ---------------- Sidebar ----------------
st.sidebar.title("🧠 Study Agent")
page = st.sidebar.radio("Choose a section", [
    "📋 Task Manager",
    "📊 Analyze & Generate"
])

# -------------- 📋 Task Manager --------------
def show_task_manager_ui():
    st.title("📋 Task Manager")

    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task Title", "")
        due_time = st.text_input("Due Time (YYYY-MM-DD HH:MM) [optional]", "")
        submitted = st.form_submit_button("➕ Add Task")

        if submitted and title.strip():
            task_manager.add_task(title, due_time.strip() if due_time else None)
            st.success("✅ Task added!")

    st.subheader("📝 Your Tasks")
    tasks = task_manager.load_tasks()

    if not tasks:
        st.info("No tasks yet. Add one above!")
    else:
        for task in tasks:
            col1, col2, col3 = st.columns([6, 2, 2])
            status = "✅" if task["done"] else "❌"
            with col1:
                st.write(f"[{task['id']}] {status} {task['title']}  \n(Due: {task['due_time'] or 'None'})")
            with col2:
                if not task["done"] and st.button("✔️ Done", key=f"done_{task['id']}"):
                    task_manager.mark_done(task["id"])
                    st.experimental_rerun()
            with col3:
                if st.button("🗑️ Delete", key=f"del_{task['id']}"):
                    task_manager.delete_task(task["id"])
                    st.experimental_rerun()

# -------------- 📊 Analyzer + 🧪 Generator --------------
def show_analyze_and_test_ui():
    st.title("📊 Analyze Submissions & 🧪 Generate Test")

    username = st.text_input("Enter your LeetCode username", placeholder="e.g. rudrasish2003")

    if username.strip():
        col1, col2 = st.columns(2)

        with col1:
            analyze_clicked = st.button("🔍 Analyze Submissions")
        with col2:
            test_clicked = st.button("🚀 Generate Weekly Test")

        if analyze_clicked:
            with st.spinner("Fetching your recent LeetCode submissions..."):
                results = leetcode_agent.fetch_recent_ac_problems(username, limit=15)

                if results:
                    st.success(f"✅ Found {len(results)} recent accepted submissions.")
                    st.markdown("### 🔍 Recent Solved Problems:")
                    for r in results:
                        st.markdown(f"- 🧩 [{r['title']}](https://leetcode.com/problems/{r['titleSlug']}/)")
                else:
                    st.warning("⚠️ No recent accepted problems found.")

        if test_clicked:
            with st.spinner("Generating personalized test..."):
                test = leetcode_agent.generate_custom_test(username=username)
                if test:
                    st.success(f"✅ Test generated with {len(test)} questions!")
                    st.markdown("### 📝 Your Practice Test:")
                    for q in test:
                        st.markdown(f"""
                        #### 🧩 [{q['title']}]({q['problemLink']})
                        - **Difficulty**: `{q['difficulty']}`
                        - **Topics**: `{', '.join(q['tags'])}`
                        - 🔗 [Community Solutions]({q['solutionLink']})
                        """)
                else:
                    st.warning("⚠️ No test could be generated at this time.")
    else:
        st.info("ℹ️ Please enter your LeetCode username to begin.")

# -------------- Router --------------
if page == "📋 Task Manager":
    show_task_manager_ui()
elif page == "📊 Analyze & Generate":
    show_analyze_and_test_ui()
