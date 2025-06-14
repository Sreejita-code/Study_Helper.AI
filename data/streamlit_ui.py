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
    "📊 LeetCode Analyzer",
    "🧪 Weekly Test Generator"
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

# -------------- 📊 LeetCode Analyzer --------------
def show_leetcode_analyzer_ui():
    st.title("📊 LeetCode Practice Analyzer")

    username = st.text_input("Enter your LeetCode username", placeholder="e.g. rudrasish2003")

    if st.button("🔍 Analyze Submissions"):
        if username.strip():
            with st.spinner("Fetching your recent LeetCode submissions..."):
                results = leetcode_agent.fetch_recent_ac_problems(username, limit=15)

                if results:
                    st.success(f"✅ Found {len(results)} recent accepted submissions.")
                    for r in results:
                        st.markdown(
                            f"- 🧩 [{r['title']}](https://leetcode.com/problems/{r['titleSlug']}/)"
                        )
                else:
                    st.warning("⚠️ No recent accepted problems found. Try solving one and retry.")
        else:
            st.warning("⚠️ Please enter a valid username.")


# -------------- 🧪 Weekly Test Generator --------------
def show_test_generator_ui():
    st.title("🧪 Weekly Test Generator")

    username = st.text_input("LeetCode username", placeholder="e.g. rudrasish2003", key="test_username")
    days = st.slider("Look at past N days of submissions", 1, 30, 10)
    topics = st.text_input("Add topics (comma-separated)", placeholder="e.g. DP, Tree, Binary Search")
    difficulty = st.selectbox("Select difficulty", ["Any", "Easy", "Medium", "Hard"])

    if st.button("🚀 Generate Test"):
        if username.strip():
            with st.spinner("Generating personalized test..."):
                test = leetcode_agent.generate_custom_test(username, days, topics, difficulty)
                if test:
                    st.success(f"✅ Test generated with {len(test)} questions!")
                    st.markdown("### 📝 Your Practice Test:")
                    for q in test:
                        st.markdown(f"- {q['title']} – {q['difficulty']}")
                else:
                    st.warning("⚠️ No test could be generated with these filters.")
        else:
            st.warning("⚠️ Please enter your LeetCode username.")

# -------------- Router --------------
if page == "📋 Task Manager":
    show_task_manager_ui()
elif page == "📊 LeetCode Analyzer":
    show_leetcode_analyzer_ui()
elif page == "🧪 Weekly Test Generator":
    show_test_generator_ui()